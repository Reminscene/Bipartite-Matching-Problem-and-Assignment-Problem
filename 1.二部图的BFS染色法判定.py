# 靡不有初，鲜克有终
# 开发时间：2023/7/7 18:31
import pandas as pd
import random


class Node:  # 定义结点类
    def __init__(self):
        self.node_id = None
        self.x_coord = None
        self.y_coord = None
        self.flow_in_link = []
        self.flow_out_link = []
        self.flow_in_node = []
        self.flow_out_node = []
        self.neighbor = []
        self.color = 0  # 0:未上色，1:红色，-1:蓝色


class Link:  # 定义路段类
    def __init__(self):
        self.link_id = None
        self.cost = None
        self.from_node_id = None
        self.to_node_id = None


class Network:  # 定义路网类
    def __init__(self, node_txt, link_txt):  # 定义了路网类属性，作用为读取路网文件
        self.node = node_txt
        self.link = link_txt

    def read_node(self):
        self.node_lst = []
        self.unique_node_id_lst = list(pd.unique(self.node["node_id"]))  # 路网道路结点编号不一定从0开始，或有间断
        for i in range(0, len(self.node)):
            a = Node()
            a.node_id = self.node.loc[i, 'node_id']
            a.x_coord = self.node.loc[i, 'x_coord']
            a.y_coord = self.node.loc[i, 'y_coord']
            self.node_lst.append(a)

    def read_link(self):
        self.link_lst = []
        for i in range(0, len(self.link)):
            b = Link()
            b.link_id = self.link.loc[i, "link_id"]
            b.cost = self.link.loc[i, "cost"]
            b.from_node_id = self.link.loc[i, "from_node_id"]
            b.to_node_id = self.link.loc[i, "to_node_id"]
            from_node_index = self.unique_node_id_lst.index(b.from_node_id)  # 这条路段是从哪个结点来的
            self.node_lst[from_node_index].flow_out_link.append(b.link_id)
            self.node_lst[from_node_index].flow_out_node.append(b.to_node_id)
            to_node_index = self.unique_node_id_lst.index(b.to_node_id)  # 这条路段是往哪个结点去的
            self.node_lst[to_node_index].flow_in_link.append(b.link_id)
            self.node_lst[to_node_index].flow_in_node.append(b.from_node_id)
            self.node_lst[to_node_index].neighbor.append(b.from_node_id)
            self.link_lst.append(b)

'''print("当前结点编号:", network.node_lst[1].node_id)
print("流入的结点编号:", network.node_lst[1].flow_in_node)
print("流出的结点编号:", network.node_lst[1].flow_out_node)
print("相邻结点编号:", network.node_lst[1].neighbor)
print("流入的路段:", network.node_lst[1].flow_in_link)
print("流出的路段:", network.node_lst[1].flow_out_link)
print("结点颜色:", network.node_lst[1].color, "\n")'''


def discriminate(net):  # 定义二部图BFS染色法，输入路网
    start_vertice_id = random.choice(net.unique_node_id_lst)  # 随机生成起始点id
    start_vertice_index = net.unique_node_id_lst.index(start_vertice_id)  # 始点id对应的序号
    net.node_lst[start_vertice_index].color = 1  # 染红色
    queue = [start_vertice_id]  # 初始队列，仅含起始点
    judje = 1  # 1表示是二部图，0不是二部图
    while len(queue) != 0:  # 当列表未清空,进行循环
        current_vertice_id = queue[0]  # 摘出队列的第一个点进行研究，BFS
        current_vertice_index = net.unique_node_id_lst.index(current_vertice_id)
        current_vertice_color = net.node_lst[current_vertice_index].color  # 摘出来的第一个点的颜色
        queue.pop(0)  # 出列
        for i in net.node_lst[current_vertice_index].neighbor:  # 这一结点的相邻结点的id，不是索引
            neighbor_vertice_index = net.unique_node_id_lst.index(i)
            if net.node_lst[neighbor_vertice_index].color != 0:  # 被染过色（访问过）
                neighbor_vertice_color = net.node_lst[neighbor_vertice_index].color  # 相邻结点的颜色
                if neighbor_vertice_color + current_vertice_color != 0:  # 不符合着色要求（即颜色不同）
                    judje = 0
                    break
                else:
                    continue
            else:  # 没有被染过色（没有访问过）
                net.node_lst[neighbor_vertice_index].color = 0 - current_vertice_color  # 染一个不同的颜色
                queue.append(i)
    remove_id_lst = []
    color_lst = []
    for i in range(0, len(net.node_lst)):
        color_lst.append(net.node_lst[i].color)
    if judje == 0:
        print("最终判断结果不是二部图")
        return 0, color_lst  # 不是二部图
    if judje != 0 and (0 not in color_lst):
        print("最终判断结果是二部图")
        return 1, color_lst  # 是二部图
    elif judje != 0 and (0 in color_lst):
        for i in range(0, len(net.node_lst)):
            if net.node_lst[i].color != 0:
                remove_id_lst.append(net.node_lst[i].node_id)
        return 2, remove_id_lst  # 需要删除子图再进行判断


node_df = pd.read_csv(r"C:\Users\张晨皓\Desktop\指派问题\network4\node.txt")
link_df = pd.read_csv(r"C:\Users\张晨皓\Desktop\指派问题\network4\link.txt")
network = Network(node_df, link_df)
network.read_node()
network.read_link()

k, remove_lst = discriminate(network)
print("判断变量（0-不是二部图、1-是二部图、2-需要删除子图）：", k)
print("需要删除的结点id【或者】结点颜色（-1蓝色、1红色）：", remove_lst)

while k == 2:
    node_df = node_df.drop(node_df[node_df.node_id.isin(remove_lst)].index)
    link_df = link_df.drop(link_df[link_df.from_node_id.isin(remove_lst)].index)
    link_df = link_df.drop(link_df[link_df.to_node_id.isin(remove_lst)].index)
    node_df.reset_index(inplace=True)
    link_df.reset_index(inplace=True)
    node_df.drop(axis=1, columns='index', inplace=True)
    link_df.drop(axis=1, columns='index', inplace=True)
    network = Network(node_df, link_df)
    network.read_node()
    network.read_link()
    k, remove_lst = discriminate(network)




