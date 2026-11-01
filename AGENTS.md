# AGENTS.md

This repository is a set of [Agent Skills](https://agentskills.io) for running a long research project as an orchestrator of dedicated agents.

**If your agent supports skills,** install them and invoke `orchestrated-research`. See the README.

**If it does not,** read `skills/orchestrated-research/SKILL.md` and follow it. It names the other files to read as each step needs them. Load them on demand, not all at once.

## If you are editing this repository

Each skill is a folder under `skills/`, with `SKILL.md` at its root and `references/`, `assets/` and `scripts/` beside it.

- The frontmatter `name` must match the folder name. Keep `metadata.version` in every skill and both plugin manifests aligned.
- `SKILL.md` stays under 500 lines. Detail belongs in `references/`.
- Say each thing once, in the file that owns it. `write-tutorial` owns the tutorial's style. `write-companion` owns the companion's standard. `orchestrated-research` owns stages, roles and records. `orchestrate-agents` owns the orchestrator's craft.
- This repository's prose follows `write-tutorial`: short direct sentences, no em dashes, few semicolons, one point per paragraph, one sentence per line.
- **Nothing private goes in.** No unpublished results, project vocabulary, collaborator names, personal paths or thread IDs. Examples use neutral textbook systems. Before committing, run `python3 tools/leak_scan.py`. Put your private terms in `leak-terms.local.txt`, which git ignores. The scan finds literal terms only. A project's method reworded in neutral terms is still a leak, so have a reader who knows the source compare by meaning.
- Keep private notes in `references/*.local.md`, which git also ignores.
- Skills stay vendor-neutral. Vendor mechanics live in `skills/orchestrate-agents/references/mechanics-*.md` and `skills/orchestrated-research/references/dedicated-agents.md`.
- Never state that something was tested unless it was, on the version named.
- After changing a script, run `python3 -m unittest discover -s tests`.
- After changing plugin metadata or a skill's frontmatter, run `claude plugin validate . --strict` if you have the Claude Code CLI.
- `.claude/CLAUDE.md` imports this file. It is not at the root, because the validator warns about a `CLAUDE.md` at a plugin's root.
