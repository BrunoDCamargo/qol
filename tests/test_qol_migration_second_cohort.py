from pathlib import Path
import unittest

from qol_kb import records


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class SecondQolMigrationTests(unittest.TestCase):
    def test_second_qol_cohort_is_fully_canonical(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        items = {
            record.front_matter["id"]: record
            for record in snapshot.items
        }
        expected_ids = {f"QOL-{number:03d}" for number in range(41, 61)}

        self.assertTrue(
            expected_ids.issubset(items),
            f"missing canonical QoL items: {sorted(expected_ids - set(items))}",
        )

    def test_known_duplicates_use_canonical_lifecycle_replacements(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        items = {
            record.front_matter["id"]: record.front_matter
            for record in snapshot.items
        }
        replacements = {
            "QOL-042": "QOL-007",
            "QOL-044": "QOL-005",
            "QOL-045": "QOL-009",
            "QOL-056": "QOL-004",
        }

        for item_id, replacement_id in replacements.items():
            with self.subTest(item=item_id):
                item = items[item_id]
                self.assertEqual(item["status"], "Deprecated")
                self.assertIn("duplicate", item["deprecation_reason"].lower())
                self.assertEqual(item["replaced_by"], (replacement_id,))


if __name__ == "__main__":
    unittest.main()
