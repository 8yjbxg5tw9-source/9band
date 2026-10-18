# Deliverable D — Lesson-Generation and Quality-Assurance Procedures

Normative procedures for producing every lesson, exercise, key, and
assessment. Quality gates are mandatory: no content advances a stage without
passing them, and no claim (audio, testing, proficiency, scores) may exceed
its evidence.

## D.1 Batch production workflow (10 steps per batch)

1. **Select batch** from `LESSON_INDEX.csv` (adjacent lessons only, max 12 per
   batch). Record the batch in `PROJECT_CHECKPOINT.md`.
2. **Pull the inventory.** List all vocabulary (status ≥ introduced) and
   grammar (status ≥ introduced) available at the batch start. This is the
   allowed-language list.
3. **Author against the inventory.** Draft each lesson from
   `templates/LESSON_TEMPLATE.md`. Every sentence is checked: known language,
   explicitly introduced new items (within per-lesson maxima), or flagged
   incidental language (see §D.3).
4. **Register new items.** Add/confirm database rows with correct
   `intro_lesson_id` before marking the lesson `drafted`.
5. **Write keys and rubrics.** Answer keys written *from the questions*
   (never copied from a draft key); speaking/writing rubrics use observable
   descriptors only.
6. **Self-check.** Author completes the template's author checklist.
7. **Independent review.** A second pass (different reviewer/model session)
   runs the §D.4 gate checklist and files findings in `QUALITY_AUDIT.md`.
8. **Repair.** Fix all blocking findings; re-run affected checks.
9. **Validate.** Record sign-off (reviewer + date + checksums) and set status
   `validated`. Ship a copy to `student/`.
10. **Update records.** Databases, lesson index, assessment register, and
    checkpoint updated in the same session as the work. Unrecorded work =
    undone work.

## D.2 Unknown-language control (§6 of the mission)

For every lesson, the reviewer verifies:

- ≥95% of lexical running words in A0–B1 controlled texts are explicitly
  introduced **before the text/task**, including current-lesson teaching
  (≥90% at B2–C1; IE glosses support authentic texts). Also report the
  prior-lesson percentage: zero-English L01 starts at 0%. These are coverage
  measures, not evidence of learner knowledge. Proper names are reported as
  labels, not silently used to inflate the percentage.
- No unintroduced grammar carries meaning (incidental occurrences must be
  meaning-transparent, e.g. a proper name, and are logged).
- Instructions use known language + **actual demonstrated actions/images**
  (A0–A1), or known language + glosses (A2+). At zero English, use the
  demonstrated symbol route instead of silently requiring look/listen/
  repeat/choose/book. An instruction word counts against the new-word cap
  if it is taught. Image specifications alone are not supplied pictures.
- Every non-target exception is listed by location and reason. Section
  titles, optional IPA and delivery metadata may be reference-only if
  action meaning is independently demonstrated. Do not exempt load-bearing
  prose or hide language inside code fences, alt text or SVG descriptions.
  Rendered SVG words are checked at each point of use; all student text
  still passes the English-only guard.
- New items ≤ per-lesson maxima and each has a database row.
- Forward references ("as you will learn…") never carry current meaning.

Practical method until tooling exists: author submits a **language manifest**
(new words, new grammar, incidental items with line numbers); reviewer
spot-checks 100% of new items and 20% of running text against the databases.

## D.3 Incidental-language policy

A small amount of unfamiliar language is permitted only when: (a) meaning
stays clear without it (proper names, cognate-proof glosses, picture-locked
words); (b) it is logged in the lesson's New Language Record as
`INCIDENTAL:`; (c) it is never tested. Incidental items must not include
load-bearing grammar. Picture-locked proper names may be identity data
inside a frame, but their meaning/spelling is never a lexical test. A
scoped grammar preview must be explicitly taught and registered: it is not
incidental permission to use the rest of its topic. In P-01, G003 supports
the main G004 identity frame; G011 is my/your + name only and G010 is only
the fixed name question. Broader expansions retain their later dependencies.

## D.4 Quality gates (all blocking unless marked advisory)

**Gate 1 — English-only.** `audit_english_only.py` passes on all new/changed
student files. Zero tolerance.

**Gate 2 — Inventory.** §D.2 manifest verified; database cross-references
valid (`validate_databases.py` passes).

**Gate 3 — Key integrity.** Every question has exactly the keyed answer(s);
ambiguous items rewritten; accepted variants listed. Second-pass solver
protocol: reviewer answers from the student text alone.

**Gate 4 — Naturalness.** Contemporary, idiomatic English; no translationese;
register appropriate; multiple acceptable forms acknowledged, never marked
wrong.

**Gate 5 — Pedagogy.** Objectives ↔ activities ↔ Lesson Check aligned
one-to-one; worked examples precede tasks; difficulty rises within the
lesson; active recall present; review plan scheduled.

**Gate 6 — Level fit.** Length, speed, support, and abstraction match the
level profile (Deliverable A). A0–A1: picture/action-locked; B2+: ambiguity
and idiomaticity deliberately present.

**Gate 7 — Honesty (advisory → blocking at validation).** No claims of audio,
testing, CEFR certification, or official IELTS material beyond evidence;
estimates labelled as estimates.

## D.5 Assessment QA

- Blueprints precede items (template §2). Items map to taught objectives only.
- Time limits are estimated honestly until trialled, then labelled `trialled`.
- Speaking/writing rubrics: 3–5 bands, observable descriptors, worked
  samples at adjacent bands. No invented decimal precision.
- Parallel forms required before any retake is offered.
- Listening scripts and audio: scripts labelled as scripts; audio rows become
  `verified` only with file + duration + intelligibility check.

## D.6 Common-defect checklist (from the risk register)

Translationese · key/question mismatch · ambiguous instructions · untaught
language in tests · over-teaching (too many new items) · under-practice
(<6 controlled + <4 meaningful items per grammar point per unit) ·
register errors · answer-variant rejection · broken cross-references ·
drill monotony (same exercise type >3 lessons running) · review-plan gaps.

## D.7 IELTS integrity rules

1. Task descriptions and timing follow current official guidance; re-verify
   from ielts.org / British Council / IDP / Cambridge before Phase 6.
2. All practice tests are **original** and labelled "practice material — not
   an official IELTS test". Never reproduce official tests.
3. Band descriptors are paraphrased for teaching; scoring of mocks yields
   **estimated bands**, never official scores. No band guarantees, ever.
4. Strategy teaching never replaces proficiency: every tactic lesson includes
   the underlying language skill work.
5. Mocks are calibrated honestly: difficulty notes, timing rules, and the
   limits of self-scoring are stated on the paper.

## D.8 Roles and sign-off

- **Author** drafts; **Reviewer** gates (must be a fresh pass — different
  session context with the checklist, at minimum); **Lead** validates and
  signs off in `QUALITY_AUDIT.md`.
- Validation record format: `lesson_id | reviewer | date | gates 1–7 pass |
  notes`. One line per lesson; no batch sign-offs.
- Automated rule-based second-solving and an author reread are valuable
  checks, but **do not constitute a fresh independent reviewer/session**.
  When none is available, record author/automated results and leave the
  lesson `drafted`, independent sign-off pending; do not publish to student/.

## D.9 Continuous improvement

Every defect found post-validation gets a root-cause note in
`QUALITY_AUDIT.md` and, where systemic, a procedure update here. Procedures
are versioned (footer): current version **D-1.1 (2026-10-18, P-01)**. Changes: explicit zero-English
visual bootstrap; point-of-use versus entry coverage; scoped previews;
actual SVG checking; no independent-review claim from author/tool passes.
