# Run limits and resumable checkpoints

Read this at the start of a run and whenever the author changes its scope or budget.

The checkpoint is `PROJECT_STATE.md`, or an existing working note that serves the same purpose.
Create one short `PROJECT_STATE.md` only when the project has no suitable record.
Do not create a separate logging system.

## Establish what ends the run

Preserve the author's specified limits and intended final state.
Respect every applicable upper limit.
Time and resource limits can interrupt a cycle.
A cycle limit controls new starts, as specified below.

Do not spend the entire budget after the requested final state has already been achieved.
Distinguish a requested final state from an intermediate milestone in an explicitly iterative run.
A reviewed first draft can be a milestone when the author has also asked for further cycles.

The author can set a limit in five forms, and each form needs its own operational rule.

### A duration or deadline

Read the actual clock.
Record the start and the deadline in UTC, and retain any timezone used to interpret the request.
Check the time between phases and before expensive operations.
Reserve realistic time for validation and handoff.

### A maximum number of cycles

Count a cycle when its selected investigation starts.
A failed or inconclusive investigation consumes a cycle.
Review and necessary repairs belong to that cycle.

A cycle limit controls whether another cycle may start.
Finish the investigation and review of the last permitted cycle unless a time or resource limit interrupts it.
Reaching the maximum number of starts does not mean abandoning that newly started cycle.

### A qualitative effort level

If the project has no convention, use quick = one cycle, standard = up to two, deep = up to four.
State this interpretation before work.
These are workflow limits, not wall-clock or token guarantees.
Preserve any model and reasoning configuration the author selected.

### A measurable resource budget

Use the runtime's actual meter when available.
Preserve its accounting across continuations.
If the resource cannot be measured, disclose that limit.
An approximate request can use a stated scope estimate.
A strict cap requires a measurable alternative before promising dependent work.
Do not invent usage figures.

### A final project state

Translate the final state into observable conditions, such as a central claim proved or refuted, an effect estimated to a stated precision, a complete specified classification, or a reviewed and compiled manuscript with no unresolved required items.
Do not quietly weaken the target to fit the result.

## When no limit is stated

If the author gives a concrete task without a budget, its completed deliverable is the stopping condition.

For open-ended exploration with no stated limit, default to one reviewed cycle and report the best candidate next outcome.
State that assumption at the start.
Ask a concise clarification only when the missing limit materially affects what can be promised.
Do not interpret "keep going" as unlimited permission to change the research objective.

## Use a goal-tracking tool only on request

Use a goal-tracking tool, if the runtime has one, only when the author has explicitly requested a goal.
Follow that tool's status and accounting rules.
Do not create a new goal for each cycle or reset an existing budget during continuation.

## Respect time during tools and review

A deadline is not a reason to start an operation that is unlikely to leave time for its necessary verification.
Prefer bounded tool calls and supported timeouts for work near the deadline.
Check the clock after long calls.
Tool latency can exceed estimates.
Report an actual overrun rather than claiming an exact stop that did not occur.

If little time remains, stop starting new investigations.
Save the current derivation and artifacts, perform the checks that fit, and identify anything still unverified.
Do not wait idly for a budget to expire or expand the question merely to fill the remaining time.

## Keep one current checkpoint

Record only what another turn needs to continue correctly.

```text
Objective, primary value, and intended artifact:
Authorized scope, what must stay untouched, and stopping condition:
Current verified result and its evidence:
Required work still open:
Run start and deadline, if timed:
Effort limit or resource budget, if specified:
Cycles started/completed and remaining budget:
Current cycle question and phase:
Current claim status: conjectured / observed / proved / refuted / needs scope
Artifact status: in progress / implemented / reviewed / accepted
Last checks and unresolved review findings:
Candidate next outcome and why it follows:
Run status and reason for continuing or stopping:
```

Keep the claim status separate from the artifact status.
A clear draft can contain an unresolved conjecture.
An inconclusive investigation can have a fully reviewed report without satisfying a requested proof target.
Only the author can supply author acceptance.

Give a conjecture, an observation, and a proved result different labels.
Use "observed" for a claim that rests on data or computation.
Reserve "proved" for a completed proof.

Update the checkpoint at a substantive result, at a phase boundary, at new direction from the author, and before yielding or stopping.
Use actual times and counts.
Do not label an interrupted cycle completed just to make the checkpoint tidy.

## Continue without resetting the task

On resumption, read the checkpoint and the latest author message together.
Preserve the original objective, unfinished required items, consumed budget, and active cycle unless the author changes them.
Feedback and new questions usually steer the current task rather than replacing it.
Record a budget change that the author authorizes explicitly in the checkpoint.

Context compaction and tool retries do not restart the clock, the cycle count, or the resource budget.
If a timed run is resumed after its deadline with no renewed budget, report the saved state and request a renewed limit only if further work is needed.
Do not silently start another timed run.
If the environment cannot continue while inactive, persist the checkpoint instead of implying unattended background execution.

## Decide whether another cycle is warranted

Continue when the required outcome is unfinished, useful work remains within scope, and the run limit allows it.
Routine corrections and review findings do not require another approval from the author.

A failed central conjecture calls for a response that fits the task.
If the central conjecture fails, use the counterexample to choose a narrower question only when that remains within the author's objective.
If the task was to investigate the conjecture, a checked refutation can answer it.
If the task specifically required a proof of a false statement, explain the obstruction.
Do not claim to have supplied the requested proof or silently substitute a different target.

A recurring obstacle is a reason to change approach.
If the same obstacle recurs without a new premise or method, stop retrying the same approach and record the specific missing evidence, access, or research choice.
Use independent work that still advances the objective before calling the run blocked.

Finish with one of these plain reasons:

- The requested final state was achieved.
- The time, effort, or resource limit was reached.
- A verified obstruction makes the requested final state unattainable under its assumptions.
- Further progress requires a specified external input, access change, or scope decision.
- The author asked to stop or change direction.

At a limit, report unfinished required work as unfinished.
Preserve the candidate next outcome and enough context to resume without repeating completed work.
