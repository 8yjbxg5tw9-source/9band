# 9band — Zero-to-C1 English Learning System with IELTS Academic Preparation

An exceptionally comprehensive, English-only learning system that takes a
complete beginner (A0) to C1 proficiency and then prepares them for
IELTS Academic. Built as a real repository: curriculum, content source,
assessments, tracking databases, and quality-assurance tooling.

## Non-negotiable rule

**Every student-facing material is written entirely in English.** No
Azerbaijani (or any other language) may appear in lessons, exercises,
answer keys, tests, scripts, or published student resources. This is enforced
by `scripts/audit_english_only.py`. Internal project records (this file,
planning docs, databases) are also written in English.

## Repository map

| Path | Purpose |
|---|---|
| `PROJECT_MASTER.md` | Mission, curriculum overview, progress, decisions. |
| `CURRICULUM_MAP.md` | Canonical curriculum reference (levels → lessons). |
| `docs/DELIVERABLE_*.md` | Deliverables A–G (architecture phase). |
| `docs/STRUCTURE_TABLES.md` | Generated full module/unit/lesson tables. |
| `docs/INITIAL_CONSISTENCY_AUDIT.md` | Architecture audit + unresolved decisions. |
| `VOCABULARY_DATABASE.csv` | Vocabulary tracking database (schema + entries). |
| `GRAMMAR_DATABASE.csv` | Grammar tracking database (100 topics). |
| `LESSON_INDEX.csv` | All 624 lessons (generated; do not hand-edit). |
| `ASSESSMENT_REGISTER.md` | Assessment framework + register. |
| `QUALITY_AUDIT.md` | Audit results, defects, corrective actions. |
| `PROJECT_CHECKPOINT.md` | Exact stopping point + next action. |
| `templates/` | Authoring templates for lessons and assessments. |
| `scripts/` | Structure generator, validators, English-only audit. |
| `content/` | Student-facing lesson source (English-only enforced). |
| `student/` | Published/assembled student materials (English-only enforced). |
| `assessments/` | Assessment files (created in Phase 2+). |

## Course at a glance

| Level | Modules | Units | Lessons | New words | Cumulative words |
|---|---|---|---|---|---|
| A0 Starter | 4 | 8 | 48 | 350 | 350 |
| A1 | 6 | 12 | 84 | 650 | 1,000 |
| A2 | 6 | 12 | 84 | 1,000 | 2,000 |
| B1 | 8 | 16 | 112 | 1,500 | 3,500 |
| B2 | 8 | 16 | 112 | 1,500 | 5,000 |
| C1 | 8 | 16 | 112 | 2,000 | 7,000 |
| IELTS Academic | 6 | 18 | 72 | 800* | 7,800* |
| **Total** | **46** | **98** | **624** | — | — |

\*IELTS vocabulary is largely receptive/academic consolidation, not all-new headwords.

## Workflow

Phases (see `PROJECT_MASTER.md`): 1 Architecture → 2 Pilot → 3 Validation →
4 Course production → 5 Level assessments → 6 IELTS → 7 Final audit.

After any change, all three checks must pass:

```bash
python3 scripts/course_structure.py
python3 scripts/validate_databases.py
python3 scripts/audit_english_only.py
```

## Continuity (resuming work)

1. Read `PROJECT_CHECKPOINT.md` (stopping point + next action).
2. Read `PROJECT_MASTER.md` (progress + decisions).
3. Read `QUALITY_AUDIT.md` (open defects).
4. Run the three checks above.
5. Resume from the documented next action. Never invent continuity.

## Honest-status policy

Content stages: `planned` → `drafted` → `reviewed` → `validated` → (`tested`
only after real learners). Claims about audio, testing, CEFR certification,
or IELTS scores must never exceed the evidence. See Deliverable D.
