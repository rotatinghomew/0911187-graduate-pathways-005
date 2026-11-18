import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graduate_pathways.analysis import summarize
from graduate_pathways.reports import build_report


class GraduatePathwayTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "g1", "graduate_id": "s1", "kind": "graduate", "cohort": "2024", "field": "电气"},
            {"id": "p1", "graduate_id": "s1", "kind": "placement", "date": "2026-06-01", "source": "student", "verification": "unverified", "consent": "granted", "sector_code": "energy"},
            {"id": "p2", "graduate_id": "s1", "kind": "placement", "date": "2026-06-15", "source": "employer", "verification": "confirmed", "consent": "granted", "sector_code": "public"},
            {"id": "t1", "graduate_id": "s1", "kind": "taxonomy", "version": "v1", "sector_code": "energy", "category": "energy"},
            {"id": "t2", "graduate_id": "s1", "kind": "taxonomy", "version": "v1", "sector_code": "public", "category": "public"},
            {"id": "g2", "graduate_id": "s2", "kind": "graduate", "cohort": "2024", "field": "材料"},
            {"id": "p3", "graduate_id": "s2", "kind": "placement", "date": "2026-06-02", "source": "student", "verification": "confirmed", "consent": "withdrawn", "sector_code": "energy"},
        ]

    def test_sources_conflict_and_withdrawn_data_is_not_currently_used(self):
        results = summarize(self.records)
        self.assertEqual(results["s1"]["placement_status"], "conflict")
        self.assertEqual(results["s1"]["reported_sources"], ["employer", "student"])
        self.assertEqual(results["s2"]["placement_status"], "unknown")
        self.assertEqual(results["s2"]["withdrawn_count"], 1)

    def test_report_groups_coverage_without_treating_unknown_as_unemployed(self):
        report = build_report(self.records, "source-v2")
        self.assertEqual(report["unobserved"], ["s2"])
        self.assertEqual(report["cohort_coverage"]["2024:电气"]["graduates"], 1)
        self.assertEqual(report["source_revision"], "source-v2")


if __name__ == "__main__":
    unittest.main()
