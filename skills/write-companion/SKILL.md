---
name: write-companion
description: Write or review the technical companion of a research project, the document where every statement of the tutorial gets its argument. Holds derivations, proofs, algorithm details, computations, complete tables, exact scope and reproducible results. Use whenever you write, extend or audit a supplement or technical companion, record computational results, or prove claims for a paired tutorial or paper. The tutorial's rules on what to leave out do not apply here.
metadata:
  version: "0.1.0"
  source: "https://github.com/chemaoxfz/orchestrated-research"
---

# Write the technical companion

The companion shows that statements are true.
It is the collection of derivations, proofs, algorithms, computations and evidence behind the tutorial.
The review standard is the opposite of the tutorial's: every statement needs its argument here, and a missing proof is a defect.

A project's `AUTHOR-PREFERENCES.md` extends these rules and wins where it differs. The author's current request wins over both.

## What belongs here

| Keep here | Keep in the tutorial |
| --- | --- |
| Proofs and derivations | The executable formula and the hypotheses needed to use it |
| Algorithm details, solver settings, convergence behavior | The operation, in plain steps |
| Complete tables, every run, every comparison | The results that answer the reader's question |
| Exact scope, boundary cases, failures of a shortcut | The rule, stated where it is used |
| Discrepancies with published models | Only what the reader needs |
| Superseded results, marked and kept | Nothing |

When the tutorial loses a derivation, the derivation must exist here first.
An audit of a cut asks one question: is the argument still findable?

## Work out the claim before writing it

Investigate first. Only after a full understanding should a claim go into any document, whichever document asked for it.

- **Treat every suggestion as a claim,** including the author's. Test it at its stated scope. A refuted suggestion is a useful result, so report it plainly with its counterexample and the corrected statement.
- **Give each claim a status** in `TECHNICAL-DESIGN.md`: CONJECTURED, OBSERVED (computation or data support it and nothing proves it), PROVED, REFUTED with a counterexample, or NEEDS SCOPE with the corrected statement.
- **Separate premises, conjectures, observations and proved conclusions.** They must never share a label. `macro.tex` has an environment for each kind of statement.
- **A computation challenges a proof, and does not replace it.** It can refute a general claim. It cannot establish one, unless it is an exhaustive enumeration of a finite case, and then it says so.
- **For a classification, prove both realization and exclusion.** For an attainable set, prove both containment and realization.
- **For a reduction, state what is preserved, what is lost, and how to reconstruct the output.**
- **For a limit, state its family, its scale and its remainder,** and keep exact statements, leading-order statements and numerical observations distinct.
- **Check domains, dimensions, quantifiers, held-fixed quantities and boundary cases** as they apply.
- **A prior result is not lifted without a rerun.** Quarantine it until it is reproduced from its source.

When a statement turns out simpler than expected, tell the orchestrator. The tutorial's method may change. Use `simplify-rules`.

## Structure

Mirror the tutorial's parts, so a reader can move between them.
Open with an index: each tutorial claim, the statement here that establishes it, and its status.

Expose the skeleton. Spend words on structure, and keep the technical content tight. Density is not clarity.

- Announce the decomposition before executing it: "There are two conditions, A and B. Handle A first."
- Introduce an object by what it is, its definition or formula, then derive its properties. Do not define by describing.
- Forward-declare each sub-goal with its payoff: "It suffices to show X, for then Y." Then do not circle back to restate the conclusion.
- Prefer the standard named operation or concept over a bespoke metaphor.
- Name the reason before the mechanical detail: "X holds because of Y. Indeed, [detail]."
- Keep a formal statement to its hypotheses and conclusion. Motivation goes before it, and interpretation goes in a remark after the proof.
- Prove in the source. Do not ask the reader to take a step from a script, a file or a recollection.

The sentence, naming and paragraph rules of `write-tutorial` apply here too: short direct sentences, no em dashes, one point per paragraph, every noun phrase naming its defined object, and the full name of a defined term at every use.
Its rules on what to leave out do not apply.

## Algorithms

A referee must be able to reimplement each algorithm and judge its convergence from the companion alone.
A script name does not explain an algorithm. For each one, state:

- its inputs and outputs, with their types and units
- its steps, in the source, as formulas or pseudocode
- its stopping test
- every setting, with its default
- its initialization and its use of randomness
- its cost
- the evidence that it converges, and what it does when it fails
- the code path and version that implement it

## Stay in step with the tutorial

- **One object, one name, across the pair.** Both documents use the same objects, notation and dataset identities. The technical writer keeps `guidance/NOTATION.md`. When the tutorial needs a different notation for its reader, the tutorial writer proposes it through the orchestrator, and both documents follow the decision. Keep a crosswalk from old labels to new ones in the record.
- **Stable anchors.** Give each row of the claim table a named anchor at its statement, `\techanchor{key}`, and keep the key stable through later edits. `python3 tools/records.py anchors` checks that each anchor named in `TECHNICAL-DESIGN.md` exists, and that any `\techref` in the tutorial has a destination. A reader still has to check that each statement delivers what the tutorial claims, and an audit classifies each as delivering, partial, missing or wrong.
- **Answer the tutorial's question, not a nearby one.** A proof of a slightly different statement leaves the tutorial's statement unproved.
- **A scripted sweep needs a read.** After a rename across the source, run an independent read and search for mangled words.

## Computation and results

Every empirical or computational number has a row in `RESULTS-LEDGER.md`. Numbers enter a document only through a row.

| Column | Content |
| --- | --- |
| Result | A stable ID |
| Value | The number, with units |
| Data | The dataset, with its version or checksum |
| Real or synthetic | Which one |
| New, reproduced or compared | Which one, with the source for the last two |
| Held out or not | The role of the data in the test |
| Script and command | What regenerates it |
| Result file with checksum | Where it is |

Published values get rows too, marked real and compared, with page locators.
A row is not edited after it is cited. A correction adds a new row and marks the old one superseded.

- **Report across seeds or noise draws,** with medians and worst cases. Keep all attempts, and keep the record of the one that failed.
- **A claim that a method does better needs a named baseline,** on the same observations and the same score.
- **Declare training, validation and test roles before fitting.** Freeze the model, rules and data splits in a record before opening a reserved test. Open it once. Report the result as it falls.
- **Report what limited a run.** A time cap, a projected gradient or a failed convergence is part of the result. A result that hit a time cap is provisional.
- **Run one experiment at a time,** guarded by a lock. Build TeX targets serially.
- **Copy dependencies into the project,** with their provenance, rather than relying on a sibling's live files.
- **Keep acquired data somewhere permanent,** with a manifest in the repository and the bytes outside version control.
- **Test code you change.** A regression test for a fixed defect goes with the fix.

When a test fails, report it to the orchestrator and the author at once.
It is a finding about the model, the test or the text, and the author decides which.
State the failure plainly in the companion, including when the tutorial stays silent on it.

## Delivery

Before you reply:

1. Build, and read the log.
2. Inspect the affected pages.
3. Run the tests for the code you changed.
4. Reread the proofs you changed, without the diff.
5. Update `TECHNICAL-DESIGN.md` and the ledger.

Reply with the verdicts first, then what changed, the source and PDF checksums, and what remains.
