import unittest

from graduate_pathways.analysis import summarize
from graduate_pathways.reports import build_report


class GraduatePathwayTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "g1", "graduate_id": "s1", "kind": "graduate", "cohort": "2024", "field": "电气", "skills": ["储能", "数据分析"]},
            {"id": "p1", "graduate_id": "s1", "kind": "placement", "date": "2026-06-01", "status": "employed", "sector": "energy"},
            {"id": "j1", "graduate_id": "s1", "kind": "job_requirement", "job_id": "r1", "required_skills": ["储能", "调度"]},
            {"id": "g2", "graduate_id": "s2", "kind": "graduate", "cohort": "2024", "field": "材料", "skills": []},
        ]

    def test_cohort_profile_matches_requirements_without_fabricating_placement(self):
        results = summarize(self.records)
        self.assertEqual(results["s1"]["job_matches"][0]["missing"], ["调度"])
        self.assertTrue(results["s1"]["energy_sector"])
        self.assertEqual(results["s2"]["placement_status"], "unknown")

    def test_report_surfaces_missing_outcome_coverage(self):
        report = build_report(self.records, "source-v2")
        self.assertEqual(report["unobserved"], ["s2"])
        self.assertEqual(report["source_revision"], "source-v2")
        self.assertEqual(report["cohort_coverage"]["2024:电气"]["graduates"], 1)


if __name__ == "__main__":
    unittest.main()
