# Deliverable C — Vocabulary and Grammar Tracking Schemas

How introduction, practice, recall, independent use, and mastery are recorded
— the memory of the whole system. Schemas are enforced by
`scripts/validate_databases.py`; status meanings are normative (authors and
all future tooling must follow them).

## C.1 Design principles

1. **One row, one learning target.** A vocabulary row = one headword + one
   sense. A grammar row = one topic usable in communication. Distinct senses
   (e.g. *book* noun vs verb) get distinct rows and IDs.
2. **Status is evidence-based.** Status advances only on recorded evidence,
   never on exposure. Appearing in a lesson ≠ learned.
3. **Introduction is single; encounters are multiple.** `intro_lesson_id` is
   the one lesson that first teaches the item. Later encounters are logged in
   `review_history` / `practice_lessons` / `review_lessons`.
4. **Production is separate from recognition.** Receptive success and
   productive success are tracked as different evidence types.
5. **Mastery is durable.** It requires spaced retrievals including a delayed
   (≥7-day) success plus assessment evidence.

## C.2 VOCABULARY_DATABASE.csv schema

| Column | Type | Rules |
|---|---|---|
| `vocab_id` | `V%04d` | Unique, never reused, assigned in introduction order. |
| `headword` | text | Dictionary form (or taught chunk, e.g. *thank you*). |
| `part_of_speech` | enum | noun / verb / adjective / adverb / determiner / pronoun / preposition / conjunction / interjection / article / question word / phrase / other. |
| `phonemic_transcription` | IPA in `/…/` | Required from A1 up; A0 uses modeled pronunciation first, IPA added at A0 review. |
| `audio_status` | enum | `script-only` until a recording exists and is verified; then `verified:<file>:<seconds>`. Never claim audio otherwise. |
| `sense_number` | int | 1, 2, 3… per headword; each sense is its own row. |
| `meaning_simple_english` | text | Definition using only previously known language. Required. |
| `level` | enum | A0/A1/A2/B1/B2/C1/IE — the level of introduction. |
| `intro_lesson_id` | lesson ID | Must exist in `LESSON_INDEX.csv`. |
| `example_1`, `example_2` | text | Real communicative sentences at/below level. |
| `collocations` | `;`-separated | Most useful 2–5 chunks (empty only if genuinely none). |
| `grammar_patterns` | `;`-separated | E.g. `enjoy + -ing`; `too + adj + to`. |
| `synonyms` / `antonyms` | `;`-separated | Only items at/below level, or marked `(later)`. |
| `word_family` | `;`-separated | Related forms with level marks, e.g. `decide (A2); decision (B1)`. |
| `register_notes` | text | formal/informal/polite/spoken/written/academic as applicable. |
| `common_mistakes` | text | The 1–3 most likely learner errors. |
| `status` | enum | `planned → introduced → practiced → recalled → used → assessed → mastered`. |
| `review_history` | log | `lesson_id:result` entries, e.g. `A1-M1-U1-L07:recall-ok`. |
| `mastery_evidence` | log | Pointers to the evidence items in §C.4. |
| `notes` | text | Internal remarks. |

### Vocabulary status transitions (all require logged evidence)

| From → To | Required evidence |
|---|---|
| planned → introduced | Lesson taught the item explicitly (meaning + form + example). |
| introduced → practiced | ≥2 correct uses in controlled exercises (different lessons). |
| practiced → recalled | ≥1 correct retrieval *without* visible support (active-recall task). |
| recalled → used | ≥1 correct productive use (speaking/writing) in a new context. |
| used → assessed | Correct on a dedicated assessment item (unit test or above). |
| assessed → mastered | Full mastery set in §C.4 satisfied. No exceptions. |

## C.3 GRAMMAR_DATABASE.csv schema

| Column | Type | Rules |
|---|---|---|
| `grammar_id` | `G%03d` | Unique, never reused. Current range G001–G100. |
| `topic` / `sub_structure` | text | Human-readable scope of the row. |
| `level` | enum | Level of introduction. |
| `intro_lesson_id` | lesson ID | Must exist in `LESSON_INDEX.csv`. |
| `prerequisites` | `|`-separated G-IDs | Must exist; no self-reference; chains in Deliverable B §B.8. |
| `communicative_purpose` | text | What the learner can *do* with it (first line of every grammar lesson). |
| `affirmative_example` / `negative_example` / `interrogative_example` | text | Canonical at-level examples; `(rare)` / `(not applicable)` where honest. |
| `common_errors` | text | Top confusions with corrections. |
| `confused_with` | G-IDs/topics | Nearest neighbours taught contrastively. |
| `practice_lessons` / `review_lessons` | lesson IDs | Where the topic is drilled and later retrieved. |
| `assessment_status` | enum | `planned` / `assessed` / `mastered`. |
| `status` | enum | `planned → introduced → practiced → assessed → mastered`. |

### Grammar status transitions

| From → To | Required evidence |
|---|---|
| planned → introduced | Taught with purpose + form + affirmative/negative/question coverage. |
| introduced → practiced | ≥80% accuracy on a controlled mixed set (≥10 items, new sentences). |
| practiced → assessed | Correct spontaneous use in a speaking/writing task + a test item correct. |
| assessed → mastered | Full mastery set in §C.5 satisfied. |

## C.4 Vocabulary mastery criteria (all required)

1. **Three spaced successful retrievals**, at least one delayed ≥7 days after
   introduction, logged in `review_history`.
2. **One productive success** (speaking or writing, new context), logged.
3. **One assessment success** (unit test item or higher), logged.
4. **No unresolved error pattern** for the item in the error log.

## C.5 Grammar mastery criteria (all required)

1. **Controlled accuracy** ≥80% on a mixed ≥10-item set of *new* sentences.
2. **Meaningful use**: correct spontaneous use in a speaking or writing task.
3. **Contrast control**: correctly chooses the structure against its
   `confused_with` neighbour in ≥3 of 4 discrimination items.
4. **Delayed check**: a ≥7-day-later mixed review set at ≥80%.

## C.6 LESSON_INDEX.csv schema (tracking side)

Full column list is defined in `scripts/course_structure.py`
(`LESSON_INDEX_HEADER`). Tracking-relevant columns:

| Column | Rules |
|---|---|
| `lesson_id` / `global_seq` | Generated; immutable once published. |
| `prerequisites` | Previous lesson (linear chain) or previous level test at level starts. |
| `new_vocab_ids` / `new_grammar_ids` | Filled at authoring; must have matching database rows pointing back. |
| `assessment_id` | Set on review lessons (unit tests). |
| `validation_status` | `planned → drafted → reviewed → validated → tested`. |

Validation-status rules:

- `drafted`: complete file exists from the template; databases updated.
- `reviewed`: passed unknown-language check, English-only audit, key check,
  and naturalness read by a second pass (human or independent model pass
  with a recorded checklist — see Deliverable D).
- `validated`: reviewer sign-off recorded in `QUALITY_AUDIT.md`; lesson may
  ship to `student/`.
- `tested`: only after observed use by real beginner learners with notes
  filed. **Never claim without evidence.**

## C.7 Spaced-repetition schedule

Default adaptive schedule (intervals from last *successful* retrieval;
any failure resets to the next-day slot and logs an error code):

| Success streak | Next interval |
|---|---|
| 0 (just learned) | next lesson |
| 1 | +1 day |
| 2 | +3 days |
| 3 | +7 days |
| 4 | +21 days |
| 5+ | +60 days, then maintenance in cumulative tests |

Retrieval formats rotate: flashcard both directions → gap-fill →
contextual production → listening recognition → mixed-set discrimination.
Every lesson's §19 Review Plan names the exact slots and tasks; the
scheduler is recorded per item in `review_history`.

## C.8 Error taxonomy (codes for the error log)

| Prefix | Category | Examples |
|---|---|---|
| VOC-FORM | word form/spelling | `V0018: books not bookes` |
| VOC-MEAN | wrong meaning/sense | `book (verb) for reserve` |
| VOC-COLLOC | collocation | `do a mistake` |
| VOC-REG | register | `thanks` in a formal letter |
| GRAM-TENSE | tense/aspect choice | present for past narrative |
| GRAM-AGR | agreement | `she go` |
| GRAM-ART | articles | missing/generic `the` |
| GRAM-WO | word order | `where you live?` |
| GRAM-PREP | prepositions | `in Monday` |
| L-MAIN / L-DETAIL / L-INF | listening | main idea / detail / inference |
| R-MAIN / R-DETAIL / R-INF / R-REF | reading | + reference/cohesion |
| S-FLU / S-ACC / S-PRON | speaking | fluency / accuracy / pronunciation |
| W-ORG / W-COH / W-ACC / W-TASK | writing | organization / cohesion / accuracy / task response |

Repeated codes (≥3 in a window) trigger targeted repair tasks before new
material continues (see ASSESSMENT_REGISTER.md remediation rules).

## C.9 Worked example (vocabulary)

`V0013 name`: introduced A0-M1-U1-L01 (status `introduced`). Controlled
practice in L02/L04 (`practiced`). Retrieved cold in L06 recall round
(`recalled`). Used in L04 speaking ("My friend's name is…") (`used`).
Correct in unit test A0-U01-T (`assessed`). Delayed mixed set + productive
writing success at +9 days → `mastered`, evidence logged. Any later test
failure demotes to `assessed` with a repair task — mastery is revocable.
