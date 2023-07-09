# 靡不有初，鲜克有终
# 开发时间：2023/7/9 14:42
import pandas as pd
from gurobipy import *


# 读取路网文件
link_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network5\link.txt')
node_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network5\node.txt')

# 根据网络建立变量下标
variables_lst = []
from_node_lst = list(pd.unique(link_df['from_node_id']))
to_node_lst = list(pd.unique(link_df['to_node_id']))
inter_node_lst = list(set(from_node_lst+to_node_lst))

# 添加从起点流出的弧
for i in from_node_lst:
    variables_lst.append(('s', i))
# 添加网络结构中存在的弧
for i in range(0, len(link_df)):
    variables_lst.append((link_df.loc[i, "from_node_id"], link_df.loc[i, "to_node_id"]))
# 添加流入终点的弧
for i in to_node_lst:
    variables_lst.append((i, 't'))
variables_tuplelist = tuplelist(variables_lst)  # tuplelist结构，以便于快速检索
print("变量下标：", variables_lst)
print("中间结点:", inter_node_lst)

# 建立模型框架
m = Model("MCBM")

# 定义变量
x = m.addVars(variables_tuplelist, vtype=GRB.BINARY, name='x')  # 弧流量
f = m.addVar(vtype=GRB.INTEGER, name='f')
m.update()

# 定义目标函数
m.setObjective(f, sense=GRB.MAXIMIZE)

# 定义约束条件
m.addConstr((quicksum(x[i, j] for i, j in variables_tuplelist.select('s', '*')) - quicksum(x[i, j] for i, j in variables_tuplelist.select('*', 's')) == f), 's')  # 起点流出-起点流入
m.addConstr((quicksum(x[i, j] for i, j in variables_tuplelist.select('t', '*')) - quicksum(x[i, j] for i, j in variables_tuplelist.select('*', 't')) == -f), 't')  # 终点流出-终点流入
m.addConstrs((quicksum(x[i, j] for i, j in variables_tuplelist.select(c, '*')) - quicksum(x[i, j] for i, j in variables_tuplelist.select('*', c)) == 0 for c in inter_node_lst), '-')

# 求解
m.optimize()

# 展示结果
var_lst = m.getVars()
print(var_lst)
print("____________求解结果____________")
print("变量值：")
for i in range(0, len(var_lst)):
    if var_lst[i].X != 0:
        print(var_lst[i].VarName, var_lst[i].X)
print("目标函数值：", m.ObjVal)
m.write('MCBM.lp')
