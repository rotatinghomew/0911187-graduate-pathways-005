"""计算毕业 cohort 的去向覆盖和岗位能力匹配。"""

from collections import defaultdict


def summarize(records):
    graduates = defaultdict(dict)
    for record in records:
        graduate = graduates[str(record["graduate_id"])]
        if record["kind"] == "graduate":
            graduate["profile"] = record
        elif record["kind"] == "placement":
            graduate.setdefault("placements", []).append(record)
        else:
            graduate.setdefault("requirements", []).append(record)
    result = {}
    for graduate_id, data in sorted(graduates.items()):
        profile = data.get("profile", {})
        placement = sorted(data.get("placements", []), key=lambda item: item.get("date", ""))
        requirements = data.get("requirements", [])
        skills = set(profile.get("skills", []))
        matches = [{"job_id": item.get("job_id"), "matched": sorted(skills & set(item.get("required_skills", []))), "missing": sorted(set(item.get("required_skills", [])) - skills)} for item in requirements]
        result[graduate_id] = {
            "cohort": profile.get("cohort"),
            "field": profile.get("field"),
            "placement_status": placement[-1].get("status") if placement else "unknown",
            "placement_count": len(placement),
            "energy_sector": bool(placement and placement[-1].get("sector") == "energy"),
            "job_matches": matches,
        }
    return result
