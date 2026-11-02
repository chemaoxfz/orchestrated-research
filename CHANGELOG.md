# Changelog

## 0.2.0, 2026-11-02

First public version.

- Released under the MIT license. `LICENSE` replaces `NOTICE`.
- `role.py`: roster changes take a lock, so parallel turns no longer lose a role's thread. Moving a role to another backend retires its old thread. Logs of quick turns no longer overwrite each other. `add` writes the Claude agent file for a role on `claude`. Rehydrating to `codex-live` says how to bind the live session. Role names are checked.
- `watch_threads.py`: a new watch saves its starting point at once, so a restart replays what arrived while it was stopped.
- `install.sh`: never replaces or removes a copy you have edited.
- `macro.tex` gains an `assumption` environment.
- `write-tutorial`: an approximate result states its regime and its accuracy. The exemplar's tutorial version now does, and its placeholders are marked.
- Ownership, handoff and distillation rules now agree across files. A published value is real or synthetic according to its source.

## 0.1.0, 2026-11-02

First version, distilled from two long research projects and generalized for sharing.

- `orchestrated-research`: roles, stages, records and dedicated agents, with a project scaffold and a dispatcher for Codex, Claude Code and the DeepSeek harness.
- `orchestrate-agents`: the orchestrator's craft, with tools for watching and steering live Codex threads.
- `write-tutorial` and `write-companion`: the two documents' standards, with a worked exemplar.
- `iterate-research`, `polish-manuscript` and `simplify-rules`: generalized from their project versions.
