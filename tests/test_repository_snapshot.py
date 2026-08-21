import dataclasses
from pathlib import Path
import tempfile
import unittest

import yaml

from qol_kb import records


class RepositorySnapshotTests(unittest.TestCase):
    def _write_record(self, root: Path, folder: str, front_matter: dict) -> None:
        directory = root / folder
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{front_matter['id']}.md"
        content = yaml.safe_dump(front_matter, sort_keys=False)
        path.write_text(f"---\n{content}---\n# Fixture\n", encoding="utf-8")

    def test_load_repository_returns_sorted_frozen_validated_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "categories.yaml").write_text(
                "categories:\n"
                "  zeta:\n"
                "    definition: Zeta category.\n"
                "    status: Active\n"
                "  alpha:\n"
                "    definition: Alpha category.\n"
                "    status: Active\n",
                encoding="utf-8",
            )
            for reference_id in ("REF-1000", "REF-999"):
                self._write_record(
                    root,
                    "references",
                    {
                        "id": reference_id,
                        "title": "Fixture reference",
                        "status": "Active",
                        "authors": ["Example Author"],
                        "year": 2026,
                        "source": "Fixture Journal",
                        "source_type": "primary research",
                        "urls": ["https://example.com/reference"],
                        "supports": ["The fixture supports the item."],
                    },
                )
            for item_id, category in (("QOL-1000", "zeta"), ("QOL-999", "alpha")):
                self._write_record(
                    root,
                    "items",
                    {
                        "id": item_id,
                        "statement": "Use the fixture item",
                        "kind": "Intervention",
                        "status": "Active",
                        "categories": [category],
                        "applicability": "General",
                        "support_mode": "Direct",
                        "evidence_reviewed_at": "2026-08-21",
                        "evidence_claims": [
                            {
                                "statement": "Moderate support.",
                                "role": "Support",
                                "strength": "Moderate",
                                "references": ["REF-999"],
                            },
                            {
                                "statement": "Low constraint.",
                                "role": "Constraint",
                                "strength": "Low",
                                "references": ["REF-1000"],
                            },
                        ],
                        "relationships": [],
                    },
                )

            snapshot = records.load_repository(root)
            self.assertEqual([category.name for category in snapshot.categories], ["alpha", "zeta"])
            self.assertEqual([record.front_matter["id"] for record in snapshot.items], ["QOL-999", "QOL-1000"])
            self.assertEqual([record.front_matter["id"] for record in snapshot.references], ["REF-999", "REF-1000"])
            self.assertEqual(snapshot.items[0].evidence_strength, "Moderate")
            with self.assertRaises(dataclasses.FrozenInstanceError):
                snapshot.items = ()
            self.assertIsNone(records.validate_repository(root))


if __name__ == "__main__":
    unittest.main()
