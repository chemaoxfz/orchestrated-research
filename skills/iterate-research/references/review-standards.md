# Review the result and how the reader reaches it

Use `AUTHOR-PREFERENCES.md` and any project polishing instructions first.
Apply this checklist to the affected argument, without restarting an entire project for a local edit.

## Capability and validity

- State the question and what the reader can now explain, predict, or calculate.
- Identify data, inputs, fixed parameters, outputs, dimensions, and index meanings.
- Define objects before discussing properties.
  Recall the actual earlier formula needed by a proof.
- Distinguish exact statements, limits, approximations, and numerical observations.
- For a classification, prove completeness and realization, including the treatment of boundaries.
- For a reduction, state the preserved quantity, reconstruction, and changed assumptions.
- For empirical work, check the data, method, uncertainty, and reproducibility of the analysis.
- Verify suggestions and narrow false claims.
  A better-written conjecture is still a conjecture.
- Inspect important full-text sources and retain their provenance under the project's literature workflow.

When simplicity is a declared priority, attempt the promised calculation from its stated data.
Check whether the main rule still hides a solve, search, or undefined operation.
Technical detail can be deferred only if the reader can still complete the calculation without it.

## Teach a calculation through its purpose and result

Use this sequence when teaching a method, rather than imposing it on every research artifact.
Begin with the question in the field's own terms, the given data, what varies, and what is held fixed.
Explain why an approximation, case distinction, or representation answers that question before selecting it.
Then state the selected case and the equations it changes or retains.
A calculation should not start before the reader knows which problem it solves.

Name a displayed step by its operation and intended result.
For example, "Solve for the steady state" and "Compare the two terms to find where the approximation holds" state more than "Solve" and "Check."
Close the step with that result and its use in the next step.
Do not replace a missing motivation with a longer heading or repeated roadmap.

An introductory worked example can establish the quantities and the destination before general shortcuts.
Complete one coherent calculation there instead of splitting its definitions and results across an abstract preview and a later example.

After that example, separate the reusable rule, its scope, its interpretation, and its application.
Keep proof-only machinery with the derivation, but keep every condition needed to use the rule beside the rule.
Show the complete expression or decision the reader needs when "substitute" or "apply the method" would hide the main work.

Review interpretations through the question they answer.
For a Jacobian with one row per output and one column per input, a row answers how one output responds to each input to first order.
A column answers how each output responds to one input to first order.
State the signs, conditions, and variables in the field's own terms rather than merely naming indices.
For a reduction, execute the reconstruction of the requested output, not only the reduced calculation.

## Logical progression and prose

Give each section a question, necessary premises, and a conclusion used later.
Put machinery before its first use, motivation before formal statements, and interpretation after proofs.
Keep statements to hypotheses and conclusions.

Use one theorem to assemble the established rules into a construction, rather than several overlapping summaries.
Make its example execute those operations in the same order.

For an extension to a new domain, such as biology, physics, or economics, state and check the new modeling assumptions before importing previous conclusions.

Give each paragraph one point and state it first.
Prefer short sentences, literal words, and established nouns.
Avoid em dashes, unnecessary semicolons, invented synonyms, and pronouns with remote referents.
Keep short concrete expressions explicit.
Repeating a small concrete assignment can help more than introducing another alias.
Use remarks and examples for substantive distinct points, not every incidental sentence.
Put one complete prose sentence on each source line unless project formatting differs.

## Examples and figures

For each example, identify the data, rule applied, visible calculation, and inference.
After a simplification, replace the old method in the example as well.
Use a richer running example when the smallest example cannot expose a rule's essential case.

When a claim concerns a sequence of steps, check them together under one parameter choice.
Steps that are each attainable alone need not be attainable together.

For each figure, identify the intended inference and each panel's job.
Draw the mechanism or simplification, rather than only the final numbers.
Keep the calculated quantity and indispensable index key inside the figure.
Match labels, units, exact or limiting meaning, and parameter choices to the prose.
Inspect placement, fonts, text size, contrast, arrow shafts, axes, and collisions at reading size.
Respect meaningful special values, such as zero, and the project's palette and layout conventions.
Use boxes and other strong emphasis for central reusable results.
Prefer reproducible vector or plotting tools for technical figures.

## Verification and synchronization

Use targeted adversarial checks where an error could affect the claim.
A build or numerical sample does not replace a proof or reader review.
Compile edited typeset artifacts, inspect affected pages, and resolve relevant references and warnings.

Synchronize definitions, dependent formulas, examples, figures, the checkpoint, and the design records.
After a major result changes, inspect the whole artifact in reading order for obsolete assumptions, old algorithms, and previews that no longer describe what has already been established.
Preserve substantial superseded work and pre-existing unrelated changes.

Report what was reviewed and what remains uncertain.
Never call an artifact accepted until the author has accepted it.
