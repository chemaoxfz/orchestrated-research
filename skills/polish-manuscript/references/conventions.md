# Manuscript conventions

These are defaults for any quantitative manuscript.
The project's instructions, `AUTHOR-PREFERENCES.md` and terminology register win over them.
Check the current source and `PROJECT_STATE.md` before treating a volatile term as settled.
[The skill](../SKILL.md#terms-and-records) defines the terms used here.

## Fit the format

Keep the project's existing format, and read the LaTeX names below through this table.

| LaTeX | Markdown | HTML |
|---|---|---|
| `\textbf{term}` at a definition site | `**term**` | `<dfn>` or `<strong>` |
| `\label` and `\ref` | Heading anchors and links | `id` attributes and `href` links |
| Annotation macro such as `\todo{...}` | `TODO` marker or comment | HTML comment or marked element |
| Build log from `latexmk` | Output of the project's renderer | The rendered page in a browser |

## Prose and source formatting

- Use one English variety throughout, American by default, and preserve original spelling in quotations, cited titles, proper names, labels, macros, identifiers and file names.
- Prefer short, direct, standalone sentences, without em dashes and with few semicolons.
- Put one complete prose sentence on each source line, in LaTeX, in Markdown and in hand-edited HTML, and do not wrap one sentence to a fixed source width.
- Give each paragraph one claim and put that claim first.
  Split a paragraph when its subject or claim changes, not when it reaches a fixed length.
- Make each paragraph advance the local argument and connect it to the preceding result.
- Announce a decomposition before executing it.
- State the reason before a calculation: what it establishes, and why that is enough for the current step.
- Put each citation at the end of the claim it supports.
- Replace a pronoun whose referent is more than one sentence back with the name of the object.
- Remove repeated conclusions, decorative transitions and closing slogans.
- Use each defined term's full name at every use, including titles, captions and figure labels, with no shortened name and no qualifier that adds no distinction.
  Rewrite the sentence when the full name is awkward.
- Do not let an undefined phrase pose as a term: say it in plain words, or define it when the text needs it repeatedly with one meaning.
- Make each title name the conceptual task, operation or question in terms a reader understands before reading the section.
  Be precise about the ideas and scope, rather than an example's narrow outcome or unexplained internal wording.
- Outside a deliberately axiomatic section, guide each section through a compact causal sequence: governing question, limitation of the current description, next object or map, and the capability its result supplies.
- Use mathematical and domain motivation to explain why the next step is needed, not as a license for repeated roadmaps or metaphor-heavy prose.
- Use the least abstract formulation that proves the claim, and prefer a direct formula involving an established object over a new wrapper around it.

## Formal writing

- Make the manuscript proof self-contained.
- Use computations to test a claim, not to justify it in print.
- Keep definitions, lemmas, propositions and theorems to hypotheses and conclusions, each compact, self-contained, direct and quotable.
- Put motivation before the environment, and put interpretation and consequences after the proof.
- Restate the exact usable content of a distant result or equation at the point of use.
  The citation identifies its source and proof, while the local text lets the reader follow the current derivation without backtracking.
- Recall the minimum operational rules the target audience needs before using unfamiliar notation or standard background in a calculation: what the quantities mean, which parameters are fixed, and one representative substitution when useful.
  Keep enough in the main text that a reader can accept the rules and continue, and cite the appendix for their longer justification.
- Do not duplicate a nearby statement when its usable conclusion is already explicit in the local paragraph.
- State a section-wide standing hypothesis once in compact form.
  Put result-specific scope qualifications immediately after the result where that hypothesis becomes load-bearing.
- Use a lemma for reusable machinery, state it once, and cite it instead of redeveloping it locally.
- Use a theorem only for a central result.
- Avoid restating a parent result as a corollary when a citation is clearer.
- Define one concept per definition.
- Write explicit formulas or explicit sets instead of vague existence descriptions.
- Introduce a new quotient, graph, map, fiber, realization or technical noun only when it supports a distinct later result or resolves a genuine ambiguity.
  Before retaining a new object, state in plain language what question it answers.

## Definition markup

- Use `\textbf{...}` for a term at its definition site only, and `\emph{...}` only for genuine emphasis.
- Define every recurring mathematical noun before using it as technical vocabulary.
- If an idea appears only locally, describe it in ordinary words instead of creating a new term, and write a small object directly, such as `\{i,j\}`, rather than introducing an auxiliary symbol.
- Reject burdened words whose established mathematical, domain or metaphorical connotations exceed the intended claim.
  Do not write "stable" without a stability analysis, "optimal" without an optimization, or "causes" on the strength of a correlation.
- Prefer an already defined noun over a synonym, even when the synonym sounds shorter or more vivid.
- A preview states the objects and conclusion at a high level, and it defers formulas and technical definitions until their first complete development.
- Do not use a later object inside an early definition unless it has already been introduced or the passage explicitly recalls it.

## Terminology register

Before introducing or renaming a recurring technical noun or symbol, follow three steps.

1. Inspect the terminology register and the macro file for an existing notation with the same role.
2. Search the target for existing definition sites.
3. Reuse the recorded noun and symbol unless the new object is mathematically different.

Give each recurring term one canonical definition site.
A project may mark that site with a macro that prints the bold term and makes one index entry, such as `\termdef{term}{sort key}`.

An index generated from those sites is a finding aid, and the complete definition in the manuscript body stays authoritative.
Do not index recalled definitions, previews, headings, captions, later occurrences or one-off local variables.
Register recurring mathematical concepts, not every displayed symbol.
Do not add a synonym merely to create another index entry.

## Stable terminology principles

Keep the project's choices in the terminology register as rows of meaning, use and avoid, as in these general cases.

| Meaning | Use | Avoid |
|---|---|---|
| Measured or selected quantity | output | readout, or any second synonym |
| Abstract adjacency of two objects | edge | interface, boundary |
| Set where two regions meet | the explicit intersection | interface, edge |

These principles decide new cases.

- Do not use a generic noun such as "interface" as a technical noun unless the manuscript defines an object by that name, and state the actual object or relation instead.
- Use a word reserved by a field, such as "group", "ring" or "manifold", only for an object that meets its definition.
- Avoid a name that collides with a standard term, as "normal form" would for a form that is merely common.
- Do not use an umbrella term for several distinct objects.
- A shorter name needs the author's authorization, and it carries exactly the existing classification.
  Retain the long name whenever the distinction must be explicit.
- Do not absorb an extra hypothesis into a decorated name, and state the property directly instead.
- A qualifier that can be read two ways needs a stated referent.
- A derived annotation or hierarchy is defined only after the proof it rests on.
- Do not turn an onto map into an isomorphism, and do not assume a bijection among different data attached to one object.
- Do not promote a necessary test to a sufficient criterion.
  A zero derivative is necessary for an interior extremum of a differentiable function, yet `x^3` has a zero derivative at 0 and no extremum there.
- Keep assumptions separate when they share a name or an example.
  For `X` standard normal and `Y = X^2`, the pair is uncorrelated but not independent.
- Retire an informal term by describing the actual object, though a historical label may remain in the source for reference stability.
- Avoid a metaphor, such as "escape" or "survivors", when a defined object names the same thing.
  A metaphor stays fine outside the naming of mathematical objects.
- Do not use a deictic comparison such as "both parts", "the two mechanisms" or "this correspondence" unless the immediately preceding paragraph names the compared objects and the question connecting them.

## Notation and local symbols

- Prefer the simplest notation that makes the mathematical content unambiguous.
- Give systems, states and outputs first in the established physical or domain quantities, and state the relation to a logarithmic or other chart once, at its canonical definition.
- Do not introduce a new symbol, decorated vector or parameter wrapper solely because a quantity can also be represented in another chart.
- A new local symbol needs a stated interpretation and a concrete simplification of a repeated argument.
- Favor full expressions of two or three terms.
  An alias needs either a genuinely cumbersome expression, for example five or more terms, or an independently useful meaning in the argument.
- Name a coordinate map by its defined formula, and specify its source and target spaces before making structural claims about it.
- Do not silently repurpose a symbol, and do not reuse a finite coordinate's symbol for its limiting direction.
- Use explicit derivatives such as `∂log y/∂log x` when they make the differentiated quantities clearer, and state what each holds fixed.
  For an ideal gas with heat capacity ratio `γ`, `∂P/∂V` is `-P/V` at fixed temperature and `-γP/V` at fixed entropy.
- Holding a parameter fixed in a derivative does not mean that it is fixed across the family.

## Exact and leading-order discipline

- Keep exact, finite-scale and leading-order statements visibly distinct.
  By Stirling's formula, the ratio of `n!` to `√(2πn)(n/e)^n` tends to 1, yet their difference diverges.
- Write "leading-order" when it modifies a formula, approximation or geometry in a stated limit, and state the family and the scale.
  The small-angle period `2π√(L/g)` is leading order in the amplitude `θ₀`, and the next factor is `1 + θ₀²/16`.
  Do not add "leading" to an established name simply to repeat the scope already in its definition.
- Use a broad name such as "asymptotic analysis" for the broad study, and reserve a precise name for a precise operation.
- Quantify the sequences and scales at the definition of a limiting object.
- Define a distance or a limiting set at its first use.
- A limit along individual sequences does not assert uniform control or convergence of the whole family.
- Do not transfer a property of exact objects to their limit without proof.
  On `[0, 1]`, each `x^n` is continuous, yet the pointwise limit is discontinuous and the convergence is not uniform.
- Keep a limit distinct from a truncation, even when they give the same formula.
- A fixed factor gives a finite offset in logarithmic coordinates, and that offset vanishes after division by the common scale: `log(2x) - log x` equals `log 2`, while `log(2x)/log x` tends to 1.
  Retain the finite consequences rather than replacing the exact ratio by equality.
- A bound that holds for one fixed system need not be uniform over all systems, so state which is meant.
- Do not transfer a shape from logarithmic to positive coordinates merely because the logarithm is a diffeomorphism.
  A straight line on log-log axes is a power law.
- Do not claim a structure before proving it.
  A function continuous in each variable need not be jointly continuous.
- State every hypothesis used by a global claim, whether exact or limiting.
- Do not state a quarantined claim as a result.

## Matrices

- Use one environment for all partitioned matrices, and keep the dividers that mark the block structure.
- State row and column ordering wherever ambiguity affects a calculation.
- Introduce a derived matrix before using its triangularity, nullity, determinant or any other property.
- When a quantity has both an algebraic name and a domain name, use each in its own development and give the identity connecting them once.
- Do not replace a proved identity by a similar, simpler-looking formula.
- When auditing dependence, distinguish a lossless change of coordinates from a restriction that can lose data.
- Do not take an entrywise logarithm of a matrix with structural zeros, and use the vector of its supported entries instead.
- Preserve the distinction between a Jacobian and a logarithmic sensitivity matrix, including the diagonal conversion factors.
  For positive `x` and `y`, `∂log y/∂log x` equals `diag(1/y) (∂y/∂x) diag(x)`.

## Figures

The steps for changing a figure are in [the workflow](workflow.md#4-finish-notation-and-figures-as-part-of-the-argument), and these are the defaults for what a figure shows.

### Positive physical axes

Label the positive quantity and let the axis carry the logarithm.
This default applies to an axis that shows a positive physical quantity across decades, or a chosen positive ratio or product of such quantities.

- Use a base-10 logarithmic axis, the shortest clear label, and positive decade ticks such as `10^-2, 10^-1, 1, 10, 10^2`, with minor ticks only when useful.
- Do not label the axis with a logarithmic coordinate, `ln(·)` or `log10(·)` when the same coordinate can be displayed as its positive quantity.
- Feed positive values to an actual logarithmic axis, or use an equivalent fully specified plotting transform with the same positive tick positions and geometry.
- Do not merely relabel negative or zero logarithmic ticks as positive values, and do not take the logarithm twice.
- For a color map, use positive scalar data with base-10 logarithmic normalization, not a transformed colorbar over unchanged logarithmic colors.
- For a 3-D surface, convert every data coordinate and limit to the base-10 logarithmic projection before creating the plot artists, and calibrate the ticks to positive values.
- If both axes have the same logarithmic meaning, use equal visual distances per decade when the geometry calls for equal aspect.
- Do not change a computation's logarithm convention or a solver's coordinates solely to obtain base-10 figure axes.
  A logarithmic derivative `∂log y/∂log x` is unchanged when both logarithms use the same new base.
- Use a fixed positive plotting range, because ordinary logarithmic axes cannot contain zero or negative data.
- Identify physical units clearly, and check that a dimensionless label is justified by its dimensions or a declared normalization.

The default concerns positive physical quantities, not every axis.
Signed sensitivities, baseline-subtracted measurements, shares with zero endpoints, graph layouts and abstract coordinates keep the scales appropriate to their own objects.
A radioactive decay plot uses a logarithmic axis for activity and a linear axis for time.

A drawing of limiting geometry on positive axes still shows limiting geometry, so say so once in the caption or the preceding prose.
Positive labels do not assert that a limiting direction is one finite state, or that a leading-order tie is an exact equality.

### Panels, labels and drawing conventions

- Label panels (A), (B), (C) and (D) as needed, and refer to panels explicitly in prose and captions.
- Use the canonical object name in a panel title, without extra qualifiers when the setting is already specified.
- Put explanations in the caption or prose instead of adding large text boxes to the graphic.
- Keep leader lines short and point them approximately normal to the relevant boundary.
- End a region leader inside the intended region, and move its label along the normal side that avoids collisions.
- Use equal aspect ratio on slices of one coordinate space.
- State the conditions of each region in the coordinates being drawn.
- A drawing convention is a choice of display, not a contraction, an isomorphism or a theorem, so state it in the caption.
- A crossing or overlap in a drawing creates no graph edge or vertex, and a marker belongs only where an object exists.
- Place a diagram after the definitions it illustrates, and display a derived annotation only after the text proves its existence and uniqueness.
- A calculation specific to one example supports that example's drawing, not a general theorem.
- In a sequence of panels, preserve the layout and object positions.
  Each later panel keeps the earlier choices and adds only the new restriction, unless it explicitly reintroduces the common starting object.
- When a restriction rejects items, fade each one according to its own test, and do not infer an edge's status from its endpoints.

### Fonts, colors and markers

- Render figures in the manuscript's native fonts, check changed output with `pdffonts`, and reject a plotting library's fallback font in production figures.
- Use the project's documented palette, and verify it before changing an established figure's colors.
- Unless the project says otherwise, use borderless filled markers with a thin white ring, and a same-hue edge for open markers.
- Keep dense scatter clouds ring-free, rasterized and behind the main geometry.
- Use deterministic, small, low-opacity points for sampled data, and raise the sample count before raising the opacity.

## Computation layout

- Keep active prose only in the source files that the project declares active.
  Archive folders, snippet folders and draft files are inactive preservation locations, and active prose never loads from them.
- Run figure and verification scripts from the project root.
- Keep one active figures folder, with production outputs in it.
- Keep preview images in a local cache folder that exists on every system the project supports, and create parent folders before saving.
- Put reusable mathematics in the project's package, with a docstring and a test, once it is used more than once.
- Keep manuscript styling in one shared figure helper.
- Do not cite a verification script in a manuscript proof.

## Build checks

- Run the project's build for the edited target from the project root, one build at a time.
  For LaTeX, that is usually `latexmk -pdf <edited-target>.tex`.
- Use the log path that the build tool prints.
  A build can write its log outside the source folder, and a cloud-synced or online-edited project can hold stale in-folder logs that are not evidence of the latest local build.
- Check errors, undefined references, multiply defined labels and warnings related to the changed passage.
- For HTML, check rendered mathematics, navigation, controls, themes and narrow screens.
  Use offline MathML or an equivalent embedded rendering when the project requires a standalone artifact.
- For Markdown, check rendered mathematics, links and images in the renderer the project uses.
