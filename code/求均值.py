import pandas as pd
import os

# 文件夹路径
folder_path = 'D:/a股是我们的/我们的模型/实验结果/各结果均值'

# 获取文件夹中所有CSV文件的路径
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# 创建一个空列表来存储结果
results = []

# 遍历每个CSV文件
for file in csv_files:
    # 读取CSV文件
    data = pd.read_csv(file)
    
    # 计算MAPE列的均值
    MAPE_mean = data['MAPE'].mean()/100
    
    # 将文件名和均值添加到结果列表中
    results.append({'文件名': os.path.basename(file), 'MAPE列的均值': MAPE_mean})

# 将结果列表转换为DataFrame
result_df = pd.DataFrame(results)

# 将结果保存为CSV文件
result_csv_path = '我们的模型/实验结果/各结果均值/各结果均值.csv'
result_df.to_csv(result_csv_path, index=False)