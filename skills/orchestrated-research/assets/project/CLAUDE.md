# Claude Code entry point

The rules live in `AGENTS.md`, imported below. It is the single source of truth for every agent.
Edit rules there, not here.

@AGENTS.md

## Mechanics mapped to Claude Code

| Generic | Claude Code |
| --- | --- |
| A dedicated writer | The subagent `tutorial-writer` or `technical-writer` in `.claude/agents/`, or `python3 tools/role.py send`. |
| A fresh reader or verifier | The subagent `fresh-reader` or `verifier`. A new instance each time. |
| Continue a writer in this session | `SendMessage` with its name or agent ID. |
| A writer in another live session | `ListAgents`, then `SendMessage`. |

Before compacting, write the checkpoint into your own role's `roles/<role>/HANDOFF.md`, so a resumed session loses nothing.
The orchestrator's is `roles/orchestrator/HANDOFF.md`.
