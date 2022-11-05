#-*- coding : utf-8-*-
# coding:unicode_escape

import numpy as np
import pandas as pd
from IPython import embed
import matplotlib.pyplot as plt
from collections import Counter
import os
import networkx as nx

region_list = [
'朝阳区'	,
'二道区',
'经开区',
'净月区',
'宽城区',
'绿园区',
'南关区',
'汽开区',
'长春新区',
]

def plot_traffic_map(housing_x_y, region, line_IDs, line_x_y_ID, node_x_y):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title("Traffic information and Community information of Changchun")
    color = ['blue', 'cyan', 'green', 'black', 'magenta', 'red', 'white', 'yellow', '#F8F8FF']
    for index, node in enumerate(housing_x_y):
        ax1.scatter(node[0], node[1], color=color[region[index] - 1], s=1.0)
    # 画交通线
    for lineID in line_IDs:
        line_start_node_ID = int(line_x_y_ID[int(lineID) - 1][0])
        line_end_node_ID = int(line_x_y_ID[int(lineID) - 1][1])
        line_start_x = node_x_y[line_start_node_ID - 1][0]
        line_start_y = node_x_y[line_start_node_ID - 1][1]
        line_end_x = node_x_y[line_end_node_ID - 1][0]
        line_end_y = node_x_y[line_end_node_ID - 1][1]
        ax1.plot([line_start_x, line_end_x], [line_start_y, line_end_y], color='#9ED8EF', linewidth=0.5)
        # if lineID == 1.0: break
    plt.show()

if __name__ == '__main__':
    traffice_nodes_data = pd.read_csv('./data/traffice_notes.csv')
    traffice_lines_data = pd.read_csv('./data/traffice_lines.csv')
    housing_data = pd.read_csv('./data/housing_data.csv')
    # 交通路口节点编号
    node_ID = traffice_nodes_data.values[:, 0]
    # 交通路口节点坐标
    node_x_y = traffice_nodes_data.values[:, 1:3]
    # 交通路口线路编号
    line_IDs = traffice_lines_data.values[:, 0]
    # 交通线路起始点路口编号
    line_x_y_ID = traffice_lines_data.values[:, 1:3]
    # 交通线路路线距离
    line_dist = traffice_lines_data.values[:, -1]
    # 小区ID
    housing_ID = housing_data.values[:, 0]
    # 小区楼栋数
    building_bumber = housing_data.values[:, 1]
    # 小区户数（户）
    house_bumber = housing_data.values[:, 2]
    # 小区人口数（人）
    population = housing_data.values[:, 3]
    # 小区横坐标，纵坐标
    housing_x_y = housing_data.values[:, 4:6]
    # 街道编号
    street_ID = housing_data.values[:, -2]
    # 所属区域
    region = housing_data.values[:, -1]

    # 画城市交通图、小区散点图
    plot_traffic_map(housing_x_y, region, line_IDs, line_x_y_ID, node_x_y)