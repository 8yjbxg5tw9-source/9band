#!/usr/bin/env python3
"""P-01 inventory, resource, template, question/key and scope audit.

Closed items are solved from student prompts, options, scripts and picture
facts BEFORE their keys are read. Open tasks are checked against declared
rubrics and displayed models; this is not automatic scoring of a learner.
Picture facts are author-supplied semantics, not computer vision or an
independent reviewer. A separate reviewer/session is still required by D.8.
All functionality uses the Python standard library.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from audit_english_only import APPROVED_IPA, audit_file, strip_exempt
from course_structure import authored_lessons

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/P01_LANGUAGE_MANIFEST.json"
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
TOKEN = re.compile(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b")
ITEM_ID = re.compile(r"^[HLRABSW TQ]\d{2}$".replace(" ", ""))
COMMENT = re.compile(r"<!--.*?-->", re.S)


def without_comments(text):
    return COMMENT.sub(lambda m: "\n" * m.group().count("\n"), text)


def plain(text):
    text = IMAGE.sub(" ", text)
    text = re.sub(r"<[^>]*>", " ", text)
    return re.sub(r"[*`]", "", text).strip()


def normal(text):
    return " ".join(TOKEN.findall(plain(text).lower()))


def sections(text):
    matches = list(re.finditer(r"^## (\d+)\. .*", text, re.M))
    found = {}
    for i, match in enumerate(matches):
        number = int(match[1])
        if number in found:
            raise ValueError(f"Duplicate section {number}")
        found[number] = text[match.end():matches[i+1].start() if i+1 < len(matches) else len(text)]
    return found


def table_rows(text):
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [part.strip() for part in line.strip().strip("|").split("|")]
            if cells and ITEM_ID.fullmatch(cells[0]):
                yield cells


def parse_tasks(text):
    parts = sections(text)
    tasks = {}
    for number, body in parts.items():
        if number == 18:
            continue
        for cells in table_rows(body):
            if len(cells) != 3 or cells[0] in tasks:
                raise ValueError(f"Malformed/duplicate task: {cells[0]}")
            tasks[cells[0]] = {"id": cells[0], "prompt": cells[1], "response": cells[2], "section": number}
    keys = {}
    for cells in table_rows(parts.get(18, "")):
        if len(cells) != 2 or cells[0] in keys:
            raise ValueError(f"Malformed/duplicate key: {cells[0]}")
        keys[cells[0]] = cells[1]
    scripts = dict(re.findall(r"^([1-4])\. (.+)$", parts.get(9, ""), re.M))
    return parts, tasks, keys, scripts


def scene(prompt):
    images = IMAGE.findall(prompt)
    if any(path.endswith("/meet.svg") for path in images):
        return "meet"
    if any(path.endswith("/leave.svg") for path in images):
        return "leave"
    return None


def valid_frame(value):
    words = normal(value)
    return bool(re.fullmatch(r"(?:i am|you are|my name is|your name is) (?:anna|tom)", words)
                or words == "what is your name")


def solve_closed(task, scripts, reading):
    """Derive an answer; never access an answer-key value here."""
    prompt, response = task["prompt"], task["response"]
    options = [value.strip() for value in response.split(" / ")]
    if len(options) != 2:
        raise ValueError(f"{task['id']}: closed task needs two options")
    rendered = plain(prompt)
    matches = []
    if task["id"].startswith("L"):
        index = re.search(r"\b([1-4])\s*→", rendered)
        if not index or index[1] not in scripts:
            raise ValueError(f"{task['id']}: missing script line")
        heard = normal(scripts[index[1]])
        for option in options:
            candidate = normal(option)
            if option in {"P1", "P2"}:
                expected = "P1" if heard.split()[0] in {"hello", "hi"} else "P2"
                if option == expected:
                    matches.append(option)
            elif candidate and re.search(r"\b" + re.escape(candidate) + r"\b", heard):
                matches.append(option)
    elif options == ["P1 → P2", "P2 → P1"]:
        utterances = [line.split(":", 1)[-1].strip() for line in reading.splitlines() if line.strip()]
        first, last = normal(utterances[0]).split()[0], normal(utterances[-1]).split()[0]
        if first in {"hello", "hi"} and last in {"bye", "goodbye"}:
            matches.append("P1 → P2")
        elif first in {"bye", "goodbye"} and last in {"hello", "hi"}:
            matches.append("P2 → P1")
    elif "? →" in rendered:
        matches = [value for value in options if normal(value) == "what is your name"]
    elif {normal(value) for value in options} <= {"hello", "hi", "goodbye", "bye"}:
        meaning = scene(prompt)
        if meaning is None:
            first = normal(rendered).split()[0]
            meaning = "meet" if first in {"hello", "hi"} else "leave" if first in {"goodbye", "bye"} else None
        acceptable = {"hello", "hi"} if meaning == "meet" else {"goodbye", "bye"} if meaning == "leave" else set()
        matches = [value for value in options if normal(value) in acceptable]
    else:
        # The only productive forms permitted in these two lessons are identity
        # frames and the exact, taught name-request chunk.
        stem = rendered.split(":", 1)[-1].strip()
        for option in options:
            filled = stem.replace("___", option)
            if not valid_frame(filled):
                continue
            if "my-anna.svg" in prompt and not normal(filled).startswith("my name"):
                continue
            if "your-tom.svg" in prompt and not normal(filled).startswith("your name"):
                continue
            # Reading referent: Tom addresses Anna; my would identify Tom,
            # whereas the visible utterance identifies Anna.
            if "Tom → Anna:" in rendered and normal(filled).startswith("my name"):
                continue
            matches.append(option)
    if len(matches) != 1:
        raise ValueError(f"{task['id']}: expected exactly one independently derived option, got {matches}")
    return matches[0]


def validate_open(task, key, rubric):
    """Check model/accepted-answer integrity, not an imaginary learner result."""
    value = normal(key)
    checks = {
        "greet": lambda: {"hello", "hi"} <= set(value.split()) and not ({"goodbye", "bye"} & set(value.split())),
        "leave": lambda: {"goodbye", "bye"} <= set(value.split()) and not ({"hello", "hi"} & set(value.split())),
        "self": lambda: "I am ___." in key and "i are" not in value,
        "you-tom": lambda: value == "you are tom",
        "name-self": lambda: "My name is ___." in key,
        "name-you-tom": lambda: value == "your name is tom",
        "name-question": lambda: value == "what is your name",
        "name-answer": lambda: "My name is ___." in key and "I am ___." in key and "/ ___." in key,
        "self-anna": lambda: value == "i am anna",
        "two-be-gaps": lambda: value == "am are",
        "name-link-gap": lambda: value == "is",
        "question-link-gap": lambda: value == "is",
        "personal-dialogue-l01": lambda: "I am ___." in key and {"hello", "hi", "goodbye", "bye"} <= set(value.split()),
        "personal-dialogue-l02": lambda: "What is your name?" in key and "My name is ___." in key,
        "dialogue-l01": lambda: value == normal(task["response"]),
        "dialogue-l02": lambda: value == normal(task["response"]),
        "copy": lambda: value == normal(plain(task["prompt"]).split("→", 1)[0]),
    }
    if rubric not in checks or not checks[rubric]():
        raise ValueError(f"{task['id']}: key/model does not satisfy open rubric {rubric}")
    # These are intentional wrong examples only elsewhere, never accepted keys.
    if re.search(r"\b(?:i are|you am|my name are|your name are|what your name is)\b", value):
        raise ValueError(f"{task['id']}: ungrammatical accepted answer")


def lexical_words(text):
    text = re.sub(r"\b(?:A0|A1|A2|B1|B2|C1|IE)-M\d+-U\d+-L\d{2}(?:-QZ)?\b", " ", text)
    return TOKEN.findall(strip_exempt(text).lower())


def svg_words(path):
    root = ET.parse(path).getroot()
    result = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] == "text":
            result.extend(lexical_words("".join(node.itertext())))
    return result


def language_audit(text, path, spec, vocab, previous_words, proper_names, forbidden):
    """Check every rendered lesson word and each SVG at the point it is used."""
    current = set(previous_words)
    new_ids, seen = set(spec["new_vocab"]), []
    unknown, nav, assets = [], [], set()
    target_count = 0
    # Comments preserve line counts. Teach markers must be read BEFORE stripping.
    hidden = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        marker = re.fullmatch(r"<!-- teach: ([^>]+) -->", raw)
        if marker:
            for vid in marker[1].split():
                if vid not in new_ids or vid in seen:
                    raise ValueError(f"{path.name}:{lineno}: unexpected/repeated teaching marker {vid}")
                current.add(vocab[vid]["headword"].lower())
                seen.append(vid)
            continue
        if "<!--" in raw:
            hidden = "-->" not in raw
            continue
        if hidden:
            if "-->" in raw:
                hidden = False
            continue
        if raw.startswith(">") or "<summary>" in raw:
            nav.append({"line": lineno, "label": plain(raw.lstrip("#> ")), "reason": "navigation/reference, not a task direction"})
            continue
        if raw.startswith("#"):
            raw = raw.lstrip("# ")
        for reference in IMAGE.findall(raw):
            asset = (path.parent / reference).resolve()
            if not asset.is_relative_to(ROOT) or not asset.is_file():
                raise ValueError(f"{path.name}:{lineno}: missing/unsafe image {reference}")
            assets.add(asset)
            if asset.suffix != ".svg":
                raise ValueError(f"Unregistered non-SVG P-01 asset: {reference}")
            words = svg_words(asset)
            for word in words:
                if word not in current and word not in proper_names:
                    unknown.append({"line": lineno, "word": word, "source": reference})
                if word in forbidden:
                    unknown.append({"line": lineno, "word": word, "source": "assumed instruction in SVG"})
        for word in lexical_words(plain(raw)):
            if word not in current and word not in proper_names:
                unknown.append({"line": lineno, "word": word, "source": "lesson body"})
            if word in forbidden:
                unknown.append({"line": lineno, "word": word, "source": "assumed instruction"})
            if word not in proper_names:
                target_count += 1
    if set(seen) != new_ids:
        raise ValueError(f"{path.name}: not every new item has an explicit before-use teaching marker")
    return {"unknown": unknown, "navigation_exemptions": nav, "assets": assets,
            "target_body_tokens": target_count, "teaching_order": seen}


def reading_text(text):
    match = re.search(r"<!-- reading:start -->(.*?)<!-- reading:end -->", text, re.S)
    if not match:
        raise ValueError("Missing controlled reading text")
    return match[1].strip()


def main_audit():
    manifest = json.loads(MANIFEST.read_text())
    lesson_map = {row["lesson_id"]: row for row in authored_lessons()}
    with (ROOT / "VOCABULARY_DATABASE.csv").open(newline="") as f:
        vocab = {row["vocab_id"]: row for row in csv.DictReader(f)}
    with (ROOT / "GRAMMAR_DATABASE.csv").open(newline="") as f:
        grammar = {row["grammar_id"]: row for row in csv.DictReader(f)}
    proper_names = {name.lower() for name in manifest["proper_names"]}
    previous_words, previous_grammar = set(), set()
    results, all_assets = {}, set()
    for lid in manifest["scope"]:
        spec = manifest["lessons"][lid]
        path = ROOT / spec["path"]
        text = path.read_text()
        parts, tasks, keys, scripts = parse_tasks(text)
        if list(parts) != list(range(1, 22)):
            raise ValueError(f"{lid}: the 21 complete template sections are required")
        if set(tasks) != set(keys):
            raise ValueError(f"{lid}: unmatched questions/keys: {set(tasks) ^ set(keys)}")
        counts = Counter(item[0] for item in tasks)
        if dict(counts) != spec["task_counts"]:
            raise ValueError(f"{lid}: task count mismatch: {dict(counts)}")
        if len(spec["new_vocab"]) > 8 or len(spec["techniques"]) < 3:
            raise ValueError(f"{lid}: A0 load/technique requirement violated")
        for field, label in [("new_vocab", "NEW_VOCAB"), ("new_grammar", "NEW_GRAMMAR"),
                             ("reviewed_vocab", "REVIEWED_VOCAB"), ("reviewed_grammar", "REVIEWED_GRAMMAR")]:
            raw = re.search(rf"^{label}: (.+)$", text, re.M)
            expected = ", ".join(spec[field]) if spec[field] else "none"
            if not raw or raw[1] != expected:
                raise ValueError(f"{lid}: {label} footer mismatch")
        for field, metadata_field in [("new_vocab", "new_vocab_ids"), ("new_grammar", "new_grammar_ids")]:
            if "|".join(spec[field]) != lesson_map[lid][metadata_field]:
                raise ValueError(f"{lid}: manifest/index {field} mismatch")
        if spec["reviewed_vocab"] and {vocab[item]["headword"].lower() for item in spec["reviewed_vocab"]} != previous_words:
            raise ValueError(f"{lid}: reviewed inventory does not match actual prior inventory")
        for gid in spec["grammar_teaching_order"]:
            info = manifest["grammar_scopes"][gid]
            requires = set(info["requires"])
            if not requires <= previous_grammar:
                raise ValueError(f"{lid}: {gid} has an untaught prerequisite {requires-previous_grammar}")
            if set(grammar[gid]["prerequisites"].split("|")) - {""} != requires:
                raise ValueError(f"{lid}: {gid} scope/database prerequisite mismatch")
            previous_grammar.add(gid)
        for vid in spec["new_vocab"]:
            if vocab[vid]["intro_lesson_id"] != lid:
                raise ValueError(f"{lid}: incorrect first-introduction reference for {vid}")
        if lesson_map[lid]["prerequisites"].split("|") != (spec["prerequisites"] or [""]):
            raise ValueError(f"{lid}: lesson prerequisite mismatch")
        audit = language_audit(text, path, spec, vocab, previous_words, proper_names,
                               set(manifest["forbidden_assumed_words"]))
        if audit["unknown"]:
            raise ValueError(f"{lid}: untaught load-bearing language: {audit['unknown'][:8]}")
        all_assets.update(audit["assets"])
        reading = reading_text(text)
        utterances = " ".join(line.split(":", 1)[-1] for line in reading.splitlines())
        read_words = [word for word in lexical_words(utterances) if word not in proper_names]
        new_words = {vocab[vid]["headword"].lower() for vid in spec["new_vocab"]}
        introduced = previous_words | new_words
        if not read_words or set(read_words) - introduced:
            raise ValueError(f"{lid}: controlled reading has untaught words")
        # Exact scripts/reading sentences must belong to the declared scopes.
        for utterance in [*scripts.values(), *[line.split(":", 1)[-1] for line in reading.splitlines() if line.strip()]]:
            for sentence in re.split(r"[.!?]+", utterance):
                sentence = sentence.strip()
                if sentence and normal(sentence) not in {"hello", "hi", "goodbye tom", "bye anna", "goodbye", "bye"} and not valid_frame(sentence):
                    raise ValueError(f"{lid}: unsupported script/reading structure: {sentence}")
        # Detect the common early-BE question leak even when all its words are known.
        if re.search(r"\b(?:Are you|Am I|Is your)\b", without_comments(text)):
            raise ValueError(f"{lid}: untaught productive BE question")
        closed, opened = [], []
        for item_id, task in tasks.items():
            if item_id in spec["open_rubrics"]:
                validate_open(task, keys[item_id], spec["open_rubrics"][item_id])
                opened.append(item_id)
            else:
                answer = solve_closed(task, scripts, reading)
                symbolic = answer in {"P1", "P2", "P1 → P2", "P2 → P1"}
                mismatch = answer != keys[item_id] if symbolic else normal(answer) != normal(keys[item_id])
                if mismatch:
                    raise ValueError(f"{lid}/{item_id}: independently solved {answer!r}, keyed {keys[item_id]!r}")
                closed.append(item_id)
        if set(spec["open_rubrics"]) - set(tasks):
            raise ValueError(f"{lid}: unused open rubric")
        mapped_checks = set()
        for objective, mapping in spec["objectives"].items():
            if not mapping["practice"] or not mapping["check"] or set(mapping["practice"]+mapping["check"]) - set(tasks):
                raise ValueError(f"{lid}: missing objective coverage: {objective}")
            mapped_checks.update(mapping["check"])
        if mapped_checks != {f"Q{i:02}" for i in range(1, 9)}:
            raise ValueError(f"{lid}: quiz items/objectives not fully aligned")
        for slot in ["+1", "+3", "+7", "+21", "+60"]:
            if slot not in parts[19]:
                raise ValueError(f"{lid}: review slot missing: {slot}")
        for reference in re.findall(r"\b[HLRABSTWQ]\d{2}\b", parts[19]):
            if reference not in tasks:
                raise ValueError(f"{lid}: broken review task reference {reference}")
        if len(scripts) != 4 or {f"E{i:02}" for i in range(1, 8)} - set(re.findall(r"\bE\d{2}\b", parts[7])):
            raise ValueError(f"{lid}: incomplete scripts or seven-model sequence")
        violations = audit_file(path, strict=True)
        if violations:
            raise ValueError(f"{lid}: English-only guard: {violations[:3]}")
        results[lid] = {
            "new_words": [vocab[vid]["headword"] for vid in spec["new_vocab"]],
            "new_grammar_scopes": spec["new_grammar"],
            "template_sections": 21,
            "tasks_with_keys": len(tasks),
            "task_counts": dict(counts),
            "closed_independently_rule_solved": closed,
            "open_key_model_rubric_checked": opened,
            "reading_lexical_tokens_excluding_name_labels": len(read_words),
            "reading_prior_lesson_known_tokens": sum(word in previous_words for word in read_words),
            "reading_prior_lesson_known_percent": round(100*sum(word in previous_words for word in read_words)/len(read_words), 2),
            "reading_point_of_use_known_percent": 100,
            "target_body_tokens": audit["target_body_tokens"],
            "untaught_load_bearing_words": audit["unknown"],
            "teaching_markers_in_order": audit["teaching_order"],
            "navigation_exemptions": audit["navigation_exemptions"],
            "unique_actual_svg_assets": len(audit["assets"]),
            "learner_scores": "none; Q07 and whole totals not assessed",
            "independent_review_and_validation": "pending",
        }
        previous_words.update(new_words)
    for asset in all_assets:
        if audit_file(asset, strict=True):
            raise ValueError(f"English-only violation in {asset}")
    files = {ROOT / manifest["lessons"][lid]["path"] for lid in manifest["scope"]} | all_assets
    files.update(ROOT / path for path in [
        "data/P01_LANGUAGE_MANIFEST.json", "data/lesson_metadata.json", "VOCABULARY_DATABASE.csv",
        "GRAMMAR_DATABASE.csv", "LESSON_INDEX.csv", "scripts/audit_pilot_batch.py", "scripts/audit_english_only.py",
        "scripts/validate_databases.py", "scripts/course_structure.py", "scripts/build_pilot_visuals.py", "scripts/test_quality_tools.py",
    ])
    return {
        "batch_id": "P-01", "audit_date": manifest["date"], "automated_status": "PASS",
        "limits": ["Rule-based second-solving is not an independent human/model review.",
                   "Picture semantics are manually supplied and require learner/reviewer confirmation.",
                   "Open-task checks validate authored keys/rubrics, not learner performance.",
                   "No audio recordings, sound intelligibility checks, observed learners or learner scores.",
                   "All visible heading words are inventory-checked. Only coded delivery metadata, script disclosure notices, optional IPA and accessibility/helper descriptions are reference exceptions."],
        "unique_svg_assets": len(all_assets), "lessons": results,
        "sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(files)},
    }


def language_report(report):
    lines = ["# P-01 Language and Exercise Audit (GENERATED)", "",
             "Regenerate: `python3 scripts/audit_pilot_batch.py --write-report`.", "",
             "Automated scope: the two authored P-01 lessons only. This is not an independent review or learner trial.", "",
             "## Token accounting", "",
             "Known at point of use means explicitly taught before that text/task, including this lesson's picture-led introductions. It does not mean known at lesson entry or retained by a learner. Proper-name labels are excluded from lexical percentages. All new words are still counted against the eight-word lesson cap.", "",
             "| Lesson | New words | Reading lexical tokens | Prior-lesson known | Point-of-use known | Keyed tasks | Closed rule-solved | Open/model checked |",
             "|---|---|---|---|---|---|---|---|"]
    for lid, result in report["lessons"].items():
        lines.append(f"| {lid} | {', '.join(result['new_words'])} | {result['reading_lexical_tokens_excluding_name_labels']} | {result['reading_prior_lesson_known_percent']}% | 100% | {result['tasks_with_keys']} | {len(result['closed_independently_rule_solved'])} | {len(result['open_key_model_rubric_checked'])} |")
    lines += ["", "Zero unexpected target-language tokens were found in the lesson body or in rendered SVG text at any use. English-only checks also scan the English accessibility descriptions and hidden records. The exact new/review IDs, grammar restrictions, rubric definitions and exception reasons are in `data/P01_LANGUAGE_MANIFEST.json`.", "",
              "## Explicit navigation/reference exemptions", "",
              "Visible lesson headings use only symbols/IDs or already-taught words and ARE inventory-checked at their point of use. Only the coded course metadata and technical disclosure notices below are reference exceptions, carrying no required task action. Every essential action is demonstrated by actual icons/pictures and worked responses. No free-prose instruction paragraph is silently exempted. Image alt text and SVG title/description nodes are English helper/accessibility descriptions, not a zero-English screen-reader route.", ""]
    for lid, result in report["lessons"].items():
        lines += [f"### {lid}", "", "| Line | Reference label (not learner inventory) |", "|---|---|"]
        for item in result["navigation_exemptions"]:
            lines.append(f"| {item['line']} | {item['label'].replace('|', '/')} |")
    lines += ["", "## Exercise verification", "",
              "Every prompt ID has exactly one key row. Closed items are solved without reading keys, using the student text/options/script and the declared visual facts; each has exactly one available correct choice. Open keys are checked against explicit rubrics/models; natural greeting/farewell alternatives and both taught name responses are admitted where the prompt permits them. Personal name choice/spelling, accent, speed and punctuation are not scored in these early frames.", "",
              "The source keys contain complete role-play models and worked personal-name substitutions. Blank lines are deliberate response spaces, not unfinished content. No learner score, successful recall, audio verification or independent sign-off has been invented.", "",
              "## Evidence", "",
              "`docs/P01_QA_RESULTS.json` contains the item-by-item check lists and SHA-256 hashes of both lessons, all used SVGs, the inventory/authoring data and the QA scripts. Independent review, pronunciation/listening audio and real-learner trials remain pending.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    try:
        report = main_audit()
    except (OSError, ValueError, KeyError, ET.ParseError) as exc:
        print(f"P-01 AUDIT FAILED: {exc}")
        return 1
    print(f"P-01 PASS: 2 lessons, {report['unique_svg_assets']} actual SVG assets.")
    for lid, result in report["lessons"].items():
        print(f"  {lid}: {len(result['new_words'])} new words; {result['tasks_with_keys']} keyed tasks "
              f"({len(result['closed_independently_rule_solved'])} closed solved, {len(result['open_key_model_rubric_checked'])} open/model checked); "
              f"reading known at entry {result['reading_prior_lesson_known_percent']}%, at point of use 100%.")
    print("  Untaught target words: 0; all scope/prerequisite, key, objective and review checks pass.")
    print("  Independent validation, recorded audio and learner evidence: PENDING (not claimed).")
    if args.write_report:
        (ROOT / "docs/P01_QA_RESULTS.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n")
        (ROOT / "docs/P01_LANGUAGE_AUDIT.md").write_text(language_report(report))
        print("  Wrote docs/P01_QA_RESULTS.json and docs/P01_LANGUAGE_AUDIT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
