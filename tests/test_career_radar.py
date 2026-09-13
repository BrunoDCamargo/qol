from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from qol_kb.career_radar import validate_career_radar


ROOT = Path(__file__).resolve().parents[1]


class CareerRadarTests(unittest.TestCase):
    def _write_radar(self, organizations: str, sources: str) -> Path:
        temp_dir = TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        radar = root / "career-radar"
        radar.mkdir()
        (radar / "organizations.yaml").write_text(organizations, encoding="utf-8")
        (radar / "sources.yaml").write_text(sources, encoding="utf-8")
        return root

    def test_accepts_minimal_valid_curitiba_organization_and_source(self):
        root = self._write_radar(
            """
- id: example-research
  name: Example Research
  organization_type: research-institute
  location:
    city: Curitiba
    state: PR
    country: Brasil
  viable_from_curitiba:
    - onsite
  rd_evidence:
    url: https://example.org/rd
    note: Maintains an institutional R&D program.
  careers_url: https://example.org/careers
  last_checked: 2026-09-13
""",
            """
- id: example-source
  name: Example Source
  source_type: academic-opportunities
  url: https://example.org/opportunities
  scope: Brasil
  last_checked: 2026-09-13
""",
        )
        validate_career_radar(root)

    def test_rejects_duplicate_organization_ids(self):
        root = self._write_radar(
            """
- &base
  id: duplicate
  name: First
  organization_type: company
  location: {city: Curitiba, state: PR, country: Brasil}
  viable_from_curitiba: [onsite]
  rd_evidence: {url: https://example.org/rd, note: R&D activity.}
  careers_url: https://example.org/careers
  last_checked: 2026-09-13
- <<: *base
  name: Second
""",
            "[]\n",
        )
        with self.assertRaisesRegex(ValueError, "duplicate organization id: duplicate"):
            validate_career_radar(root)

    def test_rejects_invalid_organization_type(self):
        root = self._write_radar(
            """
- id: bad-type
  name: Bad Type
  organization_type: consultancy
  location: {city: Curitiba, state: PR, country: Brasil}
  viable_from_curitiba: [onsite]
  rd_evidence: {url: https://example.org/rd, note: R&D activity.}
  careers_url: https://example.org/careers
  last_checked: 2026-09-13
""",
            "[]\n",
        )
        with self.assertRaisesRegex(ValueError, "organization_type"):
            validate_career_radar(root)

    def test_rejects_invalid_source_type(self):
        root = self._write_radar(
            "[]\n",
            """
- id: bad-source
  name: Bad Source
  source_type: social-media
  url: https://example.org
  scope: Brasil
  last_checked: 2026-09-13
""",
        )
        with self.assertRaisesRegex(ValueError, "source_type"):
            validate_career_radar(root)

    def test_rejects_invalid_last_checked(self):
        root = self._write_radar(
            "[]\n",
            """
- id: bad-date
  name: Bad Date
  source_type: public-jobs
  url: https://example.org
  scope: Brasil
  last_checked: 13/09/2026
""",
        )
        with self.assertRaisesRegex(ValueError, "last_checked"):
            validate_career_radar(root)

    def test_rejects_timestamp_last_checked(self):
        root = self._write_radar(
            "[]\n",
            """
- id: bad-timestamp
  name: Bad Timestamp
  source_type: public-jobs
  url: https://example.org
  scope: Brasil
  last_checked: 2026-09-13T12:00:00
""",
        )
        with self.assertRaisesRegex(ValueError, "last_checked"):
            validate_career_radar(root)


if __name__ == "__main__":
    unittest.main()
