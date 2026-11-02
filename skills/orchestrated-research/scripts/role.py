#!/usr/bin/env python3
"""Keep dedicated research agents alive across turns, sessions and vendors.

A role is a folder of durable files plus, when the backend allows it, a resumable thread:

    roles/<role>/CHARTER.md    what the role owns and how it works
    roles/<role>/MEMORY.md     durable lessons, kept by the role itself
    roles/<role>/HANDOFF.md    current state and exact next step, kept by the role itself
    roles/roster.json          role -> backend, thread id, model, status

Commands:

    role.py list
    role.py send ROLE --message-file FILE [--timeout SECONDS] [--dry-run]
    role.py reply ROLE
    role.py set ROLE [--backend B] [--thread ID] [--model M] [--status S] [--env K=V ...] [--args ...]
    role.py add ROLE --backend B
    role.py rehydrate ROLE [--backend B] [--model M] [--reason TEXT]

Backends: codex, claude, dsh, codex-live, manual.

`send` refuses a message that is not saved in a file or does not start with "From <sender>:".
It runs one turn at a time per role, and it never resends after a failed or ambiguous delivery.
Standard library only. Python 3.9 or later.
"""
import argparse
import contextlib
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import fcntl
except ImportError:  # Windows. Then run one roster change at a time.
    fcntl = None

BACKENDS = ("codex", "claude", "dsh", "codex-live", "manual")
SENDER_RE = re.compile(r"^From [^:\n]{1,60}:")
ROLE_NAME_RE = re.compile(r"[a-z0-9][a-z0-9-]{0,47}")
# `claude -p` cannot ask for approval. A writer needs its build and check commands allowed in advance.
# Running project code is the project's choice: add it with `set ROLE --args --allowedTools ...`.
CLAUDE_TOOLS = ["Bash(latexmk *)", "Bash(python3 tools/records.py *)", "Bash(shasum *)", "Bash(sha256sum *)",
                "Bash(pdfinfo *)", "Bash(pdffonts *)", "Bash(pdftoppm *)", "Bash(pdftotext *)"]

FIRST_TURN = """You are the dedicated {role} of this research project.
Your identity lives in files, not in this conversation.
Before acting, read these in order: roles/{role}/CHARTER.md, roles/{role}/MEMORY.md, roles/{role}/HANDOFF.md, AGENTS.md, PROJECT_STATE.md.
Before you end each turn, update roles/{role}/HANDOFF.md, and put durable lessons in roles/{role}/MEMORY.md.
The message below comes from the orchestrator. It is not an author prompt unless it says it relays one.

{message}
"""

LATER_TURN = """If your context was compacted, re-read roles/{role}/CHARTER.md, MEMORY.md and HANDOFF.md first.
Update roles/{role}/HANDOFF.md before you end this turn.

{message}
"""

# `claude --agent NAME` loads .claude/agents/NAME.md. A role added later gets this plain definition.
CLAUDE_AGENT = """---
name: {role}
description: Dedicated {role} of this research project. Keeps its own memory and handoff across sessions.
memory: project
---
You are the dedicated {role} of this project.
Your identity lives in files, not in this conversation.
Before acting, read `roles/{role}/CHARTER.md` and `roles/{role}/HANDOFF.md`, then `AGENTS.md` and `PROJECT_STATE.md`.
Your memory folder is `roles/{role}/`. Keep `MEMORY.md` there current, as a short list of durable lessons.
Before you end each turn, update `roles/{role}/HANDOFF.md`.
A message that starts "From <sender>:" is not an author prompt unless it says it relays one.
"""


def die(text, code=2):
    print(f"role.py: {text}", file=sys.stderr)
    sys.exit(code)


def now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def find_project(start=None):
    here = Path(start or os.getcwd()).resolve()
    for folder in [here, *here.parents]:
        if (folder / "roles" / "roster.json").is_file():
            return folder
    die("no roles/roster.json here or in a parent folder. Run init_project.py first, or pass --project.")


def load_roster(project):
    with open(project / "roles" / "roster.json", encoding="utf-8") as handle:
        return json.load(handle)


def save_roster(project, roster):
    path = project / "roles" / "roster.json"
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".roster-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(roster, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)


@contextlib.contextmanager
def roster_lock(project):
    """Hold roles/.roster.lock across one read-modify-write, so parallel turns keep each other's changes."""
    with open(project / "roles" / ".roster.lock", "a") as handle:
        if fcntl:
            fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def get_role(roster, name):
    role = roster["roles"].get(name)
    if role is None:
        die(f"unknown role {name!r}. Known roles: {', '.join(sorted(roster['roles']))}")
    return role


def new_role(backend):
    return {"backend": backend, "thread": None, "model": None, "args": [], "env": {}, "status": "active", "history": [], "last_turn": None}


class Lock:
    """One turn at a time per role. A lock left by a dead process is cleared."""

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        if self.path.exists():
            try:
                pid = int(self.path.read_text().split()[0])
                os.kill(pid, 0)
            except (ValueError, IndexError, ProcessLookupError):
                self.path.unlink()
            except PermissionError:
                pass
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            die(f"another turn is running for this role ({self.path}). Wait for it to end.", 3)
        with os.fdopen(fd, "w") as handle:
            handle.write(f"{os.getpid()} {now()}\n")
        return self

    def __exit__(self, *_exc):
        self.path.unlink(missing_ok=True)


def role_env(role):
    env = dict(os.environ)
    for key, value in (role.get("env") or {}).items():
        env[key] = os.path.expanduser(value)
    return env


def ensure_claude_agent(project, name):
    """Write .claude/agents/<name>.md if it is missing, and point its memory at the role folder."""
    path = project / ".claude" / "agents" / f"{name}.md"
    try:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(CLAUDE_AGENT.format(role=name), encoding="utf-8")
            print(f"wrote {path.relative_to(project)}. Add the skills this role uses to its frontmatter.")
        link = project / ".claude" / "agent-memory" / name
        if not (link.exists() or link.is_symlink()):
            link.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(Path("..") / ".." / "roles" / name, link, target_is_directory=True)
    except OSError as exc:
        print(f"warning: could not set up {path}: {exc}. Write it yourself before the role's first turn on claude.", file=sys.stderr)


def next_step(name, role):
    """Say in one line what the next send does for this role."""
    backend = role["backend"]
    if backend == "codex-live":
        if role.get("thread"):
            return f"{name}: the next send queues to live thread {role['thread']}."
        return (f"{name}: start a live Codex session for this role, and make its first message tell it to read "
                f"roles/{name}/CHARTER.md, MEMORY.md and HANDOFF.md. Then bind it with `set {name} --thread UUID`.")
    if backend == "manual":
        return f"{name}: the next send hands the message to you. Give a new session roles/{name}/ to read first."
    if role.get("thread"):
        return f"{name}: the next send resumes {backend} thread {role['thread']}."
    return f"{name}: the next send starts a new {backend} thread from roles/{name}/."


def build_command(name, role, project):
    """Return (argv, env, cwd) for one turn. The prompt always goes through stdin."""
    backend, thread, model = role["backend"], role.get("thread"), role.get("model")
    env = role_env(role)
    extra = list(role.get("args") or [])
    if backend == "codex":
        if thread:
            argv = ["codex", "exec", "resume", thread, "--json", "--skip-git-repo-check", "-c", 'sandbox_mode="workspace-write"']
        else:
            argv = ["codex", "exec", "--json", "--skip-git-repo-check", "-s", "workspace-write", "-C", str(project)]
        if model:
            argv += ["-m", model]
        return argv + extra + ["-"], env, project
    if backend == "claude":
        argv = ["claude", "-p", "--agent", name, "--output-format", "json"]
        if not any(arg.startswith("--permission-mode") for arg in extra):
            argv += ["--permission-mode", "acceptEdits"]
        if thread:
            argv += ["--resume", thread]
        if model:
            argv += ["--model", model]
        if not any(arg in ("--allowedTools", "--allowed-tools") for arg in extra):
            argv += ["--allowedTools", *CLAUDE_TOOLS]
        return argv + extra, env, project
    if backend == "dsh":
        env.setdefault("DSH_PERMISSION_MODE", "workspace-write")
        if env["DSH_PERMISSION_MODE"] == "danger-full-access":
            die("refusing dsh danger-full-access for delegated work.")
        if model:
            print(f"note: dsh takes its model from ~/.dsh, so {model} is not applied.", file=sys.stderr)
        argv = ["dsh", "headless", "--json"]
        if thread:
            argv += ["--session-id", thread]
        return argv + extra + ["-"], env, project
    die(f"backend {backend!r} has no command.")


def parse_codex(stdout):
    thread, text, failed = None, None, None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        kind = event.get("type")
        if kind == "thread.started":
            thread = event.get("thread_id") or thread
        elif kind == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                text = item.get("text", text)
        elif kind in ("turn.failed", "error"):
            failed = json.dumps(event)[:500]
    return thread, text, failed


def parse_claude(stdout):
    try:
        data = json.loads(stdout)
    except ValueError:
        for line in reversed(stdout.splitlines()):
            try:
                data = json.loads(line)
                break
            except ValueError:
                continue
        else:
            return None, None, "no JSON result in claude output"
    failed = json.dumps(data)[:500] if data.get("is_error") else None
    return data.get("session_id"), data.get("result"), failed


def parse_dsh(stdout):
    """Run events of dsh 0.2.0-rc.2: a session event, then status and text events, then a final event."""
    thread, final, failed = None, None, None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        kind = event.get("type")
        if kind == "session":
            thread = event.get("sessionId") or thread
        elif kind == "final":
            final = event.get("text", final)
        elif kind == "error":
            failed = json.dumps(event)[:500]
        elif kind == "status" and event.get("phase") == "turn_end":
            reason = (event.get("reason") or {}).get("kind")
            if reason and reason != "completed":
                failed = json.dumps(event)[:500]
    return thread, final, failed


PARSERS = {"codex": parse_codex, "claude": parse_claude, "dsh": parse_dsh}


def compose_prompt(name, role, message):
    template = LATER_TURN if role.get("thread") else FIRST_TURN
    return template.format(role=name, message=message)


def record_turn(project, name, entry):
    with open(project / "roles" / name / "turns.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def cmd_send(args):
    project = Path(args.project).resolve() if args.project else find_project()
    roster = load_roster(project)
    role = get_role(roster, args.role)
    if role.get("status", "active") != "active":
        die(f"{args.role} is {role['status']}. Use `set --status active` or `rehydrate` first.")
    path = Path(args.message_file)
    if not path.is_file():
        die(f"message file not found: {path}. A message goes on record before it is sent.")
    message = path.read_text(encoding="utf-8").strip()
    if not SENDER_RE.match(message):
        die('a message must start with "From <sender>:", so the receiver does not log it as an author prompt.')
    folder = project / "roles" / args.role
    (folder / "runs").mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    log = folder / "runs" / f"{stamp}.log"
    backend = role["backend"]
    entry = {"time": now(), "message_file": str(path), "backend": backend, "thread_before": role.get("thread"), "log": str(log.relative_to(project))}

    if backend == "manual":
        print(f"manual backend: deliver {path} to the {args.role} session yourself, then record what it delivers.")
        if args.dry_run:
            return 0
        record_turn(project, args.role, {**entry, "status": "handed to human"})
        return 0
    if backend == "codex-live":
        thread = role.get("thread")
        if not thread:
            die("codex-live needs a thread. Use `set ROLE --thread UUID`. Use the UUID, because names can repeat.")
        argv = ["codex", "queue", "--thread", thread, "--message", message]
        if args.dry_run:
            print(" ".join(argv[:5]) + " --message <file text>")
            return 0
        if not shutil.which("codex", path=role_env(role).get("PATH")):
            die("codex is not on PATH.", 4)
        done = subprocess.run(argv, env=role_env(role), cwd=project, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        log.write_text(done.stdout + done.stderr, encoding="utf-8")
        status = "queued" if done.returncode == 0 else f"failed {done.returncode}"
        record_turn(project, args.role, {**entry, "status": status})
        print(f"{args.role}: {status} on thread {thread}. An idle thread starts a turn at once. Read replies with read_thread.py.")
        return 0 if done.returncode == 0 else 1

    argv, env, cwd = build_command(args.role, role, project)
    prompt = compose_prompt(args.role, role, message)
    if args.dry_run:
        print(" ".join(argv))
        print("--- prompt ---")
        print(prompt)
        return 0
    if not shutil.which(argv[0], path=env.get("PATH")):
        die(f"{argv[0]} is not on PATH.", 4)

    with Lock(folder / ".lock"):
        print(f"{args.role}: turn started on {backend}, thread {role.get('thread') or '(new)'}. Log: {log}", flush=True)
        try:
            done = subprocess.run(argv, input=prompt, env=env, cwd=cwd, capture_output=True, text=True, timeout=args.timeout)
            out, err, code = done.stdout, done.stderr, done.returncode
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            err = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            code = "timeout"
        log.write_text(out + "\n--- stderr ---\n" + err, encoding="utf-8")
        thread, reply, failed = PARSERS[backend](out)

        # Re-read the roster under its lock, because another role may have changed it during this long turn.
        with roster_lock(project):
            roster = load_roster(project)
            role = get_role(roster, args.role)
            if thread and thread != role.get("thread"):
                if role.get("thread"):
                    role.setdefault("history", []).append({"thread": role["thread"], "ended": now(), "reason": "backend returned a new thread"})
                role["thread"] = thread
            ok = code == 0 and not failed and bool(reply)
            role["last_turn"] = {"time": now(), "status": "ok" if ok else "failed", "message_file": str(path), "log": entry["log"]}
            save_roster(project, roster)
        if reply:
            (folder / "last-reply.md").write_text(reply + "\n", encoding="utf-8")
        record_turn(project, args.role, {**entry, "thread_after": role.get("thread"), "exit": code, "status": "ok" if ok else "failed", "failed": failed})

    if not ok:
        print(f"{args.role}: turn FAILED (exit {code}). Read {log}. Not resent, because delivery may be ambiguous.", file=sys.stderr)
        if failed:
            print(failed, file=sys.stderr)
        return 1
    print(f"{args.role}: turn ended on thread {role.get('thread')}. Reply: {folder / 'last-reply.md'}")
    return 0


def cmd_list(args):
    project = Path(args.project).resolve() if args.project else find_project()
    roster = load_roster(project)
    print(f"{'ROLE':<22}{'BACKEND':<12}{'STATUS':<10}{'THREAD':<46}LAST TURN")
    for name in sorted(roster["roles"]):
        role = roster["roles"][name]
        last = role.get("last_turn") or {}
        print(f"{name:<22}{role['backend']:<12}{role.get('status', ''):<10}{str(role.get('thread') or '-'):<46}{last.get('time', '-')} {last.get('status', '')}")
    return 0


def cmd_reply(args):
    project = Path(args.project).resolve() if args.project else find_project()
    path = project / "roles" / args.role / "last-reply.md"
    if not path.is_file():
        die(f"no reply recorded for {args.role}.", 1)
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def apply_settings(role, args):
    backend = getattr(args, "backend", None)
    if backend and backend != role["backend"]:
        # A thread, a model name and flags belong to one vendor. Carried over, they break the first turn on the next.
        if role.get("thread"):
            role.setdefault("history", []).append({"thread": role["thread"], "ended": now(), "reason": f"moved from {role['backend']} to {backend}"})
            print(f"moving from {role['backend']} to {backend}: thread {role['thread']} moved to the roster's history.")
            role["thread"] = None
        cleared = [key for key in ("model", "args") if role.get(key)]
        if cleared:
            print(f"moving from {role['backend']} to {backend}: cleared {' and '.join(cleared)}. Set them again if needed.")
        role["backend"], role["model"], role["args"] = backend, None, []
    model = getattr(args, "model", None)
    if model is not None:
        role["model"] = model or None
    for pair in getattr(args, "env", None) or []:
        key, _, value = pair.partition("=")
        role.setdefault("env", {})[key] = value


def cmd_set(args):
    project = Path(args.project).resolve() if args.project else find_project()
    with roster_lock(project):
        roster = load_roster(project)
        role = get_role(roster, args.role)
        apply_settings(role, args)
        if args.thread:
            if role.get("thread") and role["thread"] != args.thread:
                role.setdefault("history", []).append({"thread": role["thread"], "ended": now(), "reason": "replaced with set"})
            role["thread"] = args.thread
        if args.status:
            role["status"] = args.status
        if args.args is not None:
            role["args"] = args.args
        save_roster(project, roster)
    if role["backend"] == "claude":
        ensure_claude_agent(project, args.role)
    print(json.dumps({args.role: role}, indent=2))
    print(next_step(args.role, role))
    return 0


def cmd_add(args):
    project = Path(args.project).resolve() if args.project else find_project()
    if not ROLE_NAME_RE.fullmatch(args.role):
        die("a role name uses lowercase letters, digits and hyphens, such as figure-writer.")
    with roster_lock(project):
        roster = load_roster(project)
        if args.role in roster["roles"]:
            die(f"{args.role} already exists.")
        roster["roles"][args.role] = new_role(args.backend)
        folder = project / "roles" / args.role
        folder.mkdir(parents=True, exist_ok=True)
        stubs = {
            "CHARTER.md": f"# Charter: {args.role}\n\nJob:\n\nOwns these files, and only this role edits them:\n\nDoes not touch:\n\nDelivers:\n",
            "MEMORY.md": f"# Memory: {args.role}\n\nDurable lessons, one line each, with their origin. Replace a superseded lesson instead of appending.\n",
            "HANDOFF.md": f"# Handoff: {args.role}\n\nCurrent state, open items and the exact next step. Newest entry last.\n",
        }
        for filename, text in stubs.items():
            if not (folder / filename).exists():
                (folder / filename).write_text(text, encoding="utf-8")
        save_roster(project, roster)
    if args.backend == "claude":
        ensure_claude_agent(project, args.role)
    print(f"added {args.role} on {args.backend}. Fill in {folder / 'CHARTER.md'} before its first turn.")
    print(next_step(args.role, roster["roles"][args.role]))
    return 0


def cmd_rehydrate(args):
    """Drop the thread, keep the files. The next send starts fresh from the durable record."""
    project = Path(args.project).resolve() if args.project else find_project()
    with roster_lock(project):
        roster = load_roster(project)
        role = get_role(roster, args.role)
        if role.get("thread"):
            role.setdefault("history", []).append({"thread": role["thread"], "ended": now(), "reason": args.reason or "rehydrate"})
        role["thread"] = None
        role["status"] = "active"
        apply_settings(role, args)
        save_roster(project, roster)
    if role["backend"] == "claude":
        ensure_claude_agent(project, args.role)
    print(f"{next_step(args.role, role)} Superseded threads stay in the roster's history.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", help="project folder, if not found from the current folder")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list").set_defaults(func=cmd_list)

    send = sub.add_parser("send")
    send.add_argument("role")
    send.add_argument("--message-file", required=True)
    send.add_argument("--timeout", type=int, default=None)
    send.add_argument("--dry-run", action="store_true")
    send.set_defaults(func=cmd_send)

    reply = sub.add_parser("reply")
    reply.add_argument("role")
    reply.set_defaults(func=cmd_reply)

    setter = sub.add_parser("set")
    setter.add_argument("role")
    setter.add_argument("--backend", choices=BACKENDS)
    setter.add_argument("--thread")
    setter.add_argument("--model")
    setter.add_argument("--status", choices=("active", "paused", "retired"))
    setter.add_argument("--env", action="append", metavar="KEY=VALUE")
    setter.add_argument("--args", nargs=argparse.REMAINDER, help="extra backend flags, replacing earlier ones. Must come last.")
    setter.set_defaults(func=cmd_set)

    add = sub.add_parser("add")
    add.add_argument("role")
    add.add_argument("--backend", choices=BACKENDS, required=True)
    add.set_defaults(func=cmd_add)

    rehydrate = sub.add_parser("rehydrate")
    rehydrate.add_argument("role")
    rehydrate.add_argument("--backend", choices=BACKENDS)
    rehydrate.add_argument("--model")
    rehydrate.add_argument("--env", action="append", metavar="KEY=VALUE")
    rehydrate.add_argument("--reason")
    rehydrate.set_defaults(func=cmd_rehydrate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
