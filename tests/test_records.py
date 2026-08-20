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


if __name__ == "__main__":
    unittest.main()
