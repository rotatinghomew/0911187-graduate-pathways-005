# 毕业去向与岗位匹配

项目以本地合成数据分析不同毕业 cohort 的就业结果及基层能源岗位能力要求。`graduate` 记录个人培养方向和已掌握能力，`placement` 记录去向观察，`job_requirement` 描述岗位能力需求；没有去向记录表示未知，不作为未就业。

输入为 UTF-8 JSON 数组，记录须含稳定 `id`、`graduate_id` 和 `kind`。报告给出 cohort、去向覆盖、能源行业分布以及岗位能力差距，不把岗位匹配解释成就业结果或因果关系。当前项目只看最新去向记录，尚未对更正前的已发布 cohort 结果留档。

需要 Python 3.11 或更新版本，不依赖外部服务。运行 `PYTHONPATH=src python -m unittest discover -s tests -v`。`graduate_pathways.facts` 校验记录，`graduate_pathways.analysis` 关联培养与岗位要求，`graduate_pathways.cohorts.coverage` 计算分学科去向覆盖，`graduate_pathways.reports` 汇总结果及未知去向。样例见 `examples/sample.json`。
