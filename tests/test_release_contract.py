from pathlib import Path
import re
import unittest

from qol_kb import records, views


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ReleaseContractTests(unittest.TestCase):
    def test_readme_is_an_entry_point_to_authoritative_docs(self):
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

        for target in (
            "CONTEXT.md",
            "docs/architecture.md",
            "docs/specification.md",
            "CONTRIBUTING.md",
        ):
            self.assertIn(f"]({target})", readme)

        for duplicated_normative_section in (
            "## Core design principles",
            "## Adding or revising knowledge",
            "## Evidence update policy",
        ):
            self.assertNotIn(duplicated_normative_section, readme)

    def test_authoritative_docs_use_the_resolved_evidence_vocabulary(self):
        normative_paths = (
            Path("README.md"),
            Path("CONTEXT.md"),
            Path("CONTRIBUTING.md"),
            Path("docs/architecture.md"),
            Path("docs/specification.md"),
        )
        forbidden_patterns = (
            "High | Moderate | Low | Inference",
            "Evidence Strength: High | Moderate | Low | Inference",
            "### Inference",
        )

        for relative_path in normative_paths:
            path = REPOSITORY_ROOT / relative_path
            self.assertTrue(path.is_file(), relative_path.as_posix())
            source = path.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                self.assertNotIn(pattern, source, relative_path.as_posix())

        contributing = (REPOSITORY_ROOT / "CONTRIBUTING.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Evidence Strength", contributing)
        self.assertIn("High", contributing)
        self.assertIn("Moderate", contributing)
        self.assertIn("Low", contributing)
        self.assertIn("Support Mode", contributing)
        self.assertIn("Inferred", contributing)

    def test_contribution_rules_name_every_editable_authority(self):
        contributing = (REPOSITORY_ROOT / "CONTRIBUTING.md").read_text(
            encoding="utf-8"
        )
        for canonical_source in (
            "items/",
            "references/",
            "implementation-options/",
            "categories.yaml",
            "topic-views.yaml",
        ):
            self.assertIn(canonical_source, contributing)

        for release_command in (
            "validate_repository('.')",
            "python -m qol_kb.views --check",
            "python -m unittest discover -s tests",
        ):
            self.assertIn(release_command, contributing)

    def test_transition_era_specs_and_plans_are_not_current_docs(self):
        self.assertFalse((REPOSITORY_ROOT / "docs" / "superpowers").exists())

    def test_every_emitted_qol_and_ref_identity_resolves(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        canonical_qol = {record.front_matter["id"] for record in snapshot.items}
        canonical_ref = {record.front_matter["id"] for record in snapshot.references}
        rendered = "\n".join(
            content.decode("utf-8")
            for content in views.generate_views(REPOSITORY_ROOT).values()
        )
        emitted_qol = set(re.findall(r"\bQOL-[0-9]{3,}\b", rendered))
        emitted_ref = set(re.findall(r"\bREF-[0-9]{3,}\b", rendered))

        self.assertFalse(emitted_qol - canonical_qol)
        self.assertFalse(emitted_ref - canonical_ref)
        for identity in emitted_qol:
            self.assertTrue((REPOSITORY_ROOT / "items" / f"{identity}.md").is_file())
        for identity in emitted_ref:
            self.assertTrue(
                (REPOSITORY_ROOT / "references" / f"{identity}.md").is_file()
            )

    def test_ci_is_the_final_release_gate_without_transition_repair(self):
        workflow = (
            REPOSITORY_ROOT / ".github" / "workflows" / "tests.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("name: Release gate", workflow)
        self.assertIn("name: Canonical repository release gate", workflow)
        self.assertIn(
            'python -c "from qol_kb.records import validate_repository; validate_repository(\'.\')"',
            workflow,
        )
        self.assertIn("python -m qol_kb.views --check", workflow)
        self.assertIn("python -m unittest discover -s tests", workflow)
        self.assertNotIn("if ! python -m qol_kb.views --check", workflow)
        self.assertNotIn("git diff -- catalog.md references.md", workflow)


if __name__ == "__main__":
    unittest.main()
