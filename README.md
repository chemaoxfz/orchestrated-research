# orchestrated-research

Run a long research project as an orchestrator of dedicated agents, in stages, and deliver two documents with different jobs:

- a **tutorial**, written like the main text of a high-impact paper, where a reader who accepts every statement can quickly understand, follow, use and appreciate the method
- a **technical companion**, where every derivation, proof, computation and algorithm lives

These are [Agent Skills](https://agentskills.io). They work in Claude Code, Codex, the DeepSeek harness and other skill-aware agents.
They were distilled from two long projects, each run this way over many stages and many agent sessions.
Examples here are generalized to neutral textbook systems.

## How it works

```text
                            the author
                                 |
                       verbatim requests, feedback
                                 |
                          +--------------+
                          | ORCHESTRATOR |   keeps the intent, runs the stages,
                          +--------------+   reads everything first-hand, edits no document
              numbered items /    |     \ numbered items
                            /     |      \
             +-----------------+  |   +------------------+
             | TUTORIAL WRITER |  |   | TECHNICAL WRITER |   dedicated: long-lived,
             | owns the        |  |   | owns the         |   with their own memory
             | tutorial        |  |   | companion, code, |   and handoff
             +-----------------+  |   | results ledger   |
                                  |   +------------------+
              +-------------------+------------------+
              |                   |                  |
         readers              verifiers           scouts      disposable: a new one
         (one per document,   (verdict table,     (inventory,  each time, because
         to its own standard) with evidence)      literature)  independence is the point
```

A project moves in **stages**, from a small complete version to larger ones, each using the last as a sanity check.
After every stage the orchestrator snapshots the delivery, checks the author's request ledger row by row, reads the rendered pages first-hand, gets independent review, filters the findings against the author's aims, and sends numbered items.
Nothing waits for the author's reading unless the author asks for that. The author gives feedback when they read, and every two or three corrections get distilled into a principle applied across the whole document.

## What you get

| Skill | What it holds |
| --- | --- |
| `orchestrated-research` | The entry point: roles, stages, records, dedicated agents, the project scaffold and the dispatcher |
| `orchestrate-agents` | The orchestrator's craft: messages, delegation, reviewing a delivery, distilling feedback, watching live threads |
| `write-tutorial` | The tutorial's tight style: purpose test, section kinds, teaching order, naming, prose, figures, with a worked exemplar |
| `write-companion` | The companion's standard: claim verdicts, proofs, results ledger, scope, reproducibility |
| `iterate-research` | A bounded research run with a target, a budget and a resumable checkpoint |
| `polish-manuscript` | Revising a section or a whole document as a complete argument |
| `simplify-rules` | Finding the deciding quantity, merging rules, and carrying the simplification through |

Each works alone, and `orchestrated-research` ties them together.

## Install

This repository is private, so you need access to it.

```bash
gh repo clone chemaoxfz/orchestrated-research
cd orchestrated-research
./install.sh               # links into ~/.agents/skills and ~/.claude/skills
./install.sh --all         # also ~/.cursor, ~/.gemini, ~/.codex, ~/.copilot
./install.sh --project .   # or into one project only
```

The default is a symlink, so `git pull` updates every installation. Add `--copy` for a self-contained copy.
The installer never replaces a skill of the same name that you already have. It tells you and moves on.
Restart your agent to load the skills.

For Claude Code, you can use the plugin instead:

```text
/plugin install orchestrated-research --marketplace chemaoxfz/orchestrated-research
```

This one step needs Claude Code 2.1.275 or later.
Plugin skills carry the plugin's name, so you then invoke `/orchestrated-research:orchestrated-research`.

An agent without skill support can read `skills/orchestrated-research/SKILL.md` and follow it.

## Start

In your project folder, tell your agent:

> Use orchestrated-research to develop this into a tutorial and a technical companion. [Your idea, your existing notes, and who the reader is.]

Invoke it as `/orchestrated-research` in Claude Code or `$orchestrated-research` in Codex. On the DeepSeek harness, tell it to read the skill's `SKILL.md` and follow it.
The agent saves your request verbatim, scaffolds the project, inventories what exists, and shows you a plan, the stages and its questions once. Then it keeps going.

The scaffold, `init_project.py`, never overwrites a file. It creates:

```text
your-project/
  AGENTS.md  CLAUDE.md        rules every agent loads
  PROMPT-LOG.md               your requests, verbatim
  PROJECT_STATE.md            objective, stopping condition, decisions, stages
  AUTHOR-LEDGER.md            every request, with status and evidence
  AUTHOR-PREFERENCES.md       rules distilled from your corrections
  TUTORIAL-DESIGN.md          the tutorial's spine and forms
  TECHNICAL-DESIGN.md         the companion's argument and claim verdicts
  RESULTS-LEDGER.md           every number, with data, command and checksum
  GOAL-RUN.md                 rules for an unattended run
  name-tutorial.tex           the tutorial
  name-technical.tex          the companion
  guidance/  literature/  code/  data/  figures/  revisions/
  roles/<role>/               CHARTER.md, MEMORY.md, HANDOFF.md
  roles/roster.json           which backend and thread run each role now
  tools/role.py               sends turns to dedicated agents
  tools/records.py            checks ledgers, makes snapshots
  .claude/agents/  .codex/agents/
```

The scaffold writes LaTeX. `polish-manuscript` also handles an existing Markdown or HTML manuscript.
Inside a Codex sandbox, `.codex/` is protected, so the scaffold skips the Codex agent files and warns. Writers can then run as generic subagents from their role folders.

## Dedicated agents that keep their memory

You do not need separate terminal sessions. A writer can stay dedicated, with its own memory, on any of these:

| | Durable memory | Keeps its conversation between turns |
| --- | --- | --- |
| **Claude Code** | `memory: project`, loaded automatically, kept in `roles/<role>/` | `SendMessage` within a session, or `claude -p --resume` from any process |
| **Codex** | `roles/<role>/MEMORY.md`, read by instruction | `codex exec resume <thread>` from any process |
| **DeepSeek harness** | `roles/<role>/MEMORY.md`, read by instruction | `dsh headless --session-id <id>` from any process |
| **Anything else** | `roles/<role>/MEMORY.md`, read by instruction | Starts fresh from the role's files |

The role itself lives in files, so a writer can move to another account or vendor and carry on.
`tools/role.py` drives all of these with one command:

```bash
python3 tools/role.py send tutorial-writer --message-file revisions/orchestrator/messages/20260315-T1-part1.md
python3 tools/role.py list
python3 tools/role.py rehydrate tutorial-writer --backend claude --reason "out of quota"
```

[Dedicated agents](skills/orchestrated-research/references/dedicated-agents.md) gives the three ways to run writers, what was tested, and what does not persist.

## What this insists on

- The tutorial and the companion have opposite review standards. Keep them apart.
- Writers are dedicated. Reviewers are disposable. The orchestrator edits no document.
- Requests stay verbatim, and every one is tracked to a status with evidence, checked row by row.
- Every number has a ledger row: real or synthetic, new or compared, with command and checksum.
- A failed test goes to the author at once. The tutorial's constructive tone controls what it talks about, never the evidence.
- A reader's "cut this" is a proposal. It is checked against what the author asked for.
- Delivered, reviewed and accepted are three states. Only the author accepts.

## Limits

- **It costs a lot of model usage.** This is for projects that deserve it, not for a short note. For a one-off essay, use [research-essay](https://github.com/chemaoxfz/idea-to-essay).
- **Long jobs have run only on Codex writer threads.** The `claude` and `dsh` backends of the dispatcher, and native Codex subagents, have passed smoke tests only.
- **Tools for live Codex threads use internal interfaces.** `steer.py`, `watch_threads.py`, `wait_threads.py` and `read_thread.py` read Codex's thread database and control socket. They were tested on `codex-cli` 0.166.0 and can break with an upgrade.
- **The project scaffold is LaTeX only.**
- **A clean check proves little.** `records.py` finds mechanical errors only. Proof and reading stay with people and agents.

## Requirements

Python 3.9 or later, standard library only.
At least one of Claude Code, Codex or the DeepSeek harness for dispatched writers.
A TeX distribution with `latexmk`, and Poppler's `pdfinfo`, `pdffonts` and `pdftoppm` for checking builds. Plots in figures may also need matplotlib.

## License

Private, by invitation. See [NOTICE](NOTICE).
