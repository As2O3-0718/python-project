import pandas as pd
from pathlib import Path
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt
from math import inf

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

def func(x, prefactor_scaled, activation_energy_j_mol):
    gas_constant = 8.314
    return prefactor_scaled * np.exp(-activation_energy_j_mol / (gas_constant * x))

def data_curve_fit(x, y):
    return curve_fit(
        func,
        xdata = x,
        ydata = y,
        p0 = (5.0e7, 150000.0),
        bounds = (0, inf),
        maxfev = 10000
    )

def curve_RMSE_calc(prefactor_scaled, activation_energy_j_mol, x, y):
    residual = y * 1e-12 - func(x, prefactor_scaled, activation_energy_j_mol) * 1e-12
    return residual, np.sqrt(np.pow(residual, 2).mean())

def linear_RMSE_calc(slope, intercept, x, y):
    residual = np.exp(y) - np.exp(slope * x + intercept)
    return residual, np.sqrt(np.pow(residual, 2).mean())

def print_result(result):
    if result["type"] == "non-linear":
        prefix = "非线性拟合"
    elif result["type"] == "linear":
        prefix = "线性化拟合"

    print(
        prefix + f"活化能：{result["activation_energy"]:.1f} kJ/mol",
        prefix + f"指前因子：{result["prefactor"]:.3e} m²/s",
        prefix + f" RMSE：{result["RMSE"]:.3e} m²/s",
        sep = '\n'
    )

def non_linear_process(data):
    diffusion_scaled = data["diffusion_coefficient_m2_s"].to_numpy() / 1.0e-12
    temperature_k = data["temperature_c"].to_numpy() + 273.15
    [prefactor_scaled, activation_energy_j_mol], _ = data_curve_fit(temperature_k, diffusion_scaled)

    prefactor = prefactor_scaled * 1e-12
    activation_energy_kj_mol = activation_energy_j_mol / 1e3
    residual, RMSE = curve_RMSE_calc(prefactor_scaled, activation_energy_j_mol, temperature_k, diffusion_scaled)
    return {
        "type": "non-linear",
        "activation_energy": activation_energy_kj_mol,
        "prefactor": prefactor,
        "RMSE": RMSE,
        "x": data["temperature_c"].to_numpy(),
        "y": diffusion_scaled * 1e-12,
        "residual": residual
    }

def linear_process(data):
    temperature_k = data["temperature_c"].to_numpy() + 273.15
    x = 1000 / temperature_k
    y = np.log(data["diffusion_coefficient_m2_s"].to_numpy())
    result = linregress(x, y)

    slope = result.slope
    intercept = result.intercept
    gas_constant = 8.314

    activation_energy = -slope * gas_constant
    prefactor = np.exp(intercept)
    residual, RMSE = linear_RMSE_calc(slope, intercept, x, y)

    return {
        "type": "linear",
        "activation_energy": activation_energy,
        "prefactor": prefactor,
        "RMSE": RMSE,
        "residual": residual,
        "x": data["temperature_c"].to_numpy(),
        "y": np.exp(y),
        "slope": slope,
        "intercept": intercept
    }

def print_plot(non_linear_result, linear_result):
    fig, (fit_ax, res_ax) = plt.subplots(
        2,
        1,
        figsize = (8, 7),
        sharex = True
    )

    fit_ax.scatter(
        non_linear_result["x"],
        non_linear_result["y"],
        label = "Measurements"
    )

    x_curve = np.linspace(
        non_linear_result["x"].min(),
        non_linear_result["x"].max(),
        200
    )
    y_curve = non_linear_result["prefactor"] * np.exp(-non_linear_result["activation_energy"] * 1000 / (8.314 * (x_curve + 273.15)))
    fit_ax.plot(
        x_curve,
        y_curve,
        label = "Nonlinear Fit",
        linestyle = "-"
    )

    y_line = np.exp(linear_result["slope"] * (1000 / (x_curve + 273.15)) + linear_result["intercept"])
    fit_ax.plot(
        x_curve,
        y_line,
        label = "Linearized Fit",
        linestyle = "--"
    )
    fit_ax.grid(
        True,
        alpha = 0.5,
        linestyle = "--"
    )

    fit_ax.set_yscale("log")
    fit_ax.set_title("Nonlinear Arrhenius Fit")
    fit_ax.set_ylabel("Diffusion Coefficient (m²/s)")
    fit_ax.legend(loc = "best")

    res_ax.scatter(
        non_linear_result["x"],
        non_linear_result["residual"],
        label = "Nonlinear Residuals",
        color = "blue",
        marker = 'o'
    )
    res_ax.scatter(
        linear_result["x"],
        linear_result["residual"],
        label = "Linearized Residuals",
        color = "orange",
        marker = 's'
    )
    res_ax.axhline(
        0,
        linestyle = "--"
    )
    res_ax.grid(
        True,
        alpha = 0.5,
        linestyle = "--"
    )
    res_ax.set_xlabel("Temperature (°C)")
    res_ax.set_ylabel("Residual (m²/s)")
    res_ax.legend(loc = "best")

    fig.tight_layout()
    fig.savefig(Path(__file__).parent / "arrhenius_curve_fit.png", dpi = 150)
    print("图像已保存：arrhenius_curve_fit.png")
    plt.show()

def main():
    data = read_data("diffusion_curve_data.csv")
    validity_check(data)
    print(
        f"读取扩散数据点：{len(data)}",
        f"温度范围：{data["temperature_c"].min():.0f}–{data["temperature_c"].max():.0f} °C",
        sep = '\n'
    )

    non_linear_result = non_linear_process(data)
    print_result(non_linear_result)

    linear_result = linear_process(data)
    print_result(linear_result)

    print(f"活化能差值：{np.abs(non_linear_result["activation_energy"] - linear_result["activation_energy"]):.1f} kJ/mol")
    if non_linear_result["RMSE"] < linear_result["RMSE"]:
        print("RMSE 更小的方法：非线性拟合")
    elif non_linear_result["RMSE"] > linear_result["RMSE"]:
        print("RMSE 更小的方法：线性化拟合")
    else:
        print("非线性拟合与线性化拟合方法的 RMSE 一致")

    print_plot(non_linear_result, linear_result)

if __name__ == "__main__":
    main()
