# 项目 13：Arrhenius 非线性拟合与残差

## 今日目标

从扩散实验 CSV 中读取温度与扩散系数，使用 `scipy.optimize.curve_fit()`
直接拟合 Arrhenius 非线性关系，得到控制曲线总体高低的指前因子、控制温度影响
程度的活化能，并计算单位为 `m²/s` 的残差和 RMSE、绘制结果图。

预计用时：30–45 分钟。

## 知识点

- Arrhenius 模型中两个拟合参数的基本作用
- `scipy.optimize.curve_fit()` 非线性最小二乘拟合
- 模型参数的单位换算
- 区分 CSV 实验观测值与模型预测值
- 小量级数据的数值缩放
- 预测值、残差与均方根误差（RMSE）
- Matplotlib 对数纵轴和共享横轴子图

## 明确任务

1. 使用 pandas 读取项目文件夹中的 `diffusion_curve_data.csv`。无论从仓库根目录
   还是项目文件夹启动程序，都必须正确找到输入文件；不得在程序中重新手写实验数据。
2. CSV 采用“一条测量记录一行”的长表结构：

    - `sample_id`：测量记录编号；
    - `temperature_c`：实验温度，单位为 `°C`；
    - `diffusion_coefficient_m2_s`：扩散系数，单位为 `m²/s`。

3. 检查输入数据是否包含全部三个必需列，且必需列中没有缺失值。参与拟合的数据
   至少需要 3 个不同温度点；温度必须高于绝对零度，扩散系数必须大于 0。
   遇到不满足要求的数据时，应给出清楚的错误信息。
4. 在编写模型函数前，先明确 `curve_fit()` 要从全部实验数据中估计的两个参数：

    - `prefactor_scaled`：缩放后的指前因子。它是指数函数前面的乘数，主要控制
      整条拟合曲线总体有多高；
    - `activation_energy_j_mol`：活化能，主要控制扩散系数随温度变化的快慢。

   这两个量都不是 CSV 中的输入列，也不是某一个温度下的实验观测值。本项目只要求
   理解它们在模型中的作用，不要求掌握更深的物理来源或公式推导。
5. 将摄氏温度换算为 `temperature_k`。把气体常数保存为
   `gas_constant = 8.314 J/(mol·K)`；它是题目给定的固定换算常量，本项目不要求
   推导其来源。所有拟合计算保留原始精度。
6. 从 CSV 的 `diffusion_coefficient_m2_s` 列取得实验观测数组，并命名为
   `diffusion_measured_m2_s`。这里的“实验观测值”就是 CSV 中仪器记录的扩散系数；
   本项目不把它称为“实际值”或“真实值”，因为实验测量本身也可能包含误差。

   为改善极小数值带来的计算尺度问题，按以下方式得到拟合目标：

    ```text
    diffusion_measured_scaled = diffusion_measured_m2_s / 1.0e-12
    ```

   `diffusion_measured_scaled` 只是交给 `curve_fit()` 的缩放数值。其中数值 `1.0`
   代表 `1.0e-12 m²/s`，不能直接把它当成单位为 `m²/s` 的结果输出。

7. 材料科学资料通常把本题中的量简写为 `D`、`D₀`、`Q`、`R` 和 `T`。
   本项目代码使用完整变量名；传统符号只用于帮助你以后阅读公式：

    | 传统符号 | 本项目变量 | 含义 |
    | --- | --- | --- |
    | `D`（实验观测） | `diffusion_measured_m2_s` | CSV 实验观测值 |
    | `D`（缩放观测） | `diffusion_measured_scaled` | `curve_fit()` 的拟合目标 |
    | `D`（缩放预测） | `diffusion_predicted_scaled` | 模型函数的返回值 |
    | `D₀` | `prefactor_scaled` | 缩放后的指前因子 |
    | `Q` | `activation_energy_j_mol` | 控制温度影响程度的拟合参数 |
    | `R` | `gas_constant` | 题目给定的固定常数 |
    | `T` | `temperature_k` | 开尔文温度 |

   对照完成后，编写接收 `temperature_k`、`prefactor_scaled` 和
   `activation_energy_j_mol` 的 Arrhenius 模型函数。模型返回
   `diffusion_predicted_scaled`，关系如下：

    ```text
    diffusion_predicted_scaled = prefactor_scaled × exp(
        -activation_energy_j_mol / (gas_constant × temperature_k)
    )
    ```

8. 调用 `curve_fit()` 时，以 `temperature_k` 为自变量，以
   `diffusion_measured_scaled` 为拟合目标。模型函数中第一个待拟合参数是
   `prefactor_scaled`，第二个是 `activation_energy_j_mol`，因此初始值也按这个
   顺序给出。为保证结果可复现，本项目统一使用：

    ```text
    p0 = (5.0e7, 150000.0)
    bounds = (0, inf)
    maxfev = 10000
    ```

   将拟合得到的 `prefactor_scaled` 乘以 `1.0e-12`，还原为单位 `m²/s` 的
   指前因子；将
   `activation_energy_j_mol` 除以 `1000`，转换为单位 `kJ/mol` 的活化能。
9. 使用拟合参数计算每个实验温度下的缩放预测值，再先乘回 `1.0e-12`，还原为
   单位 `m²/s` 的模型预测值。然后用 CSV 实验观测值减去模型预测值，并计算 RMSE：

    ```text
    diffusion_predicted_m2_s = diffusion_predicted_scaled × 1.0e-12
    residual_m2_s = diffusion_measured_m2_s - diffusion_predicted_m2_s
    rmse_m2_s = sqrt(mean(residual_m2_s²))
    ```

   因此，本题的残差和 RMSE 都使用 `m²/s`。RMSE 越小，表示模型预测值整体上越接近
   CSV 实验观测值。

10. 按示例顺序输出数据点数、温度范围、非线性拟合活化能、指前因子和 RMSE。
    温度输出为整数，活化能保留一位小数，指前因子与 RMSE 使用三位小数的
    科学计数法。
11. 创建一张上下排列、共享横轴的 `8 × 7` 英寸图：

    - 上图使用散点显示 CSV 实验观测值，并使用按温度递增的连续曲线显示模型预测值；
    - 上图纵轴使用对数刻度；
    - 下图使用散点显示单位为 `m²/s` 的 `residual_m2_s`，并绘制水平零线；
    - 两张子图都显示透明虚线网格，标题、坐标轴、图例和数据不得重叠或被裁切。

12. 图中使用以下准确英文：

    - 上图标题：`Nonlinear Arrhenius Fit`；
    - 上图纵轴：`Diffusion Coefficient (m²/s)`；
    - 下图横轴：`Temperature (°C)`；
    - 下图纵轴：`Residual (m²/s)`；
    - 测量点图例：`Measurements`；
    - 非线性拟合曲线图例：`Nonlinear Fit`；
    - 残差点图例：`Nonlinear Residuals`。

13. 调整布局后，将图像保存到项目文件夹中的 `arrhenius_curve_fit.png`，分辨率为
    `150 dpi`。无论从哪个工作目录启动，图像都必须保存在项目文件夹中；保存后
    按示例输出成功信息，可以自行决定是否显示交互窗口。
14. 至少将“读取并检查数据”“Arrhenius 模型”“非线性拟合与残差计算”和“绘制图像”
    拆分为职责清楚的函数。分析结果通过返回值交给需要它的流程，变量和函数使用
    清晰的 `snake_case` 命名。

## 示例输入输出

本项目没有终端交互输入。示例输入文件 `diffusion_curve_data.csv` 的完整内容为：

```csv
sample_id,temperature_c,diffusion_coefficient_m2_s
D01,650,9.1560e-14
D02,700,2.2493e-13
D03,750,6.2855e-13
D04,800,1.3835e-12
D05,850,3.2145e-12
D06,900,6.0200e-12
D07,950,1.2248e-11
D08,1000,2.1630e-11
```

主任务的完整终端输出为：

```text
读取扩散数据点：8
温度范围：650–1000 °C
非线性拟合活化能：153.7 kJ/mol
非线性拟合指前因子：4.391e-05 m²/s
非线性拟合 RMSE：1.424e-13 m²/s
图像已保存：arrhenius_curve_fit.png
```

生成的 `arrhenius_curve_fit.png` 应完整包含：

- 一张 `1200 × 1050` 像素的 PNG 图像；
- 上图中的 8 个实验观测散点和一条覆盖测量温度范围的模型预测曲线；
- 上图的对数纵轴、完整英文标题、坐标轴名称和两项图例；
- 下图中的 8 个非线性拟合残差点、水平零线、完整坐标轴名称和残差图例；
- 两张子图中完整可辨认且不遮挡数据的虚线网格。

## 验收标准

- 使用 pandas 从长表 `diffusion_curve_data.csv` 读取全部 8 条记录，程序中没有复制
  CSV 实验观测值。
- 程序能从仓库根目录和项目目录启动，并正确找到输入 CSV、将输出 PNG 保存到
  项目文件夹。
- 对缺少必需列、必需单元格缺失、少于 3 个不同温度点、温度不高于绝对零度或
  扩散系数不大于 0 的数据能够给出清楚错误信息。
- 正确完成开尔文温度换算和 `1.0e-12` 数值缩放；以
  `diffusion_measured_scaled` 作为拟合目标，计算过程中没有提前舍入。
- 使用规定的初始值、边界和最大函数调用次数完成 `curve_fit()` 非线性拟合。
- 将 `diffusion_predicted_scaled` 乘回 `1.0e-12` 后再计算 `residual_m2_s` 和
  `rmse_m2_s`。
- 正确得到活化能 `153.7 kJ/mol`、指前因子 `4.391e-05 m²/s` 和 RMSE
  `1.424e-13 m²/s`。
- 终端输出的文字、顺序、数值和格式与示例一致。
- 图中测量点、非线性拟合曲线、残差、零线、英文文字、图例和网格完整可读，
  布局没有明显重叠或裁切。
- PNG 保存在项目文件夹中，尺寸为 `1200 × 1050` 像素，且不是空白图像。
- 数据检查、模型、拟合分析和绘图职责合理拆分，命名清楚。

## 建议文件名

`arrhenius_curve_fit.py`

## 可选挑战

继续使用主任务从同一份 `diffusion_curve_data.csv` 读取的数据，不得复制或修改
CSV 实验观测值。

1. 复用项目 12 的方法，以 `1000 / temperature_k` 为横坐标、
   `ln(diffusion_coefficient_m2_s)` 为纵坐标，使用 `scipy.stats.linregress()`
   完成线性化拟合。
2. 根据线性化回归的斜率和截距计算活化能与指前因子。线性化活化能的数值单位为
   `kJ/mol`，再还原到原始 Arrhenius 方程时应转换为 `J/mol`。
3. 使用线性化拟合参数计算每个实验温度下单位为 `m²/s` 的预测值，再按主任务相同
   的定义计算残差和 RMSE。
4. 在非线性拟合结果之后输出线性化拟合结果、两种活化能的绝对差值，以及 RMSE
   更小的方法。活化能及差值保留一位小数，指前因子与 RMSE 使用三位小数的
   科学计数法。
5. 在上图增加线性化拟合曲线，使用图例 `Linearized Fit`；在下图增加线性化拟合
   残差点，使用图例 `Linearized Residuals`。主任务要求的全部图形内容必须保留。

挑战的独立示例仍以以下完整 CSV 为输入：

```csv
sample_id,temperature_c,diffusion_coefficient_m2_s
D01,650,9.1560e-14
D02,700,2.2493e-13
D03,750,6.2855e-13
D04,800,1.3835e-12
D05,850,3.2145e-12
D06,900,6.0200e-12
D07,950,1.2248e-11
D08,1000,2.1630e-11
```

完成挑战后的完整终端输出为：

```text
读取扩散数据点：8
温度范围：650–1000 °C
非线性拟合活化能：153.7 kJ/mol
非线性拟合指前因子：4.391e-05 m²/s
非线性拟合 RMSE：1.424e-13 m²/s
线性化拟合活化能：154.1 kJ/mol
线性化拟合指前因子：4.541e-05 m²/s
线性化拟合 RMSE：1.520e-13 m²/s
活化能差值：0.4 kJ/mol
RMSE 更小的方法：非线性拟合
图像已保存：arrhenius_curve_fit.png
```

挑战图像必须完整保留主任务的尺寸、标题、坐标轴、网格、测量点、非线性拟合曲线、
非线性残差和零线，并额外包含线性化拟合曲线、线性化残差点及对应图例；PNG 尺寸
仍为 `1200 × 1050` 像素。
