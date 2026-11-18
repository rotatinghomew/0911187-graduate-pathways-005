# 毕业去向与岗位匹配

项目以本地合成数据分析毕业 cohort 的多来源去向及基层能源岗位分类。`graduate` 记录毕业年份与学科，`placement` 保存学生/导师/单位来源、核实状态、授权状态和行业代码，`taxonomy` 保存带版本的岗位分类。

输入为 UTF-8 JSON 数组，记录须含稳定 `id`、`graduate_id` 和 `kind`。报告区分互相冲突的来源、未核实记录和撤回授权的资料；未联系上的毕业生不作为未就业。当前项目能按 cohort 汇总现行分类，但不保留已发布统计使用的授权与分类版本。

需要 Python 3.11 或更新版本，不依赖外部服务。运行 `PYTHONPATH=src python -m unittest discover -s tests -v`。`graduate_pathways.facts` 校验记录，`graduate_pathways.analysis` 解释来源核实与分类分歧，`graduate_pathways.cohorts.coverage` 计算分学科回访覆盖，`graduate_pathways.reports` 汇总当前结果。样例见 `examples/sample.json`。
