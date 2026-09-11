from pathlib import Path
import tempfile
import unittest

import yaml

from qol_kb import records
from qol_kb.records import load_record


class ImplementationOptionRepositoryTests(unittest.TestCase):
    def _write_record(self, root: Path, folder: str, front_matter: dict) -> Path:
        directory = root / folder
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{front_matter['id']}.md"
        yaml_text = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=True)
        path.write_text(f"---\n{yaml_text}---\n# Fixture\n", encoding="utf-8")
        return path

    def _write_registry(self, root: Path) -> None:
        (root / "categories.yaml").write_text("categories: {}\n", encoding="utf-8")

    def _reference(self) -> dict:
        return {
            "id": "REF-950",
            "title": "Implementation option fixture reference",
            "status": "Active",
            "authors": ["Example Author"],
            "year": 2026,
            "source": "Fixture Journal",
            "source_type": "primary research",
            "urls": ["https://example.com/reference"],
            "supports": ["The fixture supports the item."],
        }

    def _item(self, item_id: str, **overrides) -> dict:
        data = {
            "id": item_id,
            "statement": "Use the implementation option fixture",
            "kind": "Intervention",
            "status": "Active",
            "categories": [],
            "applicability": "General",
            "support_mode": "Direct",
            "evidence_reviewed_at": "2026-09-11",
            "evidence_claims": [
                {
                    "statement": "The fixture is supported.",
                    "role": "Support",
                    "strength": "High",
                    "references": ["REF-950"],
                }
            ],
            "relationships": [],
        }
        data.update(overrides)
        return data

    def _option(self, option_id: str, item_id: str, **overrides) -> dict:
        data = {
            "id": option_id,
            "name": "Use the fixture implementation",
            "status": "Active",
            "implements": [item_id],
            "acquisition": "purchase",
        }
        data.update(overrides)
        return data

    def test_repository_snapshot_includes_sorted_implementation_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_registry(root)
            self._write_record(root, "references", self._reference())
            self._write_record(root, "items", self._item("QOL-950"))
            self._write_record(root, "items", self._item("QOL-951"))
            self._write_record(
                root,
                "implementation-options",
                self._option("IMP-951", "QOL-951"),
            )
            self._write_record(
                root,
                "implementation-options",
                self._option("IMP-950", "QOL-950"),
            )

            snapshot = records.load_repository(root)

            self.assertEqual(
                [record.front_matter["id"] for record in snapshot.implementation_options],
                ["IMP-950", "IMP-951"],
            )

    def test_active_implementation_option_target_must_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_registry(root)
            self._write_record(
                root,
                "implementation-options",
                self._option("IMP-950", "QOL-999"),
            )

            with self.assertRaisesRegex(ValueError, r"IMP-950.*QOL-999"):
                records.validate_repository(root)

    def test_active_implementation_option_cannot_target_deprecated_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_registry(root)
            self._write_record(
                root,
                "items",
                self._item(
                    "QOL-950",
                    status="Deprecated",
                    evidence_claims=[],
                    deprecation_reason="Historical fixture.",
                    replaced_by=[],
                ),
            )
            self._write_record(
                root,
                "implementation-options",
                self._option("IMP-950", "QOL-950"),
            )

            with self.assertRaisesRegex(ValueError, r"IMP-950.*Deprecated.*QOL-950"):
                records.validate_repository(root)

    def test_deprecated_implementation_option_requires_deprecation_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp),
                "implementation-options",
                self._option("IMP-950", "QOL-950", status="Deprecated"),
            )

            with self.assertRaisesRegex(ValueError, r"deprecation_reason"):
                load_record(path)

    def test_active_implementation_option_cannot_declare_replacements(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp),
                "implementation-options",
                self._option("IMP-950", "QOL-950", replaced_by=["IMP-951"]),
            )

            with self.assertRaisesRegex(ValueError, r"Active.*replaced_by"):
                load_record(path)

    def test_deprecated_implementation_option_replacement_must_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_registry(root)
            self._write_record(
                root,
                "implementation-options",
                self._option(
                    "IMP-950",
                    "QOL-950",
                    status="Deprecated",
                    deprecation_reason="Superseded fixture.",
                    replaced_by=["IMP-999"],
                ),
            )

            with self.assertRaisesRegex(ValueError, r"IMP-950.*replacement.*IMP-999"):
                records.validate_repository(root)

    def test_deprecated_implementation_option_replacement_must_be_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_registry(root)
            self._write_record(root, "items", self._item("QOL-950"))
            self._write_record(
                root,
                "implementation-options",
                self._option(
                    "IMP-950",
                    "QOL-950",
                    status="Deprecated",
                    deprecation_reason="Superseded fixture.",
                    replaced_by=["IMP-951"],
                ),
            )
            self._write_record(
                root,
                "implementation-options",
                self._option(
                    "IMP-951",
                    "QOL-950",
                    status="Deprecated",
                    deprecation_reason="Also superseded.",
                    replaced_by=[],
                ),
            )

            with self.assertRaisesRegex(ValueError, r"IMP-950.*replacement.*Active.*IMP-951"):
                records.validate_repository(root)


if __name__ == "__main__":
    unittest.main()
