# Worked episodes: constructed illustrations of the moves

These episodes are constructed illustrations of the moves in [SKILL.md](../SKILL.md).
They do not report the history of any project.
Each before-state is written for the illustration, and each direction line (who proposed the change) assigns generic roles for the illustration.

The mathematics is standard textbook material, and the examples were checked for version 0.1.0 of this file.
Each check line reports a derivation or a short throwaway script, and the scripts are not shipped.
The one exception is episode 20, whose check is a search that only a real project can run.
The algebra carries the general justification, and a finite computation only tests examples and potential exceptions.

A project should add its own real cases in its own records, not in this file.

[SKILL.md](../SKILL.md) defines the two terms that recur below: lost case in move 14, and log sensitivity in move 3.

## Episodes by move

| Move | Episodes |
|---|---|
| 1. Find the deciding quantity | 1, 3, 23, 24, 26 |
| 2. Use the structure the scope guarantees, and push it until nothing is left to compute | 2, 10 |
| 3. State the identity that makes a step free | 3, 4, 16, 26 |
| 4. Use the scope to shrink the value set, then enumerate | 2, 5, 6 |
| 5. Add a neutral object | 7, 8 |
| 6. Order dependencies before solving | 9, 10, 11, 17 |
| 7. Change parameter when the chosen coordinate stops moving | 13 |
| 8. Eliminate by an extremal variable | 12, 14 |
| 9. Teach the simplest case first, then extend by one conversion | 15, 16 |
| 10. Merge rules that apply the same test | 8, 13, 17, 18, 25 |
| 11. List only the cases that produce something | 5 |
| 12. Extend a rule by reinterpreting one of its objects | 18, 19 |
| 13. Use one name per operation across writeups | 20 |
| 14. Check the simpler rule for lost cases | 5, 10, 14, 21, 23, 24 |
| 15. Keep the scope and restrictions visible | 1, 2, 5, 6, 10, 14, 15, 18, 19, 21, 22, 24, 25 |
| 16. Carry the simplification through | 23 |

## Episodes

**1. Title: One ratio decides enzyme saturation.**

- **Before:** A section on enzyme kinetics has three rule boxes.
  At low substrate the rate is near `(V_max/K_M) S`, at high substrate it is near `V_max`, and at `S = K_M` it is half-maximal.
- **After:** Put `s = S/K_M`.
  Then `v/V_max = s/(1 + s)`, and the log sensitivity of `v` to `S` is `1/(1 + s)`.
  Far below one the rate is first order, far above one it is saturated, and at one it is half-maximal.
- **Why allowed:** Divide the numerator and denominator of `v = V_max S/(K_M + S)` by `K_M`.
  `V_max` is a common positive factor of one enzyme's rate, so it leaves the fractional saturation unchanged.
  It does not cancel between two enzymes with different values of `V_max`.
- **Scope:** Quasi-steady state, with total enzyme small compared with `S + K_M`.
- **Direction:** A reader says the three rule boxes seem to say one thing.
  The writer proposes the ratio, and the reviewer tests the cancellation.
- **Move:** 1, also 15.
- **Check:** Symbolic differentiation confirms both formulas and their limits.
  With `(V_max, K_M)` equal to `(2, 1)` and `(1, 0.1)` at `S = 1`, the rates are `1` and `0.91`.
  Dropping `V_max` gives `0.5` and `0.91`, which reverses the order.
  Integrating the mass-action equations with all three rate constants equal to one tests the scope.
  Total enzyme `0.01` with initial substrate `10` matches the rate law to `0.002%`.
  Total enzyme `10` with initial substrate `1` misses it by a factor of `4.2` when free substrate has halved.

**2. Title: Invert a rotation by negating its angle.**

- **Before:** Several examples invert a 2-by-2 matrix that turns the plane, each by general elimination.
- **After:** The matrix is the rotation `R(t) = [[cos t, -sin t], [sin t, cos t]]`, and its inverse is `R(-t)`.
  Undoing the rotation flips the sign of one angle.
- **Why allowed:** Orthonormal columns give `Q^T Q = I`, so the inverse is the transpose.
  A 2-by-2 orthogonal matrix has determinant `+1` or `-1`, and the case `+1` is a rotation.
  Transposing `R(t)` gives `R(-t)`, because cosine is even and sine is odd.
- **Scope:** Both hypotheses are needed.
  The reflection `[[1, 0], [0, -1]]` is orthogonal with determinant `-1`, has no angle to negate, and is its own inverse.
  The shear `[[1, 1], [0, 1]]` has determinant one, and its inverse `[[1, -1], [0, 1]]` is not its transpose.
- **Direction:** The writer notices that the transpose has the same form as the matrix.
  A reader asks at each stage whether the result can be simpler still.
- **Move:** 2, also 4 and 15.
- **Check:** On 10,000 random angles, `R(-t)` matches the numerical inverse and the transpose, and `R(t) R(-t)` matches the identity, with a worst entry error of `3e-16`.
  On 10,000 random orthogonal matrices with determinant one, the rotation form matches to `8e-16`.
  Direct calculation confirms the reflection and the shear.

**3. Title: Read a ratio's direction from two log sensitivities already computed.**

- **Before:** A section computes the log sensitivity of `f` to `x` and of `g` to `x`, then derives separately the direction in which `f/g` moves.
- **After:** `d log(f/g)/d log x = d log f/d log x - d log g/d log x`.
  The sign of this difference is the direction.
- **Why allowed:** The logarithm of a ratio is a difference of logarithms.
- **Scope:** A log sensitivity gives the direction of a ratio, not its current value.
  The ratio `r = c x^gamma` has log sensitivity `gamma` for every `c`, and locating `r = 1` still needs `c`, at `x = c^(-1/gamma)`.
- **Direction:** A reader asks whether the two calculations are the same calculation.
- **Move:** 3, also 1.
- **Check:** For two Michaelis-Menten rates, symbolic differentiation of `log(v_1/v_2)` gives `K_1/(K_1 + S) - K_2/(K_2 + S)`, which is the difference of the two log sensitivities.

**4. Title: Get the second root of a quadratic from the product of the roots.**

- **Before:** Both roots of `a x^2 + b x + c` come from the quadratic formula.
- **After:** Compute the root of larger magnitude, `x_1 = -(b + sign(b) sqrt(D))/(2a)` with `sign(0) = 1`, then set `x_2 = c/(a x_1)`.
- **Why allowed:** The product of the roots is `c/a`.
  The step needs no second use of the square root, and it avoids subtracting nearly equal numbers.
- **Scope:** Real roots, `a != 0`, and `x_1 != 0`, which fails only when `b = c = 0`.
- **Direction:** The reviewer sees lost digits in a numerical example.
  The writer proposes the identity.
- **Move:** 3.
- **Check:** For `x^2 - 1e8 x + 1` in double precision, the formula gives a small root of `7.45e-9`, an error of 25%.
  The identity gives `1e-8`, which matches the exact value at double precision.
  On 12,595 random quadratics with real roots, the relative residual of the second root stays below `4e-16`.

**5. Title: Turn the quadratic formula into a list of the cases that give a real root.**

- **Before:** The text carries the formula with its square root, and three cases of equal rank for the sign of `D = b^2 - 4ac`.
- **After:** For real `a != 0`, `b` and `c`, there are exactly two ways to obtain a real root.
  `D > 0` gives two roots, and `D = 0` gives the one root `-b/(2a)`.
  One restriction sentence follows the list: "a negative `D` gives no real root, because no real number squares to a negative number".
- **Why allowed:** The shift `y = x + b/(2a)` turns the equation into `y^2 = D/(4 a^2)`.
  The right side has the sign of `D`, so three values decide everything.
- **Lost case:** A draft that says "real roots exist when `D > 0`" loses the double root.
  On perfect squares such as `x^2 - 2x + 1`, `D = 0` is the only case, and the draft reports no real root although `x = 1` is one.
  The hypothesis `a != 0` also stays visible, since `2x + 1 = 0` has a real root and no discriminant case.
- **Direction:** A reader asks for two possibilities in place of three cases.
  The writer tests the first draft and finds the double root.
- **Move:** 4, 11 and 14, also 15.
- **Check:** The list is checked over all 1,210 integer triples with `b` and `c` from `-5` to `5` and nonzero `a` from `-5` to `5`.
  It matches an independent count of distinct real roots by Sturm sequences on every triple.
  The draft fails on exactly the 26 triples with `D = 0`.

**6. Title: Rule out a sum of two squares by working modulo 4.**

- **Before:** To show that an integer of the form `4k + 3` is not a sum of two squares, the argument searches over the squares below it.
- **After:** A square is `0` or `1` modulo `4`, so a sum of two squares is `0`, `1` or `2` modulo `4`, and never `3`.
- **Why allowed:** An even number squares to `4 m^2`, and an odd number squares to `4 m (m + 1) + 1`.
- **Scope:** The test rules out one residue class and certifies nothing else.
  The number `21` is `1` modulo `4`, and it is not a sum of two squares.
- **Direction:** The writer proposes the residues.
  The reviewer builds the counterexample that fixes its scope.
- **Move:** 4, also 15.
- **Check:** All 25,000 numbers of the form `4k + 3` up to `100,000` are absent from a direct enumeration of sums of two squares.
  The enumeration also finds `21` absent, and `25` and `29` present.

**7. Title: Seed a recurrence with the empty product.**

- **Before:** The determinant of a tridiagonal matrix is stated three times: `D_1 = a_1`, then `D_2 = a_1 a_2 - b_1 c_1`, then a recurrence for `k >= 3`.
- **After:** One recurrence covers all `k >= 1`: `D_k = a_k D_(k-1) - b_(k-1) c_(k-1) D_(k-2)`, with seeds `D_0 = 1` and `D_-1 = 0`.
- **Why allowed:** Expanding along the last row gives the recurrence.
  The determinant of the empty matrix is the empty product, which is one.
  The seed `D_-1 = 0` removes the term that would use the missing product `b_0 c_0`.
  The seeds add no unknown and no equation.
- **Direction:** The reviewer asks whether the first two statements are instances of the third.
- **Move:** 5.
- **Check:** On 2,000 random integer tridiagonal matrices up to size 12, the recurrence matches the exact determinant, with an arbitrary value given to `b_0 c_0`.

**8. Title: Merge list insertions with a sentinel head.**

- **Before:** A singly linked list has separate rules for insertion at the front, in the middle and at the end, and a separate rule for deleting the first node.
- **After:** Add a sentinel head that holds no data.
  Every real node then has exactly one predecessor.
  Insertion has one rule, "link the new node after its predecessor", and deletion has one rule, "unlink the successor of the predecessor".
  "Push front" and "append" stay as case names when readers need them.
- **Why allowed:** The sentinel head stores no element, so the contents of the list do not change.
- **Scope:** Code that reports the length or walks the list starts after the sentinel head.
- **Direction:** A reader notes that the front case differs only because the first node lacks a predecessor.
- **Move:** 5 and 10.
- **Check:** A run of 20,000 random insertions and deletions, using only the two rules, matches a reference array at every sampled step and at the end.

**9. Title: Order an acyclic system before solving it.**

- **Before:** The equations `x_1 = b_1`, `x_2 = b_2 - 2 x_1`, `x_3 = b_3 - x_1` and `x_4 = b_4 - x_2 - x_3` go to a general solver.
- **After:** Put each unknown after those it depends on, then substitute forward.
  `x_2` and `x_3` need no comparison, because neither depends on the other.
- **Why allowed:** An acyclic dependency graph has a topological order, and in that order the matrix is triangular.
- **Scope:** A dependency cycle removes the order.
  The pair `x_1 = b_1 - x_2/2` and `x_2 = b_2 - x_1/2` needs a simultaneous solve.
- **Direction:** A reader asks why the unknowns are not solved one at a time.
- **Move:** 6.
- **Check:** With `b = (3, 1, 4, 1)`, both orders of `x_2` and `x_3` give `(3, -5, 1, 5)`, which matches a general solver.
  On 2,000 random scrambled acyclic systems up to size 30, the worst residual is `9e-13`.

**10. Title: Solve a tridiagonal system by a recurrence.**

- **Before:** The system goes to general elimination with a pivot search, at a cost that grows as `n^3`.
- **After:** For `l_k x_(k-1) + d_k x_k + u_k x_(k+1) = b_k`, start from `w_1 = d_1` and `y_1 = b_1`.
  Sweep forward with `w_k = d_k - l_k u_(k-1)/w_(k-1)` and `y_k = b_k - l_k y_(k-1)/w_(k-1)`.
  Then substitute back with `x_k = (y_k - u_k x_(k+1))/w_k`, where the last row has `u_n = 0`.
  The cost grows as `n`.
- **Why allowed:** Each row involves only adjacent unknowns, so each elimination step touches one row below.
  In a strictly diagonally dominant matrix, induction gives `|w_k| > |u_k|`, so no pivot vanishes and no search is needed.
- **Lost case:** The matrix `[[0, 1], [1, 0]]` is tridiagonal and invertible, yet the sweep divides by zero at its first step.
  A rule that states no restriction loses this case, so the restriction stays visible.
- **Direction:** The writer proposes the recurrence.
  The reviewer tests a zero first pivot.
- **Move:** 2 and 6, also 14 and 15.
- **Check:** On 1,000 random strictly diagonally dominant systems up to size 200, the worst difference from a general solver is `5e-14`, and `|w_k| - |u_k|` stays positive.
  On `[[0, 1], [1, 0]]` with `b = (1, 2)`, the sweep raises a division error while a general solver returns `x = (2, 1)`.

**11. Title: Find the upper envelope of lines by sorting their slopes.**

- **Before:** To find which line `y = m_i x + c_i` is largest at each `x`, the rule writes every pairwise comparison and intersects them.
- **After:** Among lines of equal slope, keep the one with the largest intercept.
  Sort the rest by slope and keep a stack.
  Before pushing a new line, pop the top while the new line overtakes the line below the top no later than the top does.
  The stack then lists the envelope in order of `x`, and the sort is the only cost above linear.
- **Why allowed:** The maximum of lines is convex, so its slope only rises along `x`.
  Each line therefore leads on at most one interval, and the lines lead in slope order.
  A new line of largest slope can only remove lines from the end of the stack.
- **Scope:** The rule needs straight lines.
  The curve `x^2` exceeds the line `1` at `x = -2` and `x = 2`, and not at `x = 0`, so a curve can lead twice.
- **Direction:** A reader asks why every pair is compared when only neighbors matter.
- **Move:** 6.
- **Check:** On 5,000 random sets of up to nine integer lines, in exact rational arithmetic, the stack matches a brute-force evaluation between all crossings.

**12. Title: Remove a variable from linear inequalities by pairing bounds.**

- **Before:** The conditions `p < x`, `1 < x`, `x < 3` and `x < 2p` are classified by a catalog of regions in the `(x, p)` plane.
- **After:** Remove `x` by pairing every lower bound with every upper bound (Fourier-Motzkin elimination).
  The pairs are `p < 3`, `p < 2p`, `1 < 3` and `1 < 2p`.
  The pair `p < 2p` says `p > 0`, which `1 < 2p` implies, so a solution exists exactly when `1/2 < p < 3`.
- **Why allowed:** A solution `x` exists exactly when the largest lower bound is below the smallest upper bound, which is the same as every pair.
  The relation from one pair is strict if either bound is strict, and weak only when both are weak.
- **Direction:** The writer proposes the pairing.
  The reviewer checks the mixed strict and weak pairs.
- **Move:** 8.
- **Check:** On 2,001 rational values of `p`, direct comparison, the pairing and the stated interval agree.
  All 196 mixtures of strict and weak bounds with integer endpoints obey the rule for strict and weak pairs.

**13. Title: Continue past a fold by arc length.**

- **Before:** The solutions of `x^3 - x - p = 0` are traced by stepping `p` and solving for `x`, with a separate rule near each fold.
- **After:** Parameterize the curve by arc length in `(x, p)`, using pseudo-arclength continuation.
  One predictor-corrector rule serves regular points and folds alike.
- **Why allowed:** At a fold, `x = 1/sqrt(3)` or `x = -1/sqrt(3)`, the parameter `p` is stationary and the fixed-`p` derivative `3 x^2 - 1` vanishes.
  Arc length still moves.
  With rows `(3 x^2 - 1, -1)` and the unit tangent, the bordered matrix has determinant of magnitude `sqrt(1 + (3 x^2 - 1)^2)` on the curve, which is at least one.
- **Scope:** Here `x` itself also works, since `p = x^3 - x`.
  Arc length is the general choice, for a curve that folds in both coordinates.
- **Direction:** A reader asks what still moves when `p` stops.
- **Move:** 7, also 10.
- **Check:** Stepping `p` up from `-6` to `6` jumps from `x = -0.58` to `x = 1.16` at `p = 0.385`, and it visits no point of the middle branch.
  Pseudo-arclength continuation runs from `x = -2` to `x = 2` in 1,483 steps and visits 142 points of the middle branch.
  It keeps the residual below `2e-15` and the bordered determinant above one.

**14. Title: Decide a system of strict comparisons by a topological sort.**

- **Before:** A system of strict comparisons such as `x - y > 0` and `y - z > 0` goes to a general solver or a case analysis of coupled inequalities.
- **After:** Read each comparison `x - y > 0` as an arrow from `x` to `y`, and run Kahn's topological sort.
  The system has a solution exactly when the sort finishes.
  Any topological order then gives a solution, with values decreasing along the order.
- **Why allowed:** At any solution, a variable of largest value has no arrow into it, so the sort cannot stop while a solution exists.
  Conversely, every arrow runs forward in a topological order, so decreasing values make every comparison true.
- **The same move on a matrix:** Suppose `A x = 0` with `x != 0`, and take `i` with `|x_i|` largest.
  Row `i` gives `|A_ii| |x_i| <= (sum over j != i of |A_ij|) |x_i|`, which strict diagonal dominance contradicts.
  So `A` is nonsingular, with no elimination.
  This is the Levy-Desplanques theorem.
- **Scope:** The sort needs comparisons of the form `x - y`.
  The inequalities `2x - y > 0` and `-x + 2y > 0` hold at `(1, 1)`, yet their arrows would form a cycle.
  The matrix rule needs strict dominance, since `[[1, 1], [1, 1]]` is singular.
- **Direction:** A reader asks whether a general solver is needed at all.
  The writer proposes the sort, and the reviewer finds the two scope failures.
- **Move:** 8, also 14 and 15.
- **Check:** The system `x - y > 0`, `y - z > 0` sorts as `x`, `y`, `z`.
  The system `x - y > 0`, `y - z > 0`, `z - x > 0` stops at once, and its sum reads `0 > 0`.
  All 4,165 systems on up to four variables, and 900 random systems on five to seven variables, agree with a search over all orderings of the variables.
  In every feasible case, the values built from the sort's order satisfy every inequality.
  All 2,000 random strictly dominant integer matrices up to size 6 have a nonzero exact determinant.

**15. Title: Extend the Michaelis-Menten rate to a competitive inhibitor by one conversion.**

- **Before:** A new section repeats the derivation, with a new rate law and a new rule box for the inhibited enzyme.
- **After:** Teach the rate without an inhibitor.
  A competitive inhibitor then needs one conversion, replacing `K_M` by `K_M (1 + I/K_I)`.
  The deciding quantity is still one ratio, and every later formula stands.
- **Why allowed:** Under the quasi-steady state of episode 1, total enzyme is `E + ES + EI`, with `ES = E S/K_M` and `EI = E I/K_I`.
  Solving for `ES` gives `v = V_max S/(K_M (1 + I/K_I) + S)`.
- **Scope:** The conversion is specific to a competitive inhibitor.
  A pure noncompetitive inhibitor instead divides `V_max` by `1 + I/K_I` and leaves `K_M` unchanged.
- **Direction:** A reader asks for the simple case first.
- **Move:** 9, also 15.
- **Check:** Symbolic solution of both enzyme balances confirms both rate laws, and confirms that they differ.

**16. Title: Extend series resistors to parallel resistors by one conversion.**

- **Before:** The series rule `R = R_1 + R_2`, the parallel rule `R = R_1 R_2/(R_1 + R_2)` and a formula for `n` parallel resistors appear as separate rules.
- **After:** Teach the series rule: resistances in series add.
  Then convert with `G = 1/R`: conductances in parallel add.
  The formula for `n` parallel resistors is the same statement.
- **Why allowed:** Series resistors share a current and their voltages add, with `V = R I`.
  Parallel resistors share a voltage and their currents add, with `I = G V`.
- **Direction:** A reader asks why the parallel formula looks unrelated to the series rule.
  The writer proposes the conversion.
- **Move:** 9, also 3.
- **Check:** On 2,000 random groups of two to eight resistors, node equations match both rules to `2e-12`.

**17. Title: Generate comparisons from adjacent pairs.**

- **Before:** One rule writes all `n(n - 1)/2` comparisons among `n` sorted values, and a second rule removes those implied by transitivity.
- **After:** Write the `n - 1` adjacent comparisons directly, and retire the second rule.
- **Why allowed:** A comparison of values that are not adjacent follows by transitivity along the chain between them.
- **Scope:** In a partial order, the edges of the Hasse diagram take this role, meaning the pairs with nothing between them.
  Incomparable elements stay uncompared.
- **Direction:** A reader asks why comparisons are generated and then removed.
- **Move:** 10, also 6.
- **Check:** All 50,069 integer tuples of length up to six get the same verdict from both rules.
  On 1,000 random partial orders, the cover relations regenerate the whole order by transitive closure.

**18. Title: Read resistance as impedance, and use one table.**

- **Before:** Series and parallel rules for resistors are followed by separate derivations for capacitors and inductors in sinusoidal circuits.
- **After:** At a fixed frequency `w`, read resistance as complex impedance from one table: `Z_R = R`, `Z_L = i w L` and `Z_C = 1/(i w C)`.
  The series and parallel rules then apply unchanged, using the rows of the table directly.
- **Why allowed:** In sinusoidal steady state, each linear element obeys `V = Z I` for complex amplitudes, and Kirchhoff's laws hold for those amplitudes.
- **Scope:** The rule covers one frequency in steady state, so transients stay outside it.
  The element types stay distinct, since only the resistor dissipates average power.
- **Direction:** A reader asks whether one sentence can extend the old rules to the new elements.
- **Move:** 10 and 12, also 15.
- **Check:** For a series circuit with `R = 2`, `L = 0.5`, `C = 0.1` and `w = 3`, integrating the differential equation past its transient matches the impedance prediction to `3e-12`.
  A driven parallel circuit of a resistor and a capacitor matches to `3e-11`.
  Period averages of power are `0.136` in the resistor, and zero to rounding in the inductor and the capacitor.

**19. Title: Read a shared direction as a point at infinity.**

- **Before:** Two lines get two rules: solve a system when they are not parallel, and report no intersection when they are.
- **After:** Write each line `a x + b y + c = 0` as the triple `(a, b, c)`.
  Two distinct lines meet in the one point given by the cross product of their triples, in every case.
  A result `(u, v, 0)` is the point at infinity in the direction `(u, v)`.
  A result `(u, v, w)` with nonzero `w` is the ordinary point `(u/w, v/w)`.
- **Why allowed:** The cross product is orthogonal to both triples, so the result lies on both lines.
  Reading a direction as a point supplies the missing meeting point of parallel lines.
- **Scope:** The lines must be distinct, since coincident lines give the zero vector.
  Lengths and distances do not extend to points at infinity.
- **Direction:** A reader asks whether the parallel case needs its own rule.
  The writer proposes the reading.
- **Move:** 12, also 15.
- **Check:** The lines `x + y + 1 = 0` and `x + y + 2 = 0` give `(1, -1, 0)`, their shared direction.
  The lines `x + y - 1 = 0` and `x - y - 3 = 0` give `(-4, 2, -2)`, which is the point `(2, -1)`.
  All 56,280 pairs of lines with coefficients from `-3` to `3` agree with Cramer's rule or the parallel case.
  The zero vector appears on exactly the 312 coincident pairs.

**20. Title: Use one name for one step.**

- **Before:** A tutorial says "forward sweep" and its technical companion says "forward elimination" for the same step of a tridiagonal solve.
- **After:** Both writeups say "forward sweep".
- **Why allowed:** The two phrases name one operation, and two names read as two objects.
- **Direction:** A reader of both writeups reports the mismatch.
  The writer changes both.
- **Move:** 13.
- **Check:** The check is a search of both writeups, their labels and their figure text for the retired name.
  It should return nothing.
  This search was not run, since the writeups are hypothetical.

**21. Title: Keep the bridge network out of the series and parallel rule.**

- **Before:** Node equations solve any resistor network.
- **Draft:** "Reduce any network to one resistor by series and parallel steps."
- **After:** The reduction is stated for series-parallel networks.
  The bridge network keeps node equations or a star-delta transformation.
- **Why allowed:** A series step needs a node, other than the two terminals, with exactly two resistors.
  A parallel step needs two resistors on the same pair of nodes.
  The bridge network has terminals `A` and `B`, two other nodes `C` and `D`, and resistors `A-C`, `C-B`, `A-D`, `D-B` and `C-D`.
  `C` and `D` each have three resistors and no two resistors share a pair of nodes, so the reduction cannot start.
- **Lost case:** With resistances `1, 2, 3, 4, 5` in that order, the effective resistance is `155/74`, about `2.095`.
  Removing `C-D` gives `2.1` and shorting it gives `2.083`, so neither shortcut recovers the value.
  The exception is a balanced bridge network, with `A-C/C-B = A-D/D-B`, which behaves as if `C-D` were absent.
  With `1, 2, 3, 6` on the first four resistors, `C` and `D` have equal potential, and the effective resistance is `2.25` for every value of `C-D`.
- **Direction:** The writer proposes the reduction.
  The reviewer tests the class of networks where no series or parallel pair exists.
- **Move:** 14, also 15.
- **Check:** Node equations and the star-delta transformation both give `155/74`, and the reduction stops with five resistors.
  In the balanced case, exact node equations at four values of `C-D` from `0.1` to `100` give equal potential at `C` and `D` and an effective resistance of `9/4`.
  All 3,000 random series-parallel networks reduce to one resistor and match node equations to `2e-12`.

**22. Title: Keep the discriminant and the stability test apart.**

- **Before:** One rule box for `x'' + b x' + c x = 0` treats the discriminant as the test for the behavior of the oscillator.
- **After:** There are two tests.
  `b^2 - 4c < 0` decides oscillation, and `b > 0` with `c > 0` decides stability.
- **Why allowed:** The characteristic roots are `(-b + sqrt(b^2 - 4c))/2` and `(-b - sqrt(b^2 - 4c))/2`.
  The discriminant decides whether they are real.
  The signs of `b` and `c` decide whether their real parts are negative.
- **Direction:** The writer proposes to reuse the discriminant test from the section on quadratics.
  The reviewer builds the pair with equal discriminant.
- **Move:** 15.
- **Check:** The pairs `(b, c) = (1, 1)` and `(-1, 1)` both have discriminant `-3`.
  Their roots have real parts `-0.5` and `+0.5`, so only the first is stable.
  On 1,681 grid points of `(b, c)`, the sign test matches computed roots for stability, and the discriminant matches them for oscillation.

**23. Title: Replace a Bernoulli sequence by the number of successes, and carry it through.**

- **Before:** The likelihood is carried as a product over `x_1, ..., x_n` through several sections, and the figures show raw sequences.
- **After:** `L(p) = p^k (1 - p)^(n - k)`, where `k` is the number of successes.
  The number of successes and `n` decide every likelihood comparison, and the estimate `k/n` follows at once.
  The per-observation notation leaves the later sections, which shorten.
  Figures of sequences become figures of likelihood against `k`.
- **Why allowed:** Given `k`, every sequence has probability `1/C(n, k)`, free of `p`, so `k` is a sufficient statistic for `p`.
- **Lost case:** The number of successes is sufficient for `p` only within the model of independent, identically distributed trials.
  It cannot test that model.
  The sequences `0000011111` and `0101010101` both have `k = 5`, with 2 runs and 10 runs, so a model check keeps the sequence.
- **Direction:** The reviewer proposes the statistic.
  The author asks that the figures follow.
- **Move:** 1 and 16, also 14.
- **Check:** On all 1,024 sequences of length 10, at `p` equal to `1/10`, `1/3` and `7/10`, the likelihood depends only on `k` and the conditional probability is `1/C(10, k)`, in exact arithmetic.
  Among the 252 sequences with `k = 5`, only 4 have 2 or 10 runs, so both example sequences are extreme under independence, and `k` cannot show it.

**24. Title: Keep the sign before taking absolute values.**

- **Before:** The series `(I - A)^-1 = I + A + A^2 + ...` is stated under `rho(|A|) < 1`, with `rho` the spectral radius.
- **After:** For the series grouped by power, the condition is `rho(A) < 1`.
- **Why allowed:** The powers of `A` go to zero exactly when `rho(A) < 1`, and the series then converges to the inverse.
  Absolute values discard cancellation between signed terms, so they give a stronger condition than the decision needs.
- **Scope:** The weaker condition covers the series grouped by power.
  Expanding each power into individual signed paths and reordering them can need the absolute-value condition.
- **Direction:** The reviewer asks which condition the argument actually uses.
- **Move:** 1, also 14 and 15.
- **Check:** The matrix `A = [[1, -1], [1, -1]]` has `A^2 = 0`, `rho(A) = 0` and `rho(|A|) = 2`, and `(I - A)^-1 = I + A` exactly.
  All 1,358 random matrices with `rho(A) < 0.9` and `rho(|A|) > 1.05` have a series that converges to the inverse.

**25. Title: Use one solvability test for nonsingular and singular systems.**

- **Before:** One rule box says a nonsingular system has a solution.
  A second says a singular system has a solution exactly when `b` is orthogonal to the left kernel.
- **After:** One rule box says `A x = b` has a solution exactly when `b` is orthogonal to the kernel of `A^T`.
  "Nonsingular" stays as a case name, since the kernel is then zero and the test passes automatically.
- **Why allowed:** The column space of `A` is the orthogonal complement of the kernel of `A^T`.
- **Scope:** The merged rule decides existence only.
  Uniqueness is a separate statement about the kernel of `A`.
  The matrix `[[1, 1], [2, 2]]` with `b = (1, 2)` passes the test, since its left kernel is spanned by `(-2, 1)`, and it has a one-parameter family of solutions.
- **Direction:** The writer notices that both rule boxes apply the same test.
- **Move:** 10, also 15.
- **Check:** On 1,500 random integer systems up to 4 by 4, exact rank comparison and the orthogonality test agree.
  The 119 full-rank square systems among them all pass.

**26. Title: Substitute the defining equation before judging a log sensitivity.**

- **Before:** For `x > 0`, the Lambert W function `w` is defined by `w e^w = x` with `w > 0`.
  Implicit differentiation gives the log sensitivity of `w` to `x` as `x/(w e^w (1 + w))`, and the reader must work out its size.
- **After:** Substitute `x = w e^w`.
  The log sensitivity becomes `1/(1 + w)`.
  It lies between zero and one by inspection.
  Its limit is one for `x` far below one, where `w` is near `x`.
  It tends to zero slowly for large `x`, where `w` grows like `log x`.
- **Why allowed:** The substitution uses the equation that defines `w`, so it changes the form of the expression and not its value.
- **Scope:** The bound holds on the principal branch with `x > 0`.
  As `x` approaches `-1/e`, `w` approaches `-1`, and the expression diverges.
- **Direction:** A reader asks how large the log sensitivity is.
  The writer proposes the substitution.
- **Move:** 3, also 1.
- **Check:** Over 2,401 values of `x` across 12 decades, the formula matches finite differences to `8e-11`.
  It is near `1.0` at `x = 1e-6` and near `0.08` at `x = 1e6`.
