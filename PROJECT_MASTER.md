# PROJECT_MASTER — 9band Zero-to-C1 + IELTS System

## 1. Mission

Build a complete, English-only, self-study English-learning system from
absolute zero (A0) to C1, followed by comprehensive IELTS Academic
preparation — with curriculum, lessons, vocabulary/grammar tracking,
four-skill development, pronunciation, spaced review, honest assessment, and
full project continuity across sessions.

## 2. Non-negotiable requirements

1. **English-only** student materials (enforced by automated audit, Gate 1).
2. **Controlled progression** — no lesson depends on untaught language.
3. **Evidence-based status** — nothing is "learned/mastered/validated/tested"
   without recorded evidence.
4. **Honest claims** — no invented audio, tests, CEFR certificates, or band
   scores. Estimates are labelled as estimates.
5. **Continuity** — every session starts from `PROJECT_CHECKPOINT.md` and
   ends with updated records.

## 3. Architecture summary

- **624 lessons** · 98 units · 46 modules · 7 levels (A0→C1 + IE).
  Source of truth: `scripts/course_structure.py` → `LESSON_INDEX.csv`.
- **100 grammar topics** (G001–G100) with full dependency chains.
- **~7,800 vocabulary targets**; 30 seed rows authored (A0-M1 pilot stock).
- **~170 assessments** planned (checks, unit tests, checkpoints, level and
  cumulative tests, IELTS diagnostic + mocks).
- Procedures: Deliverables A–G in `docs/` (version D-1.0).

## 4. Progress

| Phase | Scope | Status |
|---|---|---|
| 1 Architecture | Deliverables A–G + records + tooling + consistency audit | **COMPLETE (2026-10-18)** |
| 2 Pilot | A0-M1: 12 lessons + M1-C, validated | not started |
| 3 Validation & revision | Pilot audit, template/procedure fixes | not started |
| 4 Course production | All remaining lessons in ≤12-lesson batches | not started |
| 5 Level assessments | Level + cumulative tests, validated | not started |
| 6 IELTS preparation | IE module incl. 2 original mocks | not started |
| 7 Final audit | Full-system audit + report | not started |

Content counters: lessons validated 0/624 · vocab mastered 0/~7,800 ·
grammar mastered 0/100 · assessments ready 0/~170.

## 5. Current phase and stopping point

See `PROJECT_CHECKPOINT.md` (authoritative). Current: end of Phase 1.

## 6. Decisions log

D-01…D-08 recorded in `docs/INITIAL_CONSISTENCY_AUDIT.md` §2. New decisions
append here with date + rationale.

## 7. Open issues

O-01 (audio) · O-02 (learner testing) · O-03 (illustrations) · O-04
(platform) · O-05 (paper/computer IELTS) — see
`docs/INITIAL_CONSISTENCY_AUDIT.md` §3.

## 8. File authority (conflict order)

`course_structure.py` (structure) → databases + index (inventory) →
`PROJECT_CHECKPOINT.md` (continuity) → `QUALITY_AUDIT.md` (status) →
Deliverable D (process). Full rules: Deliverable E.

## 9. Session record

| Date | Session | Work completed | Checks |
|---|---|---|---|
| 2026-10-18 | S-01 | Phase 1: A–G, records, templates, scripts, seed data, consistency audit | structure/validate/audit PASS |
