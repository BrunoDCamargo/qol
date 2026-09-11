from pathlib import Path
import unittest

from qol_kb import records


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class SecondReferenceMigrationTests(unittest.TestCase):
    def test_second_reference_cohort_is_fully_canonical(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        canonical_ids = {
            record.front_matter["id"]
            for record in snapshot.references
        }
        expected_ids = {f"REF-{number:03d}" for number in range(31, 61)}

        self.assertTrue(
            expected_ids.issubset(canonical_ids),
            f"missing canonical references: {sorted(expected_ids - canonical_ids)}",
        )


if __name__ == "__main__":
    unittest.main()
