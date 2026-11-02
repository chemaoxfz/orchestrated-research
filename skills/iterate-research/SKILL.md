---
name: iterate-research
description: "Develop a research idea through bounded cycles of investigation, writeup, argument and presentation review, and evidence-based next-step selection. Keeps a resumable checkpoint and reports claim status separately from artifact status. Use for sustained research in any quantitative field, or to continue an existing research project to a time limit, effort budget, or target state. A single factual answer or isolated copy edit does not need this skill."
license: MIT
metadata:
  version: "0.2.0"
  source: "https://github.com/chemaoxfz/orchestrated-research"
---

# Iterate Research

Develop one usable research outcome at a time, review it, and choose the next outcome from what it actually establishes.
A proof, observation, obstruction, reduction, complete example, or clearer synthesis can all be useful outcomes.
More machinery and more generality are not goals by themselves.

The author is the person who directs the project.
Only the author can accept an artifact.

## Project records

This skill uses generic names for the project records.
`PROJECT_STATE.md` is the checkpoint.
`TUTORIAL-DESIGN.md` and `TECHNICAL-DESIGN.md` are the design records.
`AUTHOR-PREFERENCES.md` holds the author's recurring preferences.
`PROMPT-LOG.md` holds the author's requests, verbatim.
If a project keeps one of these records under another name, use that file.
If another agent owns a record, send the owner your update rather than editing the file.

## Establish the run

A run is the bounded work that takes one objective to its stopping condition.
Read [run limits](references/run-limits.md) before investigating.

Start from the project's current records.
Read the project instructions, `AUTHOR-PREFERENCES.md`, the checkpoint, the design records, and the unfinished authorized tasks.
Use current definitions and evidence rather than treating historical plans as instructions.

Preserve what the author asked for.
Record a new request once, verbatim, in `PROMPT-LOG.md`, or in the checkpoint if the project has no `PROMPT-LOG.md`.
Keep the existing artifact format unless the author asks to change it.

Record the objective, audience, artifact, scope, verified starting result, and stopping condition in the checkpoint.

Identify and record the project's primary value: what should this work let its reader explain, predict, calculate, or do?
For a specialization of an existing theory, state what the restriction should make easier or newly possible.
Do not impose hand calculation on projects whose purpose is instead empirical coverage, automation, or another declared capability.

Stay inside the authorized boundaries.
Respect any writer lock that reserves a file for another agent, any explicit project stage, and any limit on external actions.
Resolve routine choices from the authorized scope and `AUTHOR-PREFERENCES.md`.
A time budget does not authorize unrelated work, publication, or messages to other people.

## Repeat the cycle

A cycle is one pass through these four phases.

### 1. Choose the next outcome

Ask: **What can the verified results now let us predict or calculate, and what still prevents that?**
Check that the proposed work is unfinished and serves the project's primary value.
Use [next-step rules](references/next-step-rules.md) to choose the smallest coherent outcome that removes the obstacle.
Record its deliverable and the evidence needed to call it complete.
Compare alternatives only when they could materially change the direction.
Check what the run limits still allow before starting.

When the obstacle is a cumbersome rule or an opaque calculation, use [structural simplification](references/structural-simplification.md).
Do the technical investigation before treating the problem as a prose edit.
Moving a hard step to an appendix does not make the main calculation simpler.

### 2. Investigate and write together

Separate premises, conjectures, observations, and proved conclusions.
Test technical suggestions at their stated scope, including suggestions from the author.
For a complete classification, establish both realization and exclusion: every listed case occurs, and no other case does.
For empirical work, state the data, method, uncertainty, and reproducible analysis.
Computational checks challenge a theorem.
They do not prove its general form.

Use literature when it can change reasoning, attribution, terminology, or scope.
Follow the project's literature workflow, if it has one, for full texts and catalogs.
Inspect relevant passages of important lawful sources, retain provenance, and state access limitations.
Do not use an abstract or uninspected citation as evidence for a stronger claim.

Make the promised calculation executable from the stated inputs.
Start with the research question, what varies, and what is fixed before choosing an approximation or case.
When the reader must learn to apply the method, follow the section on [teaching a calculation](references/review-standards.md#teach-a-calculation-through-its-purpose-and-result).
Keep proof machinery and optional algorithms accessible without requiring readers to learn every representation first.

Use a related skill when it applies, without overriding the requested format or scope.
The related skills are `simplify-rules`, `polish-manuscript`, `write-tutorial`, and `write-companion`.
This skill does not require any of them.

### 3. Review, repair, and propagate

Review the argument before individual sentences.
Use [review standards](references/review-standards.md) and the project's style guidance.
Repair unsupported claims and missing premises before extending them.

Carry each simplification through everything the reader relies on: prerequisites, rules, dependent results, examples, figures, and the design records.

Make the examples use the new result.
A worked example should actually use the simplest applicable result.
A complete example should show the new capability from declared data through its conclusion.

Build changed typeset artifacts and inspect affected pages at reading size.
Use targeted checks when they can reveal a substantive error.
Do not equate successful compilation with a correct or understandable argument.

### 4. Reassess

Update the current result, the remaining gap, the review status, and the remaining budget in the checkpoint.
Complete the [record of the cycle](references/next-step-rules.md#record-each-cycle).

Distill reusable feedback into `AUTHOR-PREFERENCES.md` by matching the correction to the state that prompted it.
Replace or consolidate an existing rule rather than appending overlapping instructions.
Keep project-specific research choices in the project, not in this general skill.

Ask what the reviewed result enables and what earlier work it makes unnecessary.
Continue within the objective and stopping condition without asking after routine steps.
Stop when the target is reached, even if time remains.

## Deliver the state honestly

Apply the stopping and handoff rules in [run limits](references/run-limits.md).
Deliver the artifact, the result or obstruction, relevant verification, and material unfinished work.
Report the claim status separately from the artifact status.
Keep review distinct from author acceptance and a completed cycle distinct from a completed project.
