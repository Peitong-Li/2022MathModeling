import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import scipy.io as scio
from IPython import embed
from collections import Counter



plt.rcParams["font.sans-serif"]='SimHei'   #解决中文乱码问题
plt.rcParams['axes.unicode_minus']=False   #解决负号无法显示的问题
import numpy as np
#计算样本间距离
def distance(x, y, p=2):
    '''
    input:x(ndarray):第一个样本的坐标
          y(ndarray):第二个样本的坐标
          p(int):等于1时为曼哈顿距离，等于2时为欧氏距离
    output:distance(float):x到y的距离
    '''
    dis2 = np.sum(np.abs(x-y)**p) # 计算
    dis = np.power(dis2,1/p)
    return dis

def sorted_list(data,Cmass):
    '''
    input:data(ndarray):数据样本
          Cmass(ndarray):数据样本质心
    output:dis_list(list):排好序的样本到质心距离
    '''
    dis_list = []
    for i in range(len(data)):       # 遍历data数据，与质心cmass求距离
        dis_list.append(distance(Cmass,data[i][:]))
    # dis_list = sorted(dis_list)      # 排序
    return dis_list


name = 'qikai'
title_name = "汽开"
# 从Excel中读取数据存入数组
datMat = scio.loadmat("./data/" + name + ".mat")[name]
n_cluster = 13
mdl_new = np.array(datMat)[:, 0:-1]
label = np.array(datMat)[:, -1]
# rawData = xlrd.open_workbook('kmeans.xlsx')
# table = rawData.sheets()[0]
# data = []
# for i in range(table.nrows):
#     if i == 0:
#         continue
#     else:
#         data.append(table.row_values(i)[1:])
# featureList = ['PH', 'S', 'N']
# mdl = pd.DataFrame.from_records(data, columns=featureList)
# # 聚类
# mdl_new = np.array(mdl[['PH', 'S', 'N']])# 将其转化为数组
seed = 9# 设置随机数
clf = KMeans(n_clusters=n_cluster, random_state=seed)# 构造k-means聚类器
clf.fit(mdl_new)# 拟合模型
# print(clf.cluster_centers_) # 以数组形式查看KMeans聚类后的质心点，即聚类中心。
my_clf_label = clf.labels_ # 对原数据表进行类别标记
#图形化展示
label_pred = clf.labels_ #获取聚类标签
centroids = clf.cluster_centers_ #获取聚类中心
inertia = clf.inertia_ # 获取聚类准则的总和
mark = ['or', 'ob', 'og', 'ok','*y', '*k', '*c', '*k', '+m', '+g', '+k', '+r','^c', '^b', '^g', '^k','<m', '<b', '<g', '<k']
# 这里'or'代表中的'o'代表画圈，'r'代表颜色为红色，后面的依次类推
color = 0
j = 0
for i in label_pred:
    plt.plot([mdl_new[j:j+1,0]], [mdl_new[j:j+1,1]],
     mark[i], markersize = 5)
    j +=1
plt.title(title_name + "区K-means聚类结果")
plt.savefig('./data/q2/' + name + '.png')
plt.show()# 画出聚类结果简易图

class_list = [[] for i in range(n_cluster)]
points_center = []
for i in range(len(my_clf_label)):
    class_list[my_clf_label[i]].append(mdl_new[i])
    points_center.append(centroids[my_clf_label[i]])
res = Counter(my_clf_label)
dist_list = []
for i, class_num in enumerate(class_list):
    sorted_dist = sorted_list(class_num, centroids[my_clf_label[i]])
    dist_list.append(sorted_dist)

for i in range(len(dist_list)):
    # print(dist_list[i][0] * 106991)
    dist_list[i] = np.array(dist_list[i])
    if i != 0:
        temp_array = np.concatenate((temp_array, dist_list[i]),axis=0)
    else:
        temp_array = dist_list[0]
    # dist_list[i] = dist_list[i] * 106991

dist_list = np.array(temp_array) * 106991
a0 = pd.DataFrame(mdl_new, columns=['community_x', 'community_y'])
a1=pd.DataFrame(my_clf_label, columns=['community_class'])
a2= pd.DataFrame(np.array(points_center), columns=['x', 'y'])
a3= pd.DataFrame(dist_list, columns=['dist'])
a4 = pd.concat([a0, a1, a2, a3], axis=1)
a4.to_csv('./data/q4/' + name + '.csv')
print('save res to: ', './data/q4/' + name + '.csv')
print('save image to: ', './data/q2/' + name + '.png')

