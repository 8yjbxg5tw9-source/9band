#!/usr/bin/env python3
"""Validate CSV structure, persistent metadata and authored-lesson dependencies.

Uses only the standard library. All-course structural/reference checks plus
chronological dependency checks for authored lessons. Planned, unauthored
lessons are not claimed to have passed a content dependency audit.
"""
import csv
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_structure import (  # noqa: E402
    LESSON_INDEX_HEADER, authored_lessons, expected_counts,
)

ROOT = Path(__file__).resolve().parents[1]
VOCAB_PATH = ROOT / "VOCABULARY_DATABASE.csv"
GRAMMAR_PATH = ROOT / "GRAMMAR_DATABASE.csv"
LESSON_PATH = ROOT / "LESSON_INDEX.csv"
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
ALLOWED_VOCAB_STATUS = {"planned", "introduced", "practiced", "recalled", "used", "assessed", "mastered"}
ALLOWED_GRAMMAR_STATUS = {"planned", "introduced", "practiced", "assessed", "mastered"}
ALLOWED_LESSON_STATUS = {"planned", "drafted", "reviewed", "validated", "tested"}
ALLOWED_ASSESSMENT_STATUS = {"planned", "assessed", "mastered"}


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def ids(value):
    return [part.strip() for part in (value or "").split("|") if part.strip()]


def table_shape(name, header, rows, wanted, id_field, errors):
    if header != wanted:
        errors.append(f"{name}: header mismatch.")
    values = [r.get(id_field, "") for r in rows]
    if len(values) != len(set(values)):
        errors.append(f"{name}: duplicate {id_field}.")
    for i, row in enumerate(rows, 2):
        if None in row or any(v is None for v in row.values()):
            errors.append(f"{name}:{i}: CSV field count mismatch.")


def check_cycles(grammar):
    """Return cycles rather than silently accepting circular prerequisites."""
    graph = {r["grammar_id"]: ids(r["prerequisites"]) for r in grammar}
    active, finished, found = set(), set(), []

    def visit(node, path):
        if node in active:
            found.append(" -> ".join(path + [node]))
            return
        if node in finished or node not in graph:
            return
        active.add(node)
        for parent in graph[node]:
            visit(parent, path + [node])
        active.remove(node)
        finished.add(node)

    for node in graph:
        visit(node, [])
    return found


def validate():
    errors = []
    lfield, lessons = load(LESSON_PATH)
    gfield, grammar = load(GRAMMAR_PATH)
    vfield, vocab = load(VOCAB_PATH)
    table_shape("LESSON_INDEX.csv", lfield, lessons, LESSON_INDEX_HEADER, "lesson_id", errors)
    table_shape("GRAMMAR_DATABASE.csv", gfield, grammar, GRAMMAR_HEADER, "grammar_id", errors)
    table_shape("VOCABULARY_DATABASE.csv", vfield, vocab, VOCAB_HEADER, "vocab_id", errors)
    if errors:
        return errors, lessons, grammar, vocab
    expected = authored_lessons()
    if len(lessons) != len(expected):
        errors.append(f"LESSON_INDEX.csv: {len(lessons)} rows; expected {len(expected)}.")
    else:
        for got, want in zip(lessons, expected):
            for key in LESSON_INDEX_HEADER:
                if str(got[key]) != str(want[key]):
                    errors.append(f"{want['lesson_id']}: generated {key} differs; regenerate, do not hand-edit.")
    lesson_map = {r["lesson_id"]: r for r in lessons}
    grammar_map = {r["grammar_id"]: r for r in grammar}
    vocab_map = {r["vocab_id"]: r for r in vocab}
    for row in lessons:
        lid = row["lesson_id"]
        if row["validation_status"] not in ALLOWED_LESSON_STATUS:
            errors.append(f"{lid}: invalid lesson status.")
        if row["level"] not in ALLOWED_LEVELS:
            errors.append(f"{lid}: invalid level.")
        if row["validation_status"] != "planned" and not (ROOT / row["file_path"]).is_file():
            errors.append(f"{lid}: authored file missing: {row['file_path']}.")
        for column, bank, id_column in [("new_vocab_ids", vocab_map, "vocab_id"),
                                        ("new_grammar_ids", grammar_map, "grammar_id")]:
            values = ids(row[column])
            if len(values) != len(set(values)):
                errors.append(f"{lid}: duplicate IDs in {column}.")
            for value in values:
                if value not in bank:
                    errors.append(f"{lid}: unknown {id_column} {value}.")
                elif bank[value]["intro_lesson_id"] != lid:
                    errors.append(f"{lid}: {value} introduction does not point back to this lesson.")
                elif row["validation_status"] != "planned" and bank[value]["status"] == "planned":
                    errors.append(f"{lid}: {value} is still planned despite authored introduction.")
    for name, rows, key, statuses in [
        ("grammar", grammar, "grammar_id", ALLOWED_GRAMMAR_STATUS),
        ("vocab", vocab, "vocab_id", ALLOWED_VOCAB_STATUS),
    ]:
        for row in rows:
            item = row[key]
            if row["level"] not in ALLOWED_LEVELS or row["status"] not in statuses:
                errors.append(f"{item}: invalid level/status.")
            if not re.fullmatch(r"G\d{3}" if name == "grammar" else r"V\d{4}", item):
                errors.append(f"{item}: malformed ID.")
            intro = row["intro_lesson_id"]
            if intro and intro not in lesson_map:
                errors.append(f"{item}: unknown intro lesson {intro}.")
            if intro in lesson_map and lesson_map[intro]["validation_status"] != "planned":
                column = "new_grammar_ids" if name == "grammar" else "new_vocab_ids"
                if item not in ids(lesson_map[intro][column]):
                    errors.append(f"{item}: authored introduction missing from {column}.")
            if row["status"] != "planned" and (intro not in lesson_map or lesson_map[intro]["validation_status"] == "planned"):
                errors.append(f"{item}: introduced without an authored lesson.")
            if name == "vocab":
                if not row["headword"].strip() or not row["meaning_simple_english"].strip():
                    errors.append(f"{item}: empty headword/meaning.")
                if row["status"] in {"recalled", "used", "assessed", "mastered"} and not row["review_history"]:
                    errors.append(f"{item}: claimed achievement without retrieval history.")
                if row["status"] == "mastered" and not row["mastery_evidence"]:
                    errors.append(f"{item}: mastery without evidence.")
                audio = row["audio_status"]
                if audio != "script-only":
                    match = re.fullmatch(r"verified:(.+):([0-9]+(?:\.[0-9]+)?)", audio)
                    if not match or not (ROOT / match[1]).is_file() or float(match[2]) <= 0:
                        errors.append(f"{item}: invalid verified audio claim.")
            else:
                if row["assessment_status"] not in ALLOWED_ASSESSMENT_STATUS:
                    errors.append(f"{item}: invalid assessment status.")
                for pre in ids(row["prerequisites"]):
                    if pre == item or pre not in grammar_map:
                        errors.append(f"{item}: invalid prerequisite {pre}.")
                    elif intro in lesson_map and lesson_map[intro]["validation_status"] != "planned":
                        pre_intro = grammar_map[pre]["intro_lesson_id"]
                        if pre_intro not in lesson_map or int(lesson_map[pre_intro]["global_seq"]) > int(lesson_map[intro]["global_seq"]):
                            errors.append(f"{item}: prerequisite {pre} is introduced later than this authored lesson.")
                for column in ["practice_lessons", "review_lessons"]:
                    for lesson_id in ids(row[column]):
                        if lesson_id not in lesson_map:
                            errors.append(f"{item}: invalid {column} reference {lesson_id}.")
    errors.extend(f"Grammar prerequisite cycle: {cycle}" for cycle in check_cycles(grammar))
    return errors, lessons, grammar, vocab


def main():
    try:
        errors, lessons, grammar, vocab = validate()
    except (OSError, ValueError, KeyError) as exc:
        print(f"VALIDATION FAILED: {exc}")
        return 1
    print(f"Lessons: {len(lessons)} (expected {expected_counts()['TOTAL']})")
    print(f"Grammar topics: {len(grammar)} | Vocabulary entries: {len(vocab)}")
    if errors:
        print(f"VALIDATION FAILED with {len(errors)} error(s):")
        for error in errors[:100]:
            print(f"  - {error}")
        return 1
    print("PASS: CSV shape, IDs, generated metadata, authored files and dependencies are consistent.")
    print("Chronology/content scope: authored lessons only; no learner mastery inferred.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
