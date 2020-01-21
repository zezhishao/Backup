# -*- coding: UTF-8 -*-
"""
# @Project : TrajectorySimilarityMaritime
# @File    : DataGeneration.py
# @Author  : Shao Zezhi
# @Contact : zezhishao@gmail.com
# @Software: PyCharm
# @license : Copyright(C), Shao Zezhi
# @Intro   : 从原始数据生成可用数据
"""
import os
import csv
import pickle
from os import listdir
import matplotlib.pyplot as plt


def separate_data():
    """
    从原始数据，把每一艘船的轨迹数据分离出来并建立一个csv文件
    :return:
    """
    with open("AIS_2017_01_Zone10.csv") as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        # ['MMSI', 'BaseDateTime',
        # 'LAT', 'LON',
        # 'SOG', 'COG',
        # 'Heading', 'VesselName',
        # 'IMO', 'CallSign',
        # 'VesselType', 'Status',
        # 'Length', 'Width',
        # 'Draft', 'Cargo']
        MMSI_list = []
        for row in f_csv:
            data = row
            MMSI = data[0]
            # Separate data
            if MMSI in MMSI_list:
                with open("./SeparatedData/" + str(MMSI) + ".csv", 'a') as f1:
                    csv_writer = csv.writer(f1)
                    csv_writer.writerow(data)
            else:
                with open("./SeparatedData/" + str(MMSI) + ".csv", 'w') as f2:
                    csv_writer = csv.writer(f2)
                    csv_writer.writerow(headers)
                    csv_writer.writerow(data)
                    MMSI_list.append(MMSI)


def data_sort():
    """
    把数据统计一下然后排序，排序结果dict()存在DataStatistics文件中
    :return:
    """
    file_count = 0
    files = listdir("./SeparatedData/")
    # 统计row数量
    row_counter = dict()
    for file_name in files:
        with open("./SeparatedData/" + file_name, 'r') as f:
            file_content = csv.reader(f)
            row_count = sum(1 for row in file_content)
            if row_count in row_counter:
                row_counter[row_count] += 1
            else:
                row_counter[row_count] = 1
        # sort the counter
        file_count += 1
        if file_count % 100 == 0:
            print("已经处理" + str(file_count) + "个文件")

    f = open("./DataStatistics", 'wb')
    keys = list(row_counter.keys())
    keys.sort()
    sorted_row_counter = {key: row_counter[key] for key in keys}
    pickle.dump(sorted_row_counter, f)


def data_statistics():
    """
    把分离好的数据画图
    横轴：一条轨迹的轨迹点数量
    纵轴：又n个轨迹点的轨迹条数
    :return:
    """
    f = open("./DataStatistics", 'rb')
    row_counter = pickle.load(f)

    keys = list(row_counter.keys())
    values = list(row_counter.values())

    plt.bar(range(len(keys) - 5), values[5:])  # 把1和2长度的轨迹去除，这两种轨迹没有意义而且会影响统计图
    plt.show()


def data_filter(minimum, maximum):
    """
    把分离之后的数据，按照一定规则把不可用的数据给舍弃掉。
    舍弃的数据不要直接删除，应该移动到另一个文件夹当中，以备使用。
    :param minimum: 最小轨迹点数量
    :param maximum: 最大轨迹点数量
    :return:
    """
    file_count = 0
    files = listdir("./SeparatedData/")
    # 统计row数量
    for file_name in files:
        with open("./SeparatedData/" + file_name, 'r') as f:
            file_content = csv.reader(f)
            row_count = sum(1 for _row in file_content)
            if row_count < minimum or row_count > maximum:
                f.close()
                os.rename(os.getcwd() + "/SeparatedData/" + file_name, os.getcwd() + "/AbandonedData/" + file_name)
            else:
                f.close()
                os.rename(os.getcwd() + "/SeparatedData/" + file_name, os.getcwd() + "/UsefulData/" + file_name)
        # sort the counter
        file_count += 1
        if file_count % 100 == 0:
            print("已经处理" + str(file_count) + "个文件")


if __name__ == "__main__":
    os.chdir("/Users/shaozezhi/DataSet")
    # data_sort()
    # data_filter(20, 1000)
    data_statistics()


# Done set git ignore
# Done 1.draw a pic for data statistics. 2.filter data by maximum and minimum
# Donw draw pictures for different data with different length, seeing the features of real data and whether these real
#      data gets some data issues analyzed before.
#      一共1255条轨迹，轨迹点分布比较好，每一种点数量的轨迹都有，虽然大部分都是1

# Done 1. draw some trajectory data using some ship whose data suitable(not too poor or too rich)
# TODO 2. select some trajectory and use them to compare algorithms.
#      select trajectories based on what? How many trajectories should been selected?

# TODO think about how can we use these big and real data to train a model that can help solve the
#      SIMILARITY MEASUREMENT PROBLEMS.
