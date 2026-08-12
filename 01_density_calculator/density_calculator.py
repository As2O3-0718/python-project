def calc(mass, volume):
    return mass / volume

class Constant:
    ALUMINIUM = 2.70
    IRON = 7.87
    COPPER = 8.96

if __name__ == "__main__":
    mass = float(input("请输入质量（g）："))
    volume = float(input("请输入体积（cm³）："))
    if (mass <= 0) or (volume <= 0):
        print("输入数据必须大于 0")
        exit()
    density = calc(mass, volume)
    print("试样密度：" + format(density, ".2f") + " g/cm³")
    dif = [abs(density - Constant.ALUMINIUM), abs(density - Constant.IRON), abs(density - Constant.COPPER)]
    if dif[0] < min(dif[1], dif[2]):
        print("该材料密度最接近铝")
    elif dif[1] < min(dif[0], dif[2]):
        print("该材料密度最接近铁")
    else:
        print("该材料密度最接近铜")
    exit()
    