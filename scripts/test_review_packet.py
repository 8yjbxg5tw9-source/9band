"""Extraction/packaging tests; NEVER independent lesson-review evidence."""
import csv
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare_p01_review as packet
from audit_english_only import audit_file


class ReviewPacketTests(unittest.TestCase):
    def source(self, lesson_id=packet.LESSONS[0]):
        return (packet.ROOT / "content/A0" / f"{lesson_id}.md").read_text()

    def test_all_prompt_ids_and_four_script_lines_are_preserved(self):
        for lesson_id in packet.LESSONS:
            blind, script, ids = packet.split_lesson(self.source(lesson_id), lesson_id)
            self.assertEqual(len(ids), packet.COUNTS[lesson_id])
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(len(re.findall(r"^\d\. ", script, re.M)), 4)
            self.assertEqual(packet.TASK.findall(blind), ids)

    def test_keys_scripts_machine_records_are_withheld(self):
        for lesson_id in packet.LESSONS:
            blind, _, _ = packet.split_lesson(self.source(lesson_id), lesson_id)
            self.assertNotIn("<details", blind)
            self.assertNotIn("SCRIPT ONLY", blind)
            self.assertNotIn("NEW_VOCAB", blind)
            self.assertNotIn("<!--", blind)
            self.assertEqual([int(n) for n in re.findall(r"^## (\d+)\.", blind, re.M)],
                             [*range(1, 18), 19, 20])

    def test_meaningful_student_content_is_not_rewritten(self):
        text = self.source()
        blind, _, _ = packet.split_lesson(text, packet.LESSONS[0])
        for section in (4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20):
            original = re.search(rf"^## {section}\.[\s\S]*?(?=^## \d+\.|\Z)", text, re.M)[0]
            expected = re.sub(r"<!--[\s\S]*?-->", "", original)
            expected = expected.replace("(assets/p01/", "(../sealed/source/assets/p01/")
            self.assertIn(expected, blind)

    def test_structural_drift_is_rejected(self):
        with self.assertRaises(ValueError):
            packet.split_lesson(self.source().replace("## 18. ✓", "## 22. ✓"), packet.LESSONS[0])

    def test_missing_key_is_rejected(self):
        with self.assertRaises(ValueError):
            packet.split_lesson(self.source().replace("| L01 | P1 |\n", ""), packet.LESSONS[0])

    def test_duplicate_prompt_is_rejected(self):
        with self.assertRaises(ValueError):
            packet.split_lesson(self.source().replace("| L02 | 2", "| L01 | 2"), packet.LESSONS[0])

    def test_unclosed_or_malformed_helper_script_is_rejected(self):
        with self.assertRaises(ValueError):
            packet.split_lesson(self.source().replace("</details>", "", 1), packet.LESSONS[0])
        with self.assertRaises(ValueError):
            packet.split_lesson(self.source().replace("4. You are Tom.\n", ""), packet.LESSONS[0])

    def test_unsafe_image_references_are_rejected(self):
        for target in ("../../README.md", "https://example.invalid/picture.svg"):
            with self.assertRaises(ValueError):
                packet.split_lesson(self.source().replace("assets/p01/actions.svg", target), packet.LESSONS[0])

    def test_manifest_and_response_cells_make_no_review_claim(self):
        files = packet.build()
        manifest = json.loads(files["PACKET_MANIFEST.json"])
        self.assertTrue(manifest["independent_review"].startswith("PENDING"))
        self.assertEqual(manifest["new_lessons_authored"], 0)
        self.assertEqual(manifest["lesson_status"], "drafted")
        for name, digest in manifest["files_sha256"].items():
            self.assertEqual(packet.sha(files[name]), digest)
        rows = list(csv.DictReader(io.StringIO(files["forms/BLIND_RESPONSES.csv"].decode())))
        self.assertEqual(len(rows), 86)
        self.assertEqual({r["review_state"] for r in rows}, {"not reviewed"})
        for row in rows:
            self.assertEqual(row["reviewer_response_before_keys"], "")
            self.assertEqual(row["acceptable_variants"], "")

    def test_original_sources_and_image_references_are_intact(self):
        files = packet.build()
        for lesson_id in packet.LESSONS:
            original = (packet.ROOT / 'content/A0' / f'{lesson_id}.md').read_bytes()
            self.assertEqual(files[f'sealed/source/{lesson_id}.md'], original)
            blind = files[f'blind/{lesson_id}.md'].decode()
            for reference in packet.ASSET.findall(blind):
                self.assertTrue(reference.startswith('../sealed/source/assets/p01/'))
                self.assertIn(reference.removeprefix('../'), files)

    def test_generated_blind_text_passes_strict_english_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            for lesson_id in packet.LESSONS:
                blind, _, _ = packet.split_lesson(self.source(lesson_id), lesson_id)
                path = Path(directory) / f'{lesson_id}.md'
                path.write_text(blind)
                self.assertEqual(audit_file(path, strict=True), [])

    def test_archive_is_reproducible_complete_and_path_safe(self):
        files = packet.build()
        archive = packet.archive_bytes(files)
        self.assertEqual(archive, packet.archive_bytes(packet.build()))
        with zipfile.ZipFile(io.BytesIO(archive)) as zf:
            self.assertIsNone(zf.testzip())
            self.assertEqual(set(zf.namelist()), set(files))
            for name in zf.namelist():
                self.assertEqual(zf.read(name), files[name])
        for name in ("../leak.txt", "/absolute.txt", "folder\\file"):
            with self.assertRaises(ValueError):
                packet.archive_bytes({name: b"unsafe"})


if __name__ == "__main__":
    unittest.main()
