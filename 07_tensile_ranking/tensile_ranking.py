import pandas as pd
from pathlib import Path

def read_data(file_name):
    file_path = Path(__file__).parent / file_name
    return pd.read_csv(file_path, encoding = "utf-8")

def count_incomplete(data):
    seq = ["yield_strength_mpa", "tensile_strength_mpa", "elongation_pct"]
    for key in seq:
        count = data[key].isna().sum()
        print(f"{key} 缺失：{count}")

def remove_incomplete(data):
    return data[data[["yield_strength_mpa", "tensile_strength_mpa", "elongation_pct"]].notna().all(axis = "columns")]

def yield_ratio_calc(df):
    data = df.copy()
    data["yield_ratio"] = (data["yield_strength_mpa"] / data["tensile_strength_mpa"])
    return data

def performance_check(df):
    data = df.copy()
    data["performance_pass"] = (
        ((data["alloy"] == "Al-6061") & (data["tensile_strength_mpa"] >= 305) & (data["elongation_pct"] >= 12.0) & (data["yield_ratio"] <= 0.80))
        | ((data["alloy"] == "Steel-Q") & (data["tensile_strength_mpa"] >= 645) & (data["elongation_pct"] >= 13.0) & (data["yield_ratio"] <= 0.82))
        )
    return data

def data_analysis(df):
    data = df.copy()
    grouped = data.groupby(["alloy", "batch"], as_index = False)
    summary = grouped.agg(
        valid_count = ("sample_id", "count"),
        average_tensile_strength_mpa = ("tensile_strength_mpa", "mean"),
        average_elongation_pct = ("elongation_pct", "mean"),
        pass_count = ("performance_pass", "sum"),
    )
    summary["pass_rate_pct"] = summary["pass_count"] / summary["valid_count"] * 100
    summary = summary.sort_values(by = ["pass_rate_pct", "average_tensile_strength_mpa", "batch"], ascending = [False, False, True])
    summary = summary.reset_index(drop = True)
    summary.insert(0, "rank", pd.Series(range(summary.shape[0])) + 1)
    return summary

def df_to_csv(df, file_name):
    file_path = Path(__file__).parent / file_name
    df.to_csv(file_path, encoding = "utf-8", index = False, float_format = "%.2f")

def print_summary(df):
    data = df.copy()
    if data.empty:
        return
    data.apply(
        lambda data: print(f"第 {data["rank"]} 名：{data["alloy"]} {data["batch"]}，平均抗拉强度 {data["average_tensile_strength_mpa"]:.2f} MPa，达标率 {data["pass_rate_pct"]:.2f}%"),
        axis = "columns"
    )

def failed_reason_check(df):
    data = df.copy()
    reasons = []
    if data["alloy"] == "Al-6061":
        if data["tensile_strength_mpa"] < 305:
            reasons.append("tensile_strength_mpa")
        if data["elongation_pct"] < 12.0:
            reasons.append("elongation_pct")
        if data["yield_ratio"] > 0.80:
            reasons.append("yield_ratio")
    else:
        if data["tensile_strength_mpa"] < 645:
            reasons.append("tensile_strength_mpa")
        if data["elongation_pct"] < 13.0:
            reasons.append("elongation_pct")
        if data["yield_ratio"] > 0.82:
            reasons.append("yield_ratio")
    return reasons

def failure_analysis(df):
    data = df.copy()
    failed = data[(
        ((data["alloy"] == "Al-6061") & ((data["tensile_strength_mpa"] < 305) | (data["elongation_pct"] < 12.0) | (data["yield_ratio"] > 0.80)))
        | ((data["alloy"] == "Steel-Q") & ((data["tensile_strength_mpa"] < 645) | (data["elongation_pct"] < 13.0) | (data["yield_ratio"] > 0.82)))
    )]
    failed["failure_reason"] = failed.apply(failed_reason_check, axis = "columns")
    df_to_csv(failed, "failed_samples.csv")

def main():
    data = read_data("tensile_results.csv")
    print(f"总记录数：{data.shape[0]}")
    count_incomplete(data)
    valid = remove_incomplete(data)
    info = valid.copy()
    info = yield_ratio_calc(info)
    info = performance_check(info)
    summary = data_analysis(info)
    df_to_csv(summary, "batch_ranking.csv")
    print_summary(summary)
    failure_analysis(info)

if __name__ == "__main__":
    main()
