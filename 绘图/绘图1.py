import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件
file_path = "D:/a股是我们的/我们的模型/实验结果/各结果均值/绘图1.xlsxdata/绘图1.xlsx"
data = pd.read_excel(file_path, header=None)

# 提取横坐标和数据
x = list(range(20))  # 横坐标 0-19
lines = data.iloc[:, 0]  # 第一列是行名称
values = data.iloc[:, 1:]  # 后面的列是数据

# 绘制折线图
plt.figure(figsize=(10, 6))
for i, line_name in enumerate(lines):
    plt.plot(x, values.iloc[i], label=line_name)

plt.title("折线图")
plt.xlabel("横坐标")
plt.ylabel("值")
plt.legend()
plt.grid(True)
plt.show()
