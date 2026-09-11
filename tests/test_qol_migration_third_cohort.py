from pathlib import Path
import unittest

from qol_kb import records


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ThirdQolMigrationTests(unittest.TestCase):
    def test_third_qol_cohort_is_fully_canonical(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        item_ids = {
            record.front_matter["id"]
            for record in snapshot.items
        }
        expected_ids = {f"QOL-{number:03d}" for number in range(61, 81)}

        self.assertTrue(
            expected_ids.issubset(item_ids),
            f"missing canonical QoL items: {sorted(expected_ids - item_ids)}",
        )


if __name__ == "__main__":
    unittest.main()
