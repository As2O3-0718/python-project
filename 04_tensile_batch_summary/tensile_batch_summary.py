def summarize_batch(records, batch_name):
    batch_records = []
    for record in records:
        if record["batch"] == batch_name:
            batch_records.append(record)
    count = 0
    average_strength = 0
    greatest_strength = 0
    average_rate = 0
    count = len(batch_records)
    if count == 0:
        return 0, 0, 0, 0
    for record in batch_records:
        average_strength += record["strength"]
        average_rate += record["rate"]
        greatest_strength = max(greatest_strength, record["strength"])
    average_strength /= count
    average_rate /= count
    return count, average_strength, greatest_strength, average_rate

def print_summary(batch_name, count, average_strength, greatest_strength, average_rate):
    if count == 0:
        print("没有找到该批次的实验记录")
        return
    print(f"批次 {batch_name}")
    print(f"试样数量：{count}")
    print(f"平均抗拉强度：{average_strength:.1f} MPa")
    print(f"最高抗拉强度：{greatest_strength:.1f} MPa")
    print(f"平均断后伸长率：{average_rate:.1f} %")

def check_low_records(records):
    flag = False
    for record in records:
        if record["strength"] < 465:
            flag = True
            print(f"强度偏低试样：{record["code"]}（批次 {record["batch"]}，{record["strength"]:.1f} MPa）")
    if not flag:
        print("没有强度偏低的试样")

def inquire_batch(batch_name, records):
    print_summary(batch_name.upper(), *summarize_batch(records, batch_name.upper()))

def main():
    seq = ("code", "batch", "strength", "rate")
    test_records = []
    test_records.append(dict(zip(seq, ("S01", 'A', 468, 18.5))))
    test_records.append(dict(zip(seq, ("S02", 'A', 475, 17.8))))
    test_records.append(dict(zip(seq, ("S03", 'A', 459, 19.2))))
    test_records.append(dict(zip(seq, ("S04", 'B', 482, 16.9))))
    test_records.append(dict(zip(seq, ("S05", 'B', 477, 17.4))))

    inquire_batch('A', test_records)
    print()
    inquire_batch('B', test_records)
    print()
    while True:
        batch_name = str(input("请输入需要查询的实验批次（输入STOP以终止查询）"))
        if batch_name == "STOP":
            break
        inquire_batch(batch_name, test_records)
    check_low_records(test_records)

if __name__ == "__main__":
    main()