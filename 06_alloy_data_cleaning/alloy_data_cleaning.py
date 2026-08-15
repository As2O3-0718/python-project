import pandas as pd
from pathlib import Path

def read_data(file_name):
    file_path = Path(__file__).parent / file_name
    return pd.read_csv(file_path, encoding = "utf-8")

def count_na(data):
    missing_count = data.isna().sum()
    seq = ("carbon_pct", "chromium_pct", "hardness_hv")
    for key in seq:
        print(f"{key} 列的缺失值数量：{missing_count[key]}")

def df_to_csv(df, file_name):
    file_path = Path(__file__).parent / file_name
    df.to_csv(file_path, encoding = "utf-8", index = False)

def check_valid_data(data):
    valid_data = data[data[["carbon_pct", "chromium_pct", "hardness_hv"]].notna().all(axis = "columns")]
    df_to_csv(valid_data, "valid_samples.csv")
    valid_data["composition_pass"] = valid_data.apply(lambda row: (
        (row["alloy"] == "Steel-A" and (0.18 <= row["carbon_pct"] <= 0.22) and (0.95 <= row["chromium_pct"] <= 1.10))
        or (row["alloy"] == "Steel-B" and (0.32 <= row["carbon_pct"] <= 0.38) and (1.40 <= row["chromium_pct"] <= 1.55))
    ), axis = "columns")
    return valid_data

def data_analysis(valid_data):
    grouped = valid_data.groupby("alloy")
    alloy_list = valid_data["alloy"].unique().tolist()
    result = pd.DataFrame({"alloy": alloy_list})
    result["valid_count"] = result["alloy"].map(grouped["hardness_hv"].size())
    result["average_hardness_hv"] = result["alloy"].map(grouped["hardness_hv"].mean()).round(1)
    result["pass_count"] = result["alloy"].map(grouped["composition_pass"].sum())
    result["pass_rate_pct"] = (result["pass_count"] / result["valid_count"] * 100).round(1)
    return result

def incomplete_samples(data):
    incomplete = data[data.isna().any(axis = "columns")]
    incomplete["missing_fields"] = incomplete.apply(lambda data: data.isna().sum(), axis = "columns")
    df_to_csv(incomplete, "incomplete_samples.csv")

def print_result(result):
    if result.empty:
        return
    result.apply(lambda result: print(f"{result["alloy"]}：有效试样 {result["valid_count"]} 个，平均硬度 {result["average_hardness_hv"]:.1f} HV，成分合格率 {result["pass_rate_pct"]:.1f}%"), axis = "columns")

def main():
    data = read_data("alloy_composition.csv")
    print(f"总记录数：{data.shape[0]}")
    count_na(data)
    valid_data = check_valid_data(data)
    
    result = data_analysis(valid_data)
    df_to_csv(result, "alloy_quality_summary.csv")
    print_result(result)
    incomplete_samples(data)

if __name__ == "__main__":
    main()