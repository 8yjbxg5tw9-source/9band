#!/usr/bin/env python3
"""English-only character/stopword guard for student-facing text and SVGs.

Scans content/, student/, and assessments/. Code fences and inline code are
NOT exempt: a reader can see them. Only exact, registered IPA transcriptions
(and a small set of phoneme fragments used in pronunciation diagrams) are
exempt from character checks. This is not a general language identifier;
ASCII-only foreign prose still requires inventory/manual review.

Usage: python3 scripts/audit_english_only.py [--strict]
"""
import csv
import html
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [ROOT / name for name in ("content", "student", "assessments")]
EXTENSIONS = {".md", ".csv", ".txt", ".html", ".svg"}
# These three directory-policy documents are internal, not lesson text.
INTERNAL_READMES = {d / "README.md" for d in SCAN_DIRS}
AZERBAIJANI_CHARS = set("əƏğĞıİöÖüÜçÇşŞ")
AZ_STOPWORDS = {
    "və", "bir", "bu", "bunlar", "ki", "ilə", "üçün", "çox", "daha", "ən",
    "mən", "sən", "biz", "siz", "onlar", "mənim", "sənin", "bizim", "sizin",
    "deyil", "var", "yoxdur", "kimi", "sonra", "əvvəl", "bütün", "hər",
    "kitab", "dərs", "dərsdə", "cavab", "cavablar", "sual", "suallar",
    "yaxşı", "pis", "böyük", "kiçik", "yeni", "köhnə", "istəyirəm",
    "olaraq", "edir", "edirlər", "oldu", "olur", "lazımdır", "gərək",
    "haqqında", "arasında", "yanında", "üstündə", "altında", "içində",
    "çünki", "amma", "lakin", "əgər", "yəni", "belə", "elə", "orada",
    "burada", "harada", "nə", "necə", "niyə", "kim", "hansı", "neçə",
    "tərcümə", "izah", "nümunə", "çalışma", "tapşırıq", "imtahan",
    "səhifə", "hissə", "bölmə", "fəsil", "yox", "hə", "bəli", "xeyr",
}
# Typography and mathematical scoring/scheduling symbols, never foreign letters.
ALLOWED_NON_ASCII = set("—–“”‘’'… °×÷±£€§©®™•·→←↑↓⇒★✓✗≥≤")
IPA_SPAN = re.compile(r"/[^/\n]{1,60}/")
WORD = re.compile(r"[A-Za-zÀ-ÿƏəĞğIıİÖöÜüÇçŞş']+")
PLACEHOLDER = re.compile(r"\b(?:TODO|PLACEHOLDER|TBD|FIXME)\b", re.IGNORECASE)


def registered_ipa():
    values = {"/ɡʊd/", "/b/"}  # visible phoneme fragments in the goodbye diagram
    path = ROOT / "VOCABULARY_DATABASE.csv"
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            values.update(r["phonemic_transcription"] for r in csv.DictReader(f)
                          if r.get("phonemic_transcription"))
    return values


APPROVED_IPA = registered_ipa()


def strip_exempt(text):
    """Preserve line numbering; never hide arbitrary slash-delimited prose."""
    text = html.unescape(text)
    return IPA_SPAN.sub(lambda m: " " if m.group() in APPROVED_IPA else m.group(), text)


def audit_file(path, strict=False):
    path = Path(path)
    if path.resolve() in INTERNAL_READMES:
        return []
    text = path.read_text(encoding="utf-8")
    clean = strip_exempt(text)
    violations = []
    for lineno, line in enumerate(clean.splitlines(), start=1):
        for ch in line:
            if ch in AZERBAIJANI_CHARS:
                violations.append((str(path), lineno, f"character violation: {ch!r}"))
                break
        for word in WORD.findall(line.lower()):
            if word in AZ_STOPWORDS:
                violations.append((str(path), lineno, f"stopword violation: {word!r}"))
        for ch in line:
            if ord(ch) > 127 and ch not in ALLOWED_NON_ASCII and ch not in AZERBAIJANI_CHARS:
                violations.append((str(path), lineno, f"unexpected non-ASCII: {ch!r} (U+{ord(ch):04X})"))
                break
        if strict and PLACEHOLDER.search(line):
            violations.append((str(path), lineno, "unfinished placeholder text"))
    return violations


def student_files():
    for directory in SCAN_DIRS:
        if directory.is_dir():
            for path in sorted(directory.rglob("*")):
                if path.suffix.lower() in EXTENSIONS and path.resolve() not in INTERNAL_READMES:
                    yield path


def main():
    strict = "--strict" in sys.argv
    paths = list(student_files())
    violations = [v for path in paths for v in audit_file(path, strict=strict)]
    print(f"English-only audit: scanned {len(paths)} student-facing file(s), including SVG text.")
    if violations:
        print(f"VIOLATIONS FOUND: {len(violations)}")
        for path, lineno, msg in violations[:100]:
            print(f"  {os.path.relpath(path, ROOT)}:{lineno}: {msg}")
        return 1
    print("PASS: no flagged non-English content" + (" or unfinished markers." if strict else "."))
    print("Limit: lexical/character guard, not proof of language or teaching clarity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
