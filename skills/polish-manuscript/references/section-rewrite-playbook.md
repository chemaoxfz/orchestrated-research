# Section-rewrite playbook

Read this reference for a subsection-scale or section-scale rewrite.
It records a reusable rewrite method.
Document-specific intent, rationale, warnings and open design questions live in the design record.
Use [the workflow](workflow.md) for scoped context loading, the unit of completion and the final reader review.
Keep internal implementation steps within the authorized outcome.
[The skill](../SKILL.md#terms-and-records) defines the terms used here.

## Start from the destination

Before editing prose, work through these steps.

1. State the governing question of the whole section in one sentence.
2. Give each subsection one concrete question and one culminating result.
3. Inventory every definition, reusable lemma, proposition, theorem, major interpretation, example and figure.
4. Draw the dependency order among those items.
5. Classify every logical block as prerequisite, core result, interpretation, optional organization, worked example, finite-scale refinement or archived side result.
6. Identify the shortest dependency route from the prerequisites to the section's main theorem.
7. For every named intermediate object, state the distinct question it answers and the later result that uses it.
   Remove the object when an established object and one explicit formula already answer the same question.
8. Read the corresponding present and recommended entries of the narrative spine.
   Treat the present entry as a description of the source and the recommended entry as a proposal, not as automatic authorization.

Use the resulting dependency graph, not the present source order, as the first proposed narrative order.
When the hierarchy, dependency route, culmination or forward dependency changes, update every affected entry of the narrative spine in the same turn.

## Review paragraphs as arguments

Review each edited paragraph by what it claims and how the claim is earned.
For each edited paragraph, identify its single claim, the evidence that establishes it, and its forward use.
Split when the subject or claim changes.
Give each sentence one logical step, separating choosing, substituting, solving, testing and interpreting.
Before calculations, state the subgoal and why its conclusion suffices.

After the sentence pass, run the final reader review of the whole logical neighborhood.
Check that definitions precede their uses, that every cited result supplies the stated hypothesis or formula, and that each transition follows from the preceding result.
Remove repeated roadmaps, remote pronouns and unsupported concluding slogans.
The name of a model or its effort setting is not evidence that an argument has been reviewed.

Search author annotations broadly enough to catch misspelled macros as well as the project's standard annotation macro.

Treat an author's tentative mathematical suggestion as a question to verify.
When it is false, explain the constraint and supply the simplest correct example rather than promoting the suggestion into a theorem.
Use symbolic and numerical checks to challenge the derivation, then put the analytic argument in the manuscript.

## Audit every object by type

For every central object, record five facts.

- Its ambient space or coordinate chart.
- Its type: a graph, a set, a function or a statistic.
- Its status: exact, finite-scale, or leading-order in a stated limit.
- What it depends on: the structure of the data (such as which matrix entries are nonzero), the numerical values, or only a chosen coordinate representation.
- The theorem that connects it to an object of another type.

Do not identify objects merely because they share labels.
In particular, distinguish an abstract object, a realization of it and a limit of it until a proved map relates them.

## Reorder by proof dependency

The proof's dependencies set the order, and the prose follows.

- Put a reusable mechanism before the first theorem that needs it.
- If one calculation proves several later statements, package it once as a lemma and cite it.
- If one large correspondence theorem contains a general fact, a recurring intermediate object and several case-specific consequences, extract them in that order and leave a short synthesis theorem or proposition at the end.
- Prefer a visible map-and-fiber structure when two combinatorial objects are related but not isomorphic.
  Define the map, prove existence and uniqueness pointwise, describe each fiber, and only then state what labeled data can be reconstructed.
- If two constructions share a common trunk but neither depends on the other, complete them as separate branches, state the scope of each branch before comparison, and introduce the bridge only after both exist.
  Do not narrate one branch as constructing the other merely because the bridge can reconstruct some of its data.
- Complete the central theorem before optional enumeration, alternative organization or a long worked example.
- Put motivation immediately before a formal statement, and put interpretation, limitations and examples after the proof.
- Audit every proof for distant citations that conceal the algebra needed locally.
  Restate the exact formula, hypothesis or conclusion used, and retain the citation as the pointer to its proof.
- Before an auxiliary map or operator is displayed, state the equation it is meant to solve and the consequence its solution supplies.
- For a contraction proof, verify the invariant complete set and the contraction factor separately, then identify the fixed point with the original equation before invoking any global uniqueness result.
  The textbook proof of the Picard-Lindelöf theorem follows this order: a closed ball of continuous functions, a time interval short enough for the integral operator to map that ball into itself and contract, then the fixed point identified with the solution of the differential equation.
- When a bounded correction drives a limit, state at its first introduction what it corrects, whether the bound is uniform, and its unscaled and rescaled sizes.
- Remove repeated roadmaps after the dependency order makes the dependency route visible.
- Do not retain an intermediate abstraction merely because it can be defined.
  Retain it only if it supports a distinct result needed by the narrative.
- When several coordinate-free wrappers repeat one coordinate-change identity, state that identity once and transport the established objects directly.

After moving proofs, rewrite every transition.
A mechanically valid permutation can still leave false forward references, repeated promises, or a conclusion stated before its proof.

## Write an example-first application section

An example-first section separates the teaching order from the complete proof order.
Use this form when the author requests it.
Start with a small concrete system and the domain decision it motivates.
Give the usable rule with its necessary hypotheses in the main text.
Keep its illustration beside that example.
Put the general construction and long proof in a clearly referenced technical section, with every prerequisite defined before that proof.
This does not require moving the full technical example ahead of its definitions.

Keep the model's assumptions intact and distinct.
When one assumption constrains several parameter types, derive those constraints together rather than splitting the model across parameter-specific subsections.
Preserve distinctions between assumptions that the same example satisfies together.
A jointly Gaussian pair is the textbook case: zero correlation and independence coincide there, yet they are different assumptions in general.

## Teach calculations through their purpose and result

A model's equations do not by themselves motivate a calculation.
Teach a calculation in this order.

1. State the response or decision sought, which quantities vary, and which relations and coefficients remain fixed.
2. Explain why a regime, approximation or case distinction addresses that question before selecting it.
3. Put the actual choice before solving the equations it defines.
4. Name the output the calculation must return.
5. Perform the operation and let its final line supply that output.

The small-angle simple pendulum shows the order.

- Question: how does the period depend on the length?
- Fixed data: the gravitational acceleration `g` and a small amplitude.
- Choice: replace `sin θ` by `θ`, because the amplitude is small.
- Required output: the period `T`.
- Operation: solve `θ'' + (g/L) θ = 0`, which returns `T = 2π√(L/g)`.
- Answer: the period grows as the square root of the length, so doubling the length multiplies it by `√2`.

### Motivate each step locally

A subsection roadmap does not replace a local reason.

- Name the equation or rate being approximated rather than referring to an unspecified approximation.
- Keep the motivation within the proved scope, without implying a stronger reduction or a stability result that the text does not prove.
- Use an explicit assignment, state change or rate decomposition when prose would otherwise make the reader reconstruct it.
- Explain the notation after stating the formula.
- Put model-specific applications in example environments when the document has that convention.
- Name the actual variable sets and the controlled and dynamic quantities before invoking a decomposition.
  A set of variables is not interchangeable with one state coordinate.
- Keep physical indices through the first concrete calculation and link its later use explicitly.
- Name a displayed step by its operation and returned quantity, such as solving for the equilibrium state or checking inequalities to obtain validity conditions.
  The final line supplies that quantity and explains its next use.
- A longer heading alone does not repair a missing premise.

### Keep one complete calculation together

A complete introductory calculation establishes the quantities that later rules will generalize.

- Keep that calculation together instead of splitting its meaning across an abstract preview and a later example.
- Separate the general shortcut from its proof and interpretation.
- Keep all applicability conditions beside the usable rule, and expose any substitution that still constitutes the main calculation.
- Supply the local formulas and comparisons needed to finish the calculation without consulting an optional derivation.
- Keep imported construction details and exceptional examples in the technical section that already holds them when the main calculation does not need them.
- Reuse a calculation across operations without merging their distinct questions.
- Remove definition restatements and unused proof-status assurances while preserving every premise used by a later step.
- Establish existence and uniqueness before instructing the reader to choose a path, endpoint or solution.
- Distinguish properties of individual objects from properties of their union, reduction or projection.

### Make tables and boxed rules return what later steps use

Tables and boxed rules earn their place by what later steps take from them.

- Name and label a table that later steps use.
- Refer to its returned quantities instead of repeating the table as prose or another display.
- When a table summarizes a worked calculation, show the substitutions that decide each case before the table.
- Keep the same deciding quantities visible in the table, the parameter diagram and the path through the cases.
- Use a boxed rule after motivating and defining its inputs, equations and operations.
- Keep the box to the scope, the explicit calculation and the returned quantities.
- Refer to an existing formula or table instead of reintroducing its objects inside the box.
- Place the worked example immediately after the box and execute each promised operation, including the comparison or membership test.

### Let examples finish the original question

An example is complete when it answers the question that started it.

- Let an example demonstrate the current simplest rule in its stated order.
- Use a richer running example when the smallest case cannot display an essential interaction.
- Interpret a response matrix through the question its rows or columns answer, including the changed input, the affected output, the sign and the held-fixed quantities.
- After a reduction, recover the requested output and its response.
- For a complete scenario, check every condition under the same parameters.
- When a calculation involves several distinct tests, such as existence and stability, state each test at its use.
- Finish the original domain question with the promised outputs.
- When an example promises tables, parameter diagrams or other outputs, deliver all of them with their shared conditions.
- Distinguish a change in the domain from a change of label, and a leading-order event from an exact transition such as a bifurcation.

### Revisit earlier teaching after a structural advance

A structural advance can make earlier teaching obsolete, so reread everything that teaches the same material.

- Replace obsolete assumptions and calculations in previews, boxed rules, examples, captions, synthesis statements and later applications.
- Keep one complete criterion distinct from optional shortcuts.
- Preserve passages that are already clear rather than adding new rules, roadmaps or qualifications merely to touch every paragraph.
- Do not claim in a later introduction that a classification remains missing when the document already gives it and the section supplies its proof.

## Preserve author control during broad rewrites

A broad rewrite keeps the old argument recoverable and the decision with the author.

1. Freeze a mathematically stable before-state.
2. Write the dependency map and proposed narrative order in the working record, where they can be reviewed.
3. Implement directly, unless the author asked for a comparison candidate or the rewrite is exploratory.
4. Preserve central labels when their meanings do not change.
5. Audit every downstream citation immediately when a label's meaning changes.
6. Archive substantial removed mathematics under the project's established archive folder.
7. Build the edited target.
   Reuse a verified build of the before-state when its source and relevant dependencies match that before-state.
   Build a separate baseline only when needed to establish that comparison.
8. Finish the final reader review and the affected figure reviews, repair their findings within scope, and report a short reading order with any substantive decisions that still require the author.

Replace the active manuscript with a comparison candidate only on a recorded decision by the author or, when the author is absent, the orchestrator.

If author notes prevent the before-state from compiling, preserve the exact source and record the failure.
Then use a separate build copy with only the note syntax repaired for comparison.

## Explain a limiting operation at its first use

When an exact-to-leading distinction is central, audit the first introduction rather than repeatedly repairing later examples.

- Show a concrete admissible family, identify independent and derived quantities, and derive the limiting arithmetic before the abstract limit geometry.
- Separate a chosen path limit from uniform control of the map and from convergence of whole sets.
- Keep one scalar notation rule across quantities, and check the terminology register and the macros before inventing aliases.
- When a notation stands for a limiting operation, make the family and its common scale explicit, and carry the same convention into every later rescaled sequence.
- Check whether a limit gives only an `o(t)` remainder or whether the proof requires a bounded `O(1)` offset.
  For `f(t) = t + √t`, the ratio `f(t)/t` tends to 1, yet `f(t) - t` is unbounded.
- When replacing a coordinate label by an explicit operation, revisit generic definitions and set-builder domains instead of making a blind text substitution.

## Promote a parameter family without losing its specializations

When a more general parameter family becomes the main exposition, separate universal formulas from results specific to one fixed parameter slice.

- Keep parameter variation across systems distinct from the coordinates held fixed in one derivative.
- Audit every downstream claim before moving fixed-system material to an optional section.
- State the necessary specialization in the main text, and retain its complete proof in the technical document.
- After reordering preserved examples, check float barriers for stranded paragraphs and rewrite transitions at every moved boundary.

## Prefer established quantities and justify coordinate notation

Apply the simplest-notation rule throughout the manuscript, not only in the section where a reader first identified the burden.

- Inventory repeated conversion chains, such as a logarithm of an exponential of an inverse map, and identify the established state or output they represent.
- State the conversion at its canonical definition, then reuse the established quantity in domain formulas and diagrams.
- Keep explicit chart variables where the proof or algorithm uses their linear structure, and keep exact and leading-order directions visibly distinct.
- For every shortened derivative, check its coordinates, held-fixed parameters and any required diagonal conversion factors.
- For a logarithm of a dimensional quantity, fix one reference scale and derive every reference power from it before simplifying notation.
- Record an approved rule separately from its implementation status.
  Keep the present entry of the narrative spine descriptive until the source changes, and put the planned migration in the recommended entry.
- Do not turn a notation pass into a software interface change or an unproved strengthening of a coordinate claim.
- Before retaining a local alias, state its interpretation and identify the repeated calculation it materially simplifies.
- Distinguish a useful coordinate from a renamed short ratio.
- When a reader asks which formulas matter, trace downstream dependencies, move a formula to its first substantive use, and remove duplicate derivations.

## Move a figure to physical quantities on logarithmic axes

A migration to logarithmic axes changes geometry as well as labels, so convert everything together.
[The conventions reference](conventions.md#positive-physical-axes) holds the rule, and this section holds the migration.

- For each panel, identify the positive quantity represented by each axis and label it directly.
- Use base-10 logarithmic scaling and positive decade ticks, including for drawings of limiting geometry.
- Put the leading-order interpretation and any needed bridge to direction coordinates in the caption or nearby prose.
- Convert vertices, lines, limits, slice values and annotations together with `log10 a = ln a / ln 10`, because changing only labels can misrepresent the figure.
- Verify reference units and dimensionless ratios, and check that a logarithmic transform is applied exactly once.
- Inspect equal-per-decade aspect where the geometry requires it.
- Audit color normalization, shared and inset axes, 3-D projection and data coverage after changing a scale.
- Compare rendered geometry against the archived figure and an independent physical value, not only the new tick labels.
- Preserve the scale appropriate to other quantities, such as signed sensitivities or shares.

## Place each durable lesson

When a rewrite yields a durable lesson, place it as [the skill's list](../SKILL.md#where-each-lesson-lives) directs.
Reusable rewrite method stays in this playbook, and everything specific to one document stays in that project's records.

## Final review

Before handoff, verify each of these.

- Each definition precedes its first technical use.
- Each subsection states and answers one question.
- No optional branch interrupts the shortest dependency route to the main theorem.
- Every hypothesis governing a global or structural claim holds, such as connectedness, global coordinates, orientation, uniqueness or the way pieces meet.
- Terminology and notation searches across downstream sections come back clean.
- The edited target builds, and its actual log has been inspected.
- Reference, label and layout warnings have been compared with those of the before-state.
- `PROJECT_STATE.md` holds the volatile status, and the design record holds any settled design change.
- The affected present and recommended entries of the narrative spine still describe the manuscript and the proposed next direction accurately.
