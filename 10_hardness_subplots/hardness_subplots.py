import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def read_data(file_name):
    file_path = Path(__file__).parent / file_name
    data = pd.read_csv(file_path, encoding = "utf-8")
    return data

def data_analysis(data):
    print(f"读取测量点：{data.shape[0]}")
    grouped = data.groupby("temperature_c", sort = False)
    summary = grouped.agg(
        count = ("sample_id", "count"),
        average_hardness_hv = ("hardness_hv", np.mean),
        standard_deviation = ("hardness_hv", np.std)
    )
    max_hardness_temperature = summary["average_hardness_hv"].idxmax()
    summary = summary.reset_index()
    print(f"温度组数：{summary.shape[0]}")
    summary.apply(
        lambda data: print(f"{data["temperature_c"]:.0f} °C：试样 {int(data["count"])} 件，平均硬度 {data["average_hardness_hv"]:.1f} HV，标准差 {data["standard_deviation"]:.1f} HV"),
        axis = 1
    )
    print(f"最高平均硬度：{max_hardness_temperature} °C（{summary[summary["temperature_c"] == max_hardness_temperature]["average_hardness_hv"].values[0]:.1f} HV）")
    return summary, max_hardness_temperature

def print_plot(data, summary, max_hardness_temperature):
    figure, (bar_ax, hist_ax) = plt.subplots(
        1,
        2,
        figsize = (10, 4.5)
    )

    bar_xpositions = range(summary.shape[0])
    x_labels = [
        f"{temperature:.0f} °C"
        for temperature in summary["temperature_c"]
    ]
    bar_colors = [
        "orange"
        if temperature == max_hardness_temperature
        else "blue"
        for temperature in summary["temperature_c"]
    ]
    bars = bar_ax.bar(
        bar_xpositions,
        summary["average_hardness_hv"],
        yerr = summary["standard_deviation"],
        color = bar_colors,
        capsize = 5
    )
    bar_ax.bar_label(
        bars,
        fmt = "%.1f"
    )
    bar_ax.set_xticks(bar_xpositions, x_labels)
    bar_ax.set_title("Average Hardness by Temperature")
    bar_ax.set_xlabel("Heat Treatment Temperature")
    bar_ax.set_ylabel("Vickers Hardness (HV)")
    bar_ax.grid(
        True,
        alpha = 0.5,
        linestyle = "--"
    )

    hist_ax.hist(
        data["hardness_hv"],
        bins = [165, 175, 185, 195, 205],
        edgecolor = "black"
    )
    hist_ax.yaxis.set_major_locator(
        MaxNLocator(integer = True)
    )
    hist_ax.set_title("Hardness Distribution")
    hist_ax.set_xlabel("Vickers Hardness (HV)")
    hist_ax.set_ylabel("Sample Count")
    hist_ax.grid(
        True,
        alpha = 0.5,
        linestyle = "--"
    )

    hard_sample_inquiry(data)
    hist_ax.axvline(
        190,
        label = "190 HV threshold",
        linestyle = "--"
    )
    hist_ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.0, -0.15)
    )

    figure.tight_layout()
    figure.savefig(Path(__file__).parent / "hardness_subplots.png", dpi = 150)
    plt.show()
    print("图像已保存：hardness_subplots.png")

def hard_sample_inquiry(data):
    hard_samples = data[data["hardness_hv"] >= 190]
    print(f"高硬度试样（≥ 190 HV）：{hard_samples.shape[0]}/{data.shape[0]}（{hard_samples.shape[0] / data.shape[0] * 100:.1f}%）")

def main():
    data = read_data("hardness_measurements.csv")
    summary, max_hardness_temperature = data_analysis(data)
    print_plot(data, summary, max_hardness_temperature)

if __name__ == "__main__":
    main()
