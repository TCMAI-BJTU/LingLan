import json
from pathlib import Path
import tempfile
import unittest

from .diagnostic_therapeutic_data import COMPONENTS, load_diagnostic_therapeutic_examples


class DiagnosticTherapeuticDataTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.rows = {}
        for task, filename, field in COMPONENTS:
            self.rows[task] = [
                {
                    "id": f"{task}_{case_id}",
                    "task": task,
                    "医家": "医家甲",
                    "病历文本": f"病例 {case_id}",
                    "answer": f"{field}标签 {case_id}",
                }
                for case_id in ("0002", "0001")
            ]
        self.write_files()

    def write_files(self):
        for task, filename, _ in COMPONENTS:
            (self.directory / filename).write_text(
                "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in self.rows[task]),
                encoding="utf-8",
            )

    def test_join_by_id_when_component_order_differs(self):
        self.rows["treatment_method"].reverse()
        self.rows["herbal_prescription"].reverse()
        self.write_files()
        examples = load_diagnostic_therapeutic_examples(self.directory)
        self.assertEqual([row["id"] for row in examples], [
            "diagnostic_therapeutic_reasoning_0002", "diagnostic_therapeutic_reasoning_0001"
        ])
        for row in examples:
            case_id = row["id"].rsplit("_", 1)[1]
            self.assertEqual(row["病历文本"], f"病例 {case_id}")
            for task, _, field in COMPONENTS:
                self.assertEqual(row[field], f"{field}标签 {case_id}")
                self.assertEqual(row["source_ids"][task], f"{task}_{case_id}")

    def test_missing_case_fails_instead_of_dropping_it(self):
        self.rows["treatment_method"].pop()
        self.write_files()
        with self.assertRaisesRegex(ValueError, "病例编号不一致"):
            load_diagnostic_therapeutic_examples(self.directory)

    def test_different_case_set_with_same_length_fails(self):
        self.rows["herbal_prescription"][0]["id"] = "herbal_prescription_9999"
        self.write_files()
        with self.assertRaisesRegex(ValueError, "病例编号不一致"):
            load_diagnostic_therapeutic_examples(self.directory)

    def test_duplicate_case_fails(self):
        self.rows["herbal_prescription"].append(dict(self.rows["herbal_prescription"][0]))
        self.write_files()
        with self.assertRaisesRegex(ValueError, "重复病例编号"):
            load_diagnostic_therapeutic_examples(self.directory)

    def test_inconsistent_shared_fields_fail(self):
        row = self.rows["treatment_method"][0]
        for field in ("医家", "病历文本"):
            with self.subTest(field=field):
                original = row[field]
                row[field] = "另一个病例的信息"
                self.write_files()
                with self.assertRaisesRegex(ValueError, field + " 不一致"):
                    load_diagnostic_therapeutic_examples(self.directory)
                row[field] = original

    def test_task_and_four_digit_id_are_required(self):
        row = self.rows["syndrome"][0]
        for field, value in (("task", "treatment_method"), ("id", "syndrome_2"),
                             ("id", "syndrome_00002"), ("id", "treatment_method_0002")):
            with self.subTest(field=field, value=value):
                original = row[field]
                row[field] = value
                self.write_files()
                with self.assertRaises(ValueError):
                    load_diagnostic_therapeutic_examples(self.directory)
                row[field] = original

    def test_unrecorded_physicians_are_joined_without_dropping_the_case(self):
        for task, _, _ in COMPONENTS:
            self.rows[task][0]["医家"] = "未记录"
        self.write_files()
        examples = load_diagnostic_therapeutic_examples(self.directory)
        self.assertEqual(len(examples), 2)
        self.assertEqual(examples[0]["医家"], "未记录")

    def test_missing_or_empty_answer_fails(self):
        row = self.rows["syndrome"][0]
        for answer in (None, "", [], {}):
            with self.subTest(answer=answer):
                row["answer"] = answer
                self.write_files()
                with self.assertRaisesRegex(ValueError, "answer"):
                    load_diagnostic_therapeutic_examples(self.directory)

    def test_missing_and_empty_files_fail(self):
        source = self.directory / "医家处方.jsonl"
        source.unlink()
        with self.assertRaises(FileNotFoundError):
            load_diagnostic_therapeutic_examples(self.directory)
        source.write_text("\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "没有可评估的病例"):
            load_diagnostic_therapeutic_examples(self.directory)

    def test_single_file_is_not_a_joint_dataset(self):
        with self.assertRaises(FileNotFoundError):
            load_diagnostic_therapeutic_examples(self.directory / "医家辨证.jsonl")


if __name__ == "__main__":
    unittest.main()
