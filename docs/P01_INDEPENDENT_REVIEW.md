# P-01 independent-review handoff — NOT a review result

**2026-10-18 · S-04 · independent review PENDING.**

The user requested the complete 624-lesson A0–C1 + IELTS course and explicitly
chose **keep the independent-review gate**, rather than advance with unreviewed
drafts. Only the existing two lessons are authored; the other 622 are not.
No L03/P-02, validation or student publication was started in this session.

## Download and use in a fresh session

**[Download the self-contained review packet](../exports/P-01-Independent-Review.zip).**

1. Extract the ZIP. Start with `START_HERE.md` in a **new independent
   conversation/session**, or give the packet to a different competent reviewer.
   This author conversation cannot provide its own independent sign-off or
   launch a separate Arena conversation on the user's behalf.
2. Use the two answer-blind HTML files under `blind/`. They open locally in
   a browser, with all pictures embedded and no network/scripts/external fonts.
   Matching Markdown and the 28 original SVGs are included too.
3. Save answers/reasoning to all **86 prompts** using
   `forms/BLIND_RESPONSES.csv` **before reading the sealed keys**. The forms are
   intentionally unfilled. Worked teaching examples remain visible; only
   section 18 (keys), section 21 (hidden machine record), and helper script
   disclosures were removed from these derivative review views.
4. A competent helper can use `helper/` as listening input, out of view.
   These are scripts, not audio. A text-only reviewer cannot claim to have
   heard speech, assessed a real learner or validated sound intelligibility.
5. After saving and hashing the blind responses, open `sealed/` for the
   unchanged source lessons/keys, language manifest and helper guide. Use
   `reference/` for procedures, level profile, databases/index and template.
6. Complete `forms/REVIEW_RECORD.md` with real reviewer/session details,
   source hashes, per-lesson Gates 1–7 evidence, findings and required fixes.
   Return the completed forms/results to this project. Do not overwrite the
   generated blank packet with completed evidence: save it separately, e.g.
   `reviews/P01/<actual-reviewer-session>/` or attach it to this conversation.

Do not use the already-expanded full PDFs for the blind phase: they include
keys. Separation in this packet is procedural, not an encryption/security
barrier. Opening answer-bearing source/manifest/guide first invalidates a
claim of an unexposed blind solve.

## Prompt to give the new reviewer

> You are a fresh reviewer, not the author. Open START_HERE.md in this packet
> and follow it in order. Review only A0-M1-U1-L01 and A0-M1-U1-L02. First
> inspect the blind student views and actual rendered pictures, independently
> respond to all 86 IDs, then save/hash the responses before opening sealed
> keys or the author's guide/manifest. Record unavailable audio or learner
> evidence as not assessed. Then compare every answer and natural variant,
> audit Deliverable D Gates 1–7, and complete the review record with exact
> locations, source hashes and blockers/fixes. Disclose any prior key exposure.
> Do not author new lessons, switch branches, invent scores/sign-offs or
> publish to student/. Return findings for the project lead's decision.

## What passed — packaging only

The ZIP has 50 entries, two offline HTML views, all original pictures and
39/47 blank reviewer rows. Automated checks verify extraction, absence of
keys/scripts/machine records in blind views, unchanged other lesson content,
all images, desktop/mobile bounds, ZIP integrity, exact hashes and reproducible
build. All **45 tests** pass: 33 existing quality-tool tests + 12 packaging
tests. All 41 prior content/tool hashes and all three lesson PDFs are unchanged.
Details: [`../exports/P01_REVIEW_PACKET_QA.json`](../exports/P01_REVIEW_PACKET_QA.json).

These are author/tool transport checks, **not independent Gates 1–7 results**.
Both lessons remain drafted; CA-05 is open. No recordings, real-beginner
trial, learner score or mastery evidence has been added. Two fresh whole-pilot
walkthroughs remain required later under F.7; this two-lesson packet cannot
satisfy that whole-pilot requirement.

## Reproduce or verify

```bash
# Optional HTML requires the pinned markdown-it dependency in exports/README.md.
python3 scripts/prepare_p01_review.py --html
python3 scripts/prepare_p01_review.py --html --check
python3 -m unittest discover -s scripts -p 'test*.py' -v
```

The builder does not edit lessons or databases. It retains one ZIP in exports/;
extracted working files and screenshots stay under ignored .cache/p01-review/.
A changed source requires rebuilding and a fresh review of the new hashes.

## Exact S-04 repository changes

Created:

- `docs/P01_INDEPENDENT_REVIEW.md`
- `exports/P-01-Independent-Review.zip`
- `exports/P01_REVIEW_PACKET_QA.json`
- `scripts/prepare_p01_review.py`
- `scripts/test_review_packet.py`

Updated:

- `PROJECT_CHECKPOINT.md`
- `PROJECT_MASTER.md`
- `QUALITY_AUDIT.md`
- `exports/README.md`
- `scripts/README.md`

No lesson, SVG source, database, index, assessment, status or existing PDF changed.
No files deleted. Intermediate packet copies/screenshots are ignored, not course files.
