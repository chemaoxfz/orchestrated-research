# Dedicated agents

A dedicated agent is a role that outlives any one turn, session or vendor.
Read this when choosing how the writers run, or when a writer's thread is lost, stale or out of quota.

## What makes a role dedicated

A role has two layers.

**The durable layer is files, and it is what the role really is.** `roles/<role>/CHARTER.md` says what it owns. `MEMORY.md` holds its durable lessons. `HANDOFF.md` holds its current state and exact next step. Together with the project's records, these are enough for a new agent on any vendor to continue the role.

**The live layer is a thread, and it is a convenience.** A resumed thread keeps the working detail that never reached a file, and it costs less to continue than to re-read everything. Threads get lost, go stale, run out of quota, and get compacted.

On the long projects this workflow comes from, writers had to change account partway through when one ran out of quota. Work continued, because the records held what mattered.
So the rule is: **keep the files current, as if the thread could vanish after any turn.**

Readers and verifiers stay disposable on purpose. Their use comes from not knowing how the draft was made.

## Three ways to run the writers

| | What it is | Best when | Cost |
| --- | --- | --- | --- |
| **A. Dispatched threads** | One session. Writers are resumable threads, driven turn by turn by `tools/role.py`. | The usual choice outside a Codex sandbox. A single person, any mix of vendors. | The orchestrator waits for a turn to end, or runs it in the background. |
| **B. Native subagents** | One session. Writers are the runtime's own subagents, kept alive inside that session. | You work in one tool, in one long session. | Context ties to that session. Keep the files current. |
| **C. Separate live sessions** | Each writer has its own terminal. The orchestrator relays to it and watches it. | You also want to talk to the writers directly. This is how the workflow began. | Needs a watcher, and you manage the terminals. |

You can mix them per writer and change later.
`python3 tools/role.py rehydrate <role> --backend <other>` moves a role to a new thread on `codex`, `claude` or `dsh`, and `set <role> --backend <other>` does the same. The role's files carry over, and the old thread stays in the roster's history. Moving to another backend also clears the role's model and flags, because they belonged to the old vendor. A `codex-live` role needs a live session that you start: bind it with `set <role> --thread <UUID>`, and make its first message point it at its role folder.

## A. Dispatched threads

```
python3 tools/role.py set technical-writer --backend codex
python3 tools/role.py send technical-writer --message-file revisions/orchestrator/messages/20260315-C1-part1.md
python3 tools/role.py reply technical-writer
python3 tools/role.py list
```

`send` refuses a message that is not on file or does not start with "From <sender>:". It runs one turn at a time per role, records the thread in `roles/roster.json`, logs the raw output under `roles/<role>/runs/`, and writes the reply to `roles/<role>/last-reply.md`.
It never resends after a failed turn, because delivery may be ambiguous. Read the log and decide.
A long turn blocks, so run `send` as a background task where the runtime allows it.

The orchestrator must run outside a Codex sandbox to use `role.py` with the `codex` backend. From inside `workspace-write`, the nested `codex exec` fails with `failed to initialize in-process app-server client: Operation not permitted`. A Codex orchestrator in that sandbox uses native subagents instead.

Set model, account and flags per role:

```
python3 tools/role.py set technical-writer --model <model> --env CODEX_HOME=~/.codex-second
python3 tools/role.py set technical-writer --backend claude --args --allowedTools "Bash(latexmk *)" "Bash(python3 code/*)"
```

`--args` must come last. It replaces the earlier flags.
The `claude` backend cannot ask for approval, so `role.py` allows build and check commands by default: `latexmk`, `records.py`, checksums and the PDF tools. A writer that runs project code needs a list like the one above, and allowing it lets the writer run whatever it writes.
A dispatched writer's output arrives when its turn ends. It records its plan in its handoff, and you steer between turns.
The `dsh` backend takes its model from `~/.dsh`, so `--model` does not apply to it.

| Backend | First turn | Later turns |
| --- | --- | --- |
| `codex` | `codex exec --json -s workspace-write -C <project> -` | `codex exec resume <id> --json -c 'sandbox_mode="workspace-write"' -` |
| `claude` | `claude -p --agent <role> --output-format json --permission-mode acceptEdits --allowedTools ...` | The same, with `--resume <id>` |
| `dsh` | `dsh headless --json -` with `DSH_PERMISSION_MODE=workspace-write` | The same, with `--session-id <id>` |
| `codex-live` | `codex queue --thread <id> --message ...`, into a live session | The same |
| `manual` | Tells you to deliver the file yourself | The same |

Any other agent works through `manual`, or by adding a backend: a command, and a parser that returns the thread, the reply and any failure.

## B. Native subagents

**Claude Code.** `init_project.py` writes `.claude/agents/tutorial-writer.md` and `technical-writer.md`, with `memory: project` and the skills they need.
Claude Code keeps a subagent's memory in `.claude/agent-memory/<role>/`, and injects the first 200 lines or 25 KB of `MEMORY.md` into its system prompt. The scaffold links that folder to `roles/<role>/`, so one file serves every vendor.
Ask for the subagent by name, then continue it with `SendMessage`. That keeps its full conversation, including after compaction of the parent and `claude --resume` of the same session.
A new session starts a new instance, which still has the memory. Start a new session after running `init_project.py`, so it loads the definitions.

**Codex.** `init_project.py` writes `.codex/agents/<role>.toml`, with `name`, `description` and `developer_instructions`. A parent spawns one by name when asked, if the files existed when the session started.
Codex has no per-agent memory field, so the instructions tell the agent to read and update `roles/<role>/MEMORY.md`.
Inside a `workspace-write` sandbox, `.codex/` is protected, so the scaffold skips those files and warns. Run the scaffold from your own shell if you want them. Otherwise, spawn a generic subagent and tell it to read its role folder first and update it last.
Use a dispatched thread when the writer must outlive the session.

**DeepSeek.** The harness has no custom agent file. Use a dispatched thread.

**Other agents.** If the agent has subagents, tell each one to read its role folder first and update it last. If it has none, use the last section of this guide.

## C. Separate live sessions

Start each writer yourself, in the project folder, with a stable name.

- **Codex:** start it in a terminal, and find its UUID in `$CODEX_HOME/session_index.jsonl`. Bind it with `python3 tools/role.py set tutorial-writer --backend codex-live --thread <UUID>`. Use `scripts/steer.py` of `orchestrate-agents` to reach a running turn. Use `watch_threads.py` to keep a live watch.
- **Claude Code:** start it with `claude -n tutorial-writer`. From the orchestrator, use `ListAgents` and `SendMessage`. Set the role's backend to `manual` so the roster stays true.

Tell each writer on its first turn to read its role folder, because a live session you started by hand got no first-turn prompt.
Keep watching live writers. The author may instruct them directly, and you need to see it.

## What was tested, and how

| Claim | Evidence |
| --- | --- |
| A Claude subagent's `memory: project` survives into a separate later session, including through the link to `roles/<role>/` | Saved in one `claude -p` session, recalled by the subagent in another, Claude Code 2.1.316 |
| A role keeps its conversation across processes, on each of `claude`, `codex` and `dsh` | A detail given in turn 1, in conversation only, was recalled in turn 2 from a new process. `codex` and `dsh` were tested through `role.py`, and `claude` directly with `claude -p --resume`, because the writer in the `role.py` run also noted the detail in its handoff. |
| A resumed writer can still write to the project | Each wrote a file on its resumed turn |
| A dispatched Claude writer runs its build without approval, and a command off its list is refused | In one turn through `role.py`, Claude Code 2.1.316: `latexmk` and `pdfinfo` ran, and `curl` was denied with "This command requires approval". Only these three commands were tried. |
| A rehydrated role continues from its files | A new Codex thread on the same role read its role folder, took the durable word from `MEMORY.md`, and found the conversation-only detail by searching the saved message and reply files |
| `role.py` cannot start a Codex writer from inside a Codex sandbox | From a parent in `workspace-write`, the nested `codex exec` failed as quoted above, `codex-cli` 0.166.0. `role.py` recorded the failure and did not resend. |
| A Codex custom agent file loads and applies | Spawned by name, it quoted its instructions, `codex-cli` 0.166.0 |
| Codex native subagents can hold the writer roles through files alone | On a two-page project in `workspace-write`, with no custom agent files, a parent ran both writers, a fresh reader and a verifier as generic subagents, and continued the writers with follow-up messages, `codex-cli` 0.166.0. Both documents built and passed review. This tested continuation inside one parent session only. |

These were small smoke tests. Long writing jobs ran on Codex writer threads in the original projects. The `claude` and `dsh` backends have not yet run a long job. Details that depend on a version are listed in the mechanics files of `orchestrate-agents`.

## Things that do not persist

- A Claude Code subagent's conversation does not reach an unrelated new session. Its memory does.
- Claude Code deletes transcripts after `cleanupPeriodDays`, which defaults to 30. Raise it for a long project. Codex and the DeepSeek harness have their own retention settings. Check them.
- A thread can be compacted at any time, and working detail can vanish then. Files do not.
- Vendor-specific memory, such as an account-level memory feature, does not travel with the project. Keep what matters in `roles/<role>/`.

## No subagents at all

If the agent can run only one thread, it can still follow the workflow, at a real cost in independence.
Work in role-labeled passes. To start a pass, read that role's charter, memory and handoff. To end it, update those files, and say which role you have left.
Run reader and verifier passes in a fresh session whenever you can. A reader who wrote the draft misses what a fresh reader finds, so tell the author plainly when no independent review has happened.
