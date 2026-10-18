#!/usr/bin/env python3
"""Prepare a handoff, NOT an independent review or a new lesson batch.

python3 scripts/prepare_p01_review.py --html
Optional HTML uses the existing pinned markdown-it PDF-export dependency.
All extraction, integrity checks, forms and ZIP operations use the stdlib.
Generated scratch files stay in .cache/; only the requested ZIP is retained.
"""
import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ("A0-M1-U1-L01", "A0-M1-U1-L02")
COUNTS = dict(zip(LESSONS, (39, 47)))
ASSET = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
SCRIPT = re.compile(r"<details>\s*<summary>SCRIPT ONLY — no audio recording</summary>\s*([\s\S]*?)\s*</details>")
TASK = re.compile(r"^\| ([HLRABSTWQ]\d{2}) \|", re.M)
EDITION = "2026-10-18"

START = """# P-01 — Independent review handoff

**Status: independent review PENDING. This packet was prepared by the author.**
It is not a sign-off, a completed course or a learner test result.

The user has requested the full 624-lesson A0–C1 + IELTS course, but explicitly
chose to KEEP the existing independent-review gate. Only two lessons are
currently authored. Do not write L03/P-02 or substitute outlines for lessons.
All course material must remain English-only. No new lesson is in this packet.

## 1. Use a genuinely fresh reviewer

Open this packet in a separate conversation/session with a reviewer who has
not seen the existing keys, or give it to a different competent person.
The original author, an author reread and deterministic tools do NOT qualify.
A separate context is required; changing a label does not make a fresh review.
This conversation cannot launch a separate independent Arena session itself.

## 2. Blind response phase — FIRST

1. Open only `blind/A0-M1-U1-L01.html` then `blind/A0-M1-U1-L02.html`.
   If HTML was not built, use the matching Markdown files with image preview.
   HTML copies are self-contained: pictures are embedded, with no network,
   JavaScript, external fonts or separate image downloads required.
2. Render/view the pictures. Do not infer visual clarity from SVG code or
   accessibility descriptions alone. The worked examples remain intentionally
   visible: they teach the language. The dedicated answer section (18),
   helper scripts and hidden machine record (21) have been withheld.
   Original numbering and every other learner section are retained.
3. Respond to **all 39 + 47 = 86 prompt IDs** in `forms/BLIND_RESPONSES.csv`.
   Supply your own response/acceptable alternatives and reasoning before keys.
   Do not copy a keyed answer. Record ambiguity and any required untaught
   word, instruction, grammar or unexplained visual convention by location.
4. For listening, a competent helper may read `helper/` out of view as the
   task input. These are four-line SCRIPTS, not recordings. A model reading
   a script can check script/task logic, NOT audition audio or prove listening
   comprehension. Mark unavailable sound/real-learner evidence NOT ASSESSED.
5. Save a dated copy of the completed CSV and its SHA-256 BEFORE opening keys.
   The supplied response cells are intentionally blank reviewer fields;
   they are not missing lesson content or fabricated learner answers.

Do NOT open `sealed/` Markdown/JSON or the author's prior audit/guide in the
blind phase. The SVG image files under `sealed/source/assets/` are safe visual
inputs (also embedded in HTML); the original lesson Markdown is not blind.
This is procedural separation, not cryptographic access control.

## 3. Unblind and audit — SECOND

Open `sealed/source/` for the exact original lessons and their full section-18
keys/rubrics. Open `sealed/P01_LANGUAGE_MANIFEST.json` and
`sealed/P01_DELIVERY_GUIDE.md` only now. Compare EVERY response against the key:
48 closed items need exact independent solves; 38 open items need checked
models, natural variants and observable rubrics. Do not call a reasonable
alternative wrong merely because the author's model differs.

Then use the procedures, database/index snapshots and template in `reference/`
to audit Gates 1–7: English-only; inventory/dependencies; key integrity;
naturalness; pedagogy; zero-English level fit; and honesty. Verify meaning
at the exact point of first use, including headings, visible SVG words,
alt descriptions and all instruction/action conventions. Prior-lesson word
coverage is not the same as taught-before-use coverage or actual retention.

The seven-gate record in `forms/REVIEW_RECORD.md` is UNFILLED. Record per-lesson
findings and a real reviewer identity/session, date, source checksums,
pre-key response hash, commands, inspected images and evidence for each gate.
Do not pre-populate PASS or approve your own packet as independent evidence.

## 4. Return findings, not invented achievements

Return completed forms plus precise fixes for blockers. Reviewer simulation
is not a real beginner trial. No learner scores/mastery, audio intelligibility,
validation or publication may be inferred from successful tools.

No recordings, beginner trials or independent sign-off have been supplied.
Keep both lessons drafted, leave student/ untouched and keep CA-05 open until
real review evidence exists and blocking findings have been repaired.
A reviewer reports findings; the project lead separately decides validation.
F.7 still requires two independent walkthroughs for the WHOLE 12-lesson pilot;
a review of these two drafts does not complete that requirement.

The ZIP's `PACKET_MANIFEST.json` identifies the exact inputs/files. If source
hashes differ, stop and rebuild; never apply a sign-off to changed material.

## 5. Copy this into a NEW independent session

> You are a fresh reviewer, not the author. Review only P-01 lessons
> A0-M1-U1-L01 and A0-M1-U1-L02 using this packet. Follow START_HERE.md in
> order. First inspect the blind student views and actual rendered pictures;
> independently respond to all 86 prompt IDs and save/hash the responses
> BEFORE opening sealed keys or the author's guide/language manifest.
> Record unavailable audio/learner evidence honestly. Then compare all
> answers/alternatives and audit Deliverable D Gates 1–7. Complete the
> review record with source hashes, per-gate evidence and confusion points.
> If you have already seen keys, disclose that and do not claim a blind solve.
> Do not author new lessons, fabricate sign-offs/scores, publish to student/,
> or switch branches. Return findings and fixes for the project lead.
"""

RECORD = """# Independent P-01 review record — UNFILLED

This is a blank reviewer form, not author/reviewer evidence.

- Reviewer/person or fresh session:
- Independence / prior exposure to keys:
- Review date:
- Packet manifest SHA-256:
- Source hashes reviewed (both lessons):
- Saved pre-key response file and SHA-256:
- Time of blind-response save / time keys opened:
- Actual rendered images inspected:
- Checks run and their results (not inferred):
- Helper/script route used; unavailable evidence:

| Gate | A0-M1-U1-L01 finding/evidence | A0-M1-U1-L02 finding/evidence |
|---|---|---|
| 1 English-only | not reviewed | not reviewed |
| 2 Inventory and first-use dependencies | not reviewed | not reviewed |
| 3 All prompt/key pairs and natural alternatives | not reviewed | not reviewed |
| 4 Naturalness | not reviewed | not reviewed |
| 5 Objectives, practice, checks and recall | not reviewed | not reviewed |
| 6 Zero-English/level fit | not reviewed | not reviewed |
| 7 Honest claims | not reviewed | not reviewed |

## Confusion points and blockers

| Lesson / task / picture / location | Problem and student evidence | Severity | Suggested repair | Recheck evidence |
|---|---|---|---|---|

## Per-lesson recommendation (not a lead validation)

- A0-M1-U1-L01: not reviewed; remains drafted.
- A0-M1-U1-L02: not reviewed; remains drafted.
- Eight-item QZ rubrics: not independently reviewed; no learner score.
- Real beginner trial: not performed.
- Recorded audio: not supplied; not verified.
- Whole-pilot two-walkthrough requirement: not completed.
"""

NODE_RENDER = r"""
const fs=require('node:fs'),path=require('node:path');
const {createRequire}=require('node:module');
const deps=createRequire(path.join(process.argv[1],'.cache/pdf-tools/package.json'));
const MarkdownIt=deps('markdown-it');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const md=new MarkdownIt({html:true,linkify:false,typographer:false});
const original=md.renderer.rules.image;
const icons=new Set(['see.svg','say.svg','write.svg','select.svg','recall.svg','ear.svg']);
md.renderer.rules.image=(tokens,i,options,env,renderer)=>{
 const token=tokens[i],src=token.attrGet('src');
 if(!src.startsWith('../sealed/source/assets/p01/'))throw Error('Unsafe image path');
 const name=path.basename(src),data=input.assets[name];
 if(!data)throw Error('Missing image: '+name);
 token.attrSet('src','data:image/svg+xml;base64,'+data);
 token.attrSet('class',icons.has(name)?'icon':'figure');
 token.attrSet('data-asset',name);
 return original(tokens,i,options,env,renderer);
};
const css=`*{box-sizing:border-box}body{max-width:940px;margin:30px auto;padding:0 25px;
font:19px/1.5 'DejaVu Sans',Arial,sans-serif;color:#203846;background:white}
h1,h2{color:#0f766e}h2{border-top:1px solid #dce7e3;padding-top:15px;margin-top:30px}
table{border-collapse:collapse;width:100%;table-layout:fixed;margin:20px 0}
th,td{border:1px solid #cddcd7;padding:12px;overflow-wrap:anywhere;vertical-align:middle}
th{background:#eaf3ef}table:has(th:nth-child(3)) th:first-child,
table:has(th:nth-child(3)) td:first-child{width:13%}img{max-width:100%}
img.icon{width:32px;height:32px;vertical-align:middle;margin:0 4px}
img.figure{width:600px;max-height:640px;object-fit:contain;vertical-align:middle}
td img.figure{width:100%;max-height:250px}li{margin:10px 0}
input{width:18px;height:18px;vertical-align:middle}blockquote{color:#536d75}
@media(max-width:600px){body{font-size:16px;padding:0 12px;margin:12px auto}
th,td{padding:6px}img.icon{width:24px;height:24px}
table:has(th:nth-child(3)) th:first-child,table:has(th:nth-child(3)) td:first-child{width:20%}}
@media print{@page{size:A4;margin:17mm}body{margin:0;padding:0;font-size:12pt}
h2,h3{break-after:avoid}tr{break-inside:avoid}thead{display:table-header-group}
img.figure{max-height:160mm}td img.figure{max-height:50mm}}`;
const text=input.markdown.replace(/^- \[ \] /gm,'- <input type="checkbox" disabled> ');
process.stdout.write('<!doctype html><html lang="en"><head><meta charset="utf-8">'+
'<meta name="viewport" content="width=device-width,initial-scale=1">'+
'<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'">'+
'<title>'+input.id+' — answer-blind review copy</title><style>'+css+'</style></head><body>'+md.render(text)+'</body></html>');
"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def split_lesson(text, lesson_id):
    """Fail closed on structural drift; never silently leave a key in a view."""
    headings = list(re.finditer(r"^## (\d+)\.[^\n]*(?:\n|$)", text, re.M))
    if [int(m[1]) for m in headings] != list(range(1, 22)):
        raise ValueError(f"{lesson_id}: expected exactly sections 1–21")
    sections = {int(m[1]): text[m.start():headings[i + 1].start() if i + 1 < len(headings) else len(text)]
                for i, m in enumerate(headings)}
    scripts = list(SCRIPT.finditer(sections[9]))
    if len(scripts) != 1 or len(re.findall(r"^\d\. ", scripts[0][1], re.M)) != 4:
        raise ValueError(f"{lesson_id}: expected exactly one four-line helper script")
    ids = TASK.findall("".join(sections[n] for n in range(1, 18)))
    keys = TASK.findall(sections[18])
    if len(ids) != COUNTS[lesson_id] or len(set(ids)) != len(ids) or ids != keys:
        raise ValueError(f"{lesson_id}: duplicate, missing, reordered or unmatched prompt/key IDs")
    visible = text[:headings[0].start()] + "".join(
        SCRIPT.sub("", sections[n]) if n == 9 else sections[n]
        for n in [*range(1, 18), 19, 20])
    visible = re.sub(r"<!--[\s\S]*?-->", "", visible)
    for source in ASSET.findall(visible):
        if not re.fullmatch(r"assets/p01/[a-z0-9-]+\.svg", source):
            raise ValueError(f"{lesson_id}: unsafe image {source}")
    visible = visible.replace("(assets/p01/", "(../sealed/source/assets/p01/")
    if "<details" in visible or "SCRIPT ONLY" in visible or re.search(r"^## (18|21)\.", visible, re.M):
        raise ValueError(f"{lesson_id}: residual protected disclosure/record")
    return visible, scripts[0][1].strip() + "\n", ids


def render_html(lesson_id, text, assets):
    payload = {"id": lesson_id, "markdown": text,
               "assets": {name: base64.b64encode(data).decode("ascii") for name, data in assets.items()}}
    result = subprocess.run(["node", "-e", NODE_RENDER, str(ROOT)],
                            input=json.dumps(payload), text=True, capture_output=True, timeout=30)
    if result.returncode:
        raise RuntimeError("HTML rendering needs the pinned markdown-it dependency; see exports/README.md.\n" + result.stderr)
    return result.stdout.encode("utf-8")


def archive_bytes(files):
    """Deterministic, relative-only ZIP. No timestamps, credentials or caches."""
    result = io.BytesIO()
    with zipfile.ZipFile(result, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            if name.startswith("/") or ".." in Path(name).parts or "\\" in name:
                raise ValueError(f"Unsafe archive path: {name}")
            info = zipfile.ZipInfo(name, (2026, 10, 18, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return result.getvalue()


def build(include_html=False):
    files = {"START_HERE.md": START.encode(), "forms/REVIEW_RECORD.md": RECORD.encode()}
    inputs = {}
    assets = {}
    rows = []
    def add_source(source, destination):
        data = (ROOT / source).read_bytes()
        inputs[source] = sha(data)
        files[destination] = data
        return data
    for asset in sorted((ROOT / "content/A0/assets/p01").glob("*.svg")):
        assets[asset.name] = add_source(str(asset.relative_to(ROOT)), "sealed/source/assets/p01/" + asset.name)
    if len(assets) != 28:
        raise ValueError("P-01 packet expects the existing 28 unique SVGs")
    for lesson_id in LESSONS:
        original = add_source(f"content/A0/{lesson_id}.md", f"sealed/source/{lesson_id}.md")
        blind, script, ids = split_lesson(original.decode(), lesson_id)
        for match in ASSET.finditer(blind):
            if Path(match[1]).name not in assets:
                raise ValueError("Missing referenced picture: " + match[1])
        files[f"blind/{lesson_id}.md"] = blind.encode()
        if include_html:
            files[f"blind/{lesson_id}.html"] = render_html(lesson_id, blind, assets)
        files[f"helper/{lesson_id}-script.md"] = (
            f"# {lesson_id} — helper input\n\nSCRIPT ONLY — no audio recording\n\n"
            "Read out of the learner's view. This is input, not learner evidence.\n\n" + script).encode()
        rows.extend([lesson_id, task_id, "", "", "", "not reviewed"] for task_id in ids)
    for source, destination in {
        "docs/DELIVERABLE_A_HIGH_LEVEL_MAP.md": "reference/DELIVERABLE_A_HIGH_LEVEL_MAP.md",
        "docs/DELIVERABLE_C_TRACKING_SCHEMAS.md": "reference/DELIVERABLE_C_TRACKING_SCHEMAS.md",
        "docs/DELIVERABLE_D_GENERATION_QA.md": "reference/DELIVERABLE_D_GENERATION_QA.md",
        "docs/DELIVERABLE_F_PILOT_PLAN.md": "reference/DELIVERABLE_F_PILOT_PLAN.md",
        "templates/LESSON_TEMPLATE.md": "reference/LESSON_TEMPLATE.md",
        "GRAMMAR_DATABASE.csv": "reference/GRAMMAR_DATABASE.csv",
        "VOCABULARY_DATABASE.csv": "reference/VOCABULARY_DATABASE.csv",
        "LESSON_INDEX.csv": "reference/LESSON_INDEX.csv",
        "data/P01_LANGUAGE_MANIFEST.json": "sealed/P01_LANGUAGE_MANIFEST.json",
        "docs/P01_DELIVERY_GUIDE.md": "sealed/P01_DELIVERY_GUIDE.md",
    }.items():
        add_source(source, destination)
    inputs["scripts/prepare_p01_review.py"] = sha(Path(__file__).read_bytes())
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["lesson_id", "prompt_id", "reviewer_response_before_keys", "acceptable_variants", "reason_or_confusion", "review_state"])
    writer.writerows(rows)
    files["forms/BLIND_RESPONSES.csv"] = output.getvalue().encode()
    manifest = {"packet_edition": EDITION, "scope": list(LESSONS),
                "independent_review": "PENDING — author-prepared handoff only",
                "lesson_status": "drafted", "new_lessons_authored": 0,
                "prompt_rows": len(rows), "unique_original_pictures": len(assets),
                "self_contained_html": include_html, "inputs_sha256": inputs,
                "files_sha256": {name: sha(data) for name, data in sorted(files.items())}}
    files["PACKET_MANIFEST.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", action="store_true", help="include self-contained browser views (optional pinned markdown-it)")
    parser.add_argument("--check", action="store_true", help="verify the retained ZIP matches a fresh deterministic build")
    args = parser.parse_args()
    files = build(args.html)
    archive = archive_bytes(files)
    target = ROOT / "exports/P-01-Independent-Review.zip"
    if args.check:
        if not target.exists() or target.read_bytes() != archive:
            raise SystemExit("FAIL: review ZIP is stale, missing or built with different options")
        print("PASS: retained review ZIP exactly matches sources, forms and deterministic build.")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive)
        scratch = ROOT / ".cache/p01-review"
        for name, data in files.items():
            destination = scratch / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        print(f"Prepared {target.relative_to(ROOT)}: {len(files)} files, {len(archive)} bytes, 86 blank reviewer rows.")
    print("Independent review STILL PENDING. No new lesson, status promotion, audio or learner result.")


if __name__ == "__main__":
    main()
