#!/usr/bin/env python3
"""Scan tracked and untracked repository text for things that must not be shared.

    python3 tools/leak_scan.py

Checks for personal home paths, thread and session IDs, cloud-drive paths, em dashes in prose,
and every term in leak-terms.local.txt (one per line, # for comments, case-insensitive).
That file is ignored by git, so the private terms themselves are never committed.
Exit code 1 means something was found. A clean scan does not prove the text is safe to share.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = {
    "home path": re.compile(r"/Users/[A-Za-z0-9_.-]+|/home/[A-Za-z0-9_.-]+"),
    "cloud drive": re.compile(r"CloudStorage|My Drive|GoogleDrive"),
    "thread or session id": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "api key": re.compile(r"\b(sk-[A-Za-z0-9]{16,}|gho_[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{16,})\b"),
    "em dash": re.compile("—"),
}
ALLOWED = {".claude/handoff.md", "tools/leak_scan.py", "leak-terms.local.txt"}


def files():
    listing = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True)
    return [name for name in listing.stdout.splitlines() if name not in ALLOWED]


def main():
    terms_path = ROOT / "leak-terms.local.txt"
    terms = []
    if terms_path.is_file():
        for line in terms_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                terms.append(line)
    else:
        print("note: no leak-terms.local.txt, so only generic patterns are checked.")
    patterns = dict(PATTERNS)
    for term in terms:
        patterns[f"private term {term!r}"] = re.compile(re.escape(term), re.IGNORECASE)

    hits = 0
    names = files()
    for name in names:
        path = ROOT / name
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for label, pattern in patterns.items():
                if pattern.search(line):
                    print(f"{name}:{number}: {label}: {line.strip()[:110]}")
                    hits += 1
    print(f"{len(names)} files scanned, {len(terms)} private terms, {hits} hits.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
