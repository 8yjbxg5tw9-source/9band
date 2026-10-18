#!/usr/bin/env python3
"""Validate the project databases for internal consistency.

Checks:
  - LESSON_INDEX.csv, VOCABULARY_DATABASE.csv, GRAMMAR_DATABASE.csv exist
    with exact expected headers.
  - IDs are unique within each database.
  - Lesson counts match scripts/course_structure.py (single source of truth).
  - Grammar prerequisites reference existing grammar IDs (no self-reference).
  - intro_lesson_id values reference real lesson IDs from LESSON_INDEX.csv.
  - Status / validation_status values are from the allowed vocabularies.
  - Levels are from the allowed level set.

Usage:
    python3 scripts/validate_databases.py
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_structure import LESSON_INDEX_HEADER, expected_counts, iter_lessons  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_PATH = os.path.join(ROOT, "VOCABULARY_DATABASE.csv")
GRAMMAR_PATH = os.path.join(ROOT, "GRAMMAR_DATABASE.csv")
LESSON_PATH = os.path.join(ROOT, "LESSON_INDEX.csv")

VOCAB_HEADER = [
    "vocab_id", "headword", "part_of_speech", "phonemic_transcription",
    "audio_status", "sense_number", "meaning_simple_english", "level",
    "intro_lesson_id", "example_1", "example_2", "collocations",
    "grammar_patterns", "synonyms", "antonyms", "word_family",
    "register_notes", "common_mistakes", "status", "review_history",
    "mastery_evidence", "notes",
]

GRAMMAR_HEADER = [
    "grammar_id", "topic", "sub_structure", "level", "intro_lesson_id",
    "prerequisites", "communicative_purpose", "affirmative_example",
    "negative_example", "interrogative_example", "common_errors",
    "confused_with", "practice_lessons", "review_lessons",
    "assessment_status", "status", "notes",
]

ALLOWED_LEVELS = {"A0", "A1", "A2", "B1", "B2", "C1", "IE"}
ALLOWED_VOCAB_STATUS = {
    "planned", "introduced", "practiced", "recalled", "used", "assessed", "mastered",
}
ALLOWED_GRAMMAR_STATUS = {
    "planned", "introduced", "practiced", "assessed", "mastered",
}
ALLOWED_LESSON_STATUS = {"planned", "drafted", "reviewed", "validated", "tested"}


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [], []
        return reader.fieldnames, list(reader)


def main():
    errors = []

    # --- LESSON_INDEX.csv ---
    lfield, lessons = load(LESSON_PATH)
    if lfield != LESSON_INDEX_HEADER:
        errors.append(f"LESSON_INDEX.csv header mismatch:\n  got: {lfield}")
    lesson_ids = [r.get("lesson_id", "") for r in lessons]
    if len(lesson_ids) != len(set(lesson_ids)):
        errors.append("LESSON_INDEX.csv contains duplicate lesson_ids.")
    expected = list(iter_lessons())
    if len(lessons) != len(expected):
        errors.append(
            f"LESSON_INDEX.csv has {len(lessons)} rows, structure defines {len(expected)}."
        )
    else:
        for got, want in zip(lessons, expected):
            if got["lesson_id"] != want["lesson_id"] or got["title"] != want["title"]:
                errors.append(
                    f"LESSON_INDEX.csv diverges from course_structure.py at "
                    f"{want['lesson_id']} (got {got['lesson_id']})."
                )
                break
    for r in lessons:
        if r.get("validation_status") not in ALLOWED_LESSON_STATUS:
            errors.append(f"{r.get('lesson_id')}: bad validation_status {r.get('validation_status')!r}.")
        if r.get("level") not in ALLOWED_LEVELS:
            errors.append(f"{r.get('lesson_id')}: bad level {r.get('level')!r}.")
    lesson_id_set = set(lesson_ids)

    # --- GRAMMAR_DATABASE.csv ---
    gfield, grammar = load(GRAMMAR_PATH)
    if gfield != GRAMMAR_HEADER:
        errors.append(f"GRAMMAR_DATABASE.csv header mismatch:\n  got: {gfield}")
    grammar_ids = [r.get("grammar_id", "") for r in grammar]
    if len(grammar_ids) != len(set(grammar_ids)):
        errors.append("GRAMMAR_DATABASE.csv contains duplicate grammar_ids.")
    grammar_id_set = set(grammar_ids)
    for r in grammar:
        gid = r.get("grammar_id", "?")
        if r.get("level") not in ALLOWED_LEVELS:
            errors.append(f"{gid}: bad level {r.get('level')!r}.")
        if r.get("status") not in ALLOWED_GRAMMAR_STATUS:
            errors.append(f"{gid}: bad status {r.get('status')!r}.")
        intro = (r.get("intro_lesson_id") or "").strip()
        if intro and intro not in lesson_id_set:
            errors.append(f"{gid}: intro_lesson_id {intro!r} is not a real lesson.")
        for pre in (r.get("prerequisites") or "").split("|"):
            pre = pre.strip()
            if not pre:
                continue
            if pre == gid:
                errors.append(f"{gid}: lists itself as a prerequisite.")
            elif pre not in grammar_id_set:
                errors.append(f"{gid}: prerequisite {pre!r} does not exist.")

    # --- VOCABULARY_DATABASE.csv ---
    vfield, vocab = load(VOCAB_PATH)
    if vfield != VOCAB_HEADER:
        errors.append(f"VOCABULARY_DATABASE.csv header mismatch:\n  got: {vfield}")
    vocab_ids = [r.get("vocab_id", "") for r in vocab]
    if len(vocab_ids) != len(set(vocab_ids)):
        errors.append("VOCABULARY_DATABASE.csv contains duplicate vocab_ids.")
    for r in vocab:
        vid = r.get("vocab_id", "?")
        if not (r.get("headword") or "").strip():
            errors.append(f"{vid}: empty headword.")
        if r.get("level") not in ALLOWED_LEVELS:
            errors.append(f"{vid}: bad level {r.get('level')!r}.")
        if r.get("status") not in ALLOWED_VOCAB_STATUS:
            errors.append(f"{vid}: bad status {r.get('status')!r}.")
        intro = (r.get("intro_lesson_id") or "").strip()
        if intro and intro not in lesson_id_set:
            errors.append(f"{vid}: intro_lesson_id {intro!r} is not a real lesson.")
        if not (r.get("meaning_simple_english") or "").strip():
            errors.append(f"{vid}: empty English meaning.")

    counts = expected_counts()
    print(f"Lessons: {len(lessons)} (expected {counts['TOTAL']})")
    print(f"Grammar topics: {len(grammar)} | Vocabulary entries: {len(vocab)}")
    if errors:
        print(f"VALIDATION FAILED with {len(errors)} error(s):")
        for e in errors[:60]:
            print(f"  - {e}")
        return 1
    print("PASS: all databases are internally consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
