import pandas as pd
from pathlib import Path
import numpy as np
from scipy.stats import linregress, t
import matplotlib.pyplot as plt

def read_data(file_name):
    file_path = Path(__file__).parent / file_name
    data = pd.read_csv(file_path, encoding = "utf-8")
    return data

def validity_check(data):
    key_list = {"sample_id", "temperature_c", "diffusion_coefficient_m2_s"}
    missing_key = key_list - set(data.columns)
    if missing_key:
        missing_key_text = ",".join(list(missing_key))
        raise ValueError(f"缺少必需列：{missing_key_text}")
    if not data[data.isna().any(axis = 1)].empty:
        raise ValueError("存在无效数据")
    if not data[data["temperature_c"] <= -273.15].empty:
        raise ValueError("温度必须高于绝对零度")
    if not data[data["diffusion_coefficient_m2_s"] <= 0].empty:
        raise ValueError("扩散系数必须大于零")
    if len(data["temperature_c"].unique()) < 3:
        raise ValueError("数据需要至少包含 3 个不同温度点")

def linear_regression(x, y):
    result = linregress(x, y)
    return result

def data_analysis(data):
    temperature_c = data["temperature_c"].to_numpy()
    temperature_k = temperature_c + 273.15
    x = 1000 / temperature_k
    y = np.log(data["diffusion_coefficient_m2_s"].to_numpy())
    result = linear_regression(x, y)

    slope = result.slope
    intercept = result.intercept
    r2 = np.pow(result.rvalue, 2)
    stderr = result.stderr

    R = 8.314
    Q = -slope * R
    D0 = np.exp(intercept)
    D = D0 * np.exp(-Q / (R * temperature_k))

    lower_Q, upper_Q = interval_95(len(data), Q, stderr)
    print_result(len(data),temperature_c, slope, intercept, Q, lower_Q, upper_Q, D0, r2)
    return x, y, slope, intercept

def print_result(n, temperature_c, slope, intercept, Q, lower_Q, upper_Q, D0, r2):
    print(f"读取扩散数据点：{n}")
    print(f"温度范围：{temperature_c.min():.0f}–{temperature_c.max():.0f} °C")
    print(f"回归斜率：{slope:.4f}")
    print(f"回归截距：{intercept:.4f}")
    print(f"活化能：{Q:.1f} kJ/mol")
    print(f"活化能 95% 置信区间：{lower_Q:.1f}–{upper_Q:.1f} kJ/mol")
    print(f"指前因子 D₀：{D0:.3e} m²/s")
    print(f"拟合优度 R²：{r2:.4f}")

def interval_95(n, Q, stderr):
    degree_of_freedom = n - 2
    t_critical = t.ppf(0.975, degree_of_freedom)
    return Q - t_critical * stderr * 8.314, Q + t_critical * stderr * 8.314

def print_plot(x, y, slope, intercept):
    fig, ax = plt.subplots(
        1,
        1,
        figsize = (8, 6)
    )

    ax.scatter(
        x,
        y,
        color = "blue",
        label = "Measurements",
        marker = 'o'
    )

    x_1000 = 1000 / (1000 + 273.15)
    x_curve = np.linspace(
        min(x.min(), x_1000),
        max(x.max(), x_1000),
        200
    )
    y_curve = slope * x_curve + intercept
    ax.plot(
        x_curve,
        y_curve,
        color = "orange",
        label = "SciPy Linear Fit",
    )

    y_1000 = slope * x_1000 + intercept
    print(f"预测 1000 °C 扩散系数：{np.exp(y_1000):.3e} m²/s")
    ax.scatter(
        x_1000,
        y_1000,
        color = "red",
        label = "1000 °C Prediction"
    )

    ax.set_title("Arrhenius Plot for Carbon Diffusion")
    ax.set_xlabel("1000 / Temperature (1/K)")
    ax.set_ylabel("ln(Diffusion Coefficient)")
    ax.grid(
        True,
        alpha = 0.5,
        linestyle = "--"
    )

    ax.legend(loc = "best")
    fig.tight_layout()
    fig.savefig(Path(__file__).parent / "arrhenius_fit.png", dpi = 150)
    print("图像已保存：arrhenius_fit.png")
    plt.show()

def main():
    data = read_data("diffusion_data.csv")
    validity_check(data)
    x, y, slope, intercept = data_analysis(data)
    print_plot(x, y, slope, intercept)

if __name__ == "__main__":
    main()
