# P-01 PDF exports — the two existing draft lessons

Requested printable/downloadable conversion, 2026-10-18. The lesson sources
and all 28 original pictures are unchanged. This is not a new lesson batch
or an independent validation/publication sign-off.

| PDF | Contents | A4 pages |
|---|---|---:|
| [P-01-Lessons-1-and-2.pdf](P-01-Lessons-1-and-2.pdf) | Both lessons, in order | 43 |
| [A0-M1-U1-L01.pdf](A0-M1-U1-L01.pdf) | First lesson only | 20 |
| [A0-M1-U1-L02.pdf](A0-M1-U1-L02.pdf) | Second lesson only | 23 |

## Included and checked

- All actual teaching, explanations, examples, pictures, exercises,
  pronunciation guidance, recall/review plans and checklists.
- All **86 prompt/key pairs**, including the complete answer keys.
- Both four-line helper-read listening scripts. Disclosures that were
  collapsible in Markdown are **expanded** in the PDFs, never omitted.
  Keep scripts/keys covered when doing a task, as demonstrated in the lessons.
- Embedded vector illustrations and Unicode fonts; no internet connection
  or separately downloaded picture files are needed to read/print the PDFs.
- Selectable text, document bookmarks, page numbers and printable blank
  checkboxes. Main text/IPA/symbols were checked for missing glyphs.
- Machine-only section 21 and its hidden language-record footer are not
  printed. The original source records remain intact; no learner work is
  removed. The only added visible reference label is the DRAFT/page footer.

HTML checks verified all source sections, 39/47 answer rows, four script
lines per lesson and every image load. PDF checks verified A4 dimensions,
all prompt IDs and key IDs, every learner-section heading (1–20), IPA,
selectable text, page boundaries and absence of blank pages. All pages were
rendered to an inspection sheet; representative pages were reviewed at
reading size. All 41 previous content/data/tool evidence hashes still match.
Details and artifact SHA-256 hashes: `PDF_EXPORT_QA.json`.

## Status remains honest

These are **draft export copies**, not validated copies in student/. No
independent lesson review, real-learner evidence or new lesson is claimed.
There is no recorded audio; listening/pronunciation still needs a competent
helper. Generating a PDF does not change any curriculum or mastery status.

## Rebuild (optional export toolchain)

The core Python curriculum checks still use only the standard library.
PDF conversion additionally uses Node.js 22.17+ and these pinned packages,
installed under an ignored local cache, not as course/runtime dependencies:

```bash
npm install --prefix .cache/pdf-tools --no-audit --no-fund \
  @sparticuz/chromium@153.0.0 puppeteer-core@25.14.0 markdown-it@15.0.3
node scripts/export_pilot_pdf.cjs
```

DejaVu Sans regular/bold fonts must be installed at
`/usr/share/fonts/truetype/dejavu/`. The exporter loads the bundled local
Chromium libraries for minimal Linux sandboxes; no external image/font/browser
host is needed. Intermediate HTML, renderer packages and PNG previews stay
under ignored .cache/ (temporary Chromium extraction is also untracked).

Rebuilding updates the three PDFs. Rerun PDF inspection and refresh
`PDF_EXPORT_QA.json` if the PDFs or source content change; timestamps can
change a PDF's checksum even when the lesson content is identical. PDF
binaries are kept here because they are the specifically requested deliverable.

## Separate independent-review handoff (S-04)

[`P-01-Independent-Review.zip`](P-01-Independent-Review.zip) is NOT another
course PDF or a completed review. It contains answer-blind offline browser/
Markdown views of the SAME two drafts, separate scripts/original keys,
28 original SVGs, 86 blank reviewer rows, an unfilled gate record and reference
snapshots/checksums. The user chose to keep the review gate before more
lessons are authored. Use a new independent reviewer/session and follow
[`../docs/P01_INDEPENDENT_REVIEW.md`](../docs/P01_INDEPENDENT_REVIEW.md).
Packaging-only evidence: `P01_REVIEW_PACKET_QA.json`. All three original PDFs
above remain unchanged; neither new authoring nor validation is claimed.
