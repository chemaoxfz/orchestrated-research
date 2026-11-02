---
name: write-tutorial
description: Write or review a research tutorial in the style of the main text of a high-impact paper, with a reader who accepts every statement and wants to understand, follow, use and appreciate the method. Holds the tight house style for structure, procedure, examples, prose, naming, tables and figures. Use whenever you write, revise or review the human-readable tutorial of a research project, or the main text of a paper with a technical companion. Proofs and complete evidence belong to the companion, and write-companion holds their standard.
license: MIT
metadata:
  version: "0.2.0"
  source: "https://github.com/chemaoxfz/orchestrated-research"
---

# Write the tutorial

The tutorial is the main text of a high-impact paper.
Its reader accepts every statement you make and asks one thing: how can I quickly understand, follow, use and appreciate this?
The companion shows the statements are true. That is a different document, with the opposite review standard.

These rules are tight on purpose. Each one came from a recurring correction.
A project's `AUTHOR-PREFERENCES.md` extends them and wins where it differs. The author's current request wins over both.

[The worked exemplar](references/exemplar.md) shows these rules on one page, next to the same material in companion form.
[Figures and tables](references/figures-and-tables.md) holds the visual rules.

## What each passage must do

**Test every passage by the reader's use.** Does it help a reader who accepts every statement understand, follow, use or appreciate the method? Cut a passage whose only job is to prove. Never report a missing proof as a defect.

**The tutorial is self-contained in vocabulary, concepts and use.** A reader can learn every term and carry out every step from the tutorial alone. Detailed derivations are elsewhere. A sentence naming the companion is optional: one at the very beginning, or none, and never a pointer at each cut.

**Still verify every statement.** The reader takes each one on trust, so anything false, inexact or missing a needed hypothesis is a serious defect. Keep every hypothesis and formula the reader needs to execute the calculation.

**Apply the purpose test to every subsection.** Use the version that fits the project, and write the answers in `TUTORIAL-DESIGN.md`.

For a calculation done by hand:

1. Which calculation does the reader do?
2. Which picture of the whole behavior does it give?
3. Which exact simulation or measurement checks it?

Leading order is there so the reader can hold a complex behavior in mind as a whole. Exact simulation is the check. Complicated proofs and everything only a proof needs go to the companion.

For a computational step, computation takes the place of a hand calculation and must be as clear. Give it five fields:

| Field | What the reader receives |
| --- | --- |
| Supplied data | A named table, matrix, parameter set or observation, with its source |
| Operation | The actual substitution, solve, update, comparison or selection. A script name may implement it, but it does not explain it. |
| Returned object | A named object, with its order and units |
| Next use | The next named step that consumes it |
| Visible check | What the reader should inspect to see that the step did its job |

Each computation is simple, with a small returned object the reader can inspect almost as in a hand calculation.
Every demonstration says what is constructed from what information, what is learned from which observations, and which frozen prediction is tested against which baseline.

## The shape of the document

**One arc.** Every writeup runs problem, challenge, approach, demonstration, significance. If a demonstration is not finished, still write all five: planned demonstrations in "Result to complete" boxes, with a design and an outcome stated so that a result can contradict it. Rewrite the significance only from completed results.

**Say what is new, once, on the first page.** State the claim, what it adds to named prior work, and what the reader can now do. Stating the gap once is not a rebuttal.

**Set a length target.** Record a page target for the document and each part in `TUTORIAL-DESIGN.md`. When a part runs over, cut material or move it to the companion. Do not compress the sentences.

**One procedure is the spine.** Introduce one named procedure once, and run it literally on one small example. Give steps short memorable names and imperative leads. Write each step name in brackets at every mention, like [Sort], so the reader never wonders whether a word is a name.

**Three kinds of section, with different jobs.** Never force one's template on another.

| Kind | Job | Order |
| --- | --- | --- |
| Procedure section | Teach a step | Discussion with definitions, then the recipe box, then the example |
| Add-on section | Extend the procedure | Motivation, what is new, which named steps change, the general method, an example running the modified procedure, and a closing reuse sentence |
| Demonstration | Show what the procedure delivers | The system and its question, the network or model figure, the procedure's result, the conclusion for the field, then further interpretation |

**Add-ons are modular.** An add-on says "This add-on changes [X] and [Y]" and states only that change. It does not restate the base procedure or another add-on's rule, so a reader combines add-ons by applying each one's changes. The number of add-ons is not fixed. Introduce one at first use, when a new operation helps the flow, and reuse it by name.

**Every later part is a payoff for its own audience.** Open it with the question that audience is asking, in their terms. Close it with what they gain. Reused steps are brief, and space goes to what is new.

**A demonstration leads with the procedure's result, not with exact analysis.** Analyzing the response by exact formulas first defeats the purpose of the demonstration.

**A case study is a demonstration of one system, with this shape:**

1. A title naming the system and the result, such as "Case study: saturation of a Michaelis-Menten enzyme".
2. An opening that introduces the system, says what the subsection illustrates, and states the result. The first page is computable: the reader can evaluate each outcome's condition for their own parameters from that page.
3. The model, drawn.
4. The procedure in order, run literally, with every choice it makes shown rather than assumed.
5. Variants, each naming only what changes.
6. A takeaway comparing the cases.

Run a use test on a variant the text does not treat. It often finds the simplest rule.

**Across the document, the smallest symbolic case comes first.** Run the procedure on the smallest case that exercises the deciding operation, with symbolic parameters. Asymmetric cases, general counts and general rules come later in the document.

**The author may set a required minimum for every example,** naming the objects each must show, for example its model written out, a table of all outcomes with their conditions, plots of those outcomes, and a bifurcation or dose-response sweep. Record it in `TUTORIAL-DESIGN.md`, and audit each example against it first. Better narrative and deeper analysis come after the minimum is met.

## Teaching order

These rules hold inside a section, down to a paragraph. Across the document, the smallest symbolic case still comes before the general method, as above.

- **Point first.** Each section opens with its point: what earlier sections established and which question this one answers. Its title states that question or result in language available before the section.
- **Rule before case.** State the general rule, then apply it to the example. Put the example right after the rule it illustrates.
- **General first, then specialize.** State a construction in its general form, then add a separate paragraph writing out the specialization the section uses. A specialized formula before its general form hides what is being done. A general formula with no specialization leaves the reader unable to use it.
- **Derive, do not hand over.** Obtain conditions, intervals and formulas from a rule already stated. A bare list of inequalities is abrupt and unmotivated. Judge this by explanatory value, not completeness: keep a calculation when it gives the reader insight they need in order to keep going. Do not derive a result whose motivation, point and outcome are already clear.
- **Say what varies and what is fixed** before a calculation.
- **Name the reason first.** Open each step with why it is needed. A reason is one sentence.
- **Motivate an assumption by what it buys.** Say what the assumption makes possible, and name the reduced object.
- **Common case before special case,** and name all the alternatives.
- **Define at first use,** where the reason for the definition is visible, not earlier. Then reuse it. A later procedure uses an earlier result rather than deriving it again.
- **Give a condition for every outcome.** List the possible outcomes, and give each its condition. Together the conditions cover every case, boundaries included. Readers usually want to know when each behavior happens, not what happens at given numbers. Numbers belong to plotted examples, and captions name the condition those numbers satisfy.
- **An approximate result states its regime and its accuracy.** Say that a leading-order result is leading order, give the condition under which it holds, and give its error in a form the reader can use. A smooth change between two regimes is a crossover, not a switch. The derivation of the error belongs in the companion.
- **Say what an event does to defined objects,** and how it changes the output.
- **Constructive classification.** Give a positive, executable test, classify all possibilities, and read conditions directly when possible.
- **A procedure is an algorithm with a stopping test.**

## The recipe box

A recipe box holds only the short usable rule.
Definitions, motivation, intuition, observations and principles go in the discussion before the box.
It opens with what is supplied and ends with the returned object, its next use and a visible check.
Its numbered items contain formulas, operations and stopping tests. Words like "construct" and "retain" do not replace those operations.
Long blocks inside a box make a simple rule look complicated.

## Stay constructive

Frame each demonstration by what it delivers. Turn a limit into a choice or a result.
Leave out rebuttals and lists of what a model or a rival method cannot do. An easy extension that is not the point is not mentioned.
Treat what looks like a weakness as something the method delivers, when it does: a poorly determined parameter becomes a ranking of which measurement to make next.

This rule controls the subject and the emphasis. It never changes the evidence.
A failed test goes to the author at once, and the author decides what the text says.

## Say each point once

Remove whole statements that are redundant, unnecessary or irrelevant.
**Never shorten or compress the remaining sentences.**
The author: "we only remove redundancy that's above sentences, i.e. points or statements that's redundant or unnecessary or irrelevant."

Common cases to remove: plan previews that repeat a section's question, restated standing assumptions, recaps after a box or display, special cases a definition already covers, one equation in several rearranged forms.
A reused step gets a one-line pointer, not its own box item.

**Keep objects explicit.** Keep equations, tables and figures explicit unless a case is really repetitive. A proposed cut is a proposal: keep the object, with a caption starting "Candidate to cut", and do not use it in the narrative. Check every cut against the ledger of author requests before making it. The orchestrator settles a flagged cut at the next stage against that ledger, the before-state keeps the object recoverable, and the author can overturn the decision.

**Stay on the main line.** Answering a reader's question in conversation does not mean the answer belongs in the text. Skip asides about exact behavior or plot appearance.

## Naming

Every noun phrase names its precise defined object.
The reader should never wonder whether a word is a name, or which object it names.

- **Name the object, never point at it.** "These results" becomes "the fitted rates of the two-substrate model". "The approximation" becomes "the leading-order approximation".
- **Use the established noun and the standard name.** Do not coin a synonym for elegance.
- **Say exactly what a qualitative word claims.** "Close to the exact response", not "useful".
- **Name each term by what it is, in terms that work beyond the example.** Avoid case-specific coinages and decorated names. Delete emphasis words such as "full" and "complete" when they name no distinction.
- **Use the full name of a defined term at every use,** including titles, captions and figure labels. A shortened or decorated name reads as a different object. If the full name makes a sentence clumsy, rewrite the sentence.
- **One object, one name. One name, one object.** Do not let one drawing or word stand for two objects.
- **An undefined phrase must not pose as a term.** If it recurs or appears in a title, caption or label, define it where its concept first appears, say it in plain words, or delete it.
- **Every quantifier names the set it ranges over.** "For every i" leaves the reader unsure whether i is a node or an edge.
- **Define every symbol at or before first use.** A symbol earns its place by naming a defined object used repeatedly. Write the formula when it is shorter than the words. Add no alias for an expression of comparable length, and keep local parameters to as few as possible, each interpreted.
- **Let the notation carry every case.** Write conditions through defined quantities, with one inequality convention. Values the general formula covers are ordinary instances, not listed special cases. Say each rule in mathematics too, so the formula confirms the words.

## Prose

- Short, direct, standalone sentences. They give a tighter reading rhythm.
- No em dashes. Use a period, a colon or parentheses. Almost no semicolons.
- Present tense for what the model does. Imperative for what the reader does. "Solve the quadratic for its positive root. That root gives the rate." Never "the framework can be leveraged to facilitate evaluation".
- **One paragraph makes one point, and says which one up front.** Lead with a claim that could stand alone, often in bold. The failure to watch for is turns, not length: a paragraph of short clear sentences that each pivot away from the last is unreadable.
- Announce a decomposition before executing it.
- Put a citation or file reference at the end of the claim it supports, not in the middle of the argument.
- Replace a pronoun whose referent is more than one sentence back with the name of the thing.
- Delete a closing aphorism that a heading or box already carries.
- In TeX, put one sentence on each source line.
- Keep a formal statement to hypotheses and conclusion. Motivation goes before it, and interpretation after.

## Evidence in a tutorial

Every number has a source, a real or synthetic label, and a new, reproduced or compared label, either in a standing sentence that opens the part or locally.
Keep the ledger row ID in a source comment beside the claim, not in the text.
Report across noise draws: medians, ranges or worst values. A seed number never appears in the main text. What the tutorial presents must be about the system, the question or the method, not about one random fluctuation.
Keep a measured quantity, a model prediction and an expected outcome visibly distinct.

## Review, in this order

1. **Design pass.** Reread the reference document named in `TUTORIAL-DESIGN.md`. For each section: does it belong, is it told in the best order, would another story teach better? Propose the better flow.
2. **Purpose pass.** The purpose test, on each subsection. Search for proof-only material: words such as "theorem", "certificate" and "proves" in a passage the reader only needs to use.
3. **Form pass.** Each table and figure against the first of its kind. One object has one name.
4. **Sentence pass.** Name, teach and prose rules, on the final source, without the diff.
5. **Evidence pass.** Every statement against the companion. Every number against the ledger. Every author request against the ledger.
6. **Rendered pages.** Render the pages and read them at reading size, in order. A clean build does not establish a clear argument.

When a distilled principle arrives from the author, run it as a whole-document pass. A principle fixed in one section and left in the others will come back as the next correction.
