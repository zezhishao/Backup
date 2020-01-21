# _*_ coding: utf-8 _*_
# @Time   : 2020/1/21 1:02 下午 
# @Author : 邵泽志 
# @File   : Preprocess.py
# @Desc   :
import pandas as pd
import torch


def preprocess():
    """
    TODO:
    1. 读取train、test
    2. 压缩灰度至[0-1]，并调整维度
    3. split validation
    3. 处理存储成pytorch的tensor形式并存储
    :return:
    """
    # 1. 读取数据
    train_data_raw = pd.read_csv("./data/train.csv").drop(labels="label", axis=1)  # 取出所有数据
    train_label_raw = pd.read_csv("./data/train.csv")[["label"]]  # 取出所有label

    test_data_raw = pd.read_csv("./data/test.csv")

    # 2. Normalization
    train_data_raw = train_data_raw
    test_data_raw = test_data_raw

    # 3. 存储成
    train_data_tensor = torch.from_numpy(train_data_raw.values.reshape(-1, 28, 28))
    test_data_tensor = torch.from_numpy(test_data_raw.values.reshape(-1, 28, 28))
    train_label_tensor = torch.from_numpy(train_label_raw.values.reshape(-1))

    torch.save((train_data_tensor, train_label_tensor), "./data/train.pt")
    torch.save(test_data_tensor, "./data/test.pt")


if __name__ == "__main__":
    preprocess()
