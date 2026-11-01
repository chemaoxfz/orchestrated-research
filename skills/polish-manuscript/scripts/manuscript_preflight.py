#!/usr/bin/env python3
"""Read-only, baseline-aware inventory of a LaTeX manuscript source.

This does not validate mathematics, prose or layout.

Examples:
    python3 manuscript_preflight.py --target main.tex
    python3 manuscript_preflight.py --target main.tex --baseline before/main.tex
    python3 manuscript_preflight.py --target main.tex --section-label sec:results
    python3 manuscript_preflight.py --target main.tex --annotation-macro authornote \\
        --definition-macro termdef --avoid-term "read-?outs?" > review.md

Only literal TeX commands are inspected. Macros, conditionals and inputs are not
expanded. Findings are items to review, not verdicts. The actual LaTeX build is authoritative.
The script opens files only for reading and prints its report to standard output.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re

DEFAULT_ANNOTATION_MACROS = ("notate", "todo", "fixme")
DEFINITION_ENVIRONMENTS = "definition|defn|dfn"
HEADING_LEVELS = {"part": -1, "chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}
EM_DASH_PATTERN = r"\u2014|(?<!-)---(?!-)"
OPTIONAL_ARGUMENT = re.compile(r"\s*\[[^\]]*\]")


def source_lines(text: str) -> list[str]:
    """Split on newlines only, so line numbers agree with offset lookups."""
    lines = text.split("\n")
    return lines[:-1] if lines and lines[-1] == "" else lines


def mask_comments(source: str) -> str:
    """Preserve character positions and newlines while masking TeX comments."""
    chars = list(source)
    i = 0
    while i < len(source):
        if source[i] == "\\":
            i += 2
            continue
        if source[i] == "%":
            end = source.find("\n", i)
            end = len(source) if end < 0 else end
            chars[i:end] = " " * (end - i)
            i = end
        else:
            i += 1
    text = "".join(chars)
    for match in re.finditer(
        r"\\begin\{(comment|verbatim\*?|lstlisting|minted)\}.*?\\end\{\1\}",
        text,
        re.DOTALL,
    ):
        chars[match.start():match.end()] = [
            "\n" if c == "\n" else " " for c in match.group()
        ]
    return "".join(chars)


def argument(text: str, start: int) -> tuple[str, int] | None:
    """Read one balanced braced argument, including nested/escaped braces."""
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text) or text[start] != "{":
        return None
    depth, i = 1, start + 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None


def required_argument(text: str, start: int) -> tuple[str, int] | None:
    """Read one braced argument after any optional bracketed argument."""
    optional = OPTIONAL_ARGUMENT.match(text, start)
    return argument(text, optional.end() if optional else start)


def commands(text: str, pattern: str):
    for match in re.finditer(r"\\(" + pattern + r")\*?(?![A-Za-z])", text):
        arg = required_argument(text, match.end())
        if arg is not None:
            yield match.start(), match.group(1), arg[0], arg[1]


def one_edit_away(name: str, macro: str) -> bool:
    """Detect one substitution, insertion, deletion or adjacent swap, keeping the first two letters."""
    if name == macro or name[:2] != macro[:2] or abs(len(name) - len(macro)) > 1:
        return False
    if len(name) == len(macro):
        diffs = [i for i, (a, b) in enumerate(zip(name, macro)) if a != b]
        if len(diffs) == 1:
            return True
        return (len(diffs) == 2 and diffs[1] == diffs[0] + 1
                and name[diffs[0]] == macro[diffs[1]] and name[diffs[1]] == macro[diffs[0]])
    short, long = sorted((name, macro), key=len)
    return any(long[:i] + long[i + 1:] == short for i in range(len(long)))


def is_annotation(name: str, macros: tuple[str, ...]) -> bool:
    return name in macros or any(one_edit_away(name, macro) for macro in macros)


def analyze(source: str, annotation_macros: tuple[str, ...],
            definition_macros: tuple[str, ...]) -> dict:
    text = mask_comments(source)
    body = text.find(r"\begin{document}")
    if body >= 0:
        text = "".join("\n" if c == "\n" else " " for c in text[:body]) + text[body:]
    newlines = [i for i, c in enumerate(source) if c == "\n"]

    def line(offset: int) -> int:
        return bisect_right(newlines, offset) + 1

    labels = list(commands(text, "label"))
    refs = [
        {"key": key.strip(), "line": line(pos)}
        for pos, _, keys, _ in commands(text, "ref|eqref|pageref|autoref|nameref|vref|Vref|cref|Cref|labelcref")
        for key in keys.split(",") if key.strip()
    ]
    headings = [
        {"line": line(pos), "level": HEADING_LEVELS[kind], "title": " ".join(title.split())}
        for pos, kind, title, _ in commands(text, "|".join(HEADING_LEVELS))
    ]
    notes = []
    for match in re.finditer(r"\\([A-Za-z]+)\*?", text):
        if is_annotation(match.group(1), annotation_macros):
            arg = required_argument(text, match.end())
            notes.append({"line": line(match.start()), "macro": match.group(1),
                          "text": " ".join(arg[0].split()) if arg else "[unclosed or missing argument]"})
    figures = []
    for match in re.finditer(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", text, re.DOTALL):
        block = match.group()
        figures.append({"line": line(match.start()), "end_line": line(match.end() - 1),
                        "labels": [v for _, _, v, _ in commands(block, "label")],
                        "assets": [v for _, _, v, _ in commands(block, "includegraphics")],
                        "inline": r"\begin{tikzpicture}" in block})
    definitions = []
    for match in re.finditer(
        r"\\begin\{(" + DEFINITION_ENVIRONMENTS + r")\*?\}.*?\\end\{\1\*?\}", text, re.DOTALL
    ):
        bold = next(commands(match.group(), "textbf"), None)
        definitions.append({"line": line(match.start()), "end_line": line(match.end() - 1),
                            "site": match.group(1) + " environment",
                            "term": " ".join(bold[2].split()) if bold else "[no bold term]"})
    if definition_macros:
        for pos, name, term, end in commands(text, "|".join(definition_macros)):
            definitions.append({"line": line(pos), "end_line": line(end - 1), "site": "\\" + name,
                                "term": " ".join(term.split())})
    definitions.sort(key=lambda item: item["line"])
    return {"text": text, "labels": Counter(v for _, _, v, _ in labels),
            "label_lines": {v: line(p) for p, _, v, _ in labels},
            "refs": refs, "headings": headings, "notes": notes,
            "figures": figures, "definitions": definitions}


def scope(data: dict, label: str | None, count: int) -> tuple[int, int]:
    if label is None:
        return 1, count + 1
    if label not in data["label_lines"]:
        raise ValueError(f"Section label not found: {label}")
    pos = data["label_lines"][label]
    previous = [h for h in data["headings"] if h["line"] <= pos]
    if not previous:
        raise ValueError(f"No section heading before label: {label}")
    head = previous[-1]
    end = next((h["line"] for h in data["headings"]
                if h["line"] > pos and h["level"] <= head["level"]), count + 1)
    return head["line"], end


def review(current: str, before: str | None = None, label: str | None = None,
           annotation_macros: tuple[str, ...] = DEFAULT_ANNOTATION_MACROS,
           definition_macros: tuple[str, ...] = (),
           avoid_terms: tuple[str, ...] = ()) -> dict:
    data = analyze(current, annotation_macros, definition_macros)
    old = analyze(before, annotation_macros, definition_macros) if before is not None else None
    lines = source_lines(current)
    first, end = scope(data, label, len(lines))
    changed = set(range(first, end)) if old is None else set()
    if old is not None:
        matcher = SequenceMatcher(None, source_lines(before), lines, autojunk=False)
        for kind, _, _, a, b in matcher.get_opcodes():
            if kind != "equal":
                # A deletion still marks its surviving boundary for review.
                changed.update(range(a + 1, max(a + 2, b + 1)))
    selected = {i for i in changed if first <= i < end}
    old_labels = old["labels"] if old else Counter()
    missing = [r for r in data["refs"] if r["key"] not in data["labels"]]
    previous_missing = {r["key"] for r in old["refs"] if r["key"] not in old_labels} if old else set()
    notes = [n for n in data["notes"] if first <= n["line"] < end]
    old_notes = {(n["macro"], n["text"]) for n in old["notes"]} if old else set()
    current_notes = {(n["macro"], n["text"]) for n in data["notes"]}
    old_scope = (0, 0)
    if old is not None and (label is None or label in old["label_lines"]):
        try:
            old_scope = scope(old, label, len(source_lines(before)))
        except ValueError:
            pass
    for note in notes:
        note["new"] = old is not None and (note["macro"], note["text"]) not in old_notes
    warnings = []
    patterns = {"possible em dash": EM_DASH_PATTERN}
    patterns.update({f"avoid term: {term}": term for term in avoid_terms})
    clean_lines = source_lines(data["text"])
    for number in sorted(selected):
        if number > len(clean_lines):
            continue
        for name, pattern in patterns.items():
            if re.search(pattern, clean_lines[number - 1], re.IGNORECASE):
                warnings.append({"line": number, "check": name,
                                 "text": lines[number - 1].strip()})
    touched = []
    for i, h in enumerate(data["headings"]):
        stop = data["headings"][i + 1]["line"] if i + 1 < len(data["headings"]) else end
        if any(h["line"] <= number < stop for number in selected):
            touched.append(h)
    return {
        "scope_lines": [first, end - 1], "baseline_supplied": old is not None,
        "changed_or_selected_lines": len(selected), "touched_sections": touched,
        "unresolved_notes": notes,
        "annotations_no_longer_present": [n for n in old["notes"]
                                          if old_scope[0] <= n["line"] < old_scope[1]
                                          and (n["macro"], n["text"]) not in current_notes] if old else [],
        "duplicate_labels": [{"key": k, "count": v, "new_or_worse": old is not None and v > old_labels[k]}
                             for k, v in sorted(data["labels"].items()) if v > 1],
        "unresolved_literal_references": [dict(r, new=old is not None and r["key"] not in previous_missing)
                                          for r in missing],
        "added_labels": sorted(data["labels"].keys() - old_labels.keys()) if old else [],
        "removed_labels": sorted(old_labels.keys() - data["labels"].keys()) if old else [],
        "terms_to_review": warnings,
        "definition_sites_to_review": [d for d in data["definitions"]
                                       if any(d["line"] <= i <= d["end_line"] for i in selected)],
        "figure_blocks_to_inspect": [f for f in data["figures"]
                                     if any(f["line"] <= i <= f["end_line"] for i in selected)],
    }


def markdown(result: dict) -> str:
    out = ["# Manuscript source preflight", "",
           "This inventories source changes. It does not certify proofs, narrative, or rendered figures.",
           "Literal TeX commands only. Check findings against macros and the actual build.", "",
           f"Target: `{result['target']}`.",
           f"Source SHA-256: `{result['sha256']}`."]
    if result["baseline"]:
        out.append(f"Baseline: `{result['baseline']}`.")
    out += [f"Selected lines: {result['scope_lines'][0]} to {result['scope_lines'][1]}.",
            "Label and reference checks cover the whole target, including dependents outside the selected section.", ""]
    if not result["baseline_supplied"]:
        out += ["No baseline supplied. Findings describe the current source, not new regressions.", ""]
    for key, title in [
        ("touched_sections", "Changed or selected sections"),
        ("unresolved_notes", "Author annotations to resolve"),
        ("annotations_no_longer_present", "Annotations no longer present (verify substantive resolution)"),
        ("duplicate_labels", "Duplicate literal labels"),
        ("unresolved_literal_references", "Unresolved literal references"),
        ("added_labels", "Added labels"), ("removed_labels", "Removed labels"),
        ("terms_to_review", "Terminology and punctuation to review"),
        ("definition_sites_to_review", "Definition sites to review"),
        ("figure_blocks_to_inspect", "Figure blocks to inspect at manuscript size"),
    ]:
        out += [f"## {title}", ""]
        if not result[key]:
            out += ["None detected.", ""]
            continue
        for value in result[key]:
            out.append("- " + (json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else str(value)))
        out.append("")
    out += ["A separate final reader review must check each logical block's point, necessity, prerequisites,",
            "mathematical scope, domain meaning and continuity. A source scan cannot establish these.", "",
            "Changes confined to external figure scripts or PDFs are not detected here. Inspect those assets separately.", ""]
    return "\n".join(out)


def read_source(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes()
    return raw, raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def macro_name(value: str) -> str:
    name = value.lstrip("\\")
    if not re.fullmatch(r"[A-Za-z]+", name):
        raise argparse.ArgumentTypeError(f"not a macro name: {value}")
    return name


def term_pattern(value: str) -> str:
    try:
        re.compile(value)
    except re.error as exc:
        raise argparse.ArgumentTypeError(f"not a regular expression: {value} ({exc})") from exc
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", type=Path, required=True, help="The TeX source to inventory.")
    parser.add_argument("--baseline", type=Path, help="A before-state copy of the target. Findings then report changes.")
    parser.add_argument("--section-label", help="Select the heading containing this literal label and all its children.")
    parser.add_argument("--annotation-macro", type=macro_name, action="append", default=[],
                        help="Add an author-annotation macro, repeatable. Always checked: "
                             + ", ".join(DEFAULT_ANNOTATION_MACROS) + ". Likely typos are also listed.")
    parser.add_argument("--definition-macro", type=macro_name, action="append", default=[],
                        help="Add a macro that marks a definition site, repeatable. Definition environments are always checked.")
    parser.add_argument("--avoid-term", type=term_pattern, action="append", default=[],
                        help="Add a case-insensitive regular expression for a term to review, repeatable.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()
    try:
        raw, current = read_source(args.target)
        before = read_source(args.baseline)[1] if args.baseline else None
        result = review(current, before, args.section_label,
                        tuple(dict.fromkeys((*DEFAULT_ANNOTATION_MACROS, *args.annotation_macro))),
                        tuple(dict.fromkeys(args.definition_macro)),
                        tuple(dict.fromkeys(args.avoid_term)))
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    result.update(target=str(args.target), sha256=hashlib.sha256(raw).hexdigest(),
                  baseline=str(args.baseline) if args.baseline else None)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else markdown(result), end="\n" if args.json else "")


if __name__ == "__main__":
    main()
