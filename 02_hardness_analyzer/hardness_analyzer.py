if __name__ == "__main__":
    num = int(input("请输入测量次数："))
    if num <= 0:
        print("测量次数必须大于 0")
        exit()
    hardness = []
    for i in range(num):
       h = float(input("请输入第 " + str(i + 1) + " 个硬度值（HV）："))
       if(h <= 0):
           print("硬度值必须大于 0")
           exit()
       hardness.append(h)
    aver = sum(hardness) / num
    print("平均硬度：" + format(aver, ".2f") + "HV")
    minVal = min(hardness)
    maxVal = max(hardness)
    print("最大硬度：" + str(maxVal) + " HV")
    print("最小硬度：" + str(minVal) + " HV")
    print("极差：" + str(maxVal - minVal) + " HV")
    if maxVal - minVal <= 10:
        print("测试结果较稳定")
    else:
        print("测试结果波动较大")

    if maxVal == minVal:
        print("无高于平均硬度的测量值")
    else:
        print("高于平均硬度的测量值及其测量序号：")
        for i in range(num):
            if hardness[i] > aver:
                print(f"第 {i + 1} 次：{hardness[i]} HV")
    