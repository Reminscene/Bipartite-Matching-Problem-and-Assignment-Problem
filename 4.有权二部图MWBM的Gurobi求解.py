# 靡不有初，鲜克有终
# 开发时间：2023/7/11 12:14
from gurobipy import *
import pandas as pd

node_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network6\node.txt')
link_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network6\link.txt')

print(link_df)
customer_index = list(pd.unique(link_df['from_node_id']))  # 客户集合
driver_index = list(pd.unique(link_df['to_node_id']))  # 司机集合

# 使用合适的数据结构存储变量索引和成本
cost_value = []

for i in range(0, len(link_df)):
    cost_value.append(((link_df.loc[i, 'from_node_id'],link_df.loc[i, 'to_node_id']),link_df.loc[i, 'cost']))
variables, cost = multidict(cost_value)
print(variables)
print(cost)

# 定义模型
m = Model('MWBM')

# 定义变量
x = m.addVars(variables, vtype=GRB.BINARY, name='x')
m.update()
print(x)

# 定义目标函数
m.setObjective(x.prod(cost))

# 定义约束条件
m.addConstrs((quicksum(x[i, j] for i, j in variables.select(c, '*')) == 1 for c in customer_index), '-')
m.addConstrs((quicksum(x[i, j] for i, j in variables.select('*', d )) == 1 for d in driver_index), '-')

# 求解
m.optimize()

# 保存展示结果
m.write('MWBM.lp')
var_lst = m.getVars()
for i in var_lst:
    if i.X != 0:
        print(i.VarName, ':', i.X)
print("目标函数值为：", m.ObjVal)
