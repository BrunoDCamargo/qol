from pathlib import Path
import unittest

from qol_kb import records


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CanonicalCutoverTests(unittest.TestCase):
    def test_intended_informs_relationships_are_encoded(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        actual = {
            (record.front_matter["id"], relationship["target"])
            for record in snapshot.items
            for relationship in record.front_matter["relationships"]
            if relationship["type"] == "informs"
        }
        expected = {
            ("QOL-021", "QOL-022"),
            ("QOL-021", "QOL-023"),
            ("QOL-021", "QOL-024"),
            ("QOL-021", "QOL-025"),
            ("QOL-021", "QOL-026"),
            ("QOL-021", "QOL-027"),
            ("QOL-021", "QOL-028"),
            ("QOL-030", "QOL-031"),
            ("QOL-051", "QOL-115"),
            ("QOL-080", "QOL-117"),
        }

        self.assertTrue(
            expected.issubset(actual),
            f"missing intended informs relationships: {sorted(expected - actual)}",
        )


if __name__ == "__main__":
    unittest.main()
