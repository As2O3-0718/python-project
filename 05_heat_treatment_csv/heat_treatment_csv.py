from pathlib import Path
import pandas as pd
def data_read(file_name):
    file_path = Path(__file__).parent / file_name
    return pd.read_csv(file_path)

def data_analysis(data):
    keys = data.columns
    row_count, column_count = data.shape
    print(f"行数：{row_count}, 列数：{column_count}")
    print("列名：", end = '')
    for key in keys:
        print(f"{key}, ", end = '')
    for key in keys:
        print(f"{key} 的数据类型：{data[key].dtypes}")

    grouped_data = data.groupby("process")
    process_list = data["process"].unique().tolist()
    return process_analysis(grouped_data, process_list)
    
def process_analysis(grouped, process_list):
    result = {}
    count_list = grouped["hardness_hv"].count()
    average_list = grouped["hardness_hv"].mean()
    max_list = grouped["hardness_hv"].max()
    for process in process_list:
        result[process] = dict(
            sample_count = count_list[process],
            average_hardness_hv = average_list[process],
            max_hardness_hv = max_list[process]
        )
    return result

def print_result(result):
    result_list = result.items()
    for key, values in result_list:
        print(f"{key}: {values["sample_count"]} 个试样，平均硬度 {values["average_hardness_hv"]:.1f} HV，最高硬度 {values["max_hardness_hv"]:.1f} HV")

def result_to_csv(result):
    df = pd.DataFrame.from_dict(result, orient = "index")
    df.index.name = "process"
    df = df.reset_index()
    df = df.reindex(columns = ["process", "sample_count", "average_hardness_hv", "max_hardness_hv"])
    df = df.astype(dict(
        sample_count = int,
        average_hardness_hv = float,
        max_hardness_hv = float
    ))
    output_path = Path(__file__).parent / "heat_treatment_summary.csv"
    df.to_csv(output_path, encoding = "utf-8", index = False, float_format = "%.1f")

def low_hardness_csv(result):
    low_data = result[result["hardness_hv"] < 180]
    output_path = Path(__file__).parent / "low_hardness_samples.csv"
    low_data.to_csv(output_path, encoding = "utf-8", index = False, float_format = "%.1f")

def main():
    data = data_read("heat_treatment_data.csv")
    result = data_analysis(data)
    print_result(result)
    result_to_csv(result)
    low_hardness_csv(data)
    
if __name__ == "__main__":
    main()