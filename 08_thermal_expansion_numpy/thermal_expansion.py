import numpy as np

def error_check(temperatures, lengths_mm, sample_id):
    if temperatures.ndim != 1:
        raise ValueError("temperatures 不是一维数组")
    if lengths_mm.ndim != 2:
        raise ValueError("lengths_mm 不是二维数组")
    if temperatures.shape[0] != lengths_mm.shape[1]:
        raise ValueError("长度数组的列数与温度数量不一致")
    if sample_id.shape[0] != lengths_mm.shape[0]:
        raise ValueError("试样编号数量与长度数组的行数不一致")
    if temperatures.shape[0] < 2:
        raise ValueError("温度少于两个")
    if (np.diff(temperatures) <= 0).any():
        raise ValueError("温度没有严格递增")
    if (lengths_mm[:, 0] <= 0).any():
        raise ValueError("任一试样在第一个温度下的初始长度不大于 0")

def main():
    # 主任务数据
    '''
    temperatures = np.array([20, 50, 80, 110, 140])
    sample_ids = np.array(["S1", "S2", "S3", "S4"])
    lengths_mm = np.array([[50.000, 50.018, 50.036, 50.054, 50.072],
                          [49.980, 49.997, 50.015, 50.032, 50.050],
                          [50.020, 50.036, 50.053, 50.069, 50.086],
                          [50.010, 50.031, 50.051, 50.072, 50.092]])
    '''
    # 挑战任务数据
    temperatures = np.array([20, 50, 80, 110, 140])
    sample_ids = np.array(["S1", "S2", "S3", "S4", "S5"])
    lengths_mm = np.array([[50.000, 50.018, 50.036, 50.054, 50.072],
                          [49.980, 49.997, 50.015, 50.032, 50.050],
                          [50.020, 50.036, 50.053, 50.069, 50.086],
                          [50.010, 50.031, 50.051, 50.072, 50.092],
                          [50.000, 50.012, 50.025, 50.021, 50.040]])

    error_check(temperatures, lengths_mm, sample_ids)
    not_ascending_check = (np.diff(lengths_mm) <= 0).any(axis = 1)
    not_ascending_sample = sample_ids[not_ascending_check]
    if not_ascending_sample.size == 0:
        print("所有试样的长度均严格增加")
    else:
        not_ascending_text = "、".join(not_ascending_sample)
        print(f"长度未严格增加的试样：{not_ascending_text}")
    deleted_value = np.arange(0, sample_ids.shape[0])[not_ascending_check]
    sample_ids = np.delete(sample_ids, deleted_value)
    lengths_mm = np.delete(lengths_mm, deleted_value, axis = 0)

    temperatures_difference = temperatures - temperatures[0]
    print(f"温度数组形状：{temperatures.shape}")
    print(f"长度数组形状：{lengths_mm.shape}")
    print(f"S2 全部长度：{lengths_mm[1, :]}")
    print(f"80 °C 全部长度：{lengths_mm[:, 2]}")

    initial_length = lengths_mm[:, :1]
    length_difference = lengths_mm - initial_length
    expansion_rate = length_difference[:, 4] / (lengths_mm[:, 0] * temperatures_difference[4])
    for index, value in enumerate(sample_ids):
        print(f"试样 {value}：{expansion_rate[index] * 1e6:.3f} × 10⁻⁶/°C")
    print(f"平均线膨胀系数：{expansion_rate.mean() * 1e6:.3f} × 10⁻⁶/°C")
    print(f"总体标准差：{expansion_rate.std() * 1e6:.3f} × 10⁻⁶/°C")

    check = (10.500e-6 <= expansion_rate) & (expansion_rate <= 13.000e-6)
    passed_sample = sample_ids[check]
    passed_expansion_rate = expansion_rate[check]
    for index, value in enumerate(passed_sample):
        print(f"合格试样：{value}，{passed_expansion_rate[index] * 1e6:.3f} × 10⁻⁶/°C")

    average_length = lengths_mm.mean(axis = 0)
    for index, value in enumerate(temperatures):
        print(f"{value} °C 平均长度：{average_length[index]:.3f} mm")

if __name__ == "__main__":
    main()
