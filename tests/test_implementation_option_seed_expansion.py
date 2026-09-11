from pathlib import Path
import unittest

from qol_kb import records


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ImplementationOptionSeedExpansionTests(unittest.TestCase):
    def test_repository_contains_expanded_practical_options(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        options = {
            record.front_matter["id"]: (
                record.front_matter["name"],
                record.front_matter["acquisition"],
                record.front_matter["implements"],
            )
            for record in snapshot.implementation_options
        }

        expected = {
            "IMP-005": ("Grocery delivery service", "service", ("QOL-023",)),
            "IMP-006": ("Laundry wash-and-fold service", "service", ("QOL-024",)),
            "IMP-007": ("Ironing service", "service", ("QOL-024",)),
            "IMP-008": ("Recurring home maintenance service", "service", ("QOL-026",)),
            "IMP-009": ("Bedroom fan", "purchase", ("QOL-009",)),
            "IMP-010": ("Lightweight or breathable bedding", "purchase", ("QOL-009",)),
            "IMP-011": ("Weighted blanket", "purchase", ("QOL-011",)),
            "IMP-012": ("Comfortable walking shoes", "purchase", ("QOL-034",)),
            "IMP-013": ("Sit-stand desk", "purchase", ("QOL-040",)),
            "IMP-014": ("Sit-stand desk converter", "purchase", ("QOL-040",)),
            "IMP-015": ("Massage therapy session", "service", ("QOL-041",)),
            "IMP-016": ("Externally vented kitchen range hood", "purchase", ("QOL-046",)),
            "IMP-017": ("Portable HEPA air purifier", "purchase", ("QOL-047",)),
            "IMP-018": ("Higher-efficiency HVAC filter", "purchase", ("QOL-047",)),
            "IMP-019": ("Meal-kit subscription", "subscription", ("QOL-025",)),
            "IMP-020": ("Grocery delivery subscription", "subscription", ("QOL-023",)),
        }

        self.assertEqual({key: options.get(key) for key in expected}, expected)


if __name__ == "__main__":
    unittest.main()
