# A worked exemplar

The system is a textbook one, so nothing here depends on any project.
It shows one piece of material written three ways: a draft with typical defects, the tutorial version, and the companion version.
Calibrate on the difference, not on the topic.
Paths, ledger rows and figure numbers inside the quotes are placeholders for a real project's. None of them exists in this repository.

## The draft, with the defects it has

> **Michaelis-Menten kinetics.**
> The Michaelis-Menten framework can be leveraged to facilitate an understanding of saturation. Recall that $v = k_{\mathrm{cat}} E S/(K_M + S)$, which, as is well known, follows from the quasi-steady-state assumption (see the Appendix for the derivation); hence we can consider two cases. When things are small it's linear. When they are large it saturates. These regimes are useful. Note that for $S = 10\,\mu$M and $K_M = 100\,\mu$M we get $v \approx 0.09\,k_{\mathrm{cat}}E$, so the system is basically linear there. Saturation is therefore important in biology.

| Defect | Rule it breaks |
| --- | --- |
| The title names a topic, not a question | Point first |
| "can be leveraged to facilitate" | Imperative for what the reader does |
| The formula arrives before any reason to want it | Name the reason first |
| A pointer to the derivation in mid-argument | Citations go at the end, and the tutorial does not point at each cut |
| "things", "small", "these regimes" | Name the object, never point at it |
| "useful" | Say exactly what a qualitative word claims |
| Numbers stand in for a condition | Give a condition for every outcome |
| The closing line adds nothing | Delete a closing aphorism |
| One semicolon and one paragraph with four turns | One paragraph makes one point |

## The tutorial version

> **When does an enzyme stop responding to its substrate?**
> An enzyme responds to its substrate at low substrate and ignores it at high substrate.
> The crossover between the two is centered where one ratio equals one.
> That ratio is the substrate concentration divided by the Michaelis constant.
>
> **The substrate concentration decides through a single comparison.**
> Take an enzyme at total concentration $E$ acting on a substrate at concentration $S$, with catalytic constant $k_{\mathrm{cat}}$ and Michaelis constant $K_M$.
> We vary $S$ and hold $E$, $k_{\mathrm{cat}}$ and $K_M$ fixed.
> We take the enzyme to be scarce, $E \ll S + K_M$, so that binding does not deplete the substrate.
> The rate is
> $$v = k_{\mathrm{cat}} E \frac{S}{K_M + S}.$$
> The denominator is a sum of two terms, and the larger one sets the rate.
> Compare them through the ratio $\rho = S/K_M$.
>
> **The ratio gives two outcomes, each with its condition and its accuracy.**
> The two cases follow from which term of the denominator is larger.
>
> | Outcome | Condition | Leading-order rate | Relative error of that rate | Leading-order gain of $v$ in $S$ |
> | --- | --- | --- | --- | --- |
> | Unsaturated enzyme | $\rho \le 1$ | $(k_{\mathrm{cat}}/K_M) E S$ | $\rho$ | $1$ |
> | Saturated enzyme | $\rho > 1$ | $k_{\mathrm{cat}} E$ | $1/\rho$ | $0$ |
>
> Each leading-order rate is accurate only far from the crossover.
> At $\rho = 0.1$ the unsaturated rate is 10% too high, and at $\rho = 1$ both rates are twice the exact rate.
> Here the gain is $\mathrm{d}\log v/\mathrm{d}\log S$, the slope of the response on log-log axes.
> Its exact value is $1/(1+\rho)$.
>
> [Recipe box: **Read a saturation response.** *Supplied:* $S$, $K_M$, $k_{\mathrm{cat}}$ and $E$, with $E \ll S + K_M$. 1. Compute $\rho = S/K_M$. 2. If $\rho \le 1$, the leading-order rate is $(k_{\mathrm{cat}}/K_M)ES$, with relative error $\rho$. 3. If $\rho > 1$, the leading-order rate is $k_{\mathrm{cat}}E$, with relative error $1/\rho$. 4. If that error is too large for the use at hand, use the exact rate $k_{\mathrm{cat}}E\rho/(1+\rho)$. *Returns:* the outcome, a rate and its relative error. *Next:* compare the rate with other rates in the system. *Check:* the two leading-order rates agree at $\rho = 1$, where each is twice the exact rate.]
>
> Figure 1 shows the response. The thin lines are the two leading-order rates. They meet at $S = K_M$, where the broad exact curve lies a factor of two below them.

| What to notice | Rule |
| --- | --- |
| The title asks the question, and the opening states the point | Point first |
| The result comes before the machinery | The first page is computable |
| "We vary $S$ and hold... fixed" comes first | Say what varies and what is fixed |
| The ratio $\rho$ earns its symbol by carrying both conditions | A symbol names a defined object used repeatedly |
| Each outcome has its condition | A condition for every outcome |
| Each leading-order rate carries its error, the conditions cover $\rho = 1$, and the change is called a crossover | An approximate result states its regime and its accuracy |
| No derivation of the rate law appears, and no pointer to one | The reader accepts the statement. This is the main text. |
| The exact factor of two is a check the reader can see, read from the figure | The text reads the picture |
| The scarce-enzyme hypothesis appears once, where it buys the calculation, and its justification is in the companion | Motivate an assumption by what it buys, and keep every hypothesis the reader needs |

## The companion version

The same material, with the opposite job. Every statement has its argument and its scope.

> **Proposition 1 (leading-order rate of a scarce enzyme).**
> Consider the mechanism $\mathrm{E} + \mathrm{S} \rightleftharpoons \mathrm{C} \to \mathrm{E} + \mathrm{P}$ with rate constants $k_{\mathrm{on}}$, $k_{\mathrm{off}}$ and $k_{\mathrm{cat}}$, under the quasi-steady-state assumption for the complex C, with the free substrate approximated by $S$.
> Let $K_M = (k_{\mathrm{off}} + k_{\mathrm{cat}})/k_{\mathrm{on}}$ and $\rho = S/K_M$.
> Then $v = k_{\mathrm{cat}} E \rho/(1+\rho)$, and the relative errors of the two leading-order rates are
> $$\left|\frac{v - (k_{\mathrm{cat}}/K_M)ES}{v}\right| = \rho, \qquad \left|\frac{v - k_{\mathrm{cat}}E}{v}\right| = \frac{1}{\rho}.$$
>
> *Proof.* Setting $\mathrm{d}C/\mathrm{d}t = 0$ gives $k_{\mathrm{on}}(E - C)S = (k_{\mathrm{off}} + k_{\mathrm{cat}})C$, so $C = ES/(K_M + S)$, and $v = k_{\mathrm{cat}}C$.
> Writing $v_1 = (k_{\mathrm{cat}}/K_M)ES$ and $v_2 = k_{\mathrm{cat}}E$, we have $v = v_1/(1+\rho) = v_2\,\rho/(1+\rho)$. Thus $v_1/v - 1 = \rho$, and $v_2/v - 1 = 1/\rho$. $\square$
>
> **Remark (scope).** The free substrate equals $S$ only up to depletion by the complex. The quasi-steady-state assumption requires a scarce enzyme, $E \ll S + K_M$, as shown by Segel and Slemrod (SIAM Review, 1989).
> The leading-order rate $\min(v_1, v_2)$ has its largest relative error at $\rho = 1$, where $v_1 = v_2 = 2v$.
>
> **Check.** On a grid of 400 values of $\rho$ in $[10^{-3}, 10^{3}]$, the two identities hold to machine precision (`python3 code/check_mm.py`). % result: R1-MM-ERROR

| What to notice | Rule |
| --- | --- |
| Hypotheses and conclusion only, in the statement | Statements are bare. Interpretation goes in remarks. |
| The formula the tutorial stated is now derived, and the errors are exact | The companion shows statements are true |
| The scope is stated, with its source | A claim carries its limits and its citation |
| The numerical check has a ledger row and a command | A number enters only through a row |
| A numerical check supports the proof, and does not replace it | Computational checks challenge a proof |
