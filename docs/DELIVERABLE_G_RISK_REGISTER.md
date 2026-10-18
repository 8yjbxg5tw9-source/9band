# Deliverable G — Risk Register

Likelihood (L) / Impact (I): 1–5. Owner phase: the phase that must mitigate.
Detection: how we notice early. Every risk has a procedure-level mitigation —
willpower is not a mitigation.

| ID | Risk | L | I | Mitigation | Detection | Phase |
|---|---|---|---|---|---|---|
| R-01 | Vocabulary overload (too many new words, weak retention) | 4 | 5 | Per-lesson maxima (C); manifest check (D §D.2); mastery-gated status (C §C.4) | Review-history failures; unit-test VOC codes | 2–4 |
| R-02 | Unnatural English / translationese | 3 | 5 | Gate 4 naturalness read; contemporary usage checks; variant-acceptance rule | Reviewer flags; learner confusion | 2–4 |
| R-03 | Broken continuity (untaught language in lessons/tests) | 4 | 5 | Inventory-first authoring; generated index; validator; Gate 2 | `validate_databases.py`; key-solver protocol | 2–4 |
| R-04 | Invalid assessment (tests untaught items; keys wrong) | 3 | 5 | Blueprints before items; second-pass solving; Gate 3; parallel forms | Tryout failures; audit sampling | 2–6 |
| R-05 | Inconsistent difficulty (jumps or flat stretches) | 3 | 4 | Level profiles (A) enforced at Gate 6; lexical-unit pacing (B); pilot calibration | Score variance; reviewer ratings | 2–4 |
| R-06 | IELTS inaccuracies (format/scoring drift) | 2 | 5 | Re-verify from official sources in Phase 6; integrity rules (D §D.7); original mocks only | Pre-Phase-6 source check | 6 |
| R-07 | English-only violations | 2 | 5 | Automated audit on every batch (Gate 1); template reminders | `audit_english_only.py` | all |
| R-08 | Key/question mismatch at scale | 3 | 4 | Keys written from questions; solver protocol; sampling audits per batch (≥20%) | Solver failures | 2–6 |
| R-09 | Grammar dependency violations (using untaught structures) | 3 | 4 | Chain rules (B §B.8); manifest check; validator prereq check | Validator errors; reviewer flags | 2–4 |
| R-10 | Review-system collapse (plans written, never scheduled) | 3 | 4 | §19 Review Plan mandatory per lesson; scheduler fields in databases; batch audits check slots | Missing review_history entries | 2–4 |
| R-11 | Scope explosion (624 lessons × perfectionism = never done) | 4 | 4 | ≤12-lesson batches; pilot-first calibration; time-boxed review passes; checkpoint discipline | Checkpoint slippage | 1–4 |
| R-12 | Audio promises without audio (scripts labelled as recordings) | 3 | 3 | `audio_status` honesty rule (C); Gate 7; scripts labelled as scripts | Audit of status claims | 2–7 |
| R-13 | CEFR/band-score overclaim | 2 | 5 | Disclaimer in every level intro; estimates labelled; assessment-integrity rules | Text search for guarantee language in QA | 2–7 |
| R-14 | Copyright contamination (copied texts, official tests) | 2 | 5 | Original-content rule; no official-test reproduction; source log for any adapted text | Reviewer provenance check | 2–6 |
| R-15 | Reviewer fatigue / single-pass blindness | 4 | 3 | Fresh-pass reviewer rule; checklists over memory; sampling + full gates on tests | Defect escape rate in audits | 2–7 |
| R-16 | Project-memory loss across sessions | 3 | 5 | Checkpoint protocol (E §E.3); generated single source of truth; commit-per-session | Session-start verification | all |
| R-17 | Illustration/media gap (A0 needs pictures; none exist yet) | 4 | 3 | Picture specs in every A0–A1 lesson now; media decision tracked as open issue O-03; text+action fallback | Pilot walkthrough gaps | 2–3 |
| R-18 | Demotivation design (drill monotony, no wins) | 3 | 3 | Exercise-type rotation rule; mastery checklists; visible progress (statuses, portfolios) | Lesson-type audit per batch | 2–4 |

## Top-5 watch list (architecture phase → pilot)

1. **R-03 continuity** — the pilot's unknown-language audit is the first real
   test of the inventory system.
2. **R-01 overload** — pilot inventory (F §F.3) must survive reviewer
   walkthroughs without cuts exceeding 20%.
3. **R-11 scope** — pilot velocity (weeks per 12-lesson batch) sets the whole
   production schedule; measure it honestly.
4. **R-16 memory** — checkpoint discipline starts now, not "later".
5. **R-17 media** — decide the illustration strategy before Phase 4 (O-03).
