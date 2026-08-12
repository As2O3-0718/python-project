from pathlib import Path

def read_temperatures(filename):
    temperatureList = []
    directory = Path(__file__).parent
    with open(directory / filename, 'r', encoding = "utf-8") as file:
        for line in file:
            numStr = line.strip()
            if numStr != "":
                temperatureList.append(float(numStr))
    return temperatureList
    
def analyze_temperatures(temperatures):
    arr = [sum(temperatures) / len(temperatures), max(temperatures), min(temperatures)]
    overheatData = []
    count = 0
    for index, data in enumerate(temperatures):
        if data > 850:
            count += 1
            overheatData.append((index, data))
    arr.append(count)
    return arr, overheatData

def main():
    print(__file__)
    temperatures = read_temperatures("temperatures.txt")
    if not temperatures:
        print("无可用的温度数据")
        return
    result, overheatData = analyze_temperatures(temperatures)
    print(f"温度记录数：{len(temperatures)}")
    print(f"平均温度：{result[0]:.1f} °C")
    print(f"最高温度：{result[1]:.1f} °C")
    print(f"最低温度：{result[2]:.1f} °C")
    overheatCount = result[3]
    print(f"超温次数：{overheatCount}")
    if overheatCount == 0:
        print("本次热处理温度全部合格")
    else:
        print("请检查超温记录：")
        for i in overheatData:
            print(f"第 {i[0] + 1} 条：{i[1]:.1f} °C")

if __name__ == "__main__":
    main()