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
            graduate.setdefault("taxonomies", []).append(record)
    result = {}
    for graduate_id, data in sorted(graduates.items()):
        profile = data.get("profile", {})
        placements = sorted(data.get("placements", []), key=lambda item: (item.get("date", ""), item["id"]))
        authorized = [item for item in placements if item.get("consent") == "granted"]
        taxonomy = {str(item["sector_code"]): item for item in data.get("taxonomies", [])}
        categories = [taxonomy.get(str(item.get("sector_code")), {}) for item in authorized]
        sectors = {item.get("category") for item in categories if item.get("category")}
        sources = sorted({str(item["source"]) for item in authorized})
        confirmations = sorted({str(item["verification"]) for item in authorized})
        result[graduate_id] = {
            "cohort": profile.get("cohort"),
            "field": profile.get("field"),
            "placement_status": "unknown" if not authorized else ("conflict" if len(sectors) > 1 else "observed"),
            "reported_sources": sources,
            "verification_states": confirmations,
            "sector_categories": sorted(sectors),
            "unverified_count": sum(item.get("verification") != "confirmed" for item in authorized),
            "withdrawn_count": sum(item.get("consent") != "granted" for item in placements),
        }
    return result
