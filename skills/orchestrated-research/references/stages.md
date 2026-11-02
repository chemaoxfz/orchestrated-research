# Stages

Read this when planning the stages or running a long unattended stretch.

## What a stage is

A stage is one part of the work carried through both documents, with its own done condition.
The technical writer works it out and proves or computes it. The tutorial writer turns it into the reader's route. The orchestrator checks both.
Stages exist because a large document written in one go leaves half-finished parts that hide each other.

Plan them from small to large.
The first stages are small enough to understand completely, and their results become the sanity checks for the larger ones.
The author, on why: "we can do this slowly, in stages, from small to large, right? so that each larger level's result could use the previous level's observations and intuitions as sanity check."

## A typical sequence

| Stage | Work | Done means |
| --- | --- | --- |
| 0 | Records, preferences and inventories | Each inventory separates what is tested from what is only claimed |
| 1 | The method in both documents, on one small running example | A reader can run every step from the tutorial alone, and the companion proves every statement |
| 2 | The most transparent real demonstration | It answers the demonstration questions in `TUTORIAL-DESIGN.md` |
| 3 to n | Each further demonstration or level, small to large | The same form, shorter where it reuses steps, with space spent on what is new |
| last | Whole-document pass on both documents | Every ledger row is settled, and the last independent review has no material item left |

Name them by their work, and number sub-stages when a stage splits, such as 2a and 2b.
A stage may have several rounds. A round is one message to a writer and its delivery.
Keep the author's document order even when the work order differs. Do the less uncertain part first when it informs a harder one.

## The opening of a part

Before writing a part, settle these in the design record:

1. What the part's audience is asking, in their own terms.
2. The smallest case that exercises the deciding operation, with symbolic parameters where the calculation is by hand.
3. What is new, what is reused, and which named procedure steps change.
4. The expected outcome, stated so that a result can contradict it.

## The loop after every stage

Run these in order. `GOAL-RUN.md` holds the same list for an unattended run.

1. **Snapshot.** `python3 tools/records.py snapshot <label> <source> <pdf>`. Do this before any new message, because a queued message starts the next turn and the live file then changes.
2. **Ledger pass.** Check the OPEN and PARTIAL rows of `AUTHOR-LEDGER.md` against the delivered document, along with every DONE row whose evidence this stage changed. At the last stage, and before telling the author that a part is complete, check every row, split among checkers using [the brief](../assets/briefs/ledger-checker.md). Anything claimed done is checked first-hand or by a verifier, never from the writer's summary. Sampling hides failures: sampled passes can keep reporting done while rows are still partial.
3. **Purpose pass.** For each changed subsection, apply the purpose test from `write-tutorial` and search for material that belongs in the companion.
4. **Form pass.** Compare every table and figure with the first instance of its kind. Check that each object has one name.
5. **Read the rendered pages first-hand**, in reader order, beside a stretch of the reference document, for tone, density, caption length and how soon the reader calculates. Writer summaries and reviewer reports are second-hand.
6. **Independent review.** Fresh readers review the tutorial, split by section when it is long, with the current aims pasted into the brief. [Companion readers](../assets/briefs/companion-reader.md) review the companion the same way, to its standard. Verifiers check the mathematics and computations on the delivered source.
7. **Filter and send.** Check each finding against the definitions and the author's aims before relaying it. Protect what the author asked for. Send numbered items with exact locations.

Each review has two passes, and the design pass comes first: does each section belong, is it told in the best order, would a different story teach better? A section can have every number right and still be the wrong content in the wrong order.

## Baseline first, then depth

The author can set a required minimum for every example, naming the objects each one must show. Audit against it before other review questions.
A plan to cut a table or figure must not remove one of those objects.
Better narrative, deeper analysis and more interesting structure follow once the baseline holds.

## Standing checkpoints during long runs

- **Every 30 minutes:** writer status, usage limits, and one handoff line if anything changed.
- **Every 2 hours:** re-read the ledger's OPEN rows and the author's recorded aims. Ask what is forgotten, and whether the writers are on the main line. Report to the author only if a decision is needed.
- **Before each compaction:** a handoff entry with the run's rules, the stop time and the exact next step.

## After a result changes the method

When a new result simplifies the method, change the method, not just the result section.
Merge the steps it makes redundant, and carry the change through examples, figures and later parts. Use `simplify-rules`, move 16.
When a part is delivered, ask what it now lets the next part drop.

## Ending

Stop when the stopping condition in `PROJECT_STATE.md` holds, even if time remains, unless the author set a minimum running time.
At the end of an unattended run, tell the author in a short message: what is finished, what is not, the decisions you made for them to overrule, and what only they can decide.
