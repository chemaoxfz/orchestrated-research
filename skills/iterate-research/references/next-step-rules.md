# Choosing the next useful research outcome

Read this when selecting an investigation, after a substantive result, or when the current direction stops serving the research question.
These rules were distilled from long research projects.
They are decision aids, not mathematical assumptions or a fixed sequence of research topics.
Project-specific author instructions take precedence.

## Condition the choice on the current state

Separate three things before choosing.

1. The intended prediction or explanation.
2. What the existing argument actually establishes.
3. The remaining obstacle between them.

Requests and completion notes do not establish results.
An author request is evidence of a desired direction.
An agent completion note is evidence of a past assessment.
Neither substitutes for the proof or data on which the next claim depends.

Read project history in context.
When learning from project history, pair a request with its contemporary state and check later corrections.
Do not treat repeated copies of feedback as independent support.

## Choose by the obstacle, not by a fixed topic sequence

Match the current state to a row, then choose the smallest coherent outcome that advances the research question and fits the available budget.

| Current state or obstacle | Candidate next outcome | What would count as completion |
| --- | --- | --- |
| A concrete phenomenon is visible but unexplained. | A minimal model or example that isolates the mechanism, followed by a structural explanation. | The example answers a stated question and tests a plausible alternative. |
| Two independently useful representations appear to agree. | A precise correspondence, recovery map, or equivalence. | State the data, domain, and information retained. Prove the directions actually claimed. |
| A formula still hides the promised calculation behind an inverse, intermediate solve, or abstract operator that earlier work already simplifies. | A direct rule for the complete quantity the reader needs, found by substituting the established structure into the entries or cases of the formula. | A reader can compute the result from the declared data. Do not merely rename the intermediate object. |
| The calculation retains more variables than the intended response needs. | The smallest sufficient representation and its reconstruction rule. | Later calculations use the smaller object without losing the stated response. State what is lost as well as preserved. A reduction that preserves the response need not preserve the rest of the structure. |
| The common case, or the labels of the main pieces, are known. | The needed exceptional case, boundary case, or connections between the pieces. | The object the artifact promises is actually specified, with exceptions declared. Do not add unrelated cases solely for symmetry. |
| Local rules and validity conditions are known. | How the local pieces fit together globally, or a complete classification on a manageable model. | Separate coverage, adjacency, realizability, and any stronger structural property. |
| Individual entries are explicit but their collection is opaque. | The structure of the whole collection: which entries are redundant, and what each input affects. | The reader can list the whole system, remove exactly the justified redundancies, and find what an input affects without assembling everything. |
| A test checks one given candidate, but the reader needs them all. | A generator of candidates, with every choice and rejection test specified, and a proof that the list is complete. | An example lists every returned candidate or clearly identifies a chosen subset. |
| A general test is still required inside a tractable subclass. | Substitute the structure of the subclass and seek a complete criterion in its simpler terms. | Prove necessity and sufficiency, show an accepted and a rejected case, and state why the specialization removes the remaining test. |
| Many cases are known, but the question concerns a few. | A classification by the requested output. | State what counts as the same output. Preserve distinctions where later conclusions need them. |
| A relevant model in the target domain lies outside the tractable class. | A reduction under an assumption justified in that domain, such as a biological, physical, or economic assumption. | Identify which terms of the response, which inputs, and which outputs survive. Test the assumption before importing all the tools. Give an obstruction if the reduction fails. |
| A structural advance has made earlier exposition redundant. | A shorter argument, simpler examples, or a reorganized narrative. | Remove machinery that no longer has a distinct job. Preserve needed hypotheses and access to the proofs. |
| A complete criterion is correct but still cumbersome. | An equivalent local rule, a smaller sufficient test, or a complete rule for a relevant subclass. | Test false shortcuts, prove the surviving claim, and distinguish simplification of representation from elimination of a real condition. |
| A static description is complete but the question concerns behavior over time. | A declared dynamical model with its assumptions and a stability analysis. | A static description alone does not prove a trajectory. |
| A stronger conjecture or new convention looks elegant, or would support many later claims. | A hard-case check, counterexample, or narrower theorem. | Prove it, state the needed hypothesis, or preserve a counterexample and narrow the claim. Evaluate usefulness across the intended class before changing conventions or building further claims on it. |

These moves are alternatives, not compulsory stages.
Do not invent novelty when integration or an explanation is the actual missing work.

## Prioritize without inventing a scoring system

Explicit author priorities and unfinished required work come first.
Repair a false or unsupported premise before using it to extend the argument.
Then prefer an outcome that removes a necessary obstacle and makes several later steps easier.
Do not start from the longest list of open problems or the latest section number.

Evaluate a proposed extension against the primary value recorded at the start of the run.
If the project specializes a mature general theory, prefer a new usable capability over restating that theory on a smaller class.
When the framework is already usable, a complete small application can be more valuable than another isolated example or a large generalization.

Compare only genuinely plausible candidates, in a short paragraph or table.
For each, explain what current result enables it, what new question it resolves, and what would establish success or failure.
Use cost and uncertainty to choose a bounded first outcome.
Do not use arbitrary numerical weights to disguise that judgment.

The immediate outcome need not be the project's largest open question.
A tractable classification, a sharp obstruction, or a validated reduction can determine how to approach that question later.

If an investigation produces no distinct research payoff, archive its useful evidence and return to the simpler approach.

## Use research progress to improve exposition

A structural result has two possible payoffs: it can answer a stronger question, and it can make the existing answer easier to understand.
Check both.

Let the strongest established explanation determine the presentation.
For example, once a symmetric matrix is diagonalized, compute its powers from its eigenvalues and eigenvectors in the worked examples.
Once the sample mean is known to be sufficient for the mean of independent Gaussian samples with known variance, make the sample mean the main calculation.
Once a consequence is immediate, a remark beside the theorem may replace an entire subsection.
Once the final theory has a coherent structure, organize the manuscript around that structure rather than the original conversation.

These are examples of a preference, not requirements to use eigendecompositions or sufficient statistics in every project.

Use [structural simplification](structural-simplification.md) when finding the strongest explanation requires new reasoning.

## Record each cycle

The checkpoint tracks the run, and this record tracks one cycle.
Keep this record in the checkpoint.
Do not create a new hierarchy of logs.

```text
Question and intended prediction:
Verified premises and unresolved hypotheses:
Selected next outcome and why it follows now:
Scope, deliverable, and run limit:
Result, obstruction, or remaining gap:
Proof or evidence, and relevant validation:
Argument, notation, and figure review:
Files and design records synchronized:
Candidate next outcome, or reason this run stops:
```

The measure of success is a more usable research result with fewer recurring obstacles for the reader.
Page counts, theorem counts, check counts, and completed cycles are not substitutes for that outcome.
