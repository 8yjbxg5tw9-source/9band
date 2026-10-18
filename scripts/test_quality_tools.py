#!/usr/bin/env python3
"""Standard-library regression/negative tests for P-01 production guards.

Run: python3 -m unittest discover -s scripts -p 'test_*.py' -v
All mutations are temporary or in-memory. No learner achievement is tested.
"""
import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import audit_english_only as english
import audit_pilot_batch as pilot
import course_structure as structure
import validate_databases as databases


class EnglishGuardTests(unittest.TestCase):
    def check_text(self, text, name="lesson.md", strict=False):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / name
            path.write_text(text)
            return english.audit_file(path, strict=strict)

    def test_clean_english_and_typography(self):
        self.assertFalse(self.check_text("Hello! I am Anna. · ✓ → 6/8 × 1"))

    def test_registered_ipa_is_permitted(self):
        self.assertFalse(self.check_text("hello /həˈləʊ/; goodbye /ɡʊd/ → /b/"))

    def test_unregistered_slash_prose_is_not_exempt(self):
        self.assertTrue(self.check_text("/mən kitab/"))

    def test_ascii_stopword_is_detected(self):
        self.assertTrue(self.check_text("kitab"))

    def test_inline_code_does_not_hide_language(self):
        self.assertTrue(self.check_text("`mən`"))

    def test_fenced_code_does_not_hide_language(self):
        self.assertTrue(self.check_text("```text\nkitab\n```"))

    def test_other_scripts_are_detected(self):
        for value in ["Привет", "مرحبا", "你好", "γειά", "bonjour élève"]:
            with self.subTest(value=value):
                self.assertTrue(self.check_text(value))

    def test_html_entities_are_decoded(self):
        self.assertTrue(self.check_text("m&#601;n"))

    def test_svg_descriptions_and_text_are_checked(self):
        self.assertTrue(self.check_text('<svg><title>kitab</title><text>Hello</text></svg>', "picture.svg"))

    def test_arbitrary_readme_is_not_a_bypass(self):
        self.assertTrue(self.check_text("kitab", "README-extra.md"))

    def test_strict_markers_fail_but_response_spaces_do_not(self):
        self.assertTrue(self.check_text("TODO: add an exercise", strict=True))
        self.assertTrue(self.check_text("placeholder", strict=True))
        self.assertFalse(self.check_text("I ___ Anna.", strict=True))


class GeneratorAndDatabaseTests(unittest.TestCase):
    def metadata_file(self, payload):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "metadata.json"
        path.write_text(json.dumps(payload))
        return path

    def test_structure_count_and_scope(self):
        self.assertEqual(len(list(structure.iter_lessons())), 624)
        self.assertEqual(structure.expected_counts()["TOTAL"], 624)
        authored = [row for row in structure.authored_lessons() if row["validation_status"] != "planned"]
        self.assertEqual([row["lesson_id"] for row in authored], ["A0-M1-U1-L01", "A0-M1-U1-L02"])

    def test_structural_override_rejected(self):
        path = self.metadata_file({"schema_version": 1, "lessons": {"A0-M1-U1-L01": {"title": "Changed"}}})
        with self.assertRaisesRegex(ValueError, "structural"):
            structure.load_lesson_metadata(path)

    def test_unknown_lesson_rejected(self):
        path = self.metadata_file({"schema_version": 1, "lessons": {"A0-M1-U1-L99": {}}})
        with self.assertRaisesRegex(ValueError, "Unknown"):
            structure.load_lesson_metadata(path)
        with self.assertRaisesRegex(ValueError, "Missing lesson metadata"):
            structure.load_lesson_metadata(path.with_name("missing.json"))

    def test_bad_schema_and_value_types_rejected(self):
        for payload in [[], {"schema_version": 2, "lessons": {}},
                        {"schema_version": 1, "lessons": {"A0-M1-U1-L01": {"notes": 2}}}]:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                structure.load_lesson_metadata(self.metadata_file(payload))

    def test_regeneration_preserves_metadata_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.csv"
            with patch.object(structure, "LESSON_INDEX_PATH", str(path)):
                structure.write_lesson_index()
                first = path.read_bytes()
                self.assertNotIn(b"\r", first)
                structure.write_lesson_index()
                self.assertEqual(first, path.read_bytes())
            with path.open(newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["validation_status"], "drafted")
            self.assertIn("V0001", rows[0]["new_vocab_ids"])
            self.assertEqual(rows[2]["validation_status"], "planned")

    def test_malformed_csv_width_detected(self):
        errors = []
        databases.table_shape("test.csv", ["id"], [{"id": "x", None: ["extra"]}], ["id"], "id", errors)
        self.assertTrue(errors)

    def test_grammar_cycle_detected(self):
        self.assertTrue(databases.check_cycles([
            {"grammar_id": "G001", "prerequisites": "G002"},
            {"grammar_id": "G002", "prerequisites": "G001"},
        ]))

    def test_current_databases_pass(self):
        self.assertEqual(databases.validate()[0], [])


class PilotAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = pilot.ROOT / "content/A0/A0-M1-U1-L01.md"
        cls.original = cls.path.read_text()
        cls.manifest_original = pilot.MANIFEST.read_text()

    def with_replacement(self, path, replacement):
        original_read = Path.read_text

        def patched_read(instance, *args, **kwargs):
            if instance == path:
                return replacement
            return original_read(instance, *args, **kwargs)

        return patch.object(Path, "read_text", patched_read)

    def assert_lesson_mutation_fails(self, old, new, error):
        self.assertIn(old, self.original)
        changed = self.original.replace(old, new, 1)
        with self.with_replacement(self.path, changed), self.assertRaisesRegex(ValueError, error):
            pilot.main_audit()

    def test_all_86_tasks_and_honest_known_word_rates(self):
        result = pilot.main_audit()
        one, two = result["lessons"].values()
        self.assertEqual(one["tasks_with_keys"], 39)
        self.assertEqual(two["tasks_with_keys"], 47)
        self.assertEqual(one["reading_prior_lesson_known_percent"], 0)
        self.assertEqual(two["reading_prior_lesson_known_percent"], 31.58)
        self.assertEqual(one["reading_point_of_use_known_percent"], 100)
        self.assertEqual(two["reading_point_of_use_known_percent"], 100)
        self.assertEqual(result["unique_svg_assets"], 28)

    def test_wrong_key_is_detected_by_blind_rule_solver(self):
        self.assert_lesson_mutation_fails("| A05 | am |", "| A05 | are |", "independently solved")

    def test_missing_key_is_detected(self):
        self.assert_lesson_mutation_fails("| Q08 | You are Tom. |\n", "", "unmatched questions/keys")

    def test_duplicate_task_is_detected(self):
        self.assert_lesson_mutation_fails("| A05 | I ___ Anna. | am / are |", "| A05 | I ___ Anna. | am / are |\n| A05 | I ___ Anna. | am / are |", "duplicate task")

    def test_future_word_in_student_body_is_detected(self):
        self.assert_lesson_mutation_fails("## 6. I → am · you → are", "## 6. I → am · you → are\n\nbook", "untaught load-bearing")

    def test_untaught_instruction_word_is_detected(self):
        self.assert_lesson_mutation_fails("## 6. I → am · you → are", "## 6. I → am · you → are\n\nChoose", "untaught load-bearing")
        # A heading cannot be used as a hidden instruction-language bypass.
        self.assert_lesson_mutation_fails("## 6. I → am · you → are", "## 6. I → am · you → are Choose", "untaught load-bearing")

    def test_known_words_cannot_smuggle_future_question_grammar(self):
        self.assert_lesson_mutation_fails("## 6. I → am · you → are", "## 6. I → am · you → are\n\nAre you Anna?", "untaught productive BE")

    def test_missing_actual_image_is_detected(self):
        self.assert_lesson_mutation_fails("assets/p01/actions.svg", "assets/p01/missing.svg", "missing/unsafe image")

    def test_known_greeting_alternative_cannot_be_rejected(self):
        self.assert_lesson_mutation_fails("| B01 | Hello! / Hi! |", "| B01 | Hello! |", "open rubric")

    def test_natural_bare_name_answer_is_not_rejected(self):
        path = pilot.ROOT / "content/A0/A0-M1-U1-L02.md"
        text = path.read_text().replace("/ ___. → My name is Anna.", "→ My name is Anna.")
        with self.with_replacement(path, text), self.assertRaisesRegex(ValueError, "open rubric"):
            pilot.main_audit()

    def test_untaught_prerequisite_is_detected(self):
        data = json.loads(self.manifest_original)
        data["grammar_scopes"]["G010"]["requires"].append("G009")
        with self.with_replacement(pilot.MANIFEST, json.dumps(data)), self.assertRaisesRegex(ValueError, "untaught prerequisite"):
            pilot.main_audit()

    def test_ninth_new_word_is_detected(self):
        data = json.loads(self.manifest_original)
        data["lessons"]["A0-M1-U1-L01"]["new_vocab"].append("V0005")
        with self.with_replacement(pilot.MANIFEST, json.dumps(data)), self.assertRaisesRegex(ValueError, "load/technique"):
            pilot.main_audit()

    def test_new_word_marker_cannot_be_omitted(self):
        self.assert_lesson_mutation_fails("<!-- teach: V0008 V0010 -->", "", "before-use teaching marker")

    def test_gap_markers_survive_parsing(self):
        task = {"id": "A05", "prompt": "I ___ Anna.", "response": "am / are"}
        self.assertEqual(pilot.solve_closed(task, {}, ""), "am")


if __name__ == "__main__":
    unittest.main(verbosity=2)
