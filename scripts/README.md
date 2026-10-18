# Scripts and reproducible checks

Core production/QA scripts use only the Python standard library. Run from
the repository root; no pip/npm installation is required for these checks.

| Script | Purpose |
|---|---|
| `course_structure.py` | Canonical 624-lesson structure; overlays checked `data/lesson_metadata.json` authoring fields and regenerates `LESSON_INDEX.csv` / `docs/STRUCTURE_TABLES.md` without erasing progress. Rejects structural overrides. |
| `validate_databases.py` | Exact CSV headers/widths, unique IDs, generated fields/metadata, introductions/back-references, actual authored files, grammar cycles and prerequisite chronology for authored lessons. Does not claim a content audit of planned files. |
| `audit_english_only.py` | Scans `content/`, `student/`, `assessments/`, including SVG text/descriptions, code and hidden records. Only exact registered IPA/phoneme references are exempt. Character/stopword guard, not universal language identification. `--strict` also rejects unfinished markers, not legitimate response blanks. |
| `build_pilot_visuals.py` | Generates the actual 28 original P-01 SVG illustrations deterministically. No image API, external host or binary assets required. |
| `audit_pilot_batch.py` | P-01 taught-before-use vocabulary/SVG checks; 21-section completeness, grammar scopes, objectives, keys/models, exact review links and resource checks. Closed answers derived without reading keys; open keys checked against rubrics. `--write-report` regenerates the language report and hashed evidence. |
| `test_quality_tools.py` | 33 standard-library tests, including adversarial wrong keys, missing images/keys, future vocabulary/grammar, ninth-word overload, IPA/code bypasses, answer fairness boundaries and metadata persistence. |

## Complete P-01 check sequence

```bash
python3 scripts/build_pilot_visuals.py
python3 scripts/course_structure.py
python3 scripts/validate_databases.py
python3 scripts/audit_english_only.py
python3 scripts/audit_english_only.py --strict
python3 scripts/audit_pilot_batch.py --write-report
python3 -m unittest discover -s scripts -p 'test_*.py' -v
git diff --check
```

Run generation twice and compare the generated index/tables/SVG hashes when
editing the generators. The index uses deterministic LF line endings.
The regression suite checks index idempotence in a
temporary directory, without mutating the working tree.

## Persistent metadata and evidence

Edit `data/lesson_metadata.json` for authored objectives, new inventory IDs,
skills, assessment link, status and notes. Do **not** edit the generated CSV.
Title/ID/sequence/level/path/prerequisite structure cannot be overridden by
the authoring overlay. New inventory IDs must point back from their databases.
Missing/bad metadata is an error, not permission to reset authored progress.

Edit `data/P01_LANGUAGE_MANIFEST.json` when actual scopes, rubrics or objective
mappings change. Introduction markers in the lessons must match. The audit
checks each actual image and all visible heading words at their point of use, rather than assuming everything
in the finished batch was already known at its start.

Generated evidence: `docs/P01_QA_RESULTS.json` (per-item method lists + SHA-256)
and `docs/P01_LANGUAGE_AUDIT.md` (coverage + every reference-label exemption).
The report date is the documented authoring date, not a claim of an observed
learner session. Re-run after any referenced content/tool/data change.

## Visual inspection and limitations

XML parsing, inventory checks and English guard cover the source SVGs. A
separate real renderer and visual inspection are needed for clipping, speech
bubble tails, badge visibility and meaning. S-02 rendered all 28 using resvg
with temporary dependencies under ignored `.cache/`; those tools are not
runtime or core QA dependencies. ImageMagick/Cairo rendering was unavailable
in this sandbox. No PNG caches or installed dependencies are committed.

A tool PASS does not certify naturalness, icon comprehension, audio quality,
learner outcomes or independent review. P-01 remains drafted until the
required fresh reviewer signs off. No learner scores or audio are generated
by any of these scripts.

## Optional PDF conversion

`export_pilot_pdf.cjs` exports the two existing P-01 draft lessons to
combined/individual A4 PDFs, with embedded pictures, expanded scripts/keys
and printable checkboxes. It does not change sources or lesson status.
This optional Node/Chromium tool is separate from the standard-library
Python curriculum checks. See `../exports/README.md` for pinned local-cache
installation, rebuild instructions and PDF QA evidence. No renderer cache
or page-preview image belongs in Git.

## Independent-review packet (not a review)

```bash
python3 scripts/prepare_p01_review.py --html
python3 scripts/prepare_p01_review.py --html --check
python3 -m unittest discover -s scripts -p 'test*.py' -v
```

Extraction/packaging and all 45 tests use Python's standard library. Optional
`--html` uses the same pinned cached markdown-it dependency as the PDF
exporter; the resulting browser files need no runtime/network dependency.
The generator produces one review ZIP; scratch files stay in .cache/. It
never writes lesson/database status or completed reviewer evidence. Only the
dedicated keys, helper script disclosures and hidden machine record are
withheld from derivative views. Do not mistake response-form blanks for
missing lesson content or passing packaging tests for independent review.
See `../docs/P01_INDEPENDENT_REVIEW.md`; source changes require rebuild/review.
