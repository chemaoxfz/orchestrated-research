# Literature

Any source that materially informs a claim gets its full text archived in `literature/` and read before it is used.
Reading the full text routinely corrects misreadings that an abstract or a recollection cannot: the actual protocol, the actual numbers, the caveat the authors themselves state.

**When.** The moment a source becomes load-bearing: it will be cited, or a number or claim will be drawn from it. Do this before writing the prose that depends on it.

**Scope.** Archive what affects reasoning, attribution, terminology, scope, a proof or a claim. Do not archive every search result.

**Search locally first.** Check `literature/` and any local catalog before going to the network, and verify a local hit against its title, authors and version.

**Fetch in this order.** An open publisher copy, arXiv or another recognized preprint server, the author's page, an institutional repository, PubMed Central or Europe PMC, then another legitimate open-access archive. Unpaywall and OpenAlex can help locate lawful copies. Use authorized institutional access where available. Do not use unauthorized sources. If only partial access is available, state that limit and do not promote a stronger interpretation.

**Verify every download.** Guessing an identifier from a title resolves to something, just not the right thing. Resolve the identifier through a real API, extract page 1, and match a distinctive phrase from the title. Delete and retry on a mismatch. Check that the file is a PDF and not an HTML error page.

**Grab the supplement too** when the methods or the numbers live there.

**Name the file** `AuthorsEtAl-YEAR-Journal-contentSlug.pdf`. Supplements add `-SI`, and preprints add `-preprint`.

**Log it** in `literature/INDEX.md`: citation, identifier, source URL, file name, retrieval date, relevance and checksum.

**What cannot be fetched** goes in `literature/NEEDED.md`, with a ranked table for the author at the very top: paper, direct link, and why in one line. Say where to drop files, and delete a row when its file lands. Until an item arrives, any claim resting on it is marked as resting on an abstract or on memory, in the record and in conversation.

The helpers `resolve.py`, `fetch.py` and `pmcget.py` in the public skill `research-essay` (`chemaoxfz/idea-to-essay`) do DOI resolution and fetching.
