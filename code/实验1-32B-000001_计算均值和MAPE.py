import pandas as pd
import os
def calculate_mse_and_mape(actual: list[float], predicted: list[float]) -> tuple[float, float]:
    n = len(actual)
    mse = sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n
    mape = sum(abs((a - p) / a) for a, p in zip(actual, predicted) if a != 0) / n * 100
    return mse, mape

def get_all_files_absolute_path(directory_path):
    """
    获取文件夹下所有文件的绝对路径
    :param directory_path: 文件夹路径
    :return: 文件绝对路径列表
    """
    try:
        # 获取文件夹中的所有文件和子目录
        all_items = os.listdir(directory_path)
        
        # 仅保留文件的绝对路径
        file_paths = [
            os.path.abspath(os.path.join(directory_path, item))
            for item in all_items
            if os.path.isfile(os.path.join(directory_path, item))
        ]
        
        return file_paths
    except FileNotFoundError:
        print(f"错误：文件夹 '{directory_path}' 不存在。")
        return []
    except Exception as e:
        print(f"发生错误：{e}")
        return []
    

# 读取CSV文件
df = pd.read_csv("D:/a股是我们的/实验结果/实验1-32B-000001/实验1-32B-000001/预测结果表格_0.csv")
print("原始数据集的前几行:")
print(df.head())
df['预测均值'] = df.iloc[:, 1:9].mean(axis=1)
actual = df.iloc[:, 0]
predicted_values = df.iloc[:, 1:9]

# 计算每行的 MSE
mse = ((predicted_values - actual.values.reshape(-1, 1)) ** 2).mean(axis=1)

# 计算每行的 MAPE
mape = (abs(predicted_values - actual.values.reshape(-1, 1)) / actual.values.reshape(-1, 1)).mean(axis=1) 

# 将 MSE 和 MAPE 添加到新的列
"""df['MSE'] = mse
df['MAPE'] = mape
df.to_csv(f"D:/a股是我们的/实验结果/实验1-32B-000001/实验1-32B-000001/预测结果表格_0_temp.csv", index=False)"""
files = get_all_files_absolute_path("D:/a股是我们的/实验结果/实验1-32B-000001/实验1-32B-000001/")
for file in files:
    df = pd.read_csv(file)
    df['预测均值'] = df.iloc[:, 1:9].mean(axis=1)
    actual = df.iloc[:, 0]
    predicted_values = df.iloc[:, 1:9]

    # 计算每行的 MSE
    mse = ((predicted_values - actual.values.reshape(-1, 1)) ** 2).mean(axis=1)

    # 计算每行的 MAPE
    mape = (abs(predicted_values - actual.values.reshape(-1, 1)) / actual.values.reshape(-1, 1)).mean(axis=1) 

    # 将 MSE 和 MAPE 添加到新的列
    df['MSE'] = mse
    df['MAPE'] = mape
    # 获取文件名和扩展名
    file_name = os.path.basename(file)
    file_base_name, file_extension = os.path.splitext(file_name)
     # 构建输出文件路径
    file_path = os.path.join("D:/a股是我们的/实验结果/实验1-32B-000001/实验1-32B-000001_1/", f"{file_base_name}{file_extension}")
    
   
    if "date" in df.columns:
       date= df.pop("date")
       df['date'] = date
    means= df.pop("预测均值")
    df.insert(9,"预测均值",means)
    df.to_csv(file_path, index=False)
    




