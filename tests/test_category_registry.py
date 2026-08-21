from pathlib import Path
import tempfile
import unittest

from qol_kb.records import load_category_registry


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CategoryRegistryTests(unittest.TestCase):
    def _write_registry(self, root: Path, yaml_text: str) -> Path:
        path = root / "categories.yaml"
        path.write_text(yaml_text, encoding="utf-8")
        return path

    def test_seeded_registry_loads_canonical_categories(self):
        categories = load_category_registry(REPOSITORY_ROOT / "categories.yaml")
        self.assertEqual(
            set(categories),
            {"physical-activity", "environment", "mental-health", "circadian"},
        )
        self.assertEqual(categories["physical-activity"].status, "Active")
        self.assertTrue(categories["physical-activity"].definition.strip())

    def test_registry_rejects_non_kebab_case_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n  Mental Health:\n    definition: Invalid name.\n    status: Active\n",
            )
            with self.assertRaisesRegex(ValueError, r"Mental Health"):
                load_category_registry(path)

    def test_registry_rejects_non_string_category_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n  123:\n    definition: Invalid name.\n    status: Active\n",
            )
            with self.assertRaisesRegex(ValueError, r"123|string"):
                load_category_registry(path)

    def test_registry_rejects_duplicate_category_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n"
                "  physical-activity:\n"
                "    definition: First definition.\n"
                "    status: Active\n"
                "  physical-activity:\n"
                "    definition: Second definition.\n"
                "    status: Active\n",
            )
            with self.assertRaisesRegex(ValueError, r"duplicate.*physical-activity"):
                load_category_registry(path)

    def test_registry_rejects_unhashable_yaml_key_with_registry_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n"
                "  ? [invalid, key]\n"
                "  :\n"
                "    definition: Invalid key.\n"
                "    status: Active\n",
            )
            with self.assertRaisesRegex(ValueError, r"categories\.yaml.*unhashable"):
                load_category_registry(path)

    def test_registry_rejects_blank_definition_and_unknown_status(self):
        invalid_entries = (
            (
                "blank-definition",
                "categories:\n  sleep:\n    definition: '   '\n    status: Active\n",
                r"sleep.*definition|definition.*sleep",
            ),
            (
                "unknown-status",
                "categories:\n  sleep:\n    definition: Sleep timing.\n    status: Retired\n",
                r"Retired|status",
            ),
        )
        for label, yaml_text, message in invalid_entries:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                path = self._write_registry(Path(tmp), yaml_text)
                with self.assertRaisesRegex(ValueError, message):
                    load_category_registry(path)

    def test_deprecated_category_allows_no_replacement_or_active_replacement(self):
        registry_variants = (
            "categories:\n  old-name:\n    definition: Historical tag.\n    status: Deprecated\n",
            "categories:\n"
            "  current-name:\n"
            "    definition: Current tag.\n"
            "    status: Active\n"
            "  old-name:\n"
            "    definition: Historical tag.\n"
            "    status: Deprecated\n"
            "    replaced_by: current-name\n",
        )
        for yaml_text in registry_variants:
            with self.subTest(yaml_text=yaml_text), tempfile.TemporaryDirectory() as tmp:
                categories = load_category_registry(
                    self._write_registry(Path(tmp), yaml_text)
                )
                self.assertEqual(categories["old-name"].status, "Deprecated")

    def test_active_category_rejects_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n"
                "  current-name:\n"
                "    definition: Current tag.\n"
                "    status: Active\n"
                "    replaced_by: other-name\n"
                "  other-name:\n"
                "    definition: Other tag.\n"
                "    status: Active\n",
            )
            with self.assertRaisesRegex(ValueError, r"current-name.*replaced_by"):
                load_category_registry(path)

    def test_deprecated_category_replacement_must_be_distinct_known_and_active(self):
        invalid_targets = (
            ("self", "old-name", "", r"old-name.*distinct"),
            ("unknown", "missing-name", "", r"missing-name.*resolve"),
            (
                "deprecated",
                "older-name",
                "  older-name:\n"
                "    definition: Older historical tag.\n"
                "    status: Deprecated\n",
                r"older-name.*Active|Active.*older-name",
            ),
        )
        for label, target, extra_entry, message in invalid_targets:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                path = self._write_registry(
                    Path(tmp),
                    "categories:\n"
                    f"{extra_entry}"
                    "  old-name:\n"
                    "    definition: Historical tag.\n"
                    "    status: Deprecated\n"
                    f"    replaced_by: {target}\n",
                )
                with self.assertRaisesRegex(ValueError, message):
                    load_category_registry(path)


if __name__ == "__main__":
    unittest.main()
