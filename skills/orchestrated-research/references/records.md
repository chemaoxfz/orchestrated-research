# Records

Each file has one job and one owner. Do not start another log.
If a fact belongs in an existing record, it goes there.

| File | Job | Owner |
| --- | --- | --- |
| `AGENTS.md` | The rules every agent loads, and who owns what. `CLAUDE.md` only imports it and maps mechanics. | Orchestrator |
| `PROMPT-LOG.md` | The author's requests, verbatim, once, numbered | Whoever receives the prompt |
| `PROJECT_STATE.md` | Objective, stopping condition, status, writer locks, author decisions, stages, build evidence | Orchestrator |
| `AUTHOR-LEDGER.md` | Every author request as a row, with status and evidence | Orchestrator |
| `AUTHOR-PREFERENCES.md` | What recurs: rule, reason, origin. Canonical terms. | Tutorial writer |
| `TUTORIAL-DESIGN.md` | The tutorial's claim, spine, forms and route, as the source now is | Tutorial writer |
| `TECHNICAL-DESIGN.md` | The companion's argument and claim verdicts, as the source now is | Technical writer |
| `guidance/NOTATION.md` | Each symbol: what it is, its type and where it is defined | Technical writer |
| `RESULTS-LEDGER.md` | Every number: data, labels, command, checksum | Technical writer |
| `GOAL-RUN.md` | The rules of an unattended run | Orchestrator |
| `roles/<role>/CHARTER.md` | What a role owns and how it works | Orchestrator |
| `roles/<role>/MEMORY.md` | The role's durable lessons | The role |
| `roles/<role>/HANDOFF.md` | The role's current state and exact next step | The role |
| `roles/roster.json` | Which backend and thread run each role now, with the history of superseded threads | `tools/role.py` |
| `revisions/` | Before-states, snapshots, plans, deliveries | Whoever made them |
| `revisions/orchestrator/messages/` | Every message, saved before it is sent | Orchestrator |
| `revisions/orchestrator/briefs/` and `reports/` | Subagent briefs and their reports | Orchestrator |
| `literature/INDEX.md`, `NEEDED.md` | Full texts held, and what the author is asked to fetch | Scout or writer |

## The rules that make these useful

**Verbatim beats summary.** A summary loses what the author meant. Keep the author's own words in `PROMPT-LOG.md`, and read them again before each delivery. A request is logged once, by the agent the author sent it to. The orchestrator logs what it relays.

**Design records describe the source.** A design record that describes the plan instead of the source is a trap. Change it in the same turn as the source. A plan stays a proposal until it is authorized.

**Update, do not append.** A new rule replaces the one it supersedes. Two competing rules are worse than none. Keep a rule's reason and origin with it, so a later agent can judge its scope.

**Keep the evidence recoverable.** A number in a document cites its ledger row in a source comment. The companion's claim table maps each tutorial claim to the statement that establishes it. A row points to a command and a checksum. A reader of the record can always walk back to the source.

**Copy what you build on.** If this project relies on a file from a sibling project, either copy it here with its provenance and change the copy, or correct the original in place when other projects should get the same correction. In that case, check the file's version-control status first, keep the edit minimal, and record it. Do not park a known error in a report because of a folder boundary.

**Keep transcripts.** Agent transcripts are part of the project's history. Never delete or truncate one without the author's permission. Ask the author to raise the retention setting of any tool that deletes them by default.

## The author ledger, in more detail

A ledger exists because agents forget. On one long project it reached 383 rows, and it caught requests that every summary had dropped.

Build it from the verbatim messages, not from memory. One message usually holds several requests, so make one row per request.
Keep each quote short and exact. `python3 tools/records.py ledger` checks every quote against `PROMPT-LOG.md`.

When mining a transcript for author messages, read every record type the tool writes. A filter on the user role alone can miss messages sent during a running turn. On that project, it missed 23 of 45.

Before accepting a reader's proposed cut, search the ledger for a row the text serves. Readers optimize for reading speed, and they cannot see why a sentence is there.
Check each round against the verbatim requests too, because a later pass can quietly undo what an earlier pass delivered.

## Build evidence

Record for each delivery: source checksum, PDF checksum, page count, whether the log is clean, and which pages you inspected.
Say which version a statement refers to.
On a synced drive, re-check a representative phrase and the checksum before handoff, because a sync can silently revert a write.
