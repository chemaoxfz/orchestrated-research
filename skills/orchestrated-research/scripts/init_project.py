#!/usr/bin/env python3
"""Scaffold an orchestrated-research project. Existing files are never overwritten.

    init_project.py DIR --title "..." --slug short-name --reader "who reads the tutorial"
        [--backend B] [--tutorial-backend B] [--technical-backend B] [--model M] [--update-tools]

Creates the records, role folders, roster, agent definitions for Claude Code and Codex,
and copies role.py and records.py into DIR/tools, so the project stands on its own.
Standard library only.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
WRITERS = ("tutorial-writer", "technical-writer")
DISPOSABLE = ("fresh-reader", "companion-reader", "verifier")
BACKENDS = ("codex", "claude", "dsh", "codex-live", "manual")
TEX_SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
               "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def fill(text, values):
    return re.sub(r"\{\{(\w+)\}\}", lambda match: values.get(match.group(1), match.group(0)), text)


def tex_escape(text):
    return re.sub(r"[\\&%$#_{}~^]", lambda match: TEX_SPECIAL[match.group(0)], text)


def place(source, target, values, report):
    """Copy one template file. Never overwrite, so a rerun is safe."""
    if target.exists() or target.is_symlink():
        report["kept"].append(str(target))
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix == ".tex":
        values = {**values, "TITLE": tex_escape(values["TITLE"]), "READER": tex_escape(values["READER"])}
    target.write_text(fill(source.read_text(encoding="utf-8"), values), encoding="utf-8")
    report["created"].append(str(target))


def scaffold(project, values, report):
    tree = ASSETS / "project"
    for source in sorted(path for path in tree.rglob("*") if path.is_file()):
        relative = source.relative_to(tree)
        if source.name == ".DS_Store":
            continue
        name = str(relative).replace("__SLUG__", values["SLUG"])
        place(source, project / name, values, report)
    for folder in ("code", "data", "figures", "revisions/orchestrator/messages", "revisions/orchestrator/briefs",
                   "revisions/orchestrator/reports", "revisions/snapshots"):
        (project / folder).mkdir(parents=True, exist_ok=True)


def roles(project, values, backends, model, report):
    source_root = ASSETS / "roles"
    for role in ("orchestrator",) + WRITERS:
        folder = project / "roles" / role
        for filename in ("CHARTER.md", "MEMORY.md", "HANDOFF.md"):
            place(source_root / role / filename, folder / filename, values, report)
    roster_path = project / "roles" / "roster.json"
    if roster_path.exists():
        report["kept"].append(str(roster_path))
        return
    roster = {"version": 1, "roles": {}}
    for role in WRITERS:
        roster["roles"][role] = {"backend": backends[role], "thread": None, "model": model, "args": [], "env": {},
                                 "status": "active", "history": [], "last_turn": None}
    roster_path.write_text(json.dumps(roster, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report["created"].append(str(roster_path))


def adapters(project, values, report):
    """Write the vendor agent files. A sandbox may protect these folders, and the project works without them."""
    source_root = ASSETS / "agents"
    for vendor, folder, suffix in (("claude", ".claude", "md"), ("codex", ".codex", "toml")):
        try:
            for role in WRITERS + DISPOSABLE:
                place(source_root / vendor / f"{role}.{suffix}", project / folder / "agents" / f"{role}.{suffix}", values, report)
        except OSError as exc:
            report["warnings"].append(
                f"could not write {folder}/agents: {exc}. Some agent files are missing. A sandbox may protect this folder. "
                "To add them, rerun this command from your own shell. Until then, tell each subagent to read its role folder first."
            )
    # Claude Code keeps a subagent's memory in .claude/agent-memory/<role>. Point it at the role folder,
    # so one MEMORY.md serves every vendor. If links are unavailable, the charter still names the file.
    memory_root = project / ".claude" / "agent-memory"
    try:
        memory_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        report["warnings"].append(f"could not create {memory_root}: {exc}.")
        return
    for role in WRITERS:
        link = memory_root / role
        if link.exists() or link.is_symlink():
            report["kept"].append(str(link))
            continue
        try:
            os.symlink(Path("..") / ".." / "roles" / role, link, target_is_directory=True)
            report["created"].append(f"{link} -> roles/{role}")
        except OSError as exc:
            report["warnings"].append(f"could not link {link}: {exc}. Claude Code will keep a second memory there.")


def tools(project, update, report):
    target = project / "tools"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("role.py", "records.py"):
        destination = target / name
        if destination.exists() and not update:
            report["kept"].append(str(destination))
            continue
        shutil.copy2(SKILL / "scripts" / name, destination)
        report["created"].append(str(destination))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project")
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", required=True, help="short file-name stem: lowercase letters, digits, hyphens")
    parser.add_argument("--reader", required=True, help="who reads the tutorial, in one phrase")
    parser.add_argument("--backend", choices=BACKENDS, default="manual", help="default backend for both writers")
    parser.add_argument("--tutorial-backend", choices=BACKENDS)
    parser.add_argument("--technical-backend", choices=BACKENDS)
    parser.add_argument("--model")
    parser.add_argument("--update-tools", action="store_true", help="refresh tools/role.py and tools/records.py")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        parser.error("--slug must use lowercase letters, digits and single hyphens")
    backends = {"tutorial-writer": args.tutorial_backend or args.backend, "technical-writer": args.technical_backend or args.backend}
    if args.model and len(set(backends.values())) > 1:
        parser.error("--model applies to both writers, and they use different backends. After scaffolding, set each with `tools/role.py set ROLE --model M`.")

    project = Path(args.project).expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)
    values = {"TITLE": args.title, "SLUG": args.slug, "READER": args.reader, "DATE": dt.date.today().isoformat(),
              "TUTORIAL": f"{args.slug}-tutorial.tex", "TECHNICAL": f"{args.slug}-technical.tex"}
    report = {"created": [], "kept": [], "warnings": []}
    scaffold(project, values, report)
    roles(project, values, backends, args.model, report)
    tools(project, args.update_tools, report)
    adapters(project, values, report)

    print(f"{len(report['created'])} created, {len(report['kept'])} kept unchanged, in {project}")
    for line in report["warnings"]:
        print(f"WARNING {line}")
    print("Next: save the author's request verbatim in PROMPT-LOG.md, then fill in PROJECT_STATE.md.")
    print("Restart any running agent session, so it loads the new agent definitions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
