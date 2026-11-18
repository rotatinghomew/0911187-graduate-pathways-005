"""读取毕业 cohort、求职经历与岗位要求。"""

import json
from pathlib import Path


def load_records(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("记录文件必须包含数组")
    records = []
    seen = set()
    for position, record in enumerate(payload):
        if not isinstance(record, dict) or not record.get("id") or not record.get("graduate_id"):
            raise ValueError(f"第 {position + 1} 条去向记录缺少身份字段")
        if record["id"] in seen:
            raise ValueError(f"重复记录标识：{record['id']}")
        seen.add(record["id"])
        if record.get("kind") not in {"graduate", "placement", "taxonomy"}:
            raise ValueError(f"记录 {record['id']} 的 kind 无效")
        if record["kind"] == "placement" and (not record.get("source") or record.get("verification") not in {"confirmed", "unverified"}):
            raise ValueError(f"去向 {record['id']} 缺少来源或核实状态")
        if record["kind"] == "taxonomy" and (not record.get("version") or not record.get("sector_code")):
            raise ValueError(f"分类记录 {record['id']} 缺少版本或行业代码")
        records.append(dict(record))
    return records
