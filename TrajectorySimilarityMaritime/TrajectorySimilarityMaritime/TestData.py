# -*- coding: UTF-8 -*-
"""
# @Project : TrajectorySimilarityMaritime
# @File    : TestData.py
# @Author  : Shao Zezhi
# @Contact : zezhishao@gmail.com
# @Software: PyCharm
# @license : Copyright(C), Shao Zezhi
# @Intro   : 测试数据格式、测试重组数据
"""

import os
import csv
import pickle
from shutil import copyfile


import matplotlib.pyplot as plt

from DataGeneration import data_statistics

os.chdir("/Users/shaozezhi/DataSet")

files = os.listdir("./UsefulData/")
file_count = 0
for file in files:
    copyfile(os.getcwd() + "/UsefulData/" + file, os.getcwd() + "/SeparatedData/" + file)
    file_count +=1
    if file_count % 100 == 0:
        print("已经处理" + str(file_count) + "个文件")