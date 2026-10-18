# Scripts

Helper programs that keep the project consistent. All scripts use only the
Python standard library.

| Script | Purpose |
|---|---|
| `course_structure.py` | Single source of truth for levels, modules, units, and lessons. Regenerates `LESSON_INDEX.csv` and `docs/STRUCTURE_TABLES.md`. |
| `validate_databases.py` | Checks CSV headers, ID uniqueness, lesson counts, prerequisite references, and allowed status values. |
| `audit_english_only.py` | Scans student-facing files (`content/`, `student/`) for non-English characters, Azerbaijani stopwords, and unexpected non-ASCII text. |

Run after any structural change:

```bash
python3 scripts/course_structure.py
python3 scripts/validate_databases.py
python3 scripts/audit_english_only.py
```

All three must pass before a batch of work is marked complete.
