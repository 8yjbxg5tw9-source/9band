# PROJECT_MASTER — 9band Zero-to-C1 + IELTS System

## 1. Mission

Build a complete, English-only, self-study English-learning system from
absolute zero (A0) to C1, followed by comprehensive IELTS Academic
preparation — curriculum, lessons, vocabulary/grammar tracking, four skills,
pronunciation, spaced review, honest assessment and project continuity.

## 2. Non-negotiable requirements

1. **English-only** student materials, including scripts, keys and actual
   picture text (automated guard plus inventory/manual review).
2. **Controlled progression** — no task depends on untaught language or an
   assumed instruction word.
3. **Evidence-based status** — authoring coverage is not learner achievement;
   automated/author checks are not independent validation.
4. **Honest claims** — no invented audio, learner testing, scores, CEFR
   certificates or band guarantees. Estimates are labelled.
5. **Continuity** — begin and end with PROJECT_CHECKPOINT.md; update records
   in the same session as the work.

## 3. Architecture summary

- **624 lessons · 98 units · 46 modules · 7 levels** (A0→C1 + IE).
  Structural source: `scripts/course_structure.py`; checked authoring
  overlay: `data/lesson_metadata.json`; output: `LESSON_INDEX.csv`.
- **100 grammar topics**, with declared first-introduction scope and later
  expansion dependencies. P-01 introduces four narrow scopes, not four
  complete topics or learner mastery.
- **~7,800 vocabulary targets**; 30 seed rows exist, 13 with actual P-01
  introduction evidence. Remaining rows/coverage are planned.
- **~170 separate assessments + 624 embedded checks** planned.
- Procedures D-1.1; tracking clarification C-1.1; template T-1.1.

## 4. Progress

| Phase | Scope | Status |
|---|---|---|
| 1 Architecture | Deliverables A–G + records + tooling + architecture audit | COMPLETE (2026-10-18); P-01 dependency corrections recorded |
| 2 Pilot | A0-M1: 12 lessons + checkpoint and unit tests | IN PROGRESS: P-01 has 2 complete drafts, author/automated audits PASS; independent review pending |
| 3 Validation & revision | Whole-pilot review, learner trials, method fixes | not started |
| 4 Course production | Remaining lessons in controlled batches | not started |
| 5 Level assessments | Level + cumulative tests | not started |
| 6 IELTS preparation | IE module incl. 2 original mocks | not started |
| 7 Final audit | Full-system audit + report | not started |

Content counters: **2 complete drafts / 624; 0 reviewed; 0 validated;
0 tested**. Pilot: **2/12 drafted**, 0/12 validated. Two embedded Lesson
Checks drafted (16 items), no assessment ready/validated and no learner
score. Vocabulary mastered 0/~7,800; grammar mastered 0/100. No learner
retrieval or productive-use result has been logged.

## 5. Current phase and stopping point

P-01 authoring and author/automated audit complete; paused before fresh
independent review. **Do not begin P-02/L03.** Exact next action and full
check results are in `PROJECT_CHECKPOINT.md`.

Actual sources: `content/A0/A0-M1-U1-L01.md` and `A0-M1-U1-L02.md`, with 28
original linked SVGs. Full results: `docs/P01_AUDIT_REPORT.md`; hashed
machine evidence: `docs/P01_QA_RESULTS.json`.

## 6. Decisions log

D-01…D-08 remain in `docs/INITIAL_CONSISTENCY_AUDIT.md` §2.

| ID / date | Decision and rationale |
|---|---|
| D-09 / 2026-10-18 | Correct first introductions to match actual teaching: L01 eight words; L02 name/my/your/is/what; yes/no later. Teach the complete name request in L02 rather than rely on future words. G003 does not require alphabet knowledge. Scoped G011/G010 previews retain later expansion prerequisites. |
| D-10 / 2026-10-18 | P-01 uses actual deterministic SVG illustrations and demonstrated nonverbal action icons, not English instruction verbs or English-only picture descriptions as a substitute for pictures. Text-only repository policy includes SVG/JSON. |
| D-11 / 2026-10-18 | Keep authoring metadata outside the generated index, under a checked non-structural overlay; regeneration must preserve progress without allowing structural overrides. |
| D-12 / 2026-10-18 | Report both prior-lesson and point-of-use lexical coverage. L01 entry is 0%, not a fabricated 95%. Authored coverage and successful learner retention are separate. |
| D-13 / 2026-10-18 | Same-author review and a deterministic blind solver do not satisfy independent review. Both P-01 lessons remain drafted; no student/ publication or invented sign-off. Scripts are not audio. |

## 7. Open issues

O-01 audio: helper scripts supplied, no recordings/verified sound; O-02
real-learner testing; O-03 broader illustration strategy (pilot SVGs only
resolved); O-04 platform; O-05 IELTS delivery-format currency. CA-05 adds
fresh P-01 independent review before publication/next batch. See audit log.

## 8. File authority

Structure generator → checked authoring metadata/databases → generated
index for structure/inventory; checkpoint for continuity; QUALITY_AUDIT for
status; Deliverable D for process. Conflicts are resolved by field/domain,
not by blindly trusting stale prose. Full rules: Deliverable E.

## 9. Session record

| Date | Session | Work completed | Checks |
|---|---|---|---|
| 2026-10-18 | S-01 | Phase 1 A–G, records, templates, structure and seed data | original structure/validate/English guard PASS; historical limits recorded |
| 2026-10-18 | S-02 / P-01 | Two complete 21-section lessons, 86 keyed prompts, 28 SVGs; inventory/scope repairs; persistent metadata; stricter QA, 33 tests; records/reports updated | structure/validate/English normal+strict/P-01 audit/33 tests PASS; independent review, recordings and learner testing pending |
