"""可追溯的当前汇总报告。"""

from .analysis import summarize
from .cohorts import coverage


def build_report(records, source_revision=""):
    if not source_revision:
        raise ValueError("必须提供数据修订标识")
    graduates = summarize(records)
    return {
        "source_revision": source_revision,
        "record_count": len(records),
        "graduates": graduates,
        "cohort_coverage": coverage(graduates),
        "unobserved": sorted(graduate for graduate, facts in graduates.items() if facts["placement_status"] == "unknown"),
    }
