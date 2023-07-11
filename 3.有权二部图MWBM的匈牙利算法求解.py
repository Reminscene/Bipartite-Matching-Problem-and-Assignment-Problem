# 靡不有初，鲜克有终
# 开发时间：2023/7/10 16:48


import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment


def hungarian_algorithm(M):
    row_ind, col_ind = linear_sum_assignment(M)  # 算法的分配结果
    return row_ind, col_ind


if __name__ == "__main__":
    # 读取网络数据，这里仅仅适用network6
    node_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network6\node.txt')
    link_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network6\link.txt')
    print(link_df)
    size = max(len(list(pd.unique(link_df['from_node_id']))), len(list(pd.unique(link_df['to_node_id']))))
    matrix = 999 * np.ones((size, size))
    for i in range(0, len(link_df)):
        x_index = link_df.loc[i, 'from_node_id'] % 6 - 1
        y_index = link_df.loc[i, 'to_node_id'] % 6
        matrix[x_index, y_index] = link_df.loc[i, 'cost']
    matching_lst = []
    print('原始矩阵：\n', matrix, '\n')

    # 输出匹配结果
    for i in range(0, size):
        matching_lst.append([hungarian_algorithm(matrix)[0][i], hungarian_algorithm(matrix)[1][i]])
    matching_matrix = np.zeros((size, size))
    for i in matching_lst:
        matching_matrix[i[0], i[1]] = 1
        i[0] += 1
        i[1] += 6
    print('匹配选择结果：\n', matching_lst)
    # 输出计算的权重结果
    print('总权重之和为：\n', sum(sum(matching_matrix*matrix)))
