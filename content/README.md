# Content (student-facing lesson source)

Each lesson lives at `content/{LEVEL}/{LESSON_ID}.md`, exactly matching the
`file_path` column of `LESSON_INDEX.csv`. For example:

```text
content/A0/A0-M1-U1-L01.md
content/B1/B1-M7-U13-L04.md
content/IE/IE-M4-U10-L02.md
```

Rules:

1. **English only.** Everything under `content/` except this README is scanned
   by `scripts/audit_english_only.py`. No Azerbaijani anywhere.
2. **One lesson, one file**, authored from `templates/LESSON_TEMPLATE.md`.
3. **Controlled language.** Every word and structure must already be in the
   learning inventory or be explicitly introduced in the lesson (maxima per
   level apply — see the template).
4. **Database first.** New vocabulary/grammar gets database rows with this
   lesson as `intro_lesson_id` before the lesson is marked `drafted`.
5. **Status flow.** Lessons move `planned` → `drafted` → `reviewed` →
   `validated` in `LESSON_INDEX.csv`. Only `validated` lessons ship to
   `student/`.

Current status: no lessons authored yet (architecture phase).
