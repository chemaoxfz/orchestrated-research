#!/usr/bin/env bash
#
# Install the orchestrated-research skills for whichever agents are on this machine.
#
#   ./install.sh              symlink into ~/.agents/skills and ~/.claude/skills
#   ./install.sh --all        also into ~/.cursor, ~/.gemini, ~/.codex, ~/.copilot
#   ./install.sh --copy       copy instead of symlink (for a checkout you will delete)
#   ./install.sh --project .  install into one project's .agents/skills and .claude/skills
#   ./install.sh --uninstall  remove what this script installed, from every location above
#
# Symlinks are the default, so `git pull` updates the skills everywhere at once.
# Nothing is replaced unless this script installed it. A skill of the same name that
# you already have is left alone, and the script tells you so.
#
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
MODE=link
SCOPE=user
ALL=0
PROJECT_DIR=""
MARKER=".installed-by-orchestrated-research"

while [ $# -gt 0 ]; do
  case "$1" in
    --all)       ALL=1 ;;
    --copy)      MODE=copy ;;
    --uninstall) MODE=uninstall ;;
    --project)   [ $# -ge 2 ] || { echo "--project needs a folder, such as --project ." >&2; exit 2; }
                 SCOPE=project; PROJECT_DIR="$2"; shift ;;
    -h|--help)   sed -n '3,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)           echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

# ~/.agents/skills is the vendor-neutral location that Codex and several other tools read.
# Claude Code reads ~/.claude/skills.
if [ "$SCOPE" = project ]; then
  TARGETS=("$PROJECT_DIR/.agents/skills" "$PROJECT_DIR/.claude/skills")
else
  TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")
  if [ "$ALL" = 1 ] || [ "$MODE" = uninstall ]; then
    TARGETS+=("$HOME/.cursor/skills" "$HOME/.gemini/skills" "$HOME/.codex/skills" "$HOME/.copilot/skills")
  fi
fi

# True when $1 is a copy made by this script, or a link pointing into this checkout.
ours() {
  if [ ! -L "$1" ] && [ -f "$1/$MARKER" ]; then return 0; fi
  [ -L "$1" ] || return 1
  local target
  target="$(cd "$(dirname "$1")" && cd "$(dirname "$(readlink "$1")")" 2>/dev/null && pwd -P)" || return 1
  case "$target" in
    "$REPO"/*) return 0 ;;
    *) return 1 ;;
  esac
}

done_count=0
skipped=0
for skill_path in "$REPO"/skills/*/; do
  name="$(basename "$skill_path")"
  [ -f "$skill_path/SKILL.md" ] || continue
  for dir in "${TARGETS[@]}"; do
    dest="$dir/$name"
    if [ "$MODE" = uninstall ]; then
      if ours "$dest"; then
        if [ -L "$dest" ]; then rm "$dest"; else rm -rf "$dest"; fi
        echo "removed   $dest"; done_count=$((done_count+1))
      elif [ -e "$dest" ] || [ -L "$dest" ]; then
        echo "left alone (not ours)  $dest"
      fi
      continue
    fi
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      if ! ours "$dest"; then
        echo "SKIPPED, you already have this skill  $dest" >&2
        skipped=$((skipped+1))
        continue
      fi
      if [ -L "$dest" ]; then rm "$dest"; else rm -rf "$dest"; fi
    fi
    mkdir -p "$dir"
    if [ "$MODE" = copy ]; then
      cp -R "${skill_path%/}" "$dest"; touch "$dest/$MARKER"; echo "copied    $dest"
    else
      ln -s "${skill_path%/}" "$dest"; echo "linked    $dest"
    fi
    done_count=$((done_count+1))
  done
done

echo
if [ "$MODE" = uninstall ]; then
  echo "$done_count removed."
  exit 0
fi
echo "$done_count installed, $skipped skipped."
if [ "$skipped" -gt 0 ]; then
  echo "A skipped skill keeps your existing version. Compare and merge it yourself, or remove it and run this again."
fi
echo "Restart your agent so it loads the skills, then ask it to use orchestrated-research."
