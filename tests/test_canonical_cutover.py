from pathlib import Path
import unittest

from qol_kb import records, views


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

    def test_legacy_registry_compatibility_paths_are_retired(self):
        self.assertEqual(
            set(views.OUTPUT_PATHS),
            {
                Path("generated/catalog.md"),
                Path("generated/references.md"),
                Path("generated/implementation-options.md"),
            },
        )
        self.assertFalse((REPOSITORY_ROOT / "catalog.md").exists())
        self.assertFalse((REPOSITORY_ROOT / "references.md").exists())

    def test_topic_maps_are_derived_from_canonical_metadata(self):
        topic_path = Path("topics/attention-digital.md")
        generated = views.generate_views(REPOSITORY_ROOT)

        self.assertIn(topic_path, generated)
        rendered = generated[topic_path].decode("utf-8")
        self.assertIn(
            "| [QOL-014](../items/QOL-014.md) | Remove nonessential badges, banners, and vibrations | Intervention | attention, technology | Moderate | General | Inferred | Active | [REF-009](../references/REF-009.md) |",
            rendered,
        )
        self.assertIn(
            "A smartphone with continuous internet creates a high-frequency opportunity",
            rendered,
        )
        self.assertNotIn("**Categories:**", rendered)
        self.assertNotIn("**Evidence:**", rendered)
        self.assertNotIn("**Applicability:**", rendered)
        self.assertNotIn("../references.md#ref-", rendered)

    def test_topic_membership_is_separate_from_the_generated_map(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        selections = views.load_topic_selections(REPOSITORY_ROOT)
        source = (REPOSITORY_ROOT / "topics" / "attention-digital.md").read_text(
            encoding="utf-8"
        )
        tampered = source.replace(
            "[QOL-014](../items/QOL-014.md)",
            "[QOL-999](../items/QOL-999.md)",
            1,
        )

        rendered = views.render_topic_view(
            tampered,
            snapshot,
            selections["attention-digital.md"],
        )

        self.assertIn("[QOL-014](../items/QOL-014.md)", rendered)
        self.assertNotIn("[QOL-999](../items/QOL-999.md)", rendered)

    def test_topic_views_do_not_link_retired_registry_paths(self):
        for topic_path in sorted((REPOSITORY_ROOT / "topics").glob("*.md")):
            source = topic_path.read_text(encoding="utf-8")
            self.assertNotIn("../catalog.md", source, topic_path.name)
            self.assertNotIn("../references.md", source, topic_path.name)

    def test_topic_views_reject_reintroduced_legacy_registry_links(self):
        snapshot = records.load_repository(REPOSITORY_ROOT)
        selections = views.load_topic_selections(REPOSITORY_ROOT)
        source = (REPOSITORY_ROOT / "topics" / "attention-digital.md").read_text(
            encoding="utf-8"
        )
        tampered = source + "\n[Legacy catalog](../catalog.md)\n"

        with self.assertRaisesRegex(ValueError, "legacy registry link"):
            views.render_topic_view(
                tampered,
                snapshot,
                selections["attention-digital.md"],
            )


if __name__ == "__main__":
    unittest.main()
