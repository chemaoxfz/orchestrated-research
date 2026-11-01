# Results ledger

Every empirical or computational number used in either document has a row here.
Published values get rows too, marked real and compared, with page locators.
The technical writer owns this file.

In a TeX source, cite a row in a comment beside the claim, like `% result: R1-FIT-ERROR`.
`python3 tools/records.py results {{TUTORIAL}} {{TECHNICAL}}` checks that every citation has a row and that no row has an empty cell.
Write "none" or "n/a" where a cell really has no content.

A row is not edited after it is cited. A correction adds a new row and marks the old one superseded.

| Result | Value | Data | Real or synthetic | New, reproduced or compared | Held out or not | Script and command | Result file with checksum |
| --- | --- | --- | --- | --- | --- | --- | --- |
