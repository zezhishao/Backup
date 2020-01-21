# -*- coding: UTF-8 -*-
"""
# @Project : TrajectorySimilarityMaritime
# @File    : Draw.py.py
# @Author  : Shao Zezhi
# @Contact : zezhishao@gmail.com
# @Software: PyCharm
# @license : Copyright(C), Shao Zezhi
# @Intro   : 数据可视化接口
"""

import os
import numpy as np
import folium
from folium import plugins
import pandas as pd

usefule_data_path = "/Users/shaozezhi/DataSet/UsefulData"


def get_popup(time, lon, lat):
    """
    获取自定义格式的popup
    :param time:
    :param lon:
    :param lat:
    :return:
    """
    test = folium.Html(
        '<b>time: {}</b></br> <b>lon: {}</b></br> <b>lat: {}</b></br> '.format(time, lon, lat),
        script=True)
    popup = folium.Popup(test, max_width=2650)
    return popup


def draw_trajectory(trajectory, MMSI):
    # trajectory = [[time, lon, lat], [time, lon2, lat2], ... ,[time, lon n, lat n]]
    # TODO lon、lat的位置要测试一下
    # Map构建基本地图图层
    m = folium.Map(
        # lat, lon
        location=[trajectory[0][2], trajectory[0][1]],
        zoom_start=10
    )

    # 画轨迹
    for i in range(1, len(trajectory) - 1):
        folium.Marker(
            location=[trajectory[i][2], trajectory[i][1]],
            popup=get_popup(trajectory[i][0],
                            trajectory[i][1],
                            trajectory[i][2]), icon=folium.Icon(color='red')).add_to(m)

    # 给每个点画标志
    plugins.AntPath(
        locations=[[x[2], x[1]] for x in trajectory],
        reverse=False,
        dash_array=[20, 30],
        color='#FF0000'  # red
    ).add_to(m)

    # 轨迹起点
    folium.Marker(location=[trajectory[0][2], trajectory[0][1]],
                  popup=get_popup(trajectory[0][0],
                                  trajectory[0][1],
                                  trajectory[0][2]), icon=folium.Icon(color='blue')).add_to(m)

    # 轨迹终点
    folium.Marker(location=[trajectory[-1][2], trajectory[-1][1]],
                  popup=get_popup(trajectory[-1][0],
                                  trajectory[-1][1],
                                  trajectory[-1][2]), icon=folium.Icon(color='orange')).add_to(m)

    m.save(os.path.join(usefule_data_path, str(MMSI) + ".html"))


def get_trajectory(MMSI):
    """
    根据输入的MMSI，前往Useful Data文件夹中寻求到相关的文件，获取到该文件的轨迹
    使用pandas处理，方便排序
    :param MMSI:要查询的船号
    :return:
    """
    csv_file = usefule_data_path + "/" + MMSI + ".csv"
    csv_data = pd.read_csv(csv_file, low_memory=False)  # 防止弹出警告
    csv_df = pd.DataFrame(csv_data).sort_values("BaseDateTime", inplace=False).reset_index(drop=True)[
        ['BaseDateTime', 'LON', 'LAT']]  # 排序、抽取
    csv_list = np.array(csv_df).tolist()  # np.ndarray()
    return csv_list


if __name__ == "__main__":
    file_count = 0
    files = os.listdir(usefule_data_path)
    i = 0
    # 统计row数量
    for file_name in files:
        MMSI = os.path.splitext(file_name)[0]
        suffix = os.path.splitext(file_name)[1]
        if suffix == '.html':
            continue
        draw_trajectory(get_trajectory(MMSI), MMSI)
        i += 1
        if i%100 == 0:
            print("已经处理" + str(i) + "个文件")
