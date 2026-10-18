# Phase 2 / P-01 — Authoring and Audit Report

Date: **2026-10-18** · Branch: **arena/555ec1d1-9band** · Session: **S-02**

## 1. Scope and verdict

**Two actual complete lesson drafts authored; author and available automated
audits PASS after repairs. Fresh independent review is still PENDING.**
No other lesson or next batch has been authored. No independent reviewer,
recorded audio, beginner trial or learner score is claimed.

| Actual lesson | Template sections | New words | Practice / recall | Embedded check | State |
|---|---|---|---|---|---|
| content/A0/A0-M1-U1-L01.md | all 21 | 8: hello, hi, goodbye, bye, I, am, you, are | 39 total keyed prompts; 8 controlled, 4 meaningful, 6 recall, listening/reading/speaking/writing included | A0-M1-U1-L01-QZ, 8 items | drafted |
| content/A0/A0-M1-U1-L02.md | all 21 | 5: name, my, your, is, what | 47 total keyed prompts; 6 cold prior-lesson prompts, 8 controlled, 4 meaningful, 7 recall, all four skills included | A0-M1-U1-L02-QZ, 8 items | drafted |

Each lesson supplies actual explanations through picture/word contrasts,
frame equivalence and speaker reversal; seven worked models; mouth/rhythm
pronunciation guidance; four real helper-read script lines; controlled
reading and tasks; all exercises and full keys/alternatives; speaking and
trace/copy/personal writing; active recall; error/correction contrasts;
scoring display; and adaptive next-lesson/+1/+3/+7/+21/+60 recall tasks.

The **28 original SVGs are supplied illustrations**, not English prose
specifications. They are text-based, deterministic and linked by local
relative paths; no external image/audio hosting is required. The first
lesson demonstrates the action symbols before using them. No learner
needs the words look/listen/repeat/choose/book/read/write/say/point to follow
the pictured action route.

Complete exact changed paths: **`docs/P01_FILE_MANIFEST.md`**.

## 2. Vocabulary and grammar dependencies

- All thirteen targets already existed in the 30 seed rows. **No new row or
  ID was necessary.** Their first introductions, examples, picture-backed
  glosses, evidence notes and coverage status were corrected/filled.
- L01 remains at eight words. Yes/no are deferred to A0-M2-U3-L02.
  My/your/name are first taught in L02. What/is are explicitly advanced from
  L03 to L02 so the requested whole name question has no future dependency.
- G003 (I/you) supports the single G004 identity frame in L01. Alphabet/letter
  names are not a prerequisite of speaking/imitating that frame. G001 starts
  with letter symbols in L05 instead of pretending to be taught in L01.
- L02 G011 is **my/your + name only**. G010 is **What is your name? only**,
  explicitly grounded by a hidden/revealed badge. G010's productive expansion
  still requires G009 at A0-M2-U4-L02. Other wh-questions, his/her, it is,
  object nouns, negatives and productive yes/no questions are not available.
- A scope/topic's `introduced` state means authored coverage only, not that
  the entire topic has been covered or that any learner has succeeded.
  Review/mastery histories remain empty; grammar assessment status is planned.
- Both objective→practice→check maps cover every QZ item. The next L01 review
  actually exists at the start of L02, before new words; L02's L03 review is
  reserved but **L03 is not authored**.

### Coverage accounting — no bootstrap percentage trick

| Controlled reading | Lexical tokens, excluding identity labels | Known from earlier lessons | Taught before this reading |
|---|---|---|---|
| L01 | 8 | 0/8 = 0% | 8/8 = 100% |
| L02 | 19 | 6/19 = 31.58% | 19/19 = 100% |

These short A0 readings deliberately repeat words. Percentages do not count
navigation labels, proper names or image descriptions as known vocabulary,
and do not imply retention. Every rendered SVG text token is separately
checked **at every use**, not just against the end-of-batch inventory.

Actual learner headings use only symbols/IDs or already-taught words and
are inventory-checked at every use. Only coded course metadata, the technical
script-only notice, optional IPA and English accessibility/helper descriptions
are explicit reference exceptions, not required learner comprehension. Their
locations/reasons are listed in `P01_LANGUAGE_AUDIT.md` and the manifest. No free-prose unknown
instruction is silently excluded. The visual route is not claimed as a
screen-reader-only beginner route.

## 3. Exercise and key verification

**86/86 prompt IDs have exactly one matching key row.**

| Method | L01 | L02 | Total |
|---|---|---|---|
| Closed items derived from the student prompt/options/script/picture facts before reading the key | 22 | 26 | 48 |
| Open keys checked against declared acceptable frames/models/rubrics | 17 | 21 | 38 |
| All keyed tasks | 39 | 47 | 86 |

The solver confirms one available correct answer for every closed item.
The author also walked through all prompts, scripts, role perspectives,
worked examples and key rows. This is an author second pass, not a fresh
independent model/person. The deterministic solver uses declared visual
facts; it is not computer vision or evidence of beginner comprehension.

Open response fairness:

- hello/hi and goodbye/bye both accepted in matching contexts;
- own names or pictured roles accepted, without grading name spelling;
- L02 B04 accepts My name is…, I am…, **or a bare name**, all naturally
  correct; only a full frame provides evidence of frame use;
- known-language cues make full-frame demands visible in scored production;
- correct naturally produced contractions are accepted by a competent
  assessor but are not newly taught/required here;
- early capitals/punctuation, accent and speed are not scored.

Each embedded check has a blueprint in ASSESSMENT_REGISTER.md and eight
whole-point items; **6/8 = 75%** is the smallest score meeting ≥70%. Oral
Q07 cannot be guessed from reading a key; no oral evidence means not
assessed and no complete total. Same-item repairs are practice, not a scored
retake. No parallel retake is offered in this batch.

## 4. Gates — author evidence is not independent validation

| Gate | L01 | L02 | Evidence / limitation |
|---|---|---|---|
| 1 English-only | author/guard PASS | author/guard PASS | Normal + strict scans: actual lesson, hidden metadata, code and SVG text/descriptions; lexical inventory check too. Not universal statistical language identification. |
| 2 Inventory/dependencies | PASS for declared authored scope | PASS for declared authored scope | Exact first-intro/back-reference/marker checks; 8/5 word caps; chronological scoped prerequisites; no unknown target tokens. Future planned content not audited as written content. |
| 3 Key integrity | author/automated PASS | author/automated PASS | Every prompt/key paired; closed blind rule-solves; open model/rubric check and author solve. Fresh independent solve pending. |
| 4 Naturalness | author PASS, fresh review pending | author PASS, fresh review pending | Full forms deliberate at A0; alternatives accepted; final confirmations framed as badge checking, not an alleged authentic recorded conversation. |
| 5 Pedagogy | author PASS, fresh review pending | author PASS, fresh review pending | Seven models, actual action bootstrap, controlled→meaningful→personal practice, retrieval and complete keyed review tasks; objective/check alignment. Learner tryout pending. |
| 6 Level fit | author PASS with sound limitation | author PASS with sound limitation | Pictures/frame contrasts carry meaning; no instruction-vocabulary assumption. Sound model needs a helper; 50–70-minute estimates in the helper guide are untrialled. |
| 7 Honesty | PASS | PASS | Scripts labelled, no recording claim, no learner scores/mastery or independent sign-off; drafted status retained, student/ empty. |

**Independent Gates 1–7 sign-off: not performed.** D.8 forbids calling an
author/tool pass an independent review. Both lessons therefore remain
drafted, despite complete written content and passing available checks.

## 5. Commands and results

| Check | Final result |
|---|---|
| python3 scripts/build_pilot_visuals.py | PASS — reproducibly generated 28 actual SVGs |
| python3 scripts/course_structure.py | PASS — 624 lessons, 98 units, 46 modules; authoring overlay preserved |
| repeat generation + hash comparison | PASS — generated index/tables/assets unchanged |
| python3 scripts/validate_databases.py | PASS — 624 lessons, 100 grammar topics, 30 vocab; schema/CSV widths, metadata/back-references, files, cycles and authored chronology |
| python3 scripts/audit_english_only.py | PASS — 30 actual student-facing files |
| python3 scripts/audit_english_only.py --strict | PASS — same scope; no flagged language or unfinished markers |
| python3 scripts/audit_pilot_batch.py --write-report | PASS — 86 keyed tasks, 48 closed solves, 38 open/model checks; manifests, teaching order, resources, template sections, reading/scopes, objectives and review references |
| python3 -m unittest discover -s scripts -p 'test_*.py' -v | PASS — 33/33 positive and adversarial regression tests |
| resvg rendering of all 28 SVG files | PASS — no renderer errors; author visual inspection of actual diagrams |
| git diff --check | PASS |

Exact content/tool SHA-256 hashes and per-item method lists are in
`P01_QA_RESULTS.json`. Deterministic report files do not manufacture an
independent reviewer or a learner's answers.

### Failed/flagged first passes and repairs

1. Original English guard rejected legitimate middle-dot typography and
   omitted SVGs. Fixed allowlist and coverage; also removed code/arbitrary-
   IPA/fake-README bypasses. Added negative tests instead of weakening checks
   for actual foreign text.
2. Inventory audit flagged repair labels A/B as untaught tokens. Replaced
   them with numeric section references; full lesson-QZ IDs are recognised
   as codes, not a free English word QZ. No article a or instruction word was
   blessed without teaching. All learner headings were tightened to symbols
   or taught words and are now audited too, not broadly exempted.
3. First closed-solver run stripped gap markers and found no candidate for a
   valid R02 item. Fixed parsing and regression-tested it. No false claim
   that this was a learner/content error.
4. Render inspection caught face/name-badge occlusion and an incomplete
   goodbye mouth cue; repaired and rerendered. These were actual teaching
   defects, not acceptable decoration issues.
5. ImageMagick lacked rsvg-convert; CairoSVG could not load system Cairo.
   These optional render paths were unavailable, not final lesson-check
   failures. Resvg was used successfully instead, with dependencies and
   PNG scratch outputs ignored by Git. Core checks remain standard-library.

6. Git diff --check initially flagged the generated CSV's CRLF terminators.
   The generator now emits deterministic LF, and the index is newline-
   normalised. Apart from the two metadata-overlaid rows, all index values
   are unchanged. The persistence test also rejects CR output.

No current mandatory automated check is failing. All remaining work below
is explicitly pending, not silently passed.

## 6. Remaining incomplete / stop condition

1. **Fresh independent reviewer/session** for both lessons and all tasks,
   visual instructions and scope boundaries (CA-05). At least two independent
   zero-English walkthroughs are needed for the complete pilot criterion;
   neither is claimed here. Until sign-off, do not publish to student/ or
   promote statuses.
2. **Recorded, checked audio**. Helper-read scripts are usable, but fully
   autonomous zero-English listening/pronunciation is not delivered by
   silent diagrams or IPA. No recordings/verified durations exist.
3. **Real learner trials**, timing calibration, accessibility and observed
   outcomes. Nothing is tested or mastered without that evidence.
4. **The other ten pilot lessons and unit/module assessments** remain
   unauthored. No next batch has been started. L03 is only a future review
   reservation and corrected vocabulary plan.

The checkpoint's exact next action stays inside **P-01 independent review**.
