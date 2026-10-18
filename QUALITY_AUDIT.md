# QUALITY_AUDIT — Audit Results, Defects, Corrective Actions

## 1. Audit log

| Date | Scope | Auditor | Result |
|---|---|---|---|
| 2026-10-18 | Phase 1 architecture A–G, records, scripts, seeds | Project lead S-01 | Historical architecture PASS; two defects fixed. See INITIAL_CONSISTENCY_AUDIT, including its P-01 correction note. |
| 2026-10-18 | P-01: A0-M1-U1-L01 and L02; all 86 prompt/key pairs, scripts, inventory and 28 actual SVGs | Author S-02 + deterministic QA tools (not an independent reviewer) | Author/automated audit PASS after repairs; 33 regression tests PASS. Independent validation PENDING; lesson status remains drafted. Full evidence: docs/P01_AUDIT_REPORT.md and P01_QA_RESULTS.json. |

## 2. Defect log

| ID | Date | Location | Defect | Severity | Fix | Status |
|---|---|---|---|---|---|---|
| Q-001 | 2026-10-18 | Vocabulary V0006 | Bad delimiter broke row | minor | Corrected; validator PASS | fixed S-01 |
| Q-002 | 2026-10-18 | Grammar G074 | Question tags overloaded B1-U13 | minor | Moved to B1-M6-U11-L02 | fixed S-01 |
| Q-003 | 2026-10-18 | Pilot plan / seed inventory | L02 required what/is before their planned L03 introduction; my/your/name and yes/no seed placements contradicted the eight-word L01 plan | blocking | L01 exactly eight; L02 name/my/your/is/what explicitly taught; yes/no moved to G009 lesson. Plan/CSV/manifest agree | fixed S-02 |
| Q-004 | 2026-10-18 | G001/G003/G004/G010/G011 | Alphabet prerequisite was unnecessary for identity chunks; pilot previews lacked honest first-introduction/scope records | blocking | G003 no alphabet prerequisite; G001 starts L05; G003/G004 L01; scoped G011/G010 L02; later G010 still requires G009 at expansion | fixed S-02 |
| Q-005 | 2026-10-18 | course_structure.py | Regeneration overwrote all authoring inventory/status fields with defaults | blocking | Checked non-structural metadata overlay; idempotence/override regression tests | fixed S-02 |
| Q-006 | 2026-10-18 | English guard | No SVG/assessment scanning; arbitrary code/IPA/README exemptions; legitimate middle dot falsely rejected | blocking | Scan SVGs and assessments, exact registered IPA only, no code bypass, exact internal README exemptions; typography allowlist and negative tests | fixed S-02 |
| Q-007 | 2026-10-18 | Role/ownership/question SVGs | First render obscured listener faces and a revealed name badge; goodbye mouth diagram needed the first-syllable distinction | blocking visual meaning | Moved bubbles/flap, clarified /ɡʊd/ then /b/ cue; rerendered and visually rechecked | fixed S-02 |
| Q-008 | 2026-10-18 | Student draft instructions | Detailed scoring prose depended on untaught English; bare repair references A/B looked like untaught words in inventory audit | blocking | Helper-only prose in internal guide; actual learner headings use only symbols/known words and are inventory-checked; route uses demonstrated icons, known-frame cues and numeric references | fixed S-02 |
| Q-009 | 2026-10-18 | Open answers / QZ prompts | Bare name response in L02 B04 was missing from accepted alternatives; full-frame oral/written demands needed explicit known-language cues | blocking key fairness | Accept either taught frame or bare name in B04; keep frame evidence distinct; visibly cue L01 Q07/Q08 and L02 Q08 | fixed S-02 |
| Q-010 | 2026-10-18 | Deliverable E | Corrupted assessment filename token remained in actual checkout | minor | Restored {assessment_id}.md; current media/metadata policy recorded | fixed S-02 |
| Q-011 | 2026-10-18 | New P-01 solver | First run stripped ___ before solving a gap, producing no answer for a valid item | blocking QA-tool defect | Preserve response-space markers during parsing; added regression; all 48 closed items solved independently of keys | fixed S-02 |
| Q-012 | 2026-10-18 | Generated index CSV | Default CRLF output caused git diff --check whitespace flags on changed rows | minor tooling | Generator emits deterministic LF; index newline-normalised, no sequence/content changes outside the two authoring rows; regression asserts no CR | fixed S-02 |

All found content/key/tool blockers above are repaired. Independent review
is an outstanding evidence requirement, not a fabricated "fixed" defect.
Render attempts through ImageMagick/Cairo were unavailable in this sandbox;
resvg successfully rendered all supplied SVGs. Temporary tools/files are
ignored and are not core checker dependencies.

## 3. Independent validation sign-offs

A reviewer must be a fresh person/model session under D.8. The author reread
and automated rule-based solving do not qualify. No independent sign-off
has occurred; the following rows deliberately record that absence.

| Item | Independent reviewer | Date | Gates 1–7 | Status |
|---|---|---|---|---|
| A0-M1-U1-L01 | pending | — | author/automated results only; no independent decision | drafted, NOT validated |
| A0-M1-U1-L02 | pending | — | author/automated results only; no independent decision | drafted, NOT validated |
| A0-M1-U1-L01-QZ | pending | — | full blueprint/key/rubric authored and author-checked; no independent decision | drafted, no learner scores |
| A0-M1-U1-L02-QZ | pending | — | full blueprint/key/rubric authored and author-checked; no independent decision | drafted, no learner scores |

Per-gate methods/results and hashes: `docs/P01_AUDIT_REPORT.md`,
`docs/P01_LANGUAGE_AUDIT.md`, `docs/P01_QA_RESULTS.json`. Publication in
student/ is blocked pending real validation. No assessed/mastered status
is inferred from lesson production.

## 4. Open corrective actions

| ID | Action | Due | Owner phase | Status |
|---|---|---|---|---|
| CA-01 | Re-verify official IELTS format before Phase 6 mocks | Phase 6 start | 6 | open |
| CA-02 | Decide broader illustration/media strategy; P-01 SVGs are a bounded pilot decision | Phase 3 end | 3 | open (pilot supplied) |
| CA-03 | Arrange real-beginner tryouts, including instruction-symbol comprehension | Phase 3 | 3 | open |
| CA-04 | Produce/check audio route; scripts/mouth drawings are not recorded sound | Phase 3 end | 3 | open |
| CA-05 | Obtain fresh independent P-01 review, solve every task from student material, log confusion points/repair/sign-off before publication or next batch | before P-02 / student publication | 2 | open; P-01 paused |

## 5. Recurring-audit schedule

- Every batch: Gates 1–7; **100% of prompt/key pairs checked**, not the old
  ≥20% floor for second-solving. Distinguish closed rule-solves from open
  model/rubric checks and fresh independent review.
- Every level: cross-batch inventory, difficulty, review-slot and prerequisite
  expansion audit. Current content audit covers P-01, not all 622 planned files.
- Phase 7: full-system final audit. Real learner outcomes and audio
  intelligibility always require their own evidence.

## 6. PDF conversion check (2026-10-18; same two P-01 drafts)

- PASS: combined/separate PDFs with embedded SVGs/fonts, expanded scripts/
  keys, printable checkboxes and DRAFT/page footers.
- PASS: 86 prompt/key pairs, 20 learner sections and four script lines per
  lesson, IPA/symbol extraction, A4 dimensions, selectable text, page
  bounds, no replacement characters and no blank pages. Combined 43 pages
  equals individual 20 + 23 pages. HTML image/overflow checks also passed.
- PASS: 43-page inspection sheet and representative reading-size renders
  reviewed; all 41 prior content/data/tool hashes still match. All core
  checks rerun successfully, including all 33 regression tests.
- Evidence and exact PDF checksums: `exports/PDF_EXPORT_QA.json`.
  Rebuild instructions/limits: `exports/README.md`.
- This is author/tool **export QA**, not an independent pedagogical sign-off.
  Draft status, CA-05, missing recordings and missing learner trials remain
  unchanged; no source content, curriculum data or mastery result changed.

## 7. Independent-review handoff (2026-10-18, S-04)

The user explicitly retained the independent gate after requesting the full
course. This session prepares a handoff; it does **not** perform that review.

- `exports/P-01-Independent-Review.zip`: two answer-blind HTML/Markdown views,
  28 unchanged SVGs, separate helper scripts, original sources/keys and
  protocol/inventory snapshots, 86 intentionally blank reviewer-response
  rows, unfilled per-lesson Gates 1–7 form, exact input/output SHA-256s.
- PASS (transport only): 39/47 IDs; all nonwithheld learner content preserved;
  dedicated keys/helper disclosures/machine records absent from blind views;
  actual HTML image loads, desktop/mobile bounds and no external resources;
  ZIP integrity, safe relative paths and deterministic rebuild.
- PASS: 45/45 regression tests (33 existing + 12 packet tests), syntax and
  whitespace checks. All 41 previous content/tool hashes and all three
  original PDF hashes remain unchanged.
- `exports/P01_REVIEW_PACKET_QA.json` records packaging evidence;
  `docs/P01_INDEPENDENT_REVIEW.md` gives the fresh-session workflow/prompt.
- **CA-05 remains open; independent Gates 1–7 are still not performed.**
  No new lesson, validation, learner result or recording. Reviewer must save
  independent responses before opening keys; then return per-lesson evidence
  and blockers for repair/lead decision. Author render checks are not a
  zero-English learner trial or a fresh reviewer walkthrough.
