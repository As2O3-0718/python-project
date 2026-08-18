import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def read_data(file_name):
    file_path = Path(__file__).parent / file_name
    return pd.read_csv(file_path, encoding = "utf-8")

def find_max(data):
    annealed_max_index = np.argmax(data[:, 1], axis = 0)
    quenched_max_index = np.argmax(data[:, 2], axis = 0)
    print(f"退火态峰值：{data[annealed_max_index][1]:.0f} MPa，工程应变 {data[annealed_max_index][0]}%")
    print(f"调质态峰值：{data[quenched_max_index][2]:.0f} MPa，工程应变 {data[quenched_max_index][0]}%")
    return annealed_max_index, quenched_max_index

def print_graph(data, annealed_max_index, quenched_max_index):
    fig, axes = plt.subplots(figsize = (8, 5))
    axes.set_title("Engineering Stress-Strain Curves")
    axes.set_xlabel("Engineering Strain (%)")
    axes.set_ylabel("Engineering Stress (MPa)")
    axes.plot(data[:, 0], data[:, 1], linestyle = '-', marker = 'o', label = "Annealed", color = "blue")
    axes.plot(data[:, 0], data[:, 2], linestyle = "--", marker = 's', label = "Quenched & Tempered", color = "orange")
    axes.scatter(data[annealed_max_index][0], data[annealed_max_index][1], color = "blue", s = 80, marker = 'o')
    axes.scatter(data[quenched_max_index][0], data[quenched_max_index][2], color = "orange", s = 80, marker = 's')
    axes.annotate(f"Peak: {data[annealed_max_index][1]:.0f} MPa", xy = (data[annealed_max_index][0], data[annealed_max_index][1]), xytext = (5, 15), textcoords = "offset points", arrowprops={"arrowstyle": "->"})
    axes.annotate(f"Peak: {data[quenched_max_index][2]:.0f} MPa", xy = (data[quenched_max_index][0], data[quenched_max_index][2]), xytext = (5, -15), textcoords = "offset points", arrowprops={"arrowstyle": "->"})
    axes.grid(True, linestyle = "--", alpha = 0.5)

    annealed_98 = data[data[:, 1] >= 0.98 * data[annealed_max_index][1]]
    qt_98 = data[data[:, 2] >= 0.98 * data[quenched_max_index][2]]
    annealed_interval = (np.amin(annealed_98[:, 0]), np.amax(annealed_98[:, 0]))
    qt_interval = (np.amin(qt_98[:, 0]), np.amax(qt_98[:, 0]))
    axes.axvspan(*annealed_interval, alpha = 0.2, color = "blue", label = "Annealed ≥ 98% peak")
    axes.axvspan(*qt_interval, alpha = 0.2, color = "orange", label = "Q&T ≥ 98% peak")
    print(f"退火态 98% 峰值区间：{annealed_interval[0]:.1f}%–{annealed_interval[1]:.1f}%")
    print(f"调质态 98% 峰值区间：{qt_interval[0]:.1f}%–{qt_interval[1]:.1f}%")

    axes.legend()
    fig.savefig(Path(__file__).parent / "stress_strain_curve.png", dpi = 150)
    print("图像已保存：stress_strain_curve.png")
    plt.show()

def main():
    data = read_data("stress_strain.csv").to_numpy()
    count = data.shape[0]
    print(f"读取测量点：{count}")

    annealed_max_index, quenched_max_index = find_max(data)
    print_graph(data, annealed_max_index, quenched_max_index)


if __name__ == "__main__":
    main()
