#!/usr/bin/env python3
"""Check and preserve the project's records. Read-only except for `snapshot`.

    records.py snapshot LABEL FILE...
        Copy files to revisions/snapshots/LABEL with SHA256SUMS. Subfolders of the project are kept.
    records.py ledger  [--ledger F] [--log F]
        Every AUTHOR-LEDGER row has a valid status, a DONE row names its evidence,
        and every quote is an exact substring of the prompt log (whitespace normalized).
    records.py results [--ledger F] [SOURCE...]
        Every `% result: ID` comment in the sources has a row in RESULTS-LEDGER, with no empty cell.
    records.py anchors [--tutorial F] [--companion F] [--design F]
        Every anchor named in the claim table of TECHNICAL-DESIGN, and every \\techref{key} in the tutorial,
        has a \\techanchor{key} in the companion. TeX comments do not count.

`results` and `anchors` default to the one *-tutorial and one *-technical source in this folder.

Exit code 1 means a check failed. Standard library only.
"""
import argparse
import hashlib
import re
import shutil
import sys
from pathlib import Path

STATUSES = ("OPEN", "PARTIAL", "DONE", "PROCESS", "SUPERSEDED", "WAITING")


def normalize(text):
    return re.sub(r"\s+", " ", text.replace("’", "'").replace("“", '"').replace("”", '"')).strip()


def split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [cell.strip() for cell in cells]


def markdown_tables(text):
    """Yield (header cells, [row cells]) for each Markdown table in the text."""
    lines = text.splitlines()
    index = 0
    while index < len(lines) - 1:
        if lines[index].lstrip().startswith("|") and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[index + 1]):
            header = split_row(lines[index])
            index += 2
            rows = []
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                rows.append(split_row(lines[index]))
                index += 1
            yield header, rows
        else:
            index += 1


def column(header, *names):
    lowered = [cell.lower() for cell in header]
    for name in names:
        for position, cell in enumerate(lowered):
            if name in cell:
                return position
    return None


def find_source(kind):
    """The one <slug>-<kind>.tex in this folder, or None if there is not exactly one."""
    found = sorted(Path(".").glob(f"*-{kind}.tex"))
    return found[0] if len(found) == 1 else None


def strip_tex_comments(text):
    return re.sub(r"(?<!\\)%.*", "", text)


def cmd_snapshot(args):
    root = Path(args.root).resolve()
    target = root / "revisions" / "snapshots" / args.label
    if target.exists():
        print(f"{target} already exists. A snapshot is never overwritten. Choose a new label.", file=sys.stderr)
        return 1
    copies = {}
    for name in args.files:
        source = Path(name)
        if not source.is_file():
            print(f"not a file: {source}", file=sys.stderr)
            return 1
        resolved = source.resolve()
        relative = resolved.relative_to(root) if root in resolved.parents else Path(resolved.name)
        if relative in copies:
            print(f"two files would share the name {relative} in this snapshot. Nothing was copied.", file=sys.stderr)
            return 1
        copies[relative] = source
    target.mkdir(parents=True)
    lines = []
    for relative, source in copies.items():
        (target / relative).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target / relative)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        lines.append(f"{digest}  {relative.as_posix()}")
        print(f"{digest[:12]}  {source}")
    (target / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"snapshot: {target}")
    return 0


def cmd_ledger(args):
    ledger_path, log_path = Path(args.ledger), Path(args.log)
    if not ledger_path.is_file() or not log_path.is_file():
        print(f"need both {ledger_path} and {log_path}", file=sys.stderr)
        return 1
    log = normalize(log_path.read_text(encoding="utf-8"))
    problems, counts, total, tables = [], {}, 0, 0
    for header, rows in markdown_tables(ledger_path.read_text(encoding="utf-8")):
        id_col, words_col, status_col = column(header, "id"), column(header, "words", "quote"), column(header, "status")
        if None in (id_col, words_col, status_col):
            continue
        tables += 1
        for row in rows:
            if len(row) != len(header):
                problems.append(f"{row[0] if row else '?'}: expected {len(header)} cells, found {len(row)}. Escape a literal pipe as \\|")
                continue
            total += 1
            row_id, quote, status = row[id_col], row[words_col].strip().strip('"').strip("“”"), row[status_col]
            match = re.match(r"([A-Z]+)\b", status)
            word = match.group(1) if match else ""
            counts[word or "BLANK"] = counts.get(word or "BLANK", 0) + 1
            if word not in STATUSES:
                problems.append(f"{row_id}: status must start with one of {', '.join(STATUSES)}, found {status!r}")
            elif word in ("DONE", "PARTIAL", "WAITING", "SUPERSEDED"):
                detail = status[len(word):].strip(" :()-")
                if len(detail) < 8 and not re.search(r"\d", detail):
                    problems.append(f"{row_id}: {word} needs evidence, a named wait or a successor row in the status cell")
            if not quote:
                problems.append(f"{row_id}: the quote is empty")
            elif normalize(quote.replace("\\|", "|")) not in log:
                problems.append(f"{row_id}: quote is not an exact substring of {log_path.name}: {quote[:80]!r}")
    if not tables:
        problems.append("no ledger table found. Expected a table with ID, words or quote, and status columns.")
    print(f"{total} rows: " + ", ".join(f"{key} {value}" for key, value in sorted(counts.items())))
    for problem in problems:
        print(f"  FAIL {problem}")
    return 1 if problems else 0


def cmd_results(args):
    ledger_path = Path(args.ledger)
    if not ledger_path.is_file():
        print(f"missing {ledger_path}", file=sys.stderr)
        return 1
    sources = args.sources or [path for path in (find_source("tutorial"), find_source("technical")) if path]
    if not sources:
        print("name the sources to check. No single *-tutorial or *-technical source was found here.", file=sys.stderr)
        return 1
    known, problems = {}, []
    for header, rows in markdown_tables(ledger_path.read_text(encoding="utf-8")):
        id_col = column(header, "result", "id")
        if id_col is None:
            continue
        for row in rows:
            if len(row) != len(header):
                problems.append(f"{row[0] if row else '?'}: expected {len(header)} cells, found {len(row)}")
                continue
            known[row[id_col]] = row
            if any(not cell for cell in row):
                problems.append(f"{row[id_col]}: a ledger row has an empty cell")
    cited = {}
    for name in sources:
        text = Path(name).read_text(encoding="utf-8")
        for match in re.finditer(r"%\s*result:\s*([\w.,\- ]+)", text):
            # IDs are comma-separated. Words after an ID, such as "R4 median across seeds", are a note.
            for part in match.group(1).split(","):
                words = part.split()
                if words:
                    cited.setdefault(words[0], name)
    for result, name in sorted(cited.items()):
        if result not in known:
            problems.append(f"{name} cites {result}, which has no row in {ledger_path.name}")
    print(f"{len(known)} ledger rows, {len(cited)} cited in sources.")
    for problem in problems:
        print(f"  FAIL {problem}")
    return 1 if problems else 0


def cmd_anchors(args):
    tutorial_path = args.tutorial or find_source("tutorial")
    companion_path = args.companion or find_source("technical")
    if not tutorial_path or not companion_path:
        print("name the documents with --tutorial and --companion. No single pair was found here.", file=sys.stderr)
        return 1
    tutorial = strip_tex_comments(Path(tutorial_path).read_text(encoding="utf-8"))
    companion = strip_tex_comments(Path(companion_path).read_text(encoding="utf-8"))
    used = set(re.findall(r"\\techref(?:\[[^\]]*\])?\{([^}]+)\}", tutorial))
    defined = set(re.findall(r"\\techanchor\{([^}]+)\}", companion))
    named = set()
    design = Path(args.design)
    if design.is_file():
        for header, rows in markdown_tables(design.read_text(encoding="utf-8")):
            position = column(header, "anchor")
            if position is None:
                continue
            for row in rows:
                cell = row[position].strip("` ") if len(row) == len(header) else ""
                if cell and cell.lower() not in ("none", "n/a", "-"):
                    named.add(cell)
    missing = sorted((used | named) - defined)
    print(f"{len(named)} anchors named in {design.name}, {len(used)} links in the tutorial, {len(defined)} anchors in the companion, {len(missing)} missing.")
    print("A script only checks that each destination exists. A reader still checks that it delivers what the tutorial claims.")
    for key in missing:
        print(f"  FAIL no anchor for {key}")
    return 1 if missing else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("label")
    snapshot.add_argument("files", nargs="+")
    snapshot.add_argument("--root", default=".")
    snapshot.set_defaults(func=cmd_snapshot)
    ledger = sub.add_parser("ledger")
    ledger.add_argument("--ledger", default="AUTHOR-LEDGER.md")
    ledger.add_argument("--log", default="PROMPT-LOG.md")
    ledger.set_defaults(func=cmd_ledger)
    results = sub.add_parser("results")
    results.add_argument("--ledger", default="RESULTS-LEDGER.md")
    results.add_argument("sources", nargs="*")
    results.set_defaults(func=cmd_results)
    anchors = sub.add_parser("anchors")
    anchors.add_argument("--tutorial")
    anchors.add_argument("--companion")
    anchors.add_argument("--design", default="TECHNICAL-DESIGN.md")
    anchors.set_defaults(func=cmd_anchors)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
