# Driving Codex from an orchestrator

Tested with `codex-cli 0.166.0`.
The CLI commands are public. The thread database schema and control socket used by `scripts/` are internal and can change with any release. If a script fails, run `codex --version` and read the schema again before trusting it.

## A dedicated writer run turn by turn

This is the simplest way to keep a writer. Its thread persists and resumes from any new process.

    codex exec --json --skip-git-repo-check -s workspace-write -C <project> "<brief>" < /dev/null
    codex exec resume <thread-id> --json --skip-git-repo-check -c 'sandbox_mode="workspace-write"' "<next message>" < /dev/null

The first JSON event gives the id: `{"type":"thread.started","thread_id":"..."}`.
The final reply is the last `item.completed` event whose item has type `agent_message`.
`codex exec resume` takes no `-s` or `-C` flag, so set the sandbox with `-c` and start it from the project folder.
`tools/role.py` does all of this, and records the thread in the roster.

## A live session someone can also type into

Start it yourself in a terminal in the project folder, with a stable name, then read its id from `$CODEX_HOME/session_index.jsonl`. Names can repeat, so address threads by UUID.

- `codex queue --thread <UUID> --message "<text>"` waits for the current turn to end. Into an idle thread, it starts a new turn at once.
- `scripts/steer.py --thread <UUID> --message-file <file>` sends a message into the running turn. It refuses when no turn is active.
- A turn the author keeps steering can run for hours, so a queued message can go stale. A writer also reads shared files by itself, which can deliver content sooner.

## Reading what a thread did

`$CODEX_HOME/thread_history_1.sqlite` holds each thread. Always open it read-only.

- `thread_items` has one row per completed item, ordered by `rollout_ordinal`. Types include `userMessage`, `agentMessage`, `fileChange`, `commandExecution` and `contextCompaction`. Text is in `item_json` at `$.text` or `$.content[0].text`.
- The last row of `thread_turns` gives the status: `inProgress` or `completed`.

## Scripts

| Script | Job |
| --- | --- |
| `scripts/read_thread.py --thread UUID [-n 5]` | Print a thread's recent messages and turn status |
| `scripts/watch_threads.py --state-dir DIR NAME=UUID ...` | Stream new messages and status changes, one line per event, replaying from its state files after a restart |
| `scripts/wait_threads.py NAME=UUID ...` | Block until a thread changes, then exit. Use while everything is idle. |
| `scripts/steer.py --thread UUID --message-file FILE` | Send a message into the running turn |

Set `CODEX_HOME`, or pass `--codex-home` to the read-only scripts, when a project uses a second account.
Use one watcher per Codex home. Keep state files outside any session scratchpad.

## Fresh disposable agents

    codex exec --skip-git-repo-check -s workspace-write -C "$PWD" --ephemeral -o "$PWD/last.md" "$(cat brief.md)" < /dev/null > log.txt 2>&1

Run it from a fresh scratch folder, as a background task. The sandbox lets it read the project but write only in its folder.
Outside a git repository, `--skip-git-repo-check` is required.
Tell the brief to write its report to `report.md`, never to `last.md`, because `-o` overwrites that file with the final chat message when the run ends.

## Native subagents

Custom agents are TOML files in `.codex/agents/` (project) or `~/.codex/agents/` (personal), each with `name`, `description` and `developer_instructions`.
A parent spawns one by name when asked. `init_project.py` writes these files.
Use them for work inside one session. Use `codex exec resume` when a writer must outlive the session.
