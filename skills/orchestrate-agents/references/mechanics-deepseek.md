# Driving the DeepSeek harness from an orchestrator

Tested with `dsh 0.2.0-rc.2`, on one small smoke test of a first turn and a resumed turn. It has not been used on a long writing job.

## A dedicated writer run turn by turn

Sessions persist, one folder per working directory under `~/.dsh/sessions`, and resume by ID.

    cd <project> && DSH_PERMISSION_MODE=workspace-write dsh headless --json - < first-message.md
    cd <project> && DSH_PERMISSION_MODE=workspace-write dsh headless --json --session-id <id> - < next-message.md

With `--json`, the first event gives the ID, and the last gives the reply:

    {"type":"session","sessionId":"session-...","cwd":"..."}
    {"type":"final","text":"..."}

`tools/role.py` does all of this, and records the session in the roster.
The event schema is not a documented contract, so check it again after an upgrade.

## Limits to plan around

- **Sandbox.** `DSH_PERMISSION_MODE` is `read-only`, `workspace-write` (writes only under the current folder) or `danger-full-access`. Never use `danger-full-access` for delegated work. `role.py` refuses it.
- **Foreground commands have a 60-second limit.** The package's documentation says a command reaching it can continue as a background job (`promoteOnTimeout`). This was not tested. Ask for short computations, run a long job yourself and give the harness its output, or give that job to another backend.
- **There is no definition file for a custom agent.** The charter and memory reach it through the first prompt, which `role.py` writes.
- **Installation.** `npm i -g @deepseek-ai/dsh`. In a non-interactive shell, add `$(npm config get prefix)/bin` to `PATH`.

## Starting the workflow and its reviewers

Tell the harness to read `skills/orchestrated-research/SKILL.md`, or its installed copy, and follow it.
Run a disposable reader as a new `dsh headless` session in the project folder, with the filled-in brief as its message and no `--session-id`.

## How far to trust it

Check its reports as you would any delegated report, and check its high and medium items before you rely on them.
Keep a small record of which delegated reports held up, per vendor, if you route audits to it.
In one side-by-side mathematical review, it missed items another agent found. Start it on bounded work, and compare before giving it a writer's role.
