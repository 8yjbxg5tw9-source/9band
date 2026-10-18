# Initial Consistency Audit (Architecture Phase, 2026-10-18)

## 1. Checks performed

| # | Check | Method | Result |
|---|---|---|---|
| 1 | Lesson counts match across all docs | `course_structure.py` output vs README/A/B | PASS — 624 lessons, 98 units, 46 modules everywhere |
| 2 | Lesson IDs valid and unique | `validate_databases.py` | PASS |
| 3 | Grammar DB: 100 topics, valid levels/lessons/prereqs, no self-refs | `validate_databases.py` | PASS |
| 4 | Vocab seed: valid levels/lessons/meanings | `validate_databases.py` (1 defect found and fixed: V0006 delimiter) | PASS after fix |
| 5 | Grammar→unit mapping consistent with Deliverable B tables | Manual cross-check of all 100 rows | PASS after fix (G074 moved B1-U13 → B1-U11 for load balance) |
| 6 | English-only compliance of current repo | `audit_english_only.py` | PASS (no student content yet; tooling verified) |
| 7 | IELTS format currency | Web verification vs ielts.org/British Council/Cambridge/IDP, Oct 2026 | PASS — 4-part Listening, 3-passage Reading, 2-task Writing, 3-part Speaking confirmed; re-verify in Phase 6 |
| 8 | Assessment counts coherent | Register arithmetic (§2 of ASSESSMENT_REGISTER.md) | PASS |
| 9 | No overclaims (audio/testing/CEFR/scores) | Text review of all docs | PASS — honesty rules in D; disclaimers in A |
| 10 | Pilot plan feasible within A0 rules | Inventory arithmetic (F §F.3 vs maxima) | PASS — max 8 new words/lesson respected |

## 2. Decisions made (with rationale)

- **D-01: 624-lesson structure.** Granularity chosen for controlled
  unknown-language growth and reviewable batches. Cost (scale) accepted;
  mitigated by batching (R-11).
- **D-02: Lexical units.** Not every unit introduces grammar (B1-U11-style
  units). Rationale: retention and skills need space; grammar density is
  front-loaded where dependency chains require it.
- **D-03: Grammar closed at 100 topics (G001–G100).** IELTS adds no new
  grammar rows — exam work applies the system. New topics need a procedure
  exception, not silent growth.
- **D-04: Status vocabularies fixed** (C). Mastery always requires delayed
  retrieval + assessment evidence. No exposure-based mastery.
- **D-05: Generated index.** `LESSON_INDEX.csv` is never hand-edited; the
  Python module is the source of truth. Rationale: 624 rows cannot stay
  consistent by hand.
- **D-06: IPA stripped in English-only audit.** `/…/` spans are exempt from
  the Azerbaijani-character check (documented in the script) because IPA
  legitimately uses `ə`. Stopword check still applies to prose.
- **D-07: Estimates, never promises.** Hours, bands, and CEFR outcomes are
  planning estimates with disclaimers; score guarantees are forbidden (R-13).
- **D-08: Pilot = A0-M1 only.** 12 lessons validate the method before scale
  commitment. Full A0 follows in Phase 4 planning order.

## 3. Genuinely unresolved items (open issues)

| ID | Issue | Why open | Resolution path |
|---|---|---|---|
| O-01 | Audio production | No recording capability confirmed in this environment | Phase 2: scripts only, labelled; revisit studio/TTS options before Phase 4 |
| O-02 | Real learner testing | No learners available yet | Required before any `tested` status; plan tryouts in Phase 3 |
| O-03 | Illustration/media strategy | A0–A1 needs pictures; sourcing (commission/AI/print specs) undecided | Decide before Phase 4; picture specs already required in lessons |
| O-04 | Delivery platform | Repo-first vs app/book outputs unknown | Content stays platform-agnostic Markdown; decide at pilot review |
| O-05 | Paper vs computer IELTS emphasis | One 2026 source suggests computer-first rollout; official policy varies by market | Re-verify in Phase 6; teach transferable skills + both Ticketing realities |

## 4. Limitations stated plainly

- Architecture is validated for **internal consistency**, not for learner
  outcomes — outcomes require Phases 2–3 evidence.
- Vocabulary beyond the 30 seed rows is **planned, not authored**; the
  7,800-target depends on sustained Phase 4 production.
- The English-only audit is **lexical/character-based**: it catches
  Azerbaijani reliably but cannot judge explanation clarity — human review
  (Gate 4–6) covers that.
- IELTS verification reflects **October 2026 public sources**; test rules can
  change and must be re-checked before mocks ship.

## 5. Verdict

Architecture is **coherent and internally consistent**. Deliverables A–G are
complete. The project may proceed to Phase 2 (pilot production) per
`PROJECT_CHECKPOINT.md`. No blocking defects remain; open issues O-01–O-05
are tracked, not ignored.

## 6. P-01 correction note (S-02, 2026-10-18)

This is the historical architecture audit, not an audit of authored lessons.
P-01 found seed/plan introduction disagreements and an unnecessary alphabet
prerequisite that the original pilot arithmetic did not catch. They are
repaired in the current databases/Deliverables B–F and documented as
Q-003/Q-004 in QUALITY_AUDIT.md. The original PASS must not be read as proof
that zero-English content, audio, learner outcomes or all future dependency
expansions were already validated. See docs/P01_AUDIT_REPORT.md.
