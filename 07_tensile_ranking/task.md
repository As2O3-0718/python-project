# 项目 07：拉伸试验批次排名

## 今日目标

使用 pandas 清洗拉伸试验数据，筛选性能达标试样，按材料牌号汇总结果，并通过多条件排序生成批次排名。

## 知识点

- pandas 读取与写入 CSV
- 缺失值处理
- 向量化多条件布尔筛选
- 新增计算列
- `groupby()` 与多项聚合
- 多条件排序
- `pathlib.Path` 与跨目录文件定位

## 明确任务

1. 新建 `tensile_results.csv`，包含表头 `sample_id,alloy,batch,yield_strength_mpa,tensile_strength_mpa,elongation_pct`，并写入下列记录：

   ```text
   T01,Al-6061,A,245,310,13.5
   T02,Al-6061,A,238,302,11.8
   T03,Al-6061,B,252,318,14.2
   T04,Al-6061,B,,315,13.1
   T05,Steel-Q,C,520,650,16.0
   T06,Steel-Q,C,535,670,14.5
   T07,Steel-Q,D,510,640,12.0
   T08,Steel-Q,D,528,,15.2
   T09,Steel-Q,D,518,655,13.8
   ```

2. 使用 pandas 读取数据，在终端输出总记录数，以及三个强度与塑性数值列各自的缺失值数量。
3. 删除 `yield_strength_mpa`、`tensile_strength_mpa` 或 `elongation_pct` 缺失的记录，只用完整记录进行后续计算。
4. 为完整记录新增 `yield_ratio` 列，计算公式为：屈服强度 ÷ 抗拉强度。
5. 为完整记录新增布尔列 `performance_pass`。试样必须同时满足所属牌号的全部条件才算达标，边界值也算达标：
   - `Al-6061`：抗拉强度不低于 305 MPa，断后伸长率不低于 12.0%，屈强比不高于 0.80。
   - `Steel-Q`：抗拉强度不低于 645 MPa，断后伸长率不低于 13.0%，屈强比不高于 0.82。
6. 按 `alloy` 和 `batch` 分组，汇总每个批次的完整试样数、平均抗拉强度、平均断后伸长率、达标试样数和达标率。不得通过手写循环逐行累加统计。
7. 将汇总表按以下优先级排序：达标率从高到低；达标率相同时，平均抗拉强度从高到低；仍相同时，批次名称按升序排列。
8. 将结果写入 `batch_ranking.csv`，表头必须为 `rank,alloy,batch,valid_count,average_tensile_strength_mpa,average_elongation_pct,pass_count,pass_rate_pct`。排名从 1 开始且排序后连续；三个平均值或比率相关结果均保留两位小数；输出文件不得包含额外索引列。
9. 在终端按排名顺序逐行输出每个批次的牌号、批次、平均抗拉强度和达标率。

## 示例输入输出

终端输出可为：

```text
总记录数：9
yield_strength_mpa 缺失：1
tensile_strength_mpa 缺失：1
elongation_pct 缺失：0
第 1 名：Steel-Q C，平均抗拉强度 660.00 MPa，达标率 100.00%
第 2 名：Al-6061 B，平均抗拉强度 318.00 MPa，达标率 100.00%
第 3 名：Steel-Q D，平均抗拉强度 647.50 MPa，达标率 50.00%
第 4 名：Al-6061 A，平均抗拉强度 306.00 MPa，达标率 50.00%
```

## 验收标准

- 程序可从项目目录以外启动，仍能正确找到输入 CSV。
- pandas 正确读取全部 9 条记录，并正确统计三个数值列的缺失值。
- 后续计算只使用 7 条数值完整的记录。
- `yield_ratio` 和两个牌号的达标判断正确，所有边界条件均包含在内。
- 分组汇总中的完整试样数、平均值、达标数和达标率正确。
- 统计与筛选主要使用 pandas 向量化操作和分组聚合，不手写逐行累加。
- 排名严格遵守三层排序规则，`rank` 从 1 开始连续编号。
- `batch_ranking.csv` 表头、排序、两位小数格式正确，且无额外索引列。
- 输入文件只有表头、没有数据行时，程序不报错，并生成只含正确表头的 `batch_ranking.csv`。
- 代码使用清晰的 `snake_case` 命名。

## 建议文件名

`tensile_ranking.py`

## 可选挑战

额外生成 `failed_samples.csv`，保存数值完整但未达标的试样，并新增 `failure_reason` 列，内容可为“抗拉强度”“断后伸长率”“屈强比”中的一个或多个原因。
