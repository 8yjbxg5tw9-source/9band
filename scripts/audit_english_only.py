#!/usr/bin/env python3
"""English-only audit for student-facing content.

Scans student-facing source directories (content/, student/) and fails if any
non-English material is detected. This enforces the project's non-negotiable
rule: no Azerbaijani (or any other non-English language) in student materials.

Detection strategy:
  1. Azerbaijani-specific characters (excluding IPA transcriptions in /.../).
  2. A stopword list of common Azerbaijani words (word-boundary match).
  3. Unexpected non-ASCII characters outside an explicit allowlist.

IPA transcriptions such as /h@'l@U/ are stripped before the character check
because IPA legitimately uses characters like @ that also occur in Azerbaijani.

Usage:
    python3 scripts/audit_english_only.py
    python3 scripts/audit_english_only.py --strict   # also fail on TODO/placeholder text
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = [os.path.join(ROOT, "content"), os.path.join(ROOT, "student")]

# Azerbaijani-specific letters. Plain ASCII 'I' is intentionally NOT included.
AZERBAIJANI_CHARS = set("əƏğĞıİöÖüÜçÇşŞ")

# Common Azerbaijani words. If any of these appears as a whole word in
# student-facing text, it is almost certainly a language violation.
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

# Non-ASCII characters permitted in student text (typography only).
ALLOWED_NON_ASCII = set("—–“”‘’'… °×÷±£€§©®™•→←↑↓⇒★✓✗")

IPA_SPAN = re.compile(r"/[^/\n]{1,60}/")
CODE_SPAN = re.compile(r"`[^`\n]+`")
CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)
WORD = re.compile(r"[A-Za-zÀ-ÿƏəĞğIıİÖöÜüÇçŞş']+")


def strip_exempt(text):
    text = CODE_BLOCK.sub(" ", text)
    text = CODE_SPAN.sub(" ", text)
    text = IPA_SPAN.sub(" ", text)
    return text


def audit_file(path):
    violations = []
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    if "README" in os.path.basename(path).upper():
        return violations  # directory READMEs are internal, not student-facing
    clean = strip_exempt(text)
    for lineno, line in enumerate(clean.splitlines(), start=1):
        for ch in line:
            if ch in AZERBAIJANI_CHARS:
                violations.append((path, lineno, f"character violation: {ch!r}"))
                break
        for word in WORD.findall(line.lower()):
            if word in AZ_STOPWORDS:
                violations.append((path, lineno, f"stopword violation: {word!r}"))
        for ch in line:
            if ord(ch) > 127 and ch not in ALLOWED_NON_ASCII and ch not in AZERBAIJANI_CHARS:
                violations.append((path, lineno, f"unexpected non-ASCII: {ch!r} (U+{ord(ch):04X})"))
                break
    return violations


def main():
    strict = "--strict" in sys.argv
    scanned = 0
    violations = []
    for d in SCAN_DIRS:
        if not os.path.isdir(d):
            continue
        for dirpath, _dirnames, filenames in os.walk(d):
            for name in filenames:
                if not name.endswith((".md", ".csv", ".txt", ".html")):
                    continue
                scanned += 1
                violations.extend(audit_file(os.path.join(dirpath, name)))
                if strict:
                    with open(os.path.join(dirpath, name), encoding="utf-8", errors="replace") as f:
                        text = f.read()
                    for lineno, line in enumerate(text.splitlines(), start=1):
                        if "TODO" in line or "PLACEHOLDER" in line:
                            violations.append((os.path.join(dirpath, name), lineno, "placeholder text"))
    print(f"English-only audit: scanned {scanned} student-facing file(s).")
    if violations:
        print(f"VIOLATIONS FOUND: {len(violations)}")
        for path, lineno, msg in violations[:100]:
            print(f"  {os.path.relpath(path, ROOT)}:{lineno}: {msg}")
        return 1
    print("PASS: no non-English content detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
