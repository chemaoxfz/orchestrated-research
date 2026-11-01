---
name: simplify-rules
description: Find the simpler result or rule hiding in a calculation, merge the rules that apply the same test, and carry the simplification through the examples and figures. Use when asked to simplify, merge or clean up rule boxes, worked calculations or notation in a tutorial, paper or technical writeup, when a section introduces several quantities that all serve one decision, or after a rule has been simplified and the sections that use it must follow.
metadata:
  version: "0.1.0"
  source: "https://github.com/chemaoxfz/orchestrated-research"
---

# Simplify rules: find what decides, use the structure, state the rule in it

One author's bar: "this is the kind of clarity i'm looking for, when improving the writeups."
The target is fewer concepts, fewer rule boxes, and a rule a reader can apply by inspection.
The same author's words for the target: "a very strong and clear and explicit rule. and we have much less concepts introduced".
A rule box is a displayed, named rule in a writeup.

Simplifications compound, so ask again after each one succeeds.
A general inverse can become a transpose, and the transpose of a rotation can become a negated angle (move 2).
Each step applies the same question to the simpler result.

This skill adds one kind of review to the shared `polish-manuscript` workflow.
Its prose, notation and verification rules still apply.
[The worked episodes](references/worked-episodes.md) are 26 constructed illustrations drawn from standard science and mathematics.
Each has its before-state, after-state, justification, direction and a check.

## The moves

The moves come in three groups: find the simpler rule, restate the rules in it, then check and propagate.
Each move gives its test question and an example.
Episode numbers point to [the worked episodes](references/worked-episodes.md).

### Find the simpler rule

1. **Find the deciding quantity.**
   *Test.* Ask which single quantity decides the outcome the section is after.
   Remove every intermediate notation that only restates it.

   *Examples.* The Michaelis-Menten rate is `v = V_max s/(1 + s)` with `s = S/K_M`, so one ratio decides whether an enzyme is saturated (episode 1).
   Three rule boxes for low substrate, high substrate and half-maximal rate become that ratio.
   The number of successes replaces the raw sequence of a Bernoulli sample, because every likelihood comparison depends on the data through that number alone (episode 23).

   A common positive factor that leaves the decision unchanged also goes.
   `V_max` scales the rate of one enzyme and leaves its saturation unchanged.

   Check the actual ratio before canceling coefficients.
   A common positive time normalization preserves the ratio of two rates, but unequal weights do not cancel and can still decide the comparison.
   With `(V_max, K_M)` equal to `(2, 1)` and `(1, 0.1)` at `S = 1`, the rates are `1` and `0.91`, and dropping `V_max` reverses their order (episode 1).

   Keep a sign the decision needs.
   The series `I + A + A^2 + ...` needs spectral radius `rho(A) < 1`, not `rho(|A|) < 1` (episode 24).

2. **Use the structure the scope guarantees, and push it until nothing is left to compute.**
   *Test.* Ask what the special case guarantees that the general case lacks.
   Apply it, then ask the same question of the simpler result.

   *Example.* Inverting a general matrix takes elimination.
   Orthonormal columns make the inverse the transpose.
   A 2-by-2 orthogonal matrix with determinant one is a rotation `R(t)`, whose transpose is `R(-t)`.
   Undoing the rotation therefore flips the sign of one angle, and nothing is left to compute (episode 2).

   A tridiagonal system follows the same pattern.
   Each row involves only adjacent unknowns, so general elimination becomes a recurrence with linear cost (episode 10).

3. **State the identity that makes a step free.**
   *Test.* Ask whether an identity turns two calculations into one.
   State it once, in the rule it belongs to.

   *Examples.* The log sensitivity of `f` to `x` is `d log f/d log x`.
   The log sensitivity of a ratio is a difference of log sensitivities already computed, so the direction in which `f/g` moves needs no new calculation (episode 3).
   The product of the roots of a quadratic gives the second root from the first, `x_2 = c/(a x_1)`, with no second square root (episode 4).
   Substituting the defining equation `w e^w = x` of the Lambert W function into its log sensitivity gives `1/(1 + w)`, which lies between zero and one by inspection (episode 26).

4. **Use the scope to shrink the value set, then enumerate.**
   *Test.* Ask whether a hypothesis forces a quantity into a small finite set.
   A formula then becomes a short list of cases.

   *Examples.* Real coefficients with `a != 0` force the sign of the discriminant `D = b^2 - 4ac` into three values, so the quadratic formula becomes a short list of real roots (episode 5).
   A square is `0` or `1` modulo `4`, so a sum of two squares is never `3` modulo `4`, with no search (episode 6).

   Test the value set before importing a finite table into a wider scope.
   An orthogonal matrix has determinant `+1` or `-1`, but determinant one does not make a matrix orthogonal.
   The shear `[[1, 1], [0, 1]]` has determinant one, and its inverse is not its transpose (episode 2).

5. **Add a neutral object.**
   *Test.* Ask whether an exceptional case becomes ordinary once an identity-valued object is added, without adding a physical degree of freedom.
   An identity-valued object has the value that leaves an operation unchanged: one for a product, zero for a sum.

   *Examples.* The empty product is one.
   With seeds `D_0 = 1` and `D_-1 = 0`, the determinant recurrence for a tridiagonal matrix covers its first steps with no special case (episode 7).
   A sentinel head in a linked list holds no data, yet it gives every real node exactly one predecessor, so insertion at the front stops being a special case (episode 8).

6. **Order dependencies before solving.**
   *Test.* Ask whether some order makes every input of each local calculation known before it is needed.
   Then ask which comparisons the order actually uses, and drop the rest.

   *Example.* An acyclic linear system needs no simultaneous solve.
   Put each unknown after those it depends on, then substitute forward (episode 9).
   Only dependent pairs need ordering, so unknowns with no path between them need no comparison.

   Sorting lines by slope does the same for their upper envelope, because each new line is compared only with the lines at the end of a stack (episode 11).

7. **Change parameter when the chosen coordinate stops moving.**
   *Test.* Ask whether another variable still parameterizes the states uniquely where the chosen one is constant.

   *Examples.* On the curve `x^3 - x - p = 0`, the parameter `p` stops moving at the folds `x = 1/sqrt(3)` and `x = -1/sqrt(3)`.
   Stepping `p` jumps over the middle branch, while pseudo-arclength continuation follows arc length and traces all three branches (episode 13).
   During the melting of a pure substance at fixed pressure, temperature stops moving while enthalpy keeps rising, so enthalpy parameterizes the whole heating curve.

8. **Eliminate by an extremal variable.**
   *Test.* Ask what the variable of largest value or magnitude must satisfy at any solution.
   Its conditions may let you remove it, or they may contradict at once.

   *Examples.* Read each strict comparison `x - y > 0` as an arrow from `x` to `y`.
   At any solution, a variable of largest value has no arrow into it, so Kahn's topological sort can remove it first.
   The system has a solution exactly when the sort finishes, and no coupled inequalities are solved (episode 14).
   The cycle `x - y > 0`, `y - z > 0`, `z - x > 0` has no place to start, and its sum reads `0 > 0`.
   Linear inequalities lose a variable by pairing every lower bound with every upper bound, because a solution exists exactly when the largest lower bound is below the smallest upper bound (episode 12).
   The same move shows that a strictly diagonally dominant matrix is nonsingular.
   In a kernel vector, the row of the entry of largest magnitude gives a contradiction, with no elimination (episode 14).

### Restate the rules

9. **Teach the simplest case first, then extend by one conversion.**
   *Test.* Ask which case shows the result most simply, and whether one conversion reaches the rest.
   Show the result where it is simplest.
   Introduce what the extension needs only when the extension arrives.

   *Examples.* Teach the Michaelis-Menten rate without an inhibitor.
   A competitive inhibitor then needs one conversion, replacing `K_M` by `K_M (1 + I/K_I)` (episode 15).
   Teach resistors in series first.
   Parallel resistors then need one conversion, `G = 1/R`, because conductances in parallel add the way resistances in series do (episode 16).

10. **Merge rules that apply the same test.**
    *Test.* Ask whether two rule boxes filter by the same condition, or whether one rule box's special clause is an ordinary instance of another.
    If so, merge them.
    Keep the old names as case names when readers need them.

    *Examples.* Fick's law, Fourier's law and Ohm's law are one rule: flux equals a transport coefficient times the negative gradient.
    The three names stay as case names.
    Insertion at the front, insertion in the middle and appending are one operation once a sentinel head exists (episode 8).
    Adjacent comparisons generate the inequalities of a sorted list directly, which retires a separate rule for removing implied comparisons (episode 17).
    Solvability of `A x = b` needs one test, orthogonality of `b` to the kernel of the transpose, with "nonsingular" kept as a case name (episode 25).
    One predictor-corrector rule serves regular points and folds (episode 13).

    A table can supply several formulas at once.
    One table of impedances supplies the resistor, the inductor and the capacitor.
    Use its rows directly instead of repeating them in another display.
    Keep the element types distinct, since only the resistor dissipates average power (episode 18).

11. **List only the cases that produce something.**
    *Test.* Ask which listed cases produce an outcome.
    A case that gives nothing becomes one restriction sentence after the list.

    *Example.* Three cases for the real roots of a quadratic become "there are exactly two ways to obtain a real root": `D > 0` gives two roots, and `D = 0` gives one root.
    A restriction sentence follows the list: "a negative `D` gives no real root, because no real number squares to a negative number" (episode 5).
    One author's request for this form: "instead of 3 cases, it could explicitly state there are only two possibilities ... and then (iii) is not a case, but a sentence after the (i) and (ii)".

12. **Extend a rule by reinterpreting one of its objects.**
    *Test.* Before writing a new rule for a harder case, ask whether one object in the old rule can be read differently so the old rule covers it.

    *Examples.* Read a shared direction as a point at infinity.
    Two distinct lines then always meet in exactly one point, and parallel lines need no separate rule (episode 19).
    Read resistance as a complex impedance.
    The series and parallel rules then cover capacitors and inductors at a fixed frequency (episode 18).

13. **Use one name per operation across writeups.**
    *Test.* Ask whether one operation carries two names across the writeups.

    *Example.* A tutorial that says "forward sweep" and a technical companion that says "forward elimination" for the same step of a tridiagonal solve should both adopt one name (episode 20).

### Check and propagate

14. **Check the simpler rule for lost cases.**
    A lost case is a case the old rules allowed that the simpler rule no longer covers.

    *Test.* Ask which case the simpler rule no longer covers.
    Enumerate every combination of the finite values and confirm that each case the old rules allowed is still covered.
    Test the class of examples where a case is the only one.

    *Examples.* A draft "real roots exist when `D > 0`" loses the double root.
    On perfect squares `x^2 - 2cx + c^2`, `D = 0` is the only case, and the draft wrongly reports no real root (episode 5).
    A draft "reduce any resistor network by series and parallel steps" loses the bridge network, which has no series pair and no parallel pair (episode 21).
    A draft "a factor shared by two quantities cancels" needs a qualification: `xy/(xz)` cancels `x`, while `xy * xz` doubles its power.

15. **Keep the scope and restrictions visible.**
    *Test.* Ask whether a reader can see each hypothesis and restriction at the point the rule is used.
    A simpler rule still states its hypotheses and the restriction it relies on.

    *Examples.* The rule built on `S/K_M` still states quasi-steady state, with total enzyme small compared with `S + K_M` (episode 1).
    The result of move 2 still states orthonormal columns and determinant one (episode 2).

    Put each premise where it is used rather than repeating a qualification paragraph.

    Reusing one formula does not merge two tests into one.
    For `x'' + b x' + c x = 0`, the discriminant `b^2 - 4c` decides oscillation and not stability.
    The pairs `(b, c) = (1, 1)` and `(-1, 1)` have the same discriminant, and only the first is stable (episode 22).

16. **Carry the simplification through.**
    *Test.* Ask which scaffolding, sections, examples and figures still serve the old rule.
    After a rule gets simpler, remove the scaffolding the old rules needed, then shorten or merge the sections that used it.
    Rework the examples and figures so they show the new rule's steps.

    *Example.* Once the number of successes replaces a raw Bernoulli sequence, the per-observation notation leaves every later section.
    A figure of sequences becomes a figure of likelihood against that number (episode 23).
    One author's words at this stage: "the figures probably all need to be changed or upgraded."

## Procedure

- Read the rule boxes and the subsections that state the result, then the definitions they actually use.
- For each move, write the candidate simplification and check it against the current rule boxes.
  Check every mathematical claim by derivation and by a small enumeration or script.
  A script is evidence for the reviewer, never the manuscript's argument.
- Report numbered items: the simpler statement, what it replaces, what becomes redundant, and any lost case found by move 14.
- After an accepted simplification, apply move 16 to the downstream sections, examples and figures.
- Work one section, then one subsection, at a time.
  Verify each delivery before starting the next.
- The writer makes the edits and synchronizes the design record it owns, `TUTORIAL-DESIGN.md` or `TECHNICAL-DESIGN.md`.
  A reviewer does not edit the manuscript.
- The writer sends the new state to the owner of `PROJECT_STATE.md`, and any preference the author states to the owner of `AUTHOR-PREFERENCES.md`.
- A rule that appears in both writeups changes in both.
  The tutorial follows `write-tutorial`, and the technical companion follows `write-companion`.
- A simplification that opens a new research question goes back to `iterate-research`.

## Worked record

- [references/worked-episodes.md](references/worked-episodes.md): the 26 constructed episodes, with before-state, after-state, justification, direction and check.
- A project keeps its own real cases in its own records, in the same shape.
  A real case also says where its before-state is preserved, and quotes the author verbatim where it can.
- A rejected shortcut stays in those records with the counterexample that rejected it.
  It does not count as a simplification.
- When a real case shows a new move, add that move to the moves above, in the copy of this skill the project uses.
