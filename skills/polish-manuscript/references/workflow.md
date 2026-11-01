# Manuscript revision workflow

The default deliverable is a complete, readable argument within the authorized scope.
Routine corrections belong in the agent's revision cycle before author review.
The author's attention should go to the conclusion, the domain interpretation and the substantive choices.

This workflow supplements the project's rules and [the skill](../SKILL.md#terms-and-records), which defines its terms.
It does not authorize a new manuscript section, a stronger claim, or a change to a stage boundary.

## Select the target document

When a project holds several documents, identify the target before applying this workflow.
Source, macro, design, figure and build paths belong to that document's folder.
Read the shared coordination records and the target's own state.
Preserve raw prompts where they already live.
Keep each document's build output under its own folder.
Keep new revision plans and before-states with the same document across iterations.

## 1. Load the context needed for the decision

Start from the records of what was asked and what is active.
Read the project's instructions, the current entries of `PROJECT_STATE.md`, applicable writer locks, and this workflow.
Search `PROJECT_STATE.md` for the target and any unresolved issue that affects it.
Load historical entries when their provenance or acceptance history matters.
Read the target's verbatim requests in `PROMPT-LOG.md`, its open rows in `AUTHOR-LEDGER.md`, and the rules in `AUTHOR-PREFERENCES.md` that apply.

For manuscript edits, read the argument the edit depends on, not a description of it.
Read the design record's purpose, dependency route and any limits it sets on scope.
Read the full present and recommended entries of the narrative spine for the target and its dependencies.
Read the corresponding design decisions, object distinctions, and the actual manuscript definitions and proofs they reference.
Use heading and label searches to locate them.
Read the full logical neighborhood.
An index or summary never substitutes for a proof on which the edit depends.

Load conventions by topic and at the scale of the task.
Read the prose, formal-writing and definition-markup rules of [the conventions reference](conventions.md).
Then load the complete relevant topics: notation, units, object types, limits, matrices or figures.
A global notation pass requires a global occurrence search and all the affected notation and figure rules.
Before renaming a recurring term or symbol, use the terminology register and inspect the definition site in the source, because the body definition controls.

Expand the context when a dependency crosses the initial scope or a conflict appears.
A manuscript-wide reorganization or unbounded dependencies require the whole design record.
Do not repeatedly reload unchanged references already read in the same session.

## 2. Choose a useful unit of completion

For an authorized broad revision, finish the whole unit of completion: one complete argument with its directly affected examples, figures and citations.
An individual annotation is a starting point for diagnosis.
Check the same failure elsewhere in that unit of completion.
Do not require a separate author turn for each paragraph or internal implementation step.
Respect every stage boundary the author has set, and every writer lock held by another writer.

Before drafting, identify the question, the answer the subsection must establish, and the shortest dependency route between them.
For a routine repair, keep this brief and local.
For a section rewrite, put the dependency map in the working record.
Do not create another plan file for every small follow-up.

Author feedback comes in three kinds, and each is handled differently.
A settled preference, recorded in `AUTHOR-PREFERENCES.md`, should be applied consistently.
A new preference changes the local convention only as far as the author intended.
A proposed mathematical conclusion must be checked, even when the author suggests it.

## 3. Review the argument before polishing sentences

Read each logical block and ask the six block checks.

- **Point.** The reader can say what this logical block establishes and why it appears here.
  A calculation has a stated purpose and a matching conclusion.
- **Necessity.** Every definition, symbol, lemma and example has a distinct job.
  Remove or relocate an item whose deletion loses no needed argument.
- **Prerequisites.** Objects are defined before use.
  A distant citation is accompanied by the specific fact needed here.
- **Mathematical scope.** The domain, coordinate chart, independent variables, held-fixed quantities, quantifiers, and exact or leading-order status support the claim actually stated.
- **Domain meaning.** An application answers a question in its domain, whether biological, physical, economic, statistical or other.
  Its parameter choices and physical restrictions support that answer.
- **Continuity.** The next logical block follows from a question, result or dependency raised by the preceding one.

Apply the block checks to the final source, without relying on the edit diff or on the fact that earlier versions were reviewed.
For a substantial rewrite, first summarize each logical block's point and necessity in short working notes.
If that summary is merely "gives a formula" or "states a result", identify the intended inference and revise the logical block.
Keep these review notes out of the manuscript.

The block checks are a test, not a template.
A paragraph can establish a premise or transition without containing a new theorem.
Do not manufacture repetitive topic sentences or extra roadmaps to satisfy the block checks.
Sometimes the right fix is to delete or merge the logical block.

Run the scope audit on changed mathematics separately from the prose.
For a coordinate chart, check dimensions and an inverse or the stated local criterion.
For an exact attainable set, prove both containment and realization.
For a limit, check its family, scale, remainder, and uniformity when needed.
For a statistical claim, check the population, the estimator and the conditions under which the stated test or interval holds.
Use the checks relevant to the claim, rather than applying every mathematical test to every edit.

## 4. Finish notation and figures as part of the argument

Notation changes travel together with everything that uses them.
Before naming an object, search its canonical definition and the terminology register.
Prefer the existing physical or domain expression when a new alias adds no useful meaning.
For a notation change, inspect the definition, formulas, examples, captions, figure generators and downstream citations together.
State matrix row and column ordering and fixed parameters where ambiguity affects a calculation.

For each changed figure, write its intended takeaway before changing the layout.
Identify what each panel contributes and which edge, curve, limit or comparison must be visible.
Set the data and mathematical meaning before tuning labels.
Then check the standalone figure and its actual manuscript size.
Check label and edge collisions, neighboring panel titles, legends, contrast, clipping, axes, units and font size.
A contact sheet helps find suspect pages, and those pages then need inspection at reading size.
A successful render or font check does not establish visual clarity.

## 5. Automate bookkeeping and verify proportionally

Preserve a before-state before editing.
Take a fresh before-state after a machine switch or a concurrent edit.
Do not treat the entire dirty worktree as this stage's patch.
Unchanged directories need not be copied again for a local correction.

Run the read-only [preflight script](../scripts/manuscript_preflight.py) on a LaTeX target before handoff.

```text
python3 scripts/manuscript_preflight.py --target main.tex --baseline path/to/before/main.tex --section-label sec:results > review.md
```

The script path here is relative to the skill folder, so adjust it to suit where the command runs.
The `--baseline` option takes the before-state copy of the target.
Omit the section label for a global pass.
Without a baseline, the script inventories the current target.
Add the project's own macros and avoided terms with `--annotation-macro`, `--definition-macro` and `--avoid-term`.

The preflight script finds things to check and proves nothing.
It lists annotations and likely annotation typos, changed sections, literal label and reference issues, new or removed labels, terms to review, definition sites, and figure blocks affected by source changes.
It does not expand TeX, prove mathematical claims, judge paragraph purpose, detect all notation drift, or detect edits confined to external figure files.
Findings require interpretation.
Empty findings do not mean the revision is ready.

The preflight script reads LaTeX only.
For Markdown or HTML, make the same inventory by search and diff: author annotations, broken links and anchors, added or removed anchors, changed definition sites, and changed figures.

Verification follows what changed, not a fixed checklist.
Use the manuscript's existing build, mathematical tests and figure checks.
For prose changes, a relevant source audit, a final build and affected-page inspection usually suffice.
For mathematical or computational changes, add the necessary proof review and targeted adversarial checks.
Run tests for changed behavior, not for incidental wording.
Reuse a verified build of the before-state only when its source and relevant dependencies match that before-state.
Always build the edited target after the final batch of changes.
Keep builds serial.
Repeat a successful check only when a subsequent change or an unresolved concern warrants it.

## 6. Hand back a reviewed result and retain the lesson

Finish the final reader review, the notation propagation and the affected figure inspection before presenting the result.
Fix problems found by those reviews in the same authorized pass.
Report only material unresolved choices or limitations to the author.
Ask about a new research direction, incompatible interpretations or a required scope expansion.
Resolve ordinary phrasing, ordering, notation propagation and layout choices using the established preferences.

Keep the records short and current.
Keep one working record for the active outcome, with links to evidence rather than repeated reports.
Update the affected entries of the records you own, and send the owner of any other record your update for it.
Update a durable rule only when the lesson is new and reusable.
Replace a superseded rule instead of appending a competing rule.
Keep REVIEWED and ACCEPTED separate, because only the author grants ACCEPTED.

The workflow itself improves from observed failures.
For the next few substantive revisions, note any failure that recurs and whether the agent found it or the author returned it.
Use these observations to adjust the workflow.
The success measure is fewer repeated corrections and more coherent material ready for review per author turn.
Counts of edits, checks and generated pages are not quality measures.
