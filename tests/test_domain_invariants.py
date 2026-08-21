from pathlib import Path
import tempfile
import unittest

import yaml

from qol_kb import records
from qol_kb.records import load_record


class QoLDomainInvariantTests(unittest.TestCase):
    def _item(self, item_id="QOL-950", **overrides):
        data = {
            "id": item_id,
            "statement": "Use the domain invariant fixture",
            "kind": "Intervention",
            "status": "Active",
            "categories": [],
            "applicability": "General",
            "support_mode": "Direct",
            "evidence_reviewed_at": "2026-08-21",
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

    def _reference(self, reference_id="REF-950", **overrides):
        data = {
            "id": reference_id,
            "title": "Domain invariant fixture reference",
            "status": "Active",
            "authors": ["Example Author"],
            "year": 2026,
            "source": "Fixture Journal",
            "source_type": "primary research",
            "urls": ["https://example.com/reference"],
            "supports": ["The fixture reference supports the fixture claim."],
        }
        data.update(overrides)
        return data

    def _write_record(self, root: Path, folder: str, front_matter: dict) -> Path:
        directory = root / folder
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{front_matter['id']}.md"
        yaml_text = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=True)
        path.write_text(f"---\n{yaml_text}---\n# Fixture\n", encoding="utf-8")
        return path

    def _write_category_registry(
        self,
        root: Path,
        categories: dict | None = None,
    ) -> Path:
        registry_path = root / "categories.yaml"
        registry_path.write_text(
            yaml.safe_dump(
                {"categories": categories or {}},
                sort_keys=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )
        return registry_path

    def _validate_repository(self, root: Path) -> None:
        validator = getattr(records, "validate_repository", None)
        self.assertIsNotNone(
            validator,
            "repository-level validation is required for cross-record invariants",
        )
        if not (root / "categories.yaml").exists():
            self._write_category_registry(root)
        validator(root)

    def test_active_item_rejects_unknown_kind(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(Path(tmp), "items", self._item(kind="Factor"))
            with self.assertRaisesRegex(ValueError, r"kind.*Factor|Factor.*kind"):
                load_record(path)

    def test_active_item_rejects_unknown_support_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp), "items", self._item(support_mode="Inference")
            )
            with self.assertRaisesRegex(
                ValueError, r"support_mode.*Inference|Inference.*support_mode"
            ):
                load_record(path)

    def test_item_lifecycle_rejects_unknown_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(Path(tmp), "items", self._item(status="Retired"))
            with self.assertRaisesRegex(ValueError, r"status.*Retired|Retired.*status"):
                load_record(path)

    def test_active_item_rejects_unknown_applicability(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp), "items", self._item(applicability="Universal")
            )
            with self.assertRaisesRegex(
                ValueError, r"applicability.*Universal|Universal.*applicability"
            ):
                load_record(path)

    def test_active_item_requires_at_least_one_support_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            claims = [
                {
                    "statement": "A constraint alone cannot justify the item.",
                    "role": "Constraint",
                    "strength": "High",
                    "references": ["REF-950"],
                }
            ]
            path = self._write_record(
                Path(tmp), "items", self._item(evidence_claims=claims)
            )
            with self.assertRaisesRegex(ValueError, r"Support"):
                load_record(path)

    def test_conditional_item_requires_non_empty_condition(self):
        for condition in (None, "   "):
            with self.subTest(condition=condition):
                with tempfile.TemporaryDirectory() as tmp:
                    path = self._write_record(
                        Path(tmp),
                        "items",
                        self._item(applicability="Conditional", condition=condition),
                    )
                    with self.assertRaisesRegex(ValueError, r"condition"):
                        load_record(path)

    def test_general_item_does_not_require_condition(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(Path(tmp), "items", self._item())
            self.assertEqual(load_record(path).front_matter["applicability"], "General")

    def test_claim_role_accepts_only_support_or_constraint(self):
        with tempfile.TemporaryDirectory() as tmp:
            claims = [
                {
                    "statement": "Invalid role fixture.",
                    "role": "Context",
                    "strength": "High",
                    "references": ["REF-950"],
                }
            ]
            path = self._write_record(
                Path(tmp), "items", self._item(evidence_claims=claims)
            )
            with self.assertRaisesRegex(ValueError, r"role.*Context|Context.*role"):
                load_record(path)

    def test_claim_strength_rejects_inference_and_unknown_values(self):
        for strength in ("Inference", "Very High"):
            with self.subTest(strength=strength):
                with tempfile.TemporaryDirectory() as tmp:
                    claims = [
                        {
                            "statement": "Invalid strength fixture.",
                            "role": "Support",
                            "strength": strength,
                            "references": ["REF-950"],
                        }
                    ]
                    path = self._write_record(
                        Path(tmp), "items", self._item(evidence_claims=claims)
                    )
                    with self.assertRaisesRegex(
                        ValueError, rf"strength.*{strength}|{strength}.*strength"
                    ):
                        load_record(path)

    def test_item_evidence_strength_uses_weakest_support_and_ignores_constraints(self):
        with tempfile.TemporaryDirectory() as tmp:
            claims = [
                {
                    "statement": "Strong support.",
                    "role": "Support",
                    "strength": "High",
                    "references": ["REF-950"],
                },
                {
                    "statement": "Moderate support.",
                    "role": "Support",
                    "strength": "Moderate",
                    "references": ["REF-950"],
                },
                {
                    "statement": "Low-strength constraint.",
                    "role": "Constraint",
                    "strength": "Low",
                    "references": ["REF-950"],
                },
            ]
            path = self._write_record(
                Path(tmp), "items", self._item(evidence_claims=claims)
            )
            record = load_record(path)
            self.assertEqual(getattr(record, "evidence_strength", None), "Moderate")

    def test_deprecated_item_requires_deprecation_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp),
                "items",
                self._item(status="Deprecated", evidence_claims=[], replaced_by=[]),
            )
            with self.assertRaisesRegex(ValueError, r"deprecation_reason"):
                load_record(path)

    def test_deprecated_item_allows_zero_or_multiple_replacements(self):
        replacements = ([], ["QOL-951", "QOL-952"])
        for replaced_by in replacements:
            with self.subTest(replaced_by=replaced_by):
                with tempfile.TemporaryDirectory() as tmp:
                    path = self._write_record(
                        Path(tmp),
                        "items",
                        self._item(
                            status="Deprecated",
                            evidence_claims=[],
                            deprecation_reason="Superseded fixture.",
                            replaced_by=replaced_by,
                        ),
                    )
                    self.assertEqual(
                        load_record(path).front_matter["replaced_by"],
                        tuple(replaced_by),
                    )

    def test_replacement_ids_must_resolve_to_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(
                root,
                "items",
                self._item(
                    status="Deprecated",
                    evidence_claims=[],
                    deprecation_reason="Superseded fixture.",
                    replaced_by=["QOL-999"],
                ),
            )
            with self.assertRaisesRegex(ValueError, r"QOL-999"):
                self._validate_repository(root)

    def test_item_rejects_unknown_relationship_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            relationships = [{"type": "requires", "target": "QOL-951"}]
            path = self._write_record(
                Path(tmp), "items", self._item(relationships=relationships)
            )
            with self.assertRaisesRegex(ValueError, r"requires"):
                load_record(path)

    def test_relationship_target_must_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(root, "references", self._reference())
            self._write_record(
                root,
                "items",
                self._item(relationships=[{"type": "informs", "target": "QOL-999"}]),
            )
            with self.assertRaisesRegex(ValueError, r"QOL-999"):
                self._validate_repository(root)

    def test_relationship_target_must_be_a_distinct_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(root, "references", self._reference())
            self._write_record(
                root,
                "items",
                self._item(relationships=[{"type": "informs", "target": "QOL-950"}]),
            )
            with self.assertRaisesRegex(ValueError, r"QOL-950"):
                self._validate_repository(root)

    def test_reference_lifecycle_rejects_unknown_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp), "references", self._reference(status="Retired")
            )
            with self.assertRaisesRegex(ValueError, r"status.*Retired|Retired.*status"):
                load_record(path)

    def test_deprecated_reference_requires_deprecation_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp), "references", self._reference(status="Deprecated")
            )
            with self.assertRaisesRegex(ValueError, r"deprecation_reason"):
                load_record(path)

    def test_active_reference_cannot_declare_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_record(
                Path(tmp),
                "references",
                self._reference(replaced_by="REF-951"),
            )
            with self.assertRaisesRegex(
                ValueError,
                r"REF-950\.md.*Active reference.*replaced_by",
            ):
                load_record(path)

    def test_deprecated_reference_replacement_must_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(
                root,
                "references",
                self._reference(
                    status="Deprecated",
                    deprecation_reason="Superseded reference fixture.",
                    replaced_by="REF-999",
                ),
            )
            with self.assertRaisesRegex(
                ValueError,
                r"REF-950.*replacement.*does not resolve.*REF-999",
            ):
                self._validate_repository(root)

    def test_deprecated_reference_replacement_must_be_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(
                root,
                "references",
                self._reference(
                    status="Deprecated",
                    deprecation_reason="Superseded reference fixture.",
                    replaced_by="REF-950",
                ),
            )
            with self.assertRaisesRegex(
                ValueError,
                r"REF-950.*replacement.*distinct",
            ):
                self._validate_repository(root)

    def test_deprecated_reference_replacement_must_be_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(
                root,
                "references",
                self._reference(
                    status="Deprecated",
                    deprecation_reason="Superseded reference fixture.",
                    replaced_by="REF-951",
                ),
            )
            self._write_record(
                root,
                "references",
                self._reference(
                    reference_id="REF-951",
                    status="Deprecated",
                    deprecation_reason="Also superseded.",
                ),
            )
            with self.assertRaisesRegex(
                ValueError,
                r"REF-950.*replacement.*Active.*REF-951",
            ):
                self._validate_repository(root)

    def test_evidence_claim_references_must_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(root, "references", self._reference())
            claims = [
                {
                    "statement": "Unresolved reference fixture.",
                    "role": "Support",
                    "strength": "High",
                    "references": ["REF-999"],
                }
            ]
            self._write_record(root, "items", self._item(evidence_claims=claims))
            with self.assertRaisesRegex(ValueError, r"REF-999"):
                self._validate_repository(root)

    def test_active_items_cannot_use_deprecated_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(
                root,
                "references",
                self._reference(
                    status="Deprecated",
                    deprecation_reason="Superseded reference fixture.",
                ),
            )
            self._write_record(root, "items", self._item())
            with self.assertRaisesRegex(ValueError, r"REF-950.*Deprecated|Deprecated.*REF-950"):
                self._validate_repository(root)

    def test_valid_repository_with_resolved_links_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(root, "references", self._reference())
            self._write_record(root, "items", self._item())
            self._write_record(
                root,
                "items",
                self._item(
                    item_id="QOL-951",
                    statement="Use the second fixture",
                    relationships=[{"type": "informs", "target": "QOL-950"}],
                ),
            )
            self._validate_repository(root)

    def test_repository_requires_category_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, r"categories.yaml.*required"):
                records.validate_repository(Path(tmp))

    def test_active_item_accepts_only_known_active_categories(self):
        cases = (
            (
                "active",
                {"sleep": {"definition": "Sleep timing.", "status": "Active"}},
                None,
            ),
            ("unknown", {}, r"QOL-950.*unknown category.*sleep"),
            (
                "deprecated",
                {
                    "sleep": {
                        "definition": "Historical sleep tag.",
                        "status": "Deprecated",
                    }
                },
                r"QOL-950.*Deprecated category.*sleep",
            ),
        )
        for label, category_entries, message in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self._write_category_registry(root, category_entries)
                self._write_record(root, "references", self._reference())
                self._write_record(root, "items", self._item(categories=["sleep"]))
                if message is None:
                    self._validate_repository(root)
                else:
                    with self.assertRaisesRegex(ValueError, message):
                        self._validate_repository(root)

    def test_deprecated_item_may_retain_historical_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_category_registry(root)
            self._write_record(
                root,
                "items",
                self._item(
                    status="Deprecated",
                    categories=["historical-category"],
                    evidence_claims=[],
                    deprecation_reason="Historical fixture.",
                    replaced_by=[],
                ),
            )
            self._validate_repository(root)

    def test_category_rename_does_not_change_item_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_record(root, "references", self._reference())
            item_path = self._write_record(
                root,
                "items",
                self._item(categories=["old-name"]),
            )
            self._write_category_registry(
                root,
                {"old-name": {"definition": "Old tag.", "status": "Active"}},
            )
            self._validate_repository(root)

            item_path = self._write_record(
                root,
                "items",
                self._item(categories=["new-name"]),
            )
            self._write_category_registry(
                root,
                {"new-name": {"definition": "New tag.", "status": "Active"}},
            )
            self._validate_repository(root)
            self.assertEqual(load_record(item_path).front_matter["id"], "QOL-950")


if __name__ == "__main__":
    unittest.main()
