# 项目 05：热处理实验 CSV 汇总

## 今日目标

使用 pandas 从 CSV 文件读取热处理实验记录，按工艺统计试样数量、平均硬度和最高硬度，并把统计结果写入新的 CSV 文件。

## 知识点

- pandas 的 `DataFrame`
- `pandas.read_csv()` 与 `DataFrame.to_csv()`
- 列选择与数据类型检查
- `groupby()` 分组统计
- `count()`、`mean()` 和 `max()` 聚合计算
- `pathlib.Path` 与相对路径

## 明确任务

1. 新建 `heat_treatment_data.csv`，包含表头 `sample_id,process,temperature_c,hardness_hv`，并写入下列记录：

   ```text
   HT01,annealed,650,142
   HT02,annealed,650,146
   HT03,quenched,850,218
   HT04,quenched,850,224
   HT05,tempered,500,185
   HT06,tempered,500,191
   ```

2. 使用 pandas 读取该文件，并在终端输出数据行数、列名和各列的数据类型；温度列与硬度列必须是数值类型。
3. 使用 pandas 按 `process` 分组，汇总每种工艺的试样数量、平均硬度和最高硬度。统计部分不得通过手写字典和循环逐行累加完成。
4. 在终端输出每种工艺的一行汇总信息；工艺按首次出现的顺序输出。
5. 使用 pandas 新建 `heat_treatment_summary.csv`，表头必须为 `process,sample_count,average_hardness_hv,max_hardness_hv`，写入各工艺的汇总结果；输出文件不得包含额外的索引列。

## 示例输入输出

输入文件中的记录如：

```text
HT01,annealed,650,142
HT02,annealed,650,146
```

终端输出可为：

```text
annealed: 2 个试样，平均硬度 144.0 HV，最高硬度 146.0 HV
quenched: 2 个试样，平均硬度 221.0 HV，最高硬度 224.0 HV
tempered: 2 个试样，平均硬度 188.0 HV，最高硬度 191.0 HV
```

生成的汇总 CSV 内容应包含：

```text
process,sample_count,average_hardness_hv,max_hardness_hv
annealed,2,144.0,146.0
```

## 验收标准

- 程序可从项目目录以外启动，仍能正确找到输入 CSV。
- pandas 能正确读取表头和全部 6 条记录，所得表格为 6 行、4 列。
- `temperature_c` 与 `hardness_hv` 均为数值类型。
- 三种工艺的数量、平均硬度和最高硬度均正确；平均硬度与最高硬度显示一位小数。
- 统计过程使用 pandas 分组聚合完成。
- 生成的 `heat_treatment_summary.csv` 有正确表头和 3 条汇总记录，且没有多余索引列。
- 输入文件只有表头、没有数据行时，程序不报错，并生成只有表头的汇总文件。
- 代码使用清晰的 `snake_case` 命名，并正确导入 pandas。

## 建议文件名

`heat_treatment_pandas.py`

## 可选挑战

使用 pandas 条件筛选找出硬度低于 180 HV 的试样，并将结果写入 `low_hardness_samples.csv`。
