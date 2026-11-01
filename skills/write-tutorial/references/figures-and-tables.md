# Figures and tables

A picture should perform part of the calculation.
Each figure has one stated question and one returned relationship or result.
Pair each main operation or result with a local illustration, because a later complete picture does not teach an earlier construction.
The author's reminder: "remember, illustrate visually".

## One kind of object has one form

A reader who learned the first table of a kind can then read every later one without new instructions.
Record the first instance of each kind in `TUTORIAL-DESIGN.md`, and check every later instance against it.
The author, on this rule: "that's what i mean by consistency".

## Figures

- **Text goes in the caption, not in the figure.** Meanings of colors, marks and arrows belong in the caption. The figure keeps the drawing, panel titles and symbol labels.
- **Symbols on the figure, numbers in the caption.** Threshold and marker labels carry symbols. Numerical values stay in captions, and decade ticks stay on axes. A numerical value on a figure says that the number is the point.
- **Give each figure one job, and place it in the section that cites it.** A float that lands in the next section is a defect. Cite a figure in the text where the text uses it, and have the text read the picture: state what to inspect and what follows.
- **Show the result figure before deriving it** in a subsection.
- **Break up long text.** Where the reader must picture a graph, show it and let the prose point to it. Flag long stretches with no figure.
- **Let a figure carry repeated arithmetic.** Give one explicit substitution in the text, then let a consistent table or figure carry the repeated cases.
- **Size a figure to its content.** Regenerate a sparse figure at a smaller native size, with the same font size and line widths. Never scale the placed PDF.
- **Hug the content.** Narrow an axis range rather than keep an empty decade.
- **Keep positions fixed** across drawings of the same system, and keep a physical quantity's color and line style across related panels.
- **Compact glyphs after the first showing.** Draw labeled nodes the first one or two times a network appears. Use small dot glyphs afterwards, with one labeled key. Use the full graph when a figure has only two or three graphs.
- **Plain fixed-size arrowheads,** with a tip size independent of line width. A default arrow tip that scales with line width turns thick arrows in small glyphs into all tip.
- **No stray marks.** Labels sit clear of every curve. Use leader lines where needed.
- **Name panels** (A), (B) and so on.

## Exact curves, leading-order curves and data

Where a model has both, draw a broad translucent curve for the exact response and a thin solid curve for the leading-order one. Sweep every panel when one lacks it. Schematic strips with no axes are exempt.
Translucency alone does not mean uncertainty. An uncertainty band needs its own stated definition and key.
Show observations as discrete marks and predictions as curves. Mark training, validation and test roles by marker or line style, with a local key, and keep physical identity in the color.
Never draw a curve for an unrun computation. An unfinished result is a marked box.

## Axes

Use base-10 logarithmic axes for positive physical quantities when the calculation compares orders of magnitude.
Label the physical quantity. Do not label a raw axis by its logarithm.
Name the observed quantity and its units on each axis.
State the supplied input, the frozen parameters and the changed intervention in the caption.
Check the coordinates of a saved plot table before writing its axis labels. A figure can be numerically correct while answering a different question.

## Captions

Lead with the relationship the figure shows, then give its key.
Use canonical names for outcomes, never a free description.
Explain the complete key in the first caption of a series. Later captions refer back to it, unless the first is too remote.
Move numerical and scientific conclusions to the paragraph that reads the figure.

## Tables

- Top, header and bottom rules are full booktabs rules. Rules between body rows are very thin, only to guide the eye. The macro `\rowguide` in the scaffold's `macro.tex` does this.
- Merge vertically repeated cells when they express the same outcome.
- Number and caption every table the text uses, and state matrix orders and quantities locally.
- Separate rows so each entry's case is clear.

## Palette

Use one role map for every figure, so the documents read as a series. The same state keeps its color across figures.
Marks are deep strokes and regions are flat pastel fills, with identity coming from the matching stroke or a label.
Beyond six categories, do not invent a seventh hue. Fold into fills and labels, or use small multiples.

The default palette is the Okabe-Ito set, designed to stay distinct under common color blindness. Replace it in `macro.tex` and in your plotting setup if your work has its own identity.

| Tier | Colors, in fixed order |
| --- | --- |
| Marks | blue `#0072B2`, vermillion `#D55E00`, green `#009E73`, purple `#CC79A7`, orange `#E69F00`, sky `#56B4E9` |
| Fills | the same order at 15 percent strength: `#D9EAF3`, `#F9E7D9`, `#D9F0EA`, `#F7EBF2`, `#FBF1D9`, `#E6F4FC` |
| Neutrals | ink `#222222` for text and axes, gray `#777777` for edges and labels, leader `#B0B0B0`, grid `#E8E8E8` |

Roles: primary or important is vermillion, secondary is blue, highlight is orange, background data is sky.
Filled markers are borderless with a thin white ring. Open markers have a same-hue edge. Never put a dark outline on a data mark. Dense scatter clouds stay ring-less.

## Fonts in plots

Match the document. In matplotlib, set `text.usetex` to true with a serif family and the document's font packages, so labels match the text and full LaTeX works in them.
If TeX may be absent, fall back to `mathtext.fontset = "cm"` with a serif family.
Check the result with `pdffonts`.

## Verify twice

First check the science: composition, signs, units, fixed conditions, and the source of each number.
Then render the compiled pages and inspect them at reading size: fonts, captions, arrowheads, label collisions, clipping, table rules, and how close each figure sits to its discussion.
A successful render is not a visual review.
