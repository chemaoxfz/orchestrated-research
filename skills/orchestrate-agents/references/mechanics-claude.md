# Driving Claude Code from an orchestrator

Tested with Claude Code 2.1.316.

## Subagents in one session

Define them in `.claude/agents/<name>.md`. `init_project.py` writes these files. Start a new session after creating them, so it loads them.

Each call to the Agent tool starts a fresh instance.
`SendMessage` to a finished subagent, by name or agent ID, resumes it with its full conversation.
Its transcript survives compaction of the parent and `claude --resume` of the same session.
Names from before the parent's last compaction do not survive, so keep the agent ID for anything long-lived.

Claude Code deletes transcripts after `cleanupPeriodDays`, which defaults to 30. Set it high in a long project. Agent memory folders are not part of that cleanup.

## Durable memory for a subagent

`memory: project` in the agent's frontmatter gives it the folder `.claude/agent-memory/<name>/`.
The first 200 lines or 25 KB of `MEMORY.md` in that folder are injected into its system prompt, with instructions for keeping it.
In a test, a fact saved in one session was recalled by the same subagent in a separate later session.
The scopes `user` and `local` use `~/.claude/agent-memory/<name>/` and `.claude/agent-memory-local/<name>/`.
`init_project.py` links the project folder to `roles/<name>/`, so one memory file serves every vendor.

## A session as a dedicated writer

    claude -p --agent tutorial-writer --output-format json --permission-mode acceptEdits "<message>"
    claude -p --agent tutorial-writer --output-format json --permission-mode acceptEdits --resume <session-id> "<next message>"

The JSON result gives `session_id` and `result`.
A writer needs its tools allowed in advance, because `-p` cannot ask. `tools/role.py` allows build and check commands by default: `latexmk`, `records.py`, checksums and the PDF tools. Replace that list with `python3 tools/role.py set <role> --args --allowedTools "Bash(latexmk *)" "Bash(python3 code/*)"`. Allowing `python3 code/*` lets the writer run whatever it writes, so that choice is yours.

## Live sessions

Name each one when you start it: `claude -n tutorial-writer`.
Find peers with `ListAgents`, and send with `SendMessage` to the name. Add `notify_when_idle` to hear when a session goes idle, instead of polling.
Messages are plain text, not shared history. A peer running in a different permission mode can hold a message for its user's approval.
This needs Claude Code 2.1.224 or later on macOS, Linux and WSL 2, or 2.1.234 or later on native Windows. According to the documentation, `notify_when_idle` needs 2.1.236 or later in both sessions.

## Other notes

Long watches run under the Monitor tool, which turns each line of a script's output into a notification, and needs re-arming when it expires.
Agent teams are a separate experimental feature. This workflow does not need them.
A plugin can ship skills and agents, but plugin agents ignore `hooks`, `mcpServers`, `permissionMode` and `initialPrompt`. This workflow writes agent files into the project instead, so a plain skill install and a plugin install behave the same.
