from pathlib import Path
import unittest

from qol_kb.records import load_record


FIXTURES = Path(__file__).parent / "fixtures"


class StructuredRecordPipelineTests(unittest.TestCase):
    def test_loads_yaml_front_matter_and_markdown_body(self):
        record = load_record(FIXTURES / "items" / "QOL-900.md")

        self.assertEqual(record.record_type, "item")
        self.assertEqual(record.front_matter["id"], "QOL-900")
        self.assertEqual(record.front_matter["statement"], "Use the test fixture")
        self.assertEqual(record.body.strip(), "# Fixture item\n\nFixture body.")

    def test_rejects_filename_and_record_id_mismatch(self):
        with self.assertRaisesRegex(
            ValueError,
            r"QOL-901.*QOL-999",
        ):
            load_record(FIXTURES / "items" / "QOL-901.md")

    def test_rejects_unknown_front_matter_fields(self):
        with self.assertRaisesRegex(ValueError, r"unexpected_field"):
            load_record(FIXTURES / "items" / "QOL-902.md")


if __name__ == "__main__":
    unittest.main()
