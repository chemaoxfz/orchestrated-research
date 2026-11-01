# {{TITLE}}: working rules

This folder is the home of the writeup pair and of everything done for it.
The tutorial is `{{TUTORIAL}}`.
The technical companion is `{{TECHNICAL}}`.
The tutorial's reader: {{READER}}.
Put new records, code, results, figures, briefs and messages in this folder.

## Who owns what

One writer per file.
The owner makes the edit. Everyone else sends a numbered suggestion to the owner.

| Owner | Files |
| --- | --- |
| Orchestrator | `PROJECT_STATE.md`, `AUTHOR-LEDGER.md`, `GOAL-RUN.md`, `roles/orchestrator/`, `revisions/orchestrator/` |
| Tutorial writer | `{{TUTORIAL}}`, tutorial figures, `TUTORIAL-DESIGN.md`, `AUTHOR-PREFERENCES.md`, shared macros |
| Technical writer | `{{TECHNICAL}}`, `TECHNICAL-DESIGN.md`, `guidance/NOTATION.md`, `RESULTS-LEDGER.md`, `code/`, `data/`, technical figures |
| Whoever receives an author prompt | Appends it once, verbatim, to `PROMPT-LOG.md` |

A role's own memory and handoff are in `roles/<role>/`.
Who is running each role right now is in `roles/roster.json`. Read it with `python3 tools/role.py list`.
The orchestrator's handoff, `roles/orchestrator/HANDOFF.md`, holds the current plan and next step.

## Read before you act

| Task | Read |
| --- | --- |
| Any work | `PROMPT-LOG.md` entries for the task, `PROJECT_STATE.md`, your charter, memory and handoff |
| Tutorial work | `AUTHOR-PREFERENCES.md`, `TUTORIAL-DESIGN.md`, the skill `write-tutorial` |
| Companion, proofs, code, results | `AUTHOR-PREFERENCES.md`, `TECHNICAL-DESIGN.md`, `guidance/NOTATION.md`, the skill `write-companion` |
| Revising a section | The skill `polish-manuscript` and the actual definitions and proofs the section depends on |
| Too many rules or quantities | The skill `simplify-rules` |
| A bounded research question | The skill `iterate-research` |

The author's current request controls the scope.
A historical plan or a completion note is evidence, not an instruction.

## Rules every agent keeps

- Preserve each author request once, verbatim. A message that starts "From <sender>:" is not an author prompt unless it says it relays one.
- Keep a before-state of anything you substantially change. Do not delete another agent's work.
- A mathematical suggestion is a claim to prove and test, whoever made it, including the author.
- A number enters a document only through a row of `RESULTS-LEDGER.md`.
- A failed test goes to the orchestrator and the author at once. The tutorial's constructive rule controls what the text talks about. It never changes the evidence.
- Delivered, reviewed and accepted are three states. Only the author can accept.
- Never read credential files. Never widen a sandbox. Never delete a transcript without the author's permission.

## Build

Build each TeX target serially from this folder:

    latexmk -norc -r .latexmkrc -pdf {{TUTORIAL}}

The PDF stays here. Auxiliary files go to `.build/latex`. Read `.build/latex/<target>.log` to check a build.
A clean build does not establish a correct or readable argument. Inspect the rendered pages.
