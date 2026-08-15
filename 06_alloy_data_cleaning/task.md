# 项目 06：合金成分数据清洗与质量汇总

## 今日目标

使用 pandas 识别实验数据中的缺失值，筛选有效记录，判断合金成分是否合格，并按合金牌号汇总检测结果。

## 知识点

- pandas 缺失值与 `NaN`
- `isna()`、`notna()` 和 `dropna()`
- 多条件布尔筛选
- 新增布尔列
- `groupby()` 分组聚合
- 布尔值的计数与平均值
- `pathlib.Path` 与 CSV 文件读写

## 明确任务

1. 新建 `alloy_composition.csv`，包含表头 `sample_id,alloy,carbon_pct,chromium_pct,hardness_hv`，并写入下列记录：

   ```text
   S01,Steel-A,0.18,1.05,205
   S02,Steel-A,0.22,0.96,212
   S03,Steel-A,,1.10,208
   S04,Steel-B,0.34,1.42,246
   S05,Steel-B,0.39,1.55,258
   S06,Steel-B,0.36,,251
   S07,Steel-B,0.31,1.48,
   ```

2. 使用 pandas 读取数据，在终端输出总记录数，以及 `carbon_pct`、`chromium_pct`、`hardness_hv` 三列各自的缺失值数量。
3. 只保留这三个数值字段都不缺失的记录，生成 `valid_samples.csv`；文件须保留原有五列，且不得包含额外索引列。
4. 在有效记录中新增布尔列 `composition_pass`。同时满足以下范围时为合格，边界值也算合格：
   - `Steel-A`：碳含量为 0.18%–0.22%，铬含量为 0.95%–1.10%。
   - `Steel-B`：碳含量为 0.32%–0.38%，铬含量为 1.40%–1.55%。
5. 使用 pandas 按 `alloy` 分组，汇总每个牌号的有效试样数、平均硬度、成分合格数和成分合格率。统计过程不得通过手写循环逐行累加完成。
6. 将汇总结果写入 `alloy_quality_summary.csv`，表头必须为 `alloy,valid_count,average_hardness_hv,pass_count,pass_rate_pct`。平均硬度与合格率保留一位小数，输出文件不得包含额外索引列。
7. 在终端逐行输出每个牌号的汇总信息，牌号按它们在有效数据中首次出现的顺序排列。

## 示例输入输出

终端输出可为：

```text
总记录数：7
carbon_pct 缺失：1
chromium_pct 缺失：1
hardness_hv 缺失：1
Steel-A：有效试样 2 个，平均硬度 208.5 HV，成分合格率 100.0%
Steel-B：有效试样 2 个，平均硬度 252.0 HV，成分合格率 50.0%
```

生成的汇总 CSV 内容应包含：

```text
alloy,valid_count,average_hardness_hv,pass_count,pass_rate_pct
Steel-A,2,208.5,2,100.0
Steel-B,2,252.0,1,50.0
```

## 验收标准

- 程序可从项目目录以外启动，仍能正确找到输入 CSV。
- pandas 正确读取全部 7 条记录，并将空字段识别为缺失值。
- 三个数值字段的缺失值数量均统计正确。
- `valid_samples.csv` 只包含三个数值字段都完整的 4 条记录，列结构正确且无额外索引列。
- 两个牌号的成分范围判断正确，包含上下边界。
- 汇总结果中的有效试样数、平均硬度、合格数和合格率均正确。
- 统计使用 pandas 的布尔筛选与分组聚合完成。
- `alloy_quality_summary.csv` 的表头、记录顺序和一位小数格式正确，且无额外索引列。
- 输入文件只有表头、没有数据行时，程序不报错，并生成两个仅含正确表头的输出文件。
- 代码使用清晰的 `snake_case` 命名。

## 建议文件名

`alloy_data_cleaning.py`

## 可选挑战

将因缺失数据而未参与统计的记录保存为 `incomplete_samples.csv`，并新增 `missing_fields` 列，记录每个试样缺少的字段数量。
