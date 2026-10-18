# 9band — Zero-to-C1 English Learning System with IELTS Academic Preparation

An English-only learning system being built from absolute zero (A0) through
C1 and IELTS Academic preparation. The 624-lesson architecture is complete;
**the first two actual pilot lessons are drafted and author/tool-audited**.
The rest of the course is not yet authored, validated or learner-tested.

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
| `LESSON_INDEX.csv` | All 624 planned/authoring rows (generated; do not hand-edit). |
| `data/lesson_metadata.json` | Persistent non-structural authoring fields used by the generator. |
| `data/P01_LANGUAGE_MANIFEST.json` | Exact early inventory, preview scopes, objective maps, rubrics and reference exceptions. |
| `docs/P01_AUDIT_REPORT.md` | P-01 results, remaining limitations and exact file manifest link. |
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

For P-01, run the full available check sequence:

```bash
python3 scripts/build_pilot_visuals.py
python3 scripts/course_structure.py
python3 scripts/validate_databases.py
python3 scripts/audit_english_only.py
python3 scripts/audit_english_only.py --strict
python3 scripts/audit_pilot_batch.py --write-report
python3 -m unittest discover -s scripts -p 'test_*.py' -v
git diff --check
```

## Continuity (resuming work)

1. Read `PROJECT_CHECKPOINT.md` (stopping point + next action).
2. Read `PROJECT_MASTER.md` (progress + decisions).
3. Read `QUALITY_AUDIT.md` (open defects).
4. Run the checks above (details in `scripts/README.md`).
5. Resume from the documented next action. Never invent continuity.

## Honest-status policy

Content stages: `planned` → `drafted` → `reviewed` → `validated` → (`tested`
only after real learners). Claims about audio, testing, CEFR certification,
or IELTS scores must never exceed the evidence. See Deliverable D.

## Actual pilot lessons — P-01 only

- [A0-M1-U1-L01](content/A0/A0-M1-U1-L01.md): hello/hi/goodbye/bye and
  I am / You are; 39 fully keyed prompts.
- [A0-M1-U1-L02](content/A0/A0-M1-U1-L02.md): My/Your name is and the
  explicitly taught fixed question What is your name?; 47 keyed prompts.
- 28 original supplied SVGs teach meaning/action without assuming instruction
  vocabulary. No picture is merely a future illustration specification.
- Both sources have all 21 template sections, real examples/exercises/keys,
  pronunciation diagrams, helper-read listening scripts and adaptive recall.

**Limits:** no audio recordings, fresh independent sign-off or real learner
trial exists yet. Sound practice needs a competent helper; diagrams/IPA alone
are not a fully autonomous zero-English sound course. Sources remain
`drafted`, and `student/` remains unpublished. No next batch has started.
See [P-01 audit](docs/P01_AUDIT_REPORT.md), [delivery guide](docs/P01_DELIVERY_GUIDE.md)
and [exact changed files](docs/P01_FILE_MANIFEST.md).
