import pandas as pd
from pathlib import Path
from numpy.polynomial import Polynomial as P
import matplotlib.pyplot as plt
import numpy as np

def read_csv(file_name):
    file_path = Path(__file__).parent / file_name
    data = pd.read_csv(file_path, encoding = "utf-8")
    return data

def linear_fitting(x, y):
    if len(np.unique(x)) < 2:
        raise ValueError("弹性区内数据点过少")
    scaled_result = P.fit(x, y, deg = 1)
    result = scaled_result.convert()
    b, k = result.coef
    return k, b, scaled_result(x), y - scaled_result(x)

def find_max_deviation_abs(deviation):
    max_index = np.argmax(np.abs(deviation))
    return max_index

def print_plot(data, k, b, deviation, max_index):
    x = data["strain"].to_numpy()
    y = data["stress_mpa"].to_numpy()
    x1 = data[(0.0000 <= data["strain"]) & (data["strain"] <= 0.0025)]["strain"].to_numpy()
    y1 = data[(0.0000 <= data["strain"]) & (data["strain"] <= 0.0025)]["stress_mpa"].to_numpy()

    fig, (curve_ax, deviation_ax) = plt.subplots(
        2,
        1,
        figsize = (10, 7)
    )

    curve_ax.plot(
        x,
        y,
        label = "Full Stress-Strain Curve"
    )
    curve_ax.scatter(
        x1,
        y1,
        marker = 'o',
        color = "orange",
        label="Elastic Fit Points"
    )
    x0 = np.array([0.0000, 0.0025])
    y0 = k * x0 + b
    curve_ax.plot(
        x0,
        y0,
        color = "orange",
        label="Linear Fit"
    )
    curve_ax.grid(
        linestyle = "--",
        alpha = 0.5
    )
    curve_ax.set_title("Stress-Strain Curve and Elastic Fit")
    curve_ax.set_xlabel("Engineering Strain")
    curve_ax.set_ylabel("Engineering Stress (MPa)")
    curve_ax.legend(loc = "best")

    dot_colors = [
        "orange"
        if i == max_index
        else "blue"
        for i in range(len(x1))
    ]
    deviation_ax.scatter(
        x1,
        deviation,
        color = dot_colors
    )
    deviation_ax.axhline(
        0,
        label = "0 MPa",
        linestyle = "--"
    )
    deviation_ax.annotate(
        f"max |residual| = {np.abs(deviation[max_index]):.1f} MPa",
        xy = (x1[max_index], deviation[max_index]),
        xytext = (10, 0),
        textcoords = "offset points"
    )

    deviation_ax.set_title("Elastic Fit Residuals")
    deviation_ax.set_xlabel("Engineering Strain")
    deviation_ax.set_ylabel("Residual (MPa)")
    deviation_ax.grid(
        linestyle = "--",
        alpha = 0.5
    )
    deviation_ax.legend(loc = "best")


    fig.tight_layout()
    fig.savefig(Path(__file__).parent / "elastic_modulus_fit.png", dpi = 150)
    print("图像已保存：elastic_modulus_fit.png")
    plt.show()


def main():
    data = read_csv("tensile_elastic_data.csv")
    elastic_interval_data = data[(0.0000 <= data["strain"]) & (data["strain"] <= 0.0025)]
    x = elastic_interval_data["strain"].to_numpy()
    y = elastic_interval_data["stress_mpa"].to_numpy()
    k, b, yhat, deviation = linear_fitting(x, y)
    r2 = 1 - np.pow(y - yhat, 2).sum() / np.pow(y - y.mean(), 2).sum()

    print(f"读取测量点：{len(data)}")
    print(f"拟合区间：0.0000–0.0025")
    print(f"拟合点数：{len(elastic_interval_data)}")
    print(f"弹性模量：{k / 1000:.2f} GPa")
    print(f"截距：{b:.2f} MPa")
    print(f"拟合优度 R²：{r2:.4f}")

    max_index = find_max_deviation_abs(deviation)
    print(f"最大绝对残差：{np.abs(deviation[max_index]):.1f} MPa（应变 {x[max_index]:.4f}）")
    print_plot(data, k, b, deviation, max_index)

if __name__ == "__main__":
    main()
