import random
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import json

def build_finetune_dataset_name(file_path):
    """
    取股票编码，构造数据集名字

    :param file_path: 输入CSV文件的路径
    :return: 构造的数据集名字
    """
    # 获取文件名
    file_name = os.path.basename(file_path)
    
    # 去掉文件名中的 "train_" 或 "val_" 前缀
    if file_name.startswith("train_") or file_name.startswith("val_"):
        file_name = file_name[6:]  # 去掉前缀
    
    # 获取文件名前六位作为股票编码
    stock_code = file_name[3:9]
    
    # 构造数据集名字
    finetune_data_name = stock_code + "_close"
    
    return finetune_data_name

def read_xlsx_colum(file_path,column):
    """
    cloumn:列序号从0开始
    """
    # 读取Excel文件
    df = pd.read_csv(file_path)
    # 获取某列数据
    column_data = df.iloc[:, column].values  # df.iloc[:, 3] 使用 .iloc 方法基于位置来选择数据。这里 : 表示选择所有行，而 3 则表示选择第四列数据
    # 打印结果，验证数据
    print(f"已提取列： {column_data}")
    return column_data

def read_similar_questions(file_path):
    similar_questions = []
    try:
        # 打开文件并逐行读取
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                stripped_line = line.strip()  # 去除行首尾的空白字符
                if stripped_line:  # 如果行不是空行
                    similar_questions.append(stripped_line)
        return similar_questions
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到。")
    except Exception as e:
        print(f"发生错误：{e}")

def generate_finetune_data(similar_questions,prices, dates, finetune_data_name):
    dataset = []
    # 遍历整个数列，依次取第1-24、2-25、3-26的数，直到无法取满24个数为止
    for i in range(len(prices) - 23):
        # 取连续的24个数
        segment_prices = prices[i:i+24]
        segment_dates = dates[i:i+24]
        
        # 将日期和股价拼接成字符串
        input_data_str = ', '.join([str(price) for price in segment_prices[:16]])
        output_data_str = ', '.join([str(price) for price in segment_prices[16:]])
        
        # 从similar_questions中随机选取一个instruction
        instruction = random.choice(similar_questions)
        
        # 构建微调数据
        finetune_data = {
            "instruction": instruction,
            "input": input_data_str,
            "output": output_data_str
        }
        print(finetune_data)
        # 加入数据集
        dataset.append(finetune_data)
    print(f"已构建{len(dataset)}条数据")
    
    # 保存为 JSON 文件
    with open(f'cloes_finetune_data/{finetune_data_name}_finetune_data.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

def split_dataset(file_path, train_ratio=0.8, train_output_dir="训练集/",val_output_dir="验证集/"):
    """
    将CSV文件切分为训练集和验证集，并保存为新的CSV文件。

    :param file_path: 输入CSV文件的路径
    :param train_ratio: 训练集的比例，默认为0.8
    :param output_dir: 输出文件的目录
    :return: None
    """
    # 获取文件名和扩展名
    file_name = os.path.basename(file_path)
    file_base_name, file_extension = os.path.splitext(file_name)

    # 读取CSV文件
    data = pd.read_csv(file_path)

    # 查看数据集的前几行
    print("原始数据集的前几行:")
    print(data.head())

    # 计算切分索引
    split_index = int(len(data) * train_ratio)

    # 切分数据集
    train_data = data.iloc[:split_index]
    val_data = data.iloc[split_index:]

    # 查看切分后的数据集大小
    print(f"训练集大小: {len(train_data)}")
    print(f"验证集大小: {len(val_data)}")

    # 构建输出文件路径
    train_file_path = os.path.join(train_output_dir, f"train_{file_base_name}{file_extension}")
    val_file_path = os.path.join(val_output_dir, f"val_{file_base_name}{file_extension}")

    # 保存切分后的数据集
    train_data.to_csv(train_file_path, index=False)
    val_data.to_csv(val_file_path, index=False)

    print("数据集切分完成并已保存。")


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
# 数据切分
files = get_all_files_absolute_path(r"D:/a股是我们的/股票/")
for file in files:
    file_path = file
    split_dataset(file_path=file_path)


train_data=get_all_files_absolute_path(r"D:/a股是我们的/验证集/")
for file in train_data:
    file_path = file
    #微调数据集构造
    # train_file_path=r"数据集/train.csv"
    finetune_data_name=build_finetune_dataset_name(file_path)
    close_prices=read_xlsx_colum(file_path=file_path,column=5)
    dates=read_xlsx_colum(file_path=file_path,column=0)
    similr_questions=read_similar_questions("相似问法_去重.txt")
    generate_finetune_data(similr_questions,close_prices,dates,finetune_data_name)
