#!/usr/bin/env python3
"""Canonical course structure for the 9band Zero-to-C1 + IELTS system.

This file is the SINGLE SOURCE OF TRUTH for levels, modules, units, lessons,
lesson IDs, and lesson-type rotation. Authoring metadata is persistently
overlaid from data/lesson_metadata.json (no structural overrides). All other records (CURRICULUM_MAP.md,
LESSON_INDEX.csv, ASSESSMENT_REGISTER.md) must be consistent with it.

Usage:
    python3 scripts/course_structure.py      # regenerates LESSON_INDEX.csv + docs/STRUCTURE_TABLES.md

Rules enforced here:
  - Lesson ID format: {LEVEL}-M{m}-U{u}-L{nn}  (e.g. A1-M4-U8-L02)
  - Unit numbers are sequential within a level (not within a module).
  - Every unit ends with a review/checkpoint lesson linked to a unit test.
  - global_seq is a single linear order 1..N across the whole course.
"""

import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSON_INDEX_PATH = os.path.join(ROOT, "LESSON_INDEX.csv")
TABLES_PATH = os.path.join(ROOT, "docs", "STRUCTURE_TABLES.md")
METADATA_PATH = os.path.join(ROOT, "data", "lesson_metadata.json")
# Structure remains canonical here; only these authoring fields may be overlaid.
AUTHORING_FIELDS = {
    "objectives", "new_vocab_ids", "new_grammar_ids", "skills_focus",
    "assessment_id", "validation_status", "notes",
}

# ---------------------------------------------------------------------------
# Lesson-type rotations
# ---------------------------------------------------------------------------
# Each entry: (lesson_type, title_focus, short_objective, skills_focus)
ROTATION_A0 = [
    ("vocabulary", "First Words and Sounds",
     "Recognize, say, and understand the unit's core words through pictures, actions, and repetition.",
     "V|L"),
    ("grammar", "Grammar Foundations",
     "Notice and use the target pattern in short, supported sentences.",
     "G|S"),
    ("listening_speaking", "Listening and Speaking",
     "Understand and say short phrases; respond to simple prompts.",
     "L|S"),
    ("reading_vocabulary", "Reading and Vocabulary",
     "Read short supported texts and find/recognize known words.",
     "R|V"),
    ("writing_pronunciation", "Writing and Pronunciation",
     "Copy and write known words/short sentences; say sounds clearly.",
     "W|P"),
    ("review", "Review and Unit Test",
     "Recall the unit's language; complete the unit test.",
     "ALL"),
]

ROTATION_STD = [
    ("vocabulary", "Vocabulary in Context",
     "Learn the unit's core words and use them in real contexts.",
     "V"),
    ("grammar", "Grammar Focus",
     "Understand the target structure and use it accurately.",
     "G"),
    ("listening", "Listening and Pronunciation",
     "Understand the target listening text types; practise key sounds and stress.",
     "L|P"),
    ("speaking", "Speaking",
     "Speak on the unit topic with growing fluency and accuracy.",
     "S"),
    ("reading", "Reading",
     "Read the unit text type; find main ideas and details.",
     "R"),
    ("writing", "Writing",
     "Write the unit text type with clear organization.",
     "W"),
    ("review", "Review and Unit Test",
     "Recall and combine the unit's language; complete the unit test.",
     "ALL"),
]

ROTATION_IELTS = [
    ("strategy", "Strategy and Skills",
     "Learn how the task works and practise the core exam skill.",
     "VAR"),
    ("guided", "Guided Practice",
     "Complete guided exam tasks with step-by-step support.",
     "VAR"),
    ("timed", "Timed Practice and Feedback",
     "Complete exam tasks under time limits; review errors.",
     "VAR"),
    ("checkpoint", "Review and Checkpoint",
     "Consolidate the unit; complete the checkpoint test.",
     "ALL"),
]

# Full-test units (diagnostic + mocks) use section-based lessons instead.
FULL_TEST_FOCUS = [
    ("listening_test", "Full Listening Section",
     "Complete a full Listening section under exam conditions.", "L"),
    ("reading_test", "Full Reading Section",
     "Complete a full Reading section under exam conditions.", "R"),
    ("writing_test", "Full Writing Section",
     "Complete full Writing tasks under exam conditions.", "W"),
    ("speaking_test", "Full Speaking Section and Review",
     "Complete a full Speaking test; review performance.", "S"),
]
FULL_TEST_UNITS = {2, 16, 17}  # within the IE level

# ---------------------------------------------------------------------------
# Levels / modules / units
# ---------------------------------------------------------------------------
# units: list of {"num": <level-sequential>, "theme": ...}
LEVELS = [
    {
        "code": "A0", "name": "Starter (Pre-A1)", "rotation": ROTATION_A0,
        "modules": [
            {"num": 1, "title": "First Contact", "units": [
                {"num": 1, "theme": "Hello and Goodbye"},
                {"num": 2, "theme": "Names and the Alphabet"},
            ]},
            {"num": 2, "title": "People and Things", "units": [
                {"num": 3, "theme": "Family and Friends"},
                {"num": 4, "theme": "Colors, Numbers, and Objects"},
            ]},
            {"num": 3, "title": "Daily Life", "units": [
                {"num": 5, "theme": "Actions and Food"},
                {"num": 6, "theme": "Days, Time, and Likes"},
            ]},
            {"num": 4, "title": "My World", "units": [
                {"num": 7, "theme": "Places and Weather"},
                {"num": 8, "theme": "Feelings, Routines, and Review"},
            ]},
        ],
    },
    {
        "code": "A1", "name": "Beginner (A1)", "rotation": ROTATION_STD,
        "modules": [
            {"num": 1, "title": "People and Everyday Life", "units": [
                {"num": 1, "theme": "Introductions and Personal Information"},
                {"num": 2, "theme": "Daily Routines and Habits"},
            ]},
            {"num": 2, "title": "Home and Family", "units": [
                {"num": 3, "theme": "Rooms, Furniture, and Homes"},
                {"num": 4, "theme": "Family Life and Descriptions"},
            ]},
            {"num": 3, "title": "Food, Shopping, and Money", "units": [
                {"num": 5, "theme": "Food, Drink, and Meals"},
                {"num": 6, "theme": "Shopping and Prices"},
            ]},
            {"num": 4, "title": "Time, Routines, and the Past", "units": [
                {"num": 7, "theme": "Time, Dates, and Schedules"},
                {"num": 8, "theme": "Past Events and Weekends"},
            ]},
            {"num": 5, "title": "Places, Travel, and Directions", "units": [
                {"num": 9, "theme": "Towns, Places, and Directions"},
                {"num": 10, "theme": "Travel and Transport"},
            ]},
            {"num": 6, "title": "Health, Feelings, and Plans", "units": [
                {"num": 11, "theme": "Body, Health, and Feelings"},
                {"num": 12, "theme": "Abilities, Plans, and the Future"},
            ]},
        ],
    },
    {
        "code": "A2", "name": "Elementary (A2)", "rotation": ROTATION_STD,
        "modules": [
            {"num": 1, "title": "Relationships and Communication", "units": [
                {"num": 1, "theme": "Friendship and Communication"},
                {"num": 2, "theme": "Messages and Phone Calls"},
            ]},
            {"num": 2, "title": "Work and Study", "units": [
                {"num": 3, "theme": "Jobs and Workplaces"},
                {"num": 4, "theme": "School, Study, and Learning"},
            ]},
            {"num": 3, "title": "Travel and Transport", "units": [
                {"num": 5, "theme": "Journeys and Transport"},
                {"num": 6, "theme": "Hotels, Airports, and Travel Problems"},
            ]},
            {"num": 4, "title": "Past Narratives", "units": [
                {"num": 7, "theme": "Stories from the Past"},
                {"num": 8, "theme": "Biographies and Life Events"},
            ]},
            {"num": 5, "title": "Plans, Promises, and Obligations", "units": [
                {"num": 9, "theme": "Plans, Promises, and Predictions"},
                {"num": 10, "theme": "Rules and Obligations"},
            ]},
            {"num": 6, "title": "Opinions and Experiences", "units": [
                {"num": 11, "theme": "Opinions and Preferences"},
                {"num": 12, "theme": "Experiences and Comparisons"},
            ]},
        ],
    },
    {
        "code": "B1", "name": "Intermediate (B1)", "rotation": ROTATION_STD,
        "modules": [
            {"num": 1, "title": "Identity and Lifestyle", "units": [
                {"num": 1, "theme": "Identity and Personality"},
                {"num": 2, "theme": "Lifestyle and Habits"},
            ]},
            {"num": 2, "title": "Stories and the Past", "units": [
                {"num": 3, "theme": "Narratives and Memories"},
                {"num": 4, "theme": "News and Events"},
            ]},
            {"num": 3, "title": "Work, Study, and the Future", "units": [
                {"num": 5, "theme": "Work and Careers"},
                {"num": 6, "theme": "Education and the Future"},
            ]},
            {"num": 4, "title": "Health and Wellbeing", "units": [
                {"num": 7, "theme": "Health and Fitness"},
                {"num": 8, "theme": "Food, Diet, and Wellbeing"},
            ]},
            {"num": 5, "title": "Travel, Culture, and Environment", "units": [
                {"num": 9, "theme": "Travel and Culture"},
                {"num": 10, "theme": "Cities and the Environment"},
            ]},
            {"num": 6, "title": "Media, Technology, and Communication", "units": [
                {"num": 11, "theme": "Media and the News"},
                {"num": 12, "theme": "Technology and Communication"},
            ]},
            {"num": 7, "title": "Opinions and Arguments", "units": [
                {"num": 13, "theme": "Opinions and Debates"},
                {"num": 14, "theme": "Decisions and Imagined Situations"},
            ]},
            {"num": 8, "title": "Consolidation and Independence", "units": [
                {"num": 15, "theme": "Accuracy and Range Review"},
                {"num": 16, "theme": "B1 Consolidation and Checkpoint"},
            ]},
        ],
    },
    {
        "code": "B2", "name": "Upper-Intermediate (B2)", "rotation": ROTATION_STD,
        "modules": [
            {"num": 1, "title": "Advanced Narrative", "units": [
                {"num": 1, "theme": "Complex Narratives"},
                {"num": 2, "theme": "Reported Speech and Rumours"},
            ]},
            {"num": 2, "title": "Argument and Persuasion", "units": [
                {"num": 3, "theme": "Arguments and Counter-arguments"},
                {"num": 4, "theme": "Regrets and Hypothetical Situations"},
            ]},
            {"num": 3, "title": "Work and Society", "units": [
                {"num": 5, "theme": "Work, Business, and Processes"},
                {"num": 6, "theme": "Society and Institutions"},
            ]},
            {"num": 4, "title": "Science, Technology, and Environment", "units": [
                {"num": 7, "theme": "Science and Discovery"},
                {"num": 8, "theme": "Environment and Sustainability"},
            ]},
            {"num": 5, "title": "Culture, Arts, and Media", "units": [
                {"num": 9, "theme": "Arts and Entertainment"},
                {"num": 10, "theme": "Media and Persuasion"},
            ]},
            {"num": 6, "title": "Health, Psychology, and Relationships", "units": [
                {"num": 11, "theme": "Health and Psychology"},
                {"num": 12, "theme": "Relationships and Community"},
            ]},
            {"num": 7, "title": "Global Issues", "units": [
                {"num": 13, "theme": "Global Issues and Development"},
                {"num": 14, "theme": "Politics and Economics"},
            ]},
            {"num": 8, "title": "Fluency and Accuracy", "units": [
                {"num": 15, "theme": "Accuracy and Style Review"},
                {"num": 16, "theme": "B2 Consolidation and Checkpoint"},
            ]},
        ],
    },
    {
        "code": "C1", "name": "Advanced (C1)", "rotation": ROTATION_STD,
        "modules": [
            {"num": 1, "title": "Academic Reading and Vocabulary", "units": [
                {"num": 1, "theme": "Academic Vocabulary and Reading"},
                {"num": 2, "theme": "Nominalization and Dense Texts"},
            ]},
            {"num": 2, "title": "Sophisticated Argument", "units": [
                {"num": 3, "theme": "Hedging and Cautious Claims"},
                {"num": 4, "theme": "Concession and Complex Argument"},
            ]},
            {"num": 3, "title": "Lectures and Note-taking", "units": [
                {"num": 5, "theme": "Lectures and Signposting"},
                {"num": 6, "theme": "Note-taking and Summaries"},
            ]},
            {"num": 4, "title": "Reports, Data, and Processes", "units": [
                {"num": 7, "theme": "Describing Data and Trends"},
                {"num": 8, "theme": "Processes and Comparisons"},
            ]},
            {"num": 5, "title": "Essay Writing", "units": [
                {"num": 9, "theme": "Essay Structure and Thesis Statements"},
                {"num": 10, "theme": "Evidence, Cohesion, and Style"},
            ]},
            {"num": 6, "title": "Discussion and Presentation", "units": [
                {"num": 11, "theme": "Seminar Discussion"},
                {"num": 12, "theme": "Presentations and Follow-up Questions"},
            ]},
            {"num": 7, "title": "Idiomaticity, Register, and Style", "units": [
                {"num": 13, "theme": "Idiomaticity and Collocation"},
                {"num": 14, "theme": "Register and Stylistic Choice"},
            ]},
            {"num": 8, "title": "C1 Mastery", "units": [
                {"num": 15, "theme": "C1 Accuracy Review"},
                {"num": 16, "theme": "C1 Consolidation and Exam Readiness"},
            ]},
        ],
    },
    {
        "code": "IE", "name": "IELTS Academic Preparation", "rotation": ROTATION_IELTS,
        "modules": [
            {"num": 1, "title": "Orientation and Diagnostic", "units": [
                {"num": 1, "theme": "How IELTS Works"},
                {"num": 2, "theme": "Diagnostic Test A"},
                {"num": 3, "theme": "Results and Study Plan"},
            ]},
            {"num": 2, "title": "Listening Mastery", "units": [
                {"num": 4, "theme": "Sections 1 and 2: Everyday Listening"},
                {"num": 5, "theme": "Sections 3 and 4: Academic Listening"},
                {"num": 6, "theme": "Listening Question Tactics"},
            ]},
            {"num": 3, "title": "Reading Mastery", "units": [
                {"num": 7, "theme": "Question Types, Skimming, and Scanning"},
                {"num": 8, "theme": "True/False/Not Given and Matching Tactics"},
                {"num": 9, "theme": "Completion Tasks and Time Control"},
            ]},
            {"num": 4, "title": "Writing Mastery", "units": [
                {"num": 10, "theme": "Task 1: Charts and Tables"},
                {"num": 11, "theme": "Task 1: Processes and Maps"},
                {"num": 12, "theme": "Task 2: Essays from Plan to Proofread"},
            ]},
            {"num": 5, "title": "Speaking Mastery", "units": [
                {"num": 13, "theme": "Part 1: Familiar Topics"},
                {"num": 14, "theme": "Part 2: The Long Turn"},
                {"num": 15, "theme": "Part 3: Abstract Discussion"},
            ]},
            {"num": 6, "title": "Mock Tests and Review", "units": [
                {"num": 16, "theme": "Mock Test 1"},
                {"num": 17, "theme": "Mock Test 2"},
                {"num": 18, "theme": "Final Review and Test-Day Plan"},
            ]},
        ],
    },
]

LESSON_INDEX_HEADER = [
    "lesson_id", "global_seq", "level", "module", "unit", "lesson_number",
    "title", "lesson_type", "objectives", "prerequisites",
    "new_vocab_ids", "new_grammar_ids", "skills_focus",
    "assessment_id", "validation_status", "file_path", "notes",
]


def iter_lessons():
    """Yield lesson dicts in course order."""
    seq = 0
    prev_level_last = None
    for level in LEVELS:
        code = level["code"]
        prev_lesson_id = None
        for module in level["modules"]:
            for unit in module["units"]:
                rotation = level["rotation"]
                if code == "IE" and unit["num"] in FULL_TEST_UNITS:
                    rotation = FULL_TEST_FOCUS
                for i, (ltype, focus, objective, skills) in enumerate(rotation, start=1):
                    seq += 1
                    lesson_id = f"{code}-M{module['num']}-U{unit['num']}-L{i:02d}"
                    title = f"{unit['theme']} — {focus}"
                    if prev_lesson_id is None:
                        # First lesson of the level: gated by previous level test.
                        prereq = "" if prev_level_last is None else prev_level_last
                    else:
                        prereq = prev_lesson_id
                    is_last = (i == len(rotation))
                    assessment_id = f"{code}-U{unit['num']:02d}-T" if is_last else ""
                    yield {
                        "lesson_id": lesson_id,
                        "global_seq": seq,
                        "level": code,
                        "module": module["num"],
                        "unit": unit["num"],
                        "lesson_number": i,
                        "title": title,
                        "lesson_type": ltype,
                        "objectives": objective,
                        "prerequisites": prereq,
                        "new_vocab_ids": "",
                        "new_grammar_ids": "",
                        "skills_focus": skills,
                        "assessment_id": assessment_id,
                        "validation_status": "planned",
                        "file_path": f"content/{code}/{lesson_id}.md",
                        "notes": "",
                    }
                    prev_lesson_id = lesson_id
        prev_level_last = f"{code}-LT"


def expected_counts():
    counts = {}
    total = 0
    for level in LEVELS:
        n_units = sum(len(m["units"]) for m in level["modules"])
        n_lessons = n_units * len(level["rotation"])
        counts[level["code"]] = {
            "modules": len(level["modules"]),
            "units": n_units,
            "lessons": n_lessons,
        }
        total += n_lessons
    counts["TOTAL"] = total
    return counts


def load_lesson_metadata(path=METADATA_PATH):
    """Read persistent authoring data without allowing structural overrides."""
    if not os.path.exists(path):
        raise ValueError("Missing lesson metadata; restore it rather than resetting authored progress.")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("lessons"), dict):
        raise ValueError("Lesson metadata requires schema_version 1 and a lessons object.")
    known = {row["lesson_id"] for row in iter_lessons()}
    for lesson_id, fields in data["lessons"].items():
        if lesson_id not in known:
            raise ValueError(f"Unknown metadata lesson: {lesson_id}")
        if not isinstance(fields, dict) or not set(fields) <= AUTHORING_FIELDS:
            raise ValueError(f"{lesson_id}: structural or unknown metadata fields are forbidden.")
        if not all(isinstance(value, str) for value in fields.values()):
            raise ValueError(f"{lesson_id}: metadata values must be strings.")
    return data["lessons"]


def authored_lessons(metadata=None):
    """Merge structural rows and the checked, persistent authoring overlay."""
    if metadata is None:
        metadata = load_lesson_metadata()
    lessons = list(iter_lessons())
    for row in lessons:
        row.update(metadata.get(row["lesson_id"], {}))
    return lessons


def write_lesson_index():
    lessons = authored_lessons()
    with open(LESSON_INDEX_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LESSON_INDEX_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(lessons)
    return lessons


def write_tables():
    counts = expected_counts()
    lines = []
    lines.append("# Course Structure Tables (GENERATED)")
    lines.append("")
    lines.append("> This file is generated by `scripts/course_structure.py`. Do not edit by hand.")
    lines.append("> Regenerate with: `python3 scripts/course_structure.py`")
    lines.append("")
    lines.append("## Level totals")
    lines.append("")
    lines.append("| Level | Name | Modules | Units | Lessons |")
    lines.append("|---|---|---|---|---|")
    for level in LEVELS:
        c = counts[level["code"]]
        lines.append(f"| {level['code']} | {level['name']} | {c['modules']} | {c['units']} | {c['lessons']} |")
    lines.append(f"| **Total** | | | | **{counts['TOTAL']}** |")
    lines.append("")
    for level in LEVELS:
        code = level["code"]
        lines.append(f"## {code} — {level['name']}")
        lines.append("")
        lines.append("| Module | Module title | Unit | Unit theme | Lessons | Lesson IDs |")
        lines.append("|---|---|---|---|---|---|")
        for module in level["modules"]:
            for unit in module["units"]:
                n = len(level["rotation"])
                first = f"{code}-M{module['num']}-U{unit['num']}-L01"
                last = f"{code}-M{module['num']}-U{unit['num']}-L{n:02d}"
                lines.append(
                    f"| M{module['num']} | {module['title']} | U{unit['num']} | {unit['theme']} "
                    f"| {n} | `{first}` – `{last}` |"
                )
        lines.append("")
        lines.append(f"Lesson rotation ({len(level['rotation'])} lessons per unit):")
        lines.append("")
        lines.append("| # | Lesson type | Focus |")
        lines.append("|---|---|---|")
        for i, (ltype, focus, _objective, _skills) in enumerate(level["rotation"], start=1):
            lines.append(f"| L{i:02d} | `{ltype}` | {focus} |")
        if code == "IE":
            lines.append("")
            lines.append("Full-test units (U2, U16, U17) replace the rotation with:")
            lines.append("")
            lines.append("| # | Lesson type | Focus |")
            lines.append("|---|---|---|")
            for i, (ltype, focus, _o, _s) in enumerate(FULL_TEST_FOCUS, start=1):
                lines.append(f"| L{i:02d} | `{ltype}` | {focus} |")
        lines.append("")
    os.makedirs(os.path.dirname(TABLES_PATH), exist_ok=True)
    with open(TABLES_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return TABLES_PATH


def main():
    lessons = write_lesson_index()
    tables = write_tables()
    counts = expected_counts()
    print(f"Lessons written: {len(lessons)} -> {LESSON_INDEX_PATH}")
    print(f"Tables written: {tables}")
    for level in LEVELS:
        c = counts[level["code"]]
        print(f"  {level['code']}: {c['modules']} modules, {c['units']} units, {c['lessons']} lessons")
    print(f"  TOTAL: {counts['TOTAL']} lessons")


if __name__ == "__main__":
    main()
