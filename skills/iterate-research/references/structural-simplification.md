# Make the calculation simpler

Use this when a correct result is hard to apply, an object lacks a clear purpose, or the exposition has accumulated unnecessary steps.
The test is a shorter justified calculation from the declared data to the intended prediction.
A shorter sentence that hides the same solve does not pass.

## Identify the obstacle

Write the calculation in plain language: inputs, operation, output, and later use.
Identify the step the reader cannot yet carry out or explain.
Distinguish four cases:

- The mathematics keeps variables or operations unnecessary for the output.
- A simple rule is hidden behind its proof or checking algorithm.
- Individual entries are known, but the whole comparison, object, or experiment remains unclear.
- A genuine obstruction disappears only in a useful subclass.

For a specialization, compare this operation with the existing general method.
Name the concrete saving: a closed form instead of an iterative solve, a leading term instead of a full sum, whole constraints instead of entry-by-entry bookkeeping, or an explicit parameter condition instead of a search.
Use such operations only where the actual theory justifies them.

## Investigate a replacement

Try a falsifiable simplification before adding another abstraction.
Substitute an earlier structural formula, cancel shared terms, group cases by the requested output, or remove provably redundant constraints.
Move from one coefficient to the whole inequality when that is the object the reader needs.
When the question concerns a sequence of steps, check the whole sequence under one parameter choice.

Challenge the claim with small cases that expose its difficult assumptions.
Use independent calculations or finite enumeration when useful, then prove the scope actually claimed.
If the shortcut fails, retain a small counterexample in the project records and ask whether a relevant subclass admits the rule.
Do not present removal of a representation as removal of its feasibility condition.

Separate a standard identity from the special property that simplifies it.
Expose the step responsible for the saving, such as why orthogonality leaves only one term of a sum.
A name or citation for the standard identity does not explain the specialization.

Establish existence and uniqueness before a rule asks the reader to choose an object.

Check the weakest sufficient hypothesis on the object actually used: a property of each constituent need not hold for their union, reduction, or projection.

## Rebuild how the reader reaches the result

Put the operation a reader applies before optional implementation detail.
Introduce an auxiliary object only if it answers a distinct question or removes ambiguity.
Keep the original variables visible when a short expression in those variables is already readable.
Define recurring terms and the domain of every rule before relying on them.

For an assembly, give one complete construction after its component rules.
Keep the complete criterion separate from optional shortcuts and give the applicable condition at each shortcut's point of use.

When many cases are known but the question concerns a few outputs, classify by those outputs.
State the equivalence being used.
Retain the full distinctions where later conclusions need them.

Choose examples by their jobs:

| Reader need | Example job |
| --- | --- |
| See why a rule works | Show the operation on a small complete calculation. |
| Understand a necessary condition | Compare an accepted and rejected case differing at that condition. |
| Use the method across parameter values | Follow one nontrivial calculation under one parameter choice. |
| Understand a classification | State the classes and the conditions selecting them, then expose any finer distinctions. |

Reuse an example when it makes successive results comparable.
Add complexity only to reveal an interaction the smaller example cannot show.
A collection of isolated easy cases does not replace a complete nontrivial example when holistic behavior is the promised capability.

Draw the saving itself: the term that survives, the constraints removed, the parts affected, the arrows changed, or the signs propagated.
Keep positions, quantity names, and visual roles stable across panels.
Integrate the figure at the calculation it explains.

## Close the loop

Replace obsolete calculations in downstream examples, not just in the central theorem.
Check that the rule, proof, code, figures, and design records describe the same result.
Record what became easier, where the saving applies, and what remains necessary.
Stop at the requested usable and reviewed explanation rather than initiating an unrelated classification.
