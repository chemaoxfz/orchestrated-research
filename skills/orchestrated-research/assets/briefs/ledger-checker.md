# Brief template: ledger checker

Fill in the brackets. Split a large ledger among several checkers, with one range each.

Check rows [A1 to A100] of `AUTHOR-LEDGER.md` against the built document [PDF path] and source [path].
Go through every row in your range. Do not sample. Do not trust the status already in the row.

For each row, read the author's words and the source message in `PROMPT-LOG.md`, then find what the document does about it.
Write a new status for every row: DONE with the printed page or source line, PARTIAL with what is missing, OPEN, PROCESS for a standing rule, WAITING with what it waits on, or SUPERSEDED by a named later row.
A request the document meets in letter but not in purpose is PARTIAL.

Report a table with ID, status and evidence, then a short list of what is missing, most serious first.
Write the report to [path]. Do not edit the ledger or the document.
