import pandas as pd
import os

def calculate_mse_and_mape(actual: list[float], predicted: list[float]) -> tuple[float, float]:
    n = len(actual)
    mse = sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n
    mape = sum(abs((a - p) / a) for a, p in zip(actual, predicted) if a != 0) / n * 100
    return mse, mape


folder_path = 'D:/a股是我们的/实验结果/3B'
file_names = os.listdir(folder_path)

# 用于存储每个文件读取的数据
data_frames = []
for file in file_names:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    data_frames.append(df)

# 计算每列
result = pd.DataFrame()
for col in range(8):
    col_data = [df.iloc[:, col+1].values for df in data_frames]
    mean_values = [sum(x) / len(x) for x in zip(*col_data)]
    result[f'col_{col + 1}'] = mean_values
df = pd.read_csv("D:/a股是我们的/实验结果/3B/3b预测结果表格_均值.csv")
result.insert(0,"真实",df["真实"])
# 将结果输出到新的csv文件
result.to_csv('D:/a股是我们的/实验结果/3B结果预测表格/avg.csv', index=False)


df = pd.read_csv("D:/a股是我们的/实验结果/3B结果预测表格/avg.csv")
print("原始数据集的前几行:")
print(df.head())
mse_list =[]
mape_list =[]
for i in range(len(df["真实"])):
    actual = df.iloc[i:i+8,0].to_list()
    predicted_values = df.iloc[i,1:9].to_list()
    mse, mape = calculate_mse_and_mape(actual, predicted_values)
    mse_list.append(mse)
    mape_list.append(mape)

# 将 MSE 和 MAPE 添加到新的列
df['MSE'] = pd.Series(mse_list)
df['MAPE'] = pd.Series(mape_list)
df.iloc[:,1:9]=df.iloc[:,1:9].round(7)
df.iloc[:,9:11]=df.iloc[:,9:11].round(13)
for i in range(8):
    df = df.rename(columns={df.columns[i+1]: f'预测{i+1}'})
df.to_csv(f"D:/a股是我们的/实验结果/3B结果预测表格/3b预测结果表格_mse&mape.csv", index=False)