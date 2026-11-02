# Autonomous run

Fill this in when the author says to keep going without them, for example "until everything is done, and at least until 11am".
Copy the instruction verbatim into `PROMPT-LOG.md` and quote it here.
The orchestrator owns this file. Delete nothing when the run ends. Mark it finished and say what is finished and what is not.

## Goal

Author's instruction:

Done means: the stopping condition in `PROJECT_STATE.md` holds.

Stop time, and whether the author set it as a limit or a minimum:

## After every stage, in this order

1. Snapshot source and PDF with checksums before any new message: `python3 tools/records.py snapshot <label> <files>`.
2. Ledger pass, covering the rows the stage guide of the skill `orchestrated-research` names. Check first-hand or by a verifier, never from the writer's summary.
3. Purpose pass: the purpose test for each changed subsection.
4. Form pass: every table and figure against the first instance of its kind. One name per object.
5. Read the rendered pages first-hand, in reader order, beside a stretch of the reference document for tone and density.
6. Independent reader review of the whole changed part, with the current aims in the brief, and a mathematical check.
7. Filter the reports by the aims and the ledger. Send numbered items. Next stage.

## Standing checkpoints

- Every 30 minutes: writer status, usage limits, one handoff line if anything changed. Re-arm the watcher if writers run live.
- Every 2 hours: re-read the ledger's OPEN rows and the author's recorded aims. Ask: what is forgotten? Are the writers on the main line? Report to the author only if a decision is needed.
- Before each compaction: a handoff entry with this file's path, the stop time and the next step.

## Standing design review

Finishing the ledger does not end the review.
Look for the simpler story at section level, not only for defects.
After every two or three author corrections, name the aim they share, send it as a whole-document pass, and record it.
Filter every reviewer's item through the aims. Protect what the author asked for.
When all stages are delivered, run whole-document read-through passes, section by section, each ending in numbered improvements, until the stopping condition holds and any minimum running time has passed.

## Sequence

Stages planned for this run, in order.

## Constraints

Which agents and accounts may be used. Serial builds. Objects are cut only by the plan's decisions or the author's. Save every message before sending it.
