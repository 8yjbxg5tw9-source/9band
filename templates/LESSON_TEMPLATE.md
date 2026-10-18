# Lesson Template (INTERNAL — guides authors; not shown to students as-is)

Every student-facing lesson is authored from this template. Section headings in
[BRACKETS] are author guidance and must be replaced by real student-facing
content. Nothing in the final lesson may violate the English-only rule.

> Authoring template **T-1.1 (2026-10-18, P-01)**.

## Zero-English adaptation (mandatory at A0 entry)

- Keep all 21 learner sections below, but replace abstract prose explanations
  and directions with **actual supplied pictures, demonstrated action
  symbols, known/new word contrasts and worked responses**. Headings may be
  reference-only; do not require their comprehension.
- Do not use look/listen/repeat/choose/read/write/say/book as assumed
  instructional vocabulary. Teach a word explicitly within the A0 cap, or
  demonstrate its action without the English label first.
- Supply the images, not just prose describing images to be made later.
  Check rendered text, speech-bubble tails, perspective and all prompt images.
- Log before-use vocabulary markers, exact scopes and all navigation/IPA/
  accessibility exceptions. No load-bearing prose can be declared incidental.
  Report both entry/prior-lesson and point-of-use reading coverage.
- One main new frame; supporting references or fixed-chunk previews require
  explicit instruction and scoped database records. Deferred grammar is
  not available merely because its broad topic has a first-introduction row.
- Early copying is shape copying, not assumed alphabet knowledge. Names,
  case, punctuation and accent must not become unstated assessment targets.
- Keep complete keys/rubrics; use known-language frame cues where a complete
  form is demanded. Put complex helper/scoring directions in a clearly
  internal guide, not as untaught student instructions.
- Script-only sound work requires a competent helper. Mouth diagrams/IPA
  alone are not recorded audio or a fully independent sound-learning route.
- An author reread or deterministic solver is not a fresh independent review.
  Without that review, keep status drafted and student/ unpublished.

---

# {LESSON_ID}: {Title}

> Level: {A0|A1|A2|B1|B2|C1|IE} · Module {m}: {module title} · Unit {u}: {unit theme}
> Lesson {n} of {unit length} · Type: {lesson_type} · Time: {minutes}

## 1. Before You Start (Prerequisites)

- You can already: {list of abilities, each referencing a past lesson ID}.
- Words you need: {list, all previously introduced}.

## 2. In This Lesson (Objectives)

After this lesson, you can:

1. {observable ability 1}
2. {observable ability 2}
3. {observable ability 3}

## 3. Words and Language You Need

[Table of previously learned language this lesson depends on. Every item must
already be introduced in the vocabulary/grammar databases.]

## 4. New Language

### New words

| Word | Say it | What it means | Example |
|---|---|---|---|
| {headword} | /{IPA}/ | {simple English meaning} | {example sentence} |

[Maximum new words per lesson: A0–A1: 8; A2: 10; B1: 12; B2–C1: 15; IE: 15.
Every new word gets a vocab_id and a database row.]

### New grammar

[One main structure per lesson. State the communicative purpose first, then the
form. Show affirmative, negative, and question forms where they exist.]

## 5. Situation

[A meaningful context: picture description, story opening, dialogue setting, or
task scenario. At A0–A1 this section carries most of the meaning — specify the
exact images, objects, or actions.]

## 6. Explanation

[Clear English explanation using only known language plus the new items above.
Short sentences. One idea per paragraph. Contrast with known language.]

## 7. Examples

[Carefully sequenced examples: 2 trivially easy → 3 typical → 2 challenging.
Mark stress/important words where useful.]

## 8. Pronunciation

[Target sounds, word stress, sentence stress, or connected speech. Include
minimal pairs, chants, or drills. State audio status: script-only until audio
is recorded and verified.]

## 9. Listening

[Script reference or inline script at the right level + tasks: main idea,
detail, inference. State replay procedure. Label scripts as scripts.]

## 10. Reading

[Controlled text + tasks: main idea, detail, words in context, inference.
Record the percentage of known words; target ≥95% known at A0–B1, ≥90% at
B2–C1, authentic at IE with glossed support.]

## 11. Exercises A — Controlled Practice

[Recognition and form practice: match, choose, complete, order. 6–10 items.]

## 12. Exercises B — Meaningful Practice

[Contextual use: complete dialogues, answer about yourself, decide, compare.
4–8 items.]

## 13. Speaking

[Task with roles/steps, useful phrases (known language), model exchange, and a
self-check list. Recording + self-review instructions where supported.]

## 14. Writing

[Guided task: model → plan → write → check. Word/sentence targets by level.
Editing checklist.]

## 15. Remember (Active Recall)

[5–8 questions answered WITHOUT looking back. Mix: today's words, today's
grammar, one item from a past lesson (spaced retrieval).]

## 16. Mistakes to Avoid

[2–5 common errors with WRONG → RIGHT corrections and one-line reasons.]

## 17. Lesson Check (Short Assessment)

[5–10 items covering objectives. Linked assessment_id. Pass mark stated.]

## 18. Answer Key

[Every answer with a short explanation where useful. Keys are verified against
the questions before release — see Deliverable D.]

## 19. Review Plan

[When this lesson's items return: next lesson + 3-day + 7-day + 21-day slots,
with the exact retrieval task each time.]

## 20. Mastery Checklist

- [ ] I can {objective 1}
- [ ] I can {objective 2}
- [ ] I can {objective 3}
- [ ] I scored ≥ {pass mark} on the Lesson Check

## 21. New Language Record

[Machine-readable footer. Author must fill it exactly.]

```text
NEW_VOCAB: V0001, V0002
NEW_GRAMMAR: G004
REVIEWED_VOCAB: (ids)
REVIEWED_GRAMMAR: (ids)
```

---

## Author checklist (delete before publishing to students)

- [ ] All language checked against the learning inventory (Deliverable D, step 3).
- [ ] New items added to the databases with this lesson as intro_lesson_id.
- [ ] English-only audit passed (`audit_english_only.py`).
- [ ] Answer key verified by a second pass.
- [ ] Objectives match the Lesson Check items one-to-one.
