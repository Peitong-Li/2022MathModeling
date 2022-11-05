from math import cos, sin, atan2, sqrt, pi, radians, degrees
import numpy as np
import pandas as pd
from IPython import embed
import matplotlib.pyplot as plt
from collections import Counter
import os
import networkx as nx

'''
one_level_points: list, len() == 1, [x, y]
two_level_points: list, len() == 物资投放点个数, [[x1,y1], [x2,y2]]
three_level_points: np.array, shape == (小区数, 2), [[x1,y1], [x2,y2]]
'''

def calc_dist(x1, x2, y1, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2) * 106991

def plot_graph(one_level_points, two_level_points, three_level_points, three_level_class, center_label, region_name):
    one_level_number = 1
    two_level_number = len(two_level_points)
    three_level_number = three_level_points.shape[0]
    # 制作pos
    a = []
    a.append(list(one_level_points))
    for two_level in two_level_points:
        a.append(two_level)   # 13
    for three_level in list(three_level_points):
        a.append(three_level)  # 200

    G = nx.DiGraph()
    pos = a
    nodes = {
        'r':[0],
        'g':[i for i in range(1, two_level_number+1)],  # 13
        'b':[i for i in range(two_level_number+1, two_level_number + three_level_number+1)]  # 200
    }
    edge_info_list = []


    for i in range(len(a)):
        G.add_node(i, desc=i)
    for i in range(len(a)):
        if i > two_level_number + 1:
            temp_three_sum += 1
            node_class = three_level_class[temp_three_sum]
            current_center_pos = center_label[int(node_class)][0]
            # calc_dist()
            x1 = two_level_points[current_center_pos][0]
            y1 = two_level_points[current_center_pos][1]
            x2 = three_level_points[i - two_level_number - 1][0]
            y2 = three_level_points[i - two_level_number - 1][1]
            dist = calc_dist(x1, x2, y1, y2)
            G.add_edge(current_center_pos+1, i, name=dist)
            edge_info_list.append(dist)

        if i > 0 and i < two_level_number+1:
            x1 = one_level_points[0]
            y1 = one_level_points[1]
            x2 = two_level_points[i-1][0]
            y2 = two_level_points[i-1][1]
            dist = calc_dist(x1, x2, y1, y2)
            G.add_edge(0, i, name=dist)
            edge_info = {
                    'node1': 0,
                    'node2': i,
                    'weight': dist
                }
            edge_info_list.append(dist)

        if i==two_level_number+1:
            temp_three_sum = 0
            node_class = three_level_class[temp_three_sum]
            x1 = two_level_points[0][0]
            y1 = two_level_points[0][1]
            x2 = three_level_points[i-0-1][0]
            y2 = three_level_points[i-0-1][1]
            dist = calc_dist(x1, x2, y1, y2)
            G.add_edge(center_label[int(node_class)][0]+1, i, name=dist)
            edge_info = {
                'node1': 0,
                'node2': i,
                'weight': dist
            }
            edge_info_list.append(dist)


    nx.draw(G, pos, nodelist=nodes['r'], edge_color='k', node_color='r', node_size=200, with_labels=False, linewidths=0.1)
    nx.draw(G, pos, nodelist=nodes['g'], edge_color='k', node_color='g', node_size=150, with_labels=False, linewidths=0.1)
    nx.draw(G, pos, nodelist=nodes['b'], edge_color='k', node_color='b', node_size=100, with_labels=False, linewidths=0.1)

    # nx.draw_networkx_nodes(G, pos, nodelist=nodes['r'], node_color='r', node_size=50, )
    # nx.draw_networkx_nodes(G, pos, nodelist=nodes['g'], node_color='k', node_size=30)
    # nx.draw_networkx_nodes(G, pos, nodelist=nodes['b'], node_color='g', node_size=3)
    # 画出边权值
    # edge_labels = nx.get_edge_attributes(G, 'name')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title('AOE_CPM', fontsize=10)
    # plt.savefig('./data/q4/'+region_name+'_1.jpg')
    plt.show()
    print(name, '   ', sum(edge_info_list))


def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)

    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


if __name__ == '__main__':
    # traffice_nodes_data = pd.read_csv('./data/traffice_notes.csv')
    # traffice_lines_data = pd.read_csv('./data/traffice_lines.csv')
    # housing_data = pd.read_csv('./data/housing_data.csv')
    name_list = ['chaoyang', 'lvyuan', 'nanguan', 'kuanchengqu', 'erdao', 'changchunxin', 'jingyue', 'jingkai', 'qikai']
    for name in name_list:
        region_name = name
        data = pd.read_csv('./data/q4/'+ region_name + '.csv').values
        community_x = data[:, 1]
        community_y = data[:, 2]
        community_class = data[:, 3]
        community_x_y = data[:, 1:3]
        center_x = data[:, 4]
        center_y = data[:, 5]
        dist = data[:, 6]
        list_center_x = list(center_x)
        list_center_y = list(center_y)

        # 寻找中心点坐标 (center_points)
        center_points = []
        temp_x = []
        center_label = [[] for i in range(int(max(list(community_class)) + 1))]
        for i, x in enumerate(list_center_x):
            if i == 0:
                temp_x.append(x)
                center_points.append([x, list_center_y[i]])
                center_label[int(list(community_class)[i])].append(0)
            else:
                if x not in temp_x:
                    temp_x.append(x)
                    center_points.append([x, list_center_y[i]])
                    center_label[int(list(community_class)[i])].append(len(temp_x)-1)
        three_level_points = community_x_y
        two_level_points = center_points
        one_level_points = center_geolocation(two_level_points)
        print(name + ":", one_level_points)
        plot_graph(one_level_points, two_level_points, three_level_points, community_class, center_label, region_name)



