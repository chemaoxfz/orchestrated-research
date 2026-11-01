# Author ledger

Every thing the author asked for, one row each, with its current status and the evidence for it.
The orchestrator owns this file. It is how nothing gets forgotten.

Rules:

- The quote is short and exact. `python3 tools/records.py ledger` checks that every quote is an exact substring of `PROMPT-LOG.md`.
- The stage guide of the skill `orchestrated-research` says which rows each pass covers. A full pass goes through every row against the built document. Never sample, and never trust a status carried over from an earlier pass.
- Split a large ledger among several checkers, each writing a status for every row.
- Before accepting a proposed cut, search this file for a row the text serves.

Status starts with one word: OPEN, PARTIAL, DONE, PROCESS (a standing rule), SUPERSEDED (say by which row) or WAITING (say on what).
DONE and PARTIAL name their evidence, such as a printed page or a source line in the latest stage.

| ID | When | Author's words | What it asks | Relayed as | Status |
| --- | --- | --- | --- | --- | --- |
