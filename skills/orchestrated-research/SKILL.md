---
name: orchestrated-research
description: Run a long research project as an orchestrator of dedicated agents, in stages, delivering a human-readable tutorial written like the main text of a high-impact paper and a technical companion that holds every derivation, proof, computation and algorithm. Use when the author wants to develop a theory, method or computational result into a paired writeup over many sessions, to coordinate writer and verifier agents across Claude, Codex, DeepSeek or other tools, to keep agents with dedicated memory, or to resume such a project. A single question, a small edit or a one-off essay does not need this.
metadata:
  version: "0.1.0"
  source: "https://github.com/chemaoxfz/orchestrated-research"
---

# Orchestrated research

One agent stays the orchestrator. It keeps the author's intent, runs the stages, and checks everything independently.
Dedicated writers own the two documents and make the edits.
Fresh readers and verifiers review each delivery and then go away.
The durable project lives in files, so any agent on any vendor can take over a role.

## The two documents have different jobs

| | Tutorial | Technical companion |
| --- | --- | --- |
| Model | The main text of a high-impact paper | The supplement that a referee checks |
| Reader | Accepts every statement and wants to understand, follow, use and appreciate the method | Wants to see that each statement is true |
| Test of a passage | Does it help that reader use the method or see the point? | Does this statement have its argument, its scope and its evidence? |
| Holds | The question, the procedure, the decisive calculations, the pictures and the results | Derivations, proofs, algorithms, computations, complete tables and limits |
| A missing proof | Not a defect | A defect |
| Skill | `write-tutorial` | `write-companion` |

A review standard that fits one document is wrong for the other.
Keep them separate in every brief and every review.

## Roles

| Role | Lifetime | Owns | Runs as |
| --- | --- | --- | --- |
| Orchestrator | Dedicated | `PROJECT_STATE.md`, `AUTHOR-LEDGER.md`, `GOAL-RUN.md`, `roles/orchestrator/`, `revisions/orchestrator/` | The session the author talks to |
| Tutorial writer | Dedicated | The tutorial, its figures, shared macros, `TUTORIAL-DESIGN.md`, `AUTHOR-PREFERENCES.md` | See [dedicated agents](references/dedicated-agents.md) |
| Technical writer | Dedicated | The companion, `TECHNICAL-DESIGN.md`, `guidance/NOTATION.md`, `RESULTS-LEDGER.md`, code and data | See [dedicated agents](references/dedicated-agents.md) |
| Fresh reader | Disposable | Its report | A new subagent for each review of the tutorial |
| Companion reader | Disposable | Its report | A new subagent for each review of the companion |
| Verifier | Disposable | Its report | A new subagent for each check |
| Scout | Disposable | Its report or fetched files | A new subagent for an inventory or a literature fetch |

Writers are dedicated because a long argument needs one continuous owner.
Readers and verifiers are disposable because their independence is the point. An agent that remembers the last draft cannot read as a newcomer.

One writer per file. The orchestrator edits only its own records, briefs and scripts.

## Start a project

1. Choose how the writers run. Read [dedicated agents](references/dedicated-agents.md). The choice is `codex`, `claude`, `dsh`, `codex-live` or `manual`. It can differ per writer and change later. An orchestrator inside a Codex sandbox uses `manual` with native subagents.
2. Scaffold the project, with this path relative to this skill's folder:
   ```
   python3 scripts/init_project.py <project-folder> --title "..." --slug short-name --reader "who reads the tutorial" --backend <choice>
   ```
   It never overwrites a file, so it is safe in an existing folder. It creates the records, role folders, roster and agent definitions, and copies `role.py` and `records.py` into `<project-folder>/tools`. See the project's `AGENTS.md` for who owns what. To use native subagents, restart the session now, so it loads the new agent definitions.
3. Save the author's request verbatim in `PROMPT-LOG.md`. Keep doing this for every later request.
4. Inventory what already exists, with one scout per part, using [the inventory brief](assets/briefs/inventory.md). Spot-check the TESTED and CLAIMED items yourself. A plan built on a claimed result is the most expensive mistake available.
5. Fill in the objective, the reader, what the reader can do after reading, and the stopping condition in `PROJECT_STATE.md`.
6. Show the author the plan, the stages and your questions once, in one short message. Ask only what changes the work, and always ask which one or two documents set the standard for the tutorial. If the author names none, propose one. The tutorial writer records it as the clarity bar in `TUTORIAL-DESIGN.md`.
7. Once the author answers, or at once if the author said not to wait, keep going. See [the author's place](#the-authors-place).

## Resume a project

Read `roles/orchestrator/HANDOFF.md` from its newest entry, then `PROJECT_STATE.md`.
Run `python3 tools/role.py list`.
Read what each writer did since then.
Continue from the handoff's next step.
A historical plan or completion note is evidence, not an instruction.

## Run in stages

[The stage guide](references/stages.md) holds the full method.
A stage is one part of the work carried through both documents, from a smallest complete version to a larger one.
Each larger level uses the previous level's results as a sanity check.

After every stage, in this order:

1. **Snapshot** source and PDF with checksums, before sending any new message. A queued message can start the next turn at once, and the live file then changes under you.
2. **Ledger pass.** Check the rows that [the stage guide](references/stages.md#the-loop-after-every-stage) names against the delivered document.
3. **Purpose pass.** Apply the purpose test to each changed subsection.
4. **Form pass.** Check each table and figure against the first instance of its kind.
5. **Read the rendered pages first-hand**, in reader order.
6. **Independent review** by fresh readers of the tutorial, companion readers and verifiers, briefed with the current aims.
7. **Filter** every finding against the definitions and the author's aims. Send numbered items. Start the next stage.

Use the skill `orchestrate-agents` for messages, delegation and the review of each delivery.

## The author's place

The author steers. The agents do the routine work.

- **Keep going.** No stage waits for the author's reading unless the author asked for that. Apply feedback when it arrives. Report done work briefly and carry on.
- **Do not invent gates.** Before saying something needs the author's decision, check that the author actually set that rule. If they did not, settle it with a recorded procedure, or decide it and say so.
- **Silence is not a decision.** Never cite what the author has not mentioned, or a statement made before they saw something, as a reason for or against it.
- **Distill.** After every two or three author corrections, name the aim they share in one line. Tell the author, send it to the writer as a whole-document pass, and record it in `AUTHOR-PREFERENCES.md`. Line-by-line corrections are examples of a few principles.
- **Delivered, reviewed and accepted are three states.** Only the author can accept.
- **Report short.** Lead with the state of the document and any decision needed. Point to the document, not to records. The author reads the document.

## Honesty rules

The tutorial stays constructive. It shows what the method does and leaves out rebuttals and lists of what other approaches cannot do.
This rule controls what the text talks about. It never changes the evidence.

- A failed test goes to the author at once, before the text says anything about it.
- A prior result is not lifted into a document without a rerun. Quarantine it in `PROJECT_STATE.md` until then.
- Every number has a row in `RESULTS-LEDGER.md`, labeled real or synthetic, and new, reproduced or compared.
- A mathematical suggestion is a claim to prove and test, whoever made it, including the author.
- A conjecture, a numerical observation and a proved result never share a label.
- Write unfinished demonstrations as "Result to complete" boxes, with a design and an expected outcome stated so that a result can contradict it. Never draw a curve for a computation that has not run.

## Records

[The records guide](references/records.md) gives each file's job and owner.
The core rule is one record per job, with no parallel logs.
Keep a before-state of any substantial change in `revisions/`.

`python3 tools/records.py` checks the ledgers and makes snapshots. It finds mechanical errors only. A clean check says nothing about whether the argument is right.

## Bundled skills

| Skill | Use it for |
| --- | --- |
| `orchestrate-agents` | The orchestrator's messages, delegation, review of a delivery and watching live threads |
| `write-tutorial` | The tutorial's style and teaching method, held tightly |
| `write-companion` | The technical companion's standard of evidence |
| `iterate-research` | A bounded research run with a target, a budget and a resumable checkpoint |
| `polish-manuscript` | Revising a section or whole document as a complete argument |
| `simplify-rules` | Finding the deciding quantity, merging rules and carrying the simplification through |

For a short standalone essay, the separate public skill `research-essay` in `chemaoxfz/idea-to-essay` fits better than this one.
Its essay can also seed a project like this.

## Literature

Anything a claim rests on gets its full text archived and read. See [the literature guide](references/literature.md).
