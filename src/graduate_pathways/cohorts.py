"""按毕业年份和学科计算去向观测覆盖。"""

from collections import defaultdict


def coverage(graduates):
    groups = defaultdict(lambda: {"graduates": 0, "placement_observed": 0, "energy_sector": 0})
    for graduate in graduates.values():
        cohort = (str(graduate.get("cohort", "unknown")), str(graduate.get("field", "unknown")))
        group = groups[cohort]
        group["graduates"] += 1
        if graduate["placement_status"] != "unknown":
            group["placement_observed"] += 1
        group["energy_sector"] += int(graduate["energy_sector"])
    return {f"{year}:{field}": values for (year, field), values in sorted(groups.items())}
