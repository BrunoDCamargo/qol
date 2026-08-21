import json
from pathlib import Path
import unittest

from qol_kb.records import load_record


ROOT = Path(__file__).parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
SCHEMAS = ROOT / "schemas"


class StructuredRecordPipelineTests(unittest.TestCase):
    def test_loads_yaml_front_matter_and_markdown_body(self):
        record = load_record(FIXTURES / "items" / "QOL-900.md")

        self.assertEqual(record.record_type, "item")
        self.assertEqual(record.front_matter["id"], "QOL-900")
        self.assertEqual(record.front_matter["statement"], "Use the test fixture")
        self.assertEqual(record.body.strip(), "# Fixture item\n\nFixture body.")

    def test_loads_reference_records_through_the_same_pipeline(self):
        record = load_record(FIXTURES / "references" / "REF-900.md")

        self.assertEqual(record.record_type, "reference")
        self.assertEqual(record.front_matter["id"], "REF-900")
        self.assertEqual(record.front_matter["title"], "Fixture reference")
        self.assertEqual(
            record.front_matter["supports"],
            ("The fixture reference can be loaded.",),
        )

    def test_rejects_filename_and_record_id_mismatch(self):
        with self.assertRaisesRegex(
            ValueError,
            r"QOL-901.*QOL-999",
        ):
            load_record(FIXTURES / "items" / "QOL-901.md")

    def test_rejects_unknown_item_front_matter_fields(self):
        with self.assertRaisesRegex(ValueError, r"unexpected_field"):
            load_record(FIXTURES / "items" / "QOL-902.md")

    def test_rejects_missing_required_item_fields(self):
        with self.assertRaisesRegex(ValueError, r"statement"):
            load_record(FIXTURES / "items" / "QOL-903.md")

    def test_rejects_unknown_reference_front_matter_fields(self):
        with self.assertRaisesRegex(ValueError, r"unexpected_field"):
            load_record(FIXTURES / "references" / "REF-901.md")

    def test_rejects_non_markdown_record_files(self):
        with self.assertRaisesRegex(ValueError, r"QOL-904\.txt.*\.md"):
            load_record(FIXTURES / "items" / "QOL-904.txt")

    def test_nested_validation_errors_include_the_field_path(self):
        with self.assertRaisesRegex(ValueError, r"evidence_claims\[0\]\.role"):
            load_record(FIXTURES / "items" / "QOL-905.md")

    def test_version_controlled_schemas_define_closed_core_records(self):
        schema_paths = (
            SCHEMAS / "qol-item.schema.json",
            SCHEMAS / "reference.schema.json",
        )

        for schema_path in schema_paths:
            with self.subTest(schema=schema_path.name):
                self.assertTrue(schema_path.is_file(), f"missing schema: {schema_path}")
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                self.assertFalse(schema["additionalProperties"])
                self.assertIn("id", schema["required"])


if __name__ == "__main__":
    unittest.main()
