---
name: polish-manuscript
description: Audit, polish, tighten, restructure, harmonize or rewrite a quantitative manuscript and its figures to shareable rigor, with one complete argument as the unit of completion. LaTeX by default, and also Markdown or HTML. Use for section overhauls, dependency or narrative mapping, proof repair, hypothesis and scope review, notation or terminology cleanup, compactness passes, unresolved author annotations, purpose-first teaching of calculations, figure-prose synchronization, comparison rewrites and staged revisions. Do not use for a simple factual answer that requires no manuscript change.
license: MIT
metadata:
  version: "0.2.0"
  source: "https://github.com/chemaoxfz/orchestrated-research"
---

# Polish a manuscript as a complete argument

Produce a compact, self-contained argument within the author's authorized scope.
Complete the authorized revision through the final reader review and proportional verification.
Resolve routine defects before handoff, so that the author's attention goes to the conclusion, the domain interpretation and the substantive choices.

Use the active project's instructions, canonical definitions and build tools.
Do not import another manuscript's notation, section numbering, assumptions or approval stages.

Keep the project's existing format.
LaTeX is the default, and the method applies unchanged to Markdown and HTML manuscripts.
[The conventions reference](references/conventions.md#fit-the-format) gives the equivalents.

If the document being polished is a tutorial, `write-tutorial` holds the style rules that win over this skill's generic rules.
If it is a technical companion, `write-companion` does.

## Terms and records

This skill and its references use these terms with one meaning each.

- A **logical block** is a stretch of text that does one job in the argument, such as a definition with its motivation, a proof, a worked calculation or a transition.
- The **logical neighborhood** of a target is the target, the definitions, hypotheses and proofs it depends on, and the text that cites it.
- The **dependency route** is the chain of definitions and results that leads from a question to its answer.
- The **unit of completion** is one complete argument with its directly affected examples, figures and citations.
- The **block checks** are six questions asked of each logical block: point, necessity, prerequisites, mathematical scope, domain meaning and continuity.
- The **scope audit** checks that the changed mathematics supports the claim actually stated.
- The **final reader review** is a reread of the final logical neighborhood without the edit diff, by the agent or an independent reviewer, applying the block checks.
- A **before-state** is a literal copy of every file expected to change, taken before the edit and kept under `revisions/` or the project's equivalent.
- A **comparison candidate** is a separate rewritten copy for the author to compare with the active source.
- A **stage** is one part of the project's work with its own done condition.
  It waits for the author only when the author asked for that.
- A **writer lock** is an entry in `PROJECT_STATE.md` that reserves a file for one writer.
- A **quarantined claim** is a claim recorded as unproved or doubtful, so that no text may rely on it.
- The **working record** is the one existing note that tracks the active outcome: its files, claims, scoped changes and verification evidence. In a scaffolded project, it is the writer's `roles/<role>/HANDOFF.md`.
- The **design record** is the design file of the target document.
- The **narrative spine** is the ordered account of a document's logical blocks in its design record, each with its question and result, whatever heading the design record gives it.
  A present entry describes the source as it stands.
  A recommended entry, if there is one, proposes a changed order.
  It stays a proposal until a recorded decision adopts it.
  A rewrite the author asked for is such a decision. Otherwise the author decides, or the orchestrator when the author is absent.
  In a scaffolded project, the narrative spine is the part-by-part route of `TUTORIAL-DESIGN.md` or the present argument of `TECHNICAL-DESIGN.md`.
- The **terminology register** is the project's list of recurring terms and symbols, each with its one definition site, such as `guidance/NOTATION.md` and the canonical terms in `AUTHOR-PREFERENCES.md`.

The project keeps these records, under these names by default.

| Record | Holds |
|---|---|
| `PROJECT_STATE.md` | Status, writer locks, quarantined claims and build evidence |
| `TUTORIAL-DESIGN.md`, `TECHNICAL-DESIGN.md` | The narrative spine and the decisions of each document |
| `AUTHOR-PREFERENCES.md` | Each author preference as rule, reason and origin |
| `PROMPT-LOG.md` | Verbatim author requests |
| `AUTHOR-LEDGER.md` | Every author request with its status and evidence |

When a project lacks one of these records, keep that content in its nearest existing record instead of starting a parallel one.
If another agent owns a record, send the owner your update rather than editing the file.

## Load the relevant context

Read the project's instructions and [the workflow](references/workflow.md), whose first section sets the reading order.
That order runs through the records, the design record, the conventions and the actual proofs, at the scale of the task.
For a subsection-scale or section-scale rewrite, also read [the section-rewrite playbook](references/section-rewrite-playbook.md).

Read first-hand what the edit depends on.
An analogue is a comparison, not proof that two constructions have the same properties.
A finding aid or an old completion record does not replace the current argument.

## Establish the authorized outcome

State the question, intended conclusion, files and scope before substantial editing.
For a broad rewrite, map the shortest dependency route and each subsection's culmination using the playbook.

Work inside the author's boundaries without asking for each step.
Plan internal steps without requiring an author turn for each one.
Respect every stage boundary the author has set, and every writer lock held by another writer.
Ask only when a substantive unresolved choice or a necessary scope expansion requires the author.

Protect the existing work before editing.
A writer edits its own document directly, with a before-state, inside the brief it received. Use a comparison candidate only when the author asks for one, or for an exploratory rewrite that may not be kept.
Save a before-state and preserve all pre-existing work.
Archive substantial cuts in the project's established archive categories.
Do not treat the whole dirty worktree as this stage's patch.

## Review the argument before polishing sentences

Apply [the block checks](references/workflow.md#3-review-the-argument-before-polishing-sentences) to the argument first, because a well-written sentence cannot repair a logical block with no job.
For each new object, identify its distinct question and later use.
Prefer an established object and an explicit formula when they suffice.
Put reusable machinery before use and optional material after the culmination unless it is a prerequisite.
Classify material as prerequisite, main result, interpretation, example, refinement or optional branch.
Give each subsection one question and one culminating result.
Keep formal statements to hypotheses and conclusions, with motivation before and interpretation after.

## Teach through purpose and definitions

The reader learns why before how.
State what the reader needs to determine and why the next concept helps before introducing it.
Define the object before discussing its properties or using it.
For a tutorial or worked calculation, teach in this order: the question and fixed data, the explicit choice, the required output, then the operation that produces it.
Name each sub-goal and why it suffices before performing the step.
Use [the playbook's checks](references/section-rewrite-playbook.md#teach-calculations-through-their-purpose-and-result) for local motivation, individual inference steps, reuse of tables and complete example results throughout the affected sections.

When a section introduces several quantities that serve one decision, or several boxed rules that apply the same test, use `simplify-rules`.
It finds the deciding quantity, uses the stated scope to reduce it to a few cases, and merges the rules that apply the same test.

Apply [the prose rules](references/conventions.md#prose-and-source-formatting) at the level of the paragraph, where the usual failure is two points rather than excessive length.
Check paragraph logic, section transitions and the whole argument after those edits, because a clearer sentence can still leave a missing premise.

## Audit the scope of changed mathematics

The scope audit asks whether the mathematics supports the claim as stated, whatever the prose says.
Check domains, dimensions, quantifiers, held-fixed quantities, boundary cases, and exact versus limiting status as applicable.
Keep an abstract object, any realization of it and any limit of it distinct.
Distinguish dependence on structure (such as which matrix entries are nonzero), on numerical values, and on a chosen coordinate basis.
Distinguish normalized quantities from physical quantities.
Treat an author's proposed mathematical conclusion as a claim to check.
Narrow an unsupported claim or record it as open.
A numerical or computational check can challenge a proof, but it does not replace one.

## Propagate every change

A change is finished only when everything that depends on it agrees.
Carry each in-scope change through definitions, formulas, examples, tables, citations, captions, figure generators, figure annotations, controls and downstream references.
Search downstream references whenever a label's meaning changes, even if compilation succeeds.
Record necessary out-of-scope dependents in the design record or `PROJECT_STATE.md` rather than silently expanding the task.
Index a recurring term only at its canonical definition.

## Review and verify the completed unit

Run the final reader review before any handoff.
Review section transitions and the whole dependency route after local sentence edits.
Remove stale forward references and objects whose purpose arrives after use.

Verify in proportion to what changed, as [the workflow](references/workflow.md#5-automate-bookkeeping-and-verify-proportionally) describes.
For LaTeX, use [the preflight script](scripts/manuscript_preflight.py) as an advisory inventory, not as a certificate of prose or mathematics.
It reads LaTeX only, so make the same inventory by search for other formats.
Review affected figures at manuscript size.
Build the edited target serially and inspect its authoritative log.
For HTML, check rendered mathematics, navigation, controls, themes and narrow screens.
Repeat a check only after a change or an unresolved concern warrants it.
Repair review findings within the authorized outcome before handoff.

## Hand off the reviewed result

Leave the records describing the final source.
Use the working record for files, claims, scoped changes and verification evidence.
Synchronize the affected entries of the narrative spine and the settled decisions in the design record in the same turn as material manuscript edits.
Keep build status, writer locks and quarantined claims in `PROJECT_STATE.md`.
Report the rows of `AUTHOR-LEDGER.md` that this pass settled, with their evidence, to the owner of that record.
Keep process notes out of the manuscript.

Give a short reading order and report material remaining choices or limitations.

Mark the work REVIEWED when the reviews pass, or REVISE when a defect remains.
Do not mark it ACCEPTED for the author, because only the author grants ACCEPTED.

Stop at the end of the authorized outcome.
Do not enter a stage that the author reserved for separate authorization.
When the next step needs new investigation rather than revision, say so, because sustained research development belongs to `iterate-research`.

## Where each lesson lives

Maintain each lesson in one place.

- Reusable workflow steps and final reader review checks: [the workflow](references/workflow.md).
- Reusable dependency and proof organization: [the section-rewrite playbook](references/section-rewrite-playbook.md).
- Reusable simplifications of rules, calculations or notation, each with a worked example: `simplify-rules`.
- General prose, notation, terminology, unit and figure defaults: [the conventions reference](references/conventions.md).
- The project's canonical notation and terminology: the terminology register and the single definition site in the source.
- The author's preferences: `AUTHOR-PREFERENCES.md`, with rule, reason and origin.
- Document-specific rationale and architecture: the design record.
- Active files, writer locks, stage status and build evidence: `PROJECT_STATE.md`.
- Detailed derivations, counterexamples and discarded alternatives: dated provenance notes or verification scripts.

A lesson enters this skill's references only when it holds for any manuscript.
Project notation and project science stay in the project's records.
Replace a superseded rule instead of stacking contradictory instructions.
