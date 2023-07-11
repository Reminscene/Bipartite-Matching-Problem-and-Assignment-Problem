# 靡不有初，鲜克有终
# 开发时间：2023/7/10 16:48

import numpy as np
import random
import pandas as pd


def cover_lines(matrix):
    new_matrix = matrix.copy()  # 这个矩阵是可以进行调整的
    row_zero_lst = []  # 存储矩阵每行的0数量的列表
    col_zero_lst = []  # 存储矩阵每列的0数量的列表
    size = len(matrix)
    for i in range(0, size):
        row_zero_lst.append(list(matrix[i, :]).count(0))  # 行视角下，每行0的数量(原本矩阵)
    for j in range(0, size):
        col_zero_lst.append(list(matrix[:, j]).count(0))  # 列视角下，每列0的数量（原本矩阵）
    max_zero_row = max(row_zero_lst)  # 在行视角下，最多的0的数量
    max_zero_col = max(col_zero_lst)  # 在列视角下，最多的0的数量

    row_line_lst = []  # 横线（行）集合
    col_line_lst = []  # 竖线（列）集合

    while 0 in new_matrix:  # 当0在新矩阵中时，说明0还没有被完全覆盖掉
        if max_zero_row >= max_zero_col:  # 如果行的0比列的多，则使用横线覆盖
            row_line_index = row_zero_lst.index(max_zero_row)  # 需要被覆盖的行索引
            row_line_lst.append(row_line_index)
            for i in range(0, size):
                new_matrix[row_line_index, i] = 1  # 用1来进行覆盖操作，消除0
        else:
            col_line_index = col_zero_lst.index(max_zero_col)  # 需要被覆盖的列索引
            col_line_lst.append(col_line_index)
            for i in range(0, size):
                new_matrix[i, col_line_index] = 1  # 用1来进行覆盖操作，消除0

        row_zero_lst = []
        col_zero_lst = []
        for i in range(0, size):
            row_zero_lst.append(list(new_matrix[i, :]).count(0))  # 行视角下，每行0的数量(覆盖操作的矩阵)
        for j in range(0, size):
            col_zero_lst.append(list(new_matrix[:, j]).count(0))  # 列视角下，每列0的数量（覆盖操作的矩阵）
        max_zero_row = max(row_zero_lst)  # 在行视角下，覆盖后，当前最多的0的数量
        max_zero_col = max(col_zero_lst)  # 在列视角下，覆盖后，当前最多的0的数量

    return row_line_lst, col_line_lst


def matrix_transformation(matrix, row_line_lst, col_line_lst):  # 输入矩阵、行覆盖线、列覆盖线，输出新矩阵

    un_cover_num = []  # 矩阵中没有被覆盖的元素集合
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            if i not in row_line_lst and j not in col_line_lst:
                un_cover_num.append(matrix[i, j])
    min_num = min(un_cover_num)  # 找到未覆盖元素的最小值

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            if i not in row_line_lst and j not in col_line_lst:
                matrix[i, j] = matrix[i, j] - min_num
            if i in row_line_lst and j in col_line_lst:
                matrix[i, j] = matrix[i, j] + min_num

    return matrix


def row_col_subtraction(matrix):  # 输入初始矩阵，输出行减去行最小值、而后列减去列最小值的矩阵

    size = len(matrix)
    new_matrix_row = matrix.copy()  # 减去行最小后的矩阵
    # 减去每一行最小值
    for i in range(0, size):
        min_value_row = min(list(matrix[i, :]))  # 第i行最小值
        for j in range(0, size):
            new_matrix_row[i, j] = new_matrix_row[i, j] - min_value_row
    # 减去每一列最小值
    new_matrix_col = new_matrix_row.copy()  # 减去列最小后的矩阵
    for j in range(0, size):
        min_value_col = min(list(new_matrix_row[:, j]))  # 第j列最小值
        for i in range(0, size):
            new_matrix_col[i, j] = new_matrix_col[i, j] - min_value_col

    return new_matrix_col


def min_zero(lst):  # 输入列表，输出列表中的除了0之外的最小值

    total = sum(lst)
    new_lst = lst.copy()
    for i in range(0, len(lst)):
        if lst[i] == 0:
            new_lst[i] = total

    return min(new_lst)


def select_zero_elements(matrix):  # 输入矩阵，输出n个符合条件的元素位置（行标、列标）

    new_matrix = matrix.copy()  # 这个矩阵是用来判断循环是否结束的
    size = len(matrix)
    row_zero_lst = []
    col_zero_lst = []
    unvisited_row_lst = [i for i in range(0,size)]  # 用于记录还没有访问过的行和列
    unvisited_col_lst = [i for i in range(0,size)]
    for i in range(0, size):
        row_zero_lst.append(list(matrix[i, :]).count(0))  # 行视角下，每行0的数量(原本矩阵)
    for j in range(0, size):
        col_zero_lst.append(list(matrix[:, j]).count(0))  # 列视角下，每列0的数量（原本矩阵）
    min_zero_row = min_zero(row_zero_lst)  # 在行视角下，最少的0的数量
    min_zero_col = min_zero(col_zero_lst)  # 在列视角下，最少的0的数量
    select_lst = []  # 所选的0元素的集合

    while 0 in new_matrix:
        if min_zero_row <= min_zero_col:  # 如果行的0比列的少，则选择该行中的0元素
            row_line_index = row_zero_lst.index(min_zero_row)  # 需要挑选0的行索引
            zero_pool_row = []  # 用来暂时存放该行0元素索引的列表
            for i in unvisited_col_lst:  # 列索引
                if matrix[row_line_index, i] == 0:
                    zero_pool_row.append(i)
            col = random.choice(zero_pool_row)
            select_lst.append([row_line_index, col])  # 挑选一个0入列【行索引，列索引】
            unvisited_row_lst.remove(row_line_index)
            unvisited_col_lst.remove(col)

        else:
            col_line_index = col_zero_lst.index(min_zero_col)  # 需要挑选0的列索引
            zero_pool_col = []  # 用来暂时存放该列0元素索引的列表
            for i in unvisited_row_lst:  # 行索引
                if matrix[i, col_line_index] == 0:
                    zero_pool_col.append(i)
            row = random.choice(zero_pool_col)
            select_lst.append([row, col_line_index])  # 挑选一个0入列【行索引，列索引】
            unvisited_row_lst.remove(row)
            unvisited_col_lst.remove(col_line_index)

        row_zero_lst = []
        col_zero_lst = []
        # 要将所选元素所在列对应其他行的0（如果存在）的数量-1(用1来覆盖)，行也如此
        for i in range(0, len(select_lst)):
            line_col = select_lst[i][1]
            line_row = select_lst[i][0]
            for j in unvisited_row_lst:
                if matrix[j, line_col] == 0:
                    matrix[j, line_col] = 1
            for k in unvisited_col_lst:
                if matrix[line_row, k] == 0:
                    matrix[line_row, k] = 1

        new_matrix = matrix.copy()  # 这个矩阵是用来判断循环是否结束的
        for i in range(0, len(select_lst)):
            new_matrix[select_lst[i][0], select_lst[i][1]] = 1

        # 承接上一个，由于挑选的0元素，而导致的改变矩阵中0数量的改变（将所选0元素所在的行/列的0总数设置为size+1）
        for i in range(0, size):
            if i in unvisited_row_lst:
                row_zero_lst.append(list(matrix[i, :]).count(0))  # 行视角下，每行0的数量(新矩阵)
            else:
                row_zero_lst.append(size+1)
        for j in range(0, size):
            if j in unvisited_col_lst:
                col_zero_lst.append(list(matrix[:, j]).count(0))  # 列视角下，每列0的数量（新矩阵）
            else:
                col_zero_lst.append(size+1)

        min_zero_row = min_zero(row_zero_lst)  # 在行视角下，最少的0的数量
        min_zero_col = min_zero(col_zero_lst)  # 在列视角下，最少的0的数量

    return select_lst


def hungarian_algorithm(matrix):  # 匈牙利算法，输入矩阵，输出0元素的位置（行标，列标）,以及最小权重之和

    size = len(matrix)
    matrix_subtraction = row_col_subtraction(matrix)  # 行列元素各减去最小值
    row_lines = cover_lines(matrix_subtraction)[0]
    col_lines = cover_lines(matrix_subtraction)[1]
    total_lines = len(row_lines) + len(col_lines)
    matrix_iteration = matrix_subtraction.copy()

    while total_lines < size:  # 当覆盖线的数量小于矩阵规模时，进行循环
        matrix_iteration = matrix_transformation(matrix_iteration, row_lines, col_lines)
        row_lines = cover_lines(matrix_iteration)[0]
        col_lines = cover_lines(matrix_iteration)[1]
        total_lines = len(row_lines) + len(col_lines)

    print('变换后的矩阵为：,\n', matrix_iteration, '\n')
    select_lst = select_zero_elements(matrix_iteration)
    # 输出最小权值之和
    total_weight = 0
    for i in select_lst:
        total_weight += matrix[i[0], i[1]]

    return select_lst, total_weight


# 读取网络数据，这里仅仅适用network6
node_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network6\node.txt')
link_df = pd.read_csv(r'C:\Users\张晨皓\Desktop\指派问题\network6\link.txt')
print(link_df)
size = max(len(list(pd.unique(link_df['from_node_id']))), len(list(pd.unique(link_df['to_node_id']))))
matrix = np.zeros((size, size))
for i in range(0, len(link_df)):
    x_index = link_df.loc[i, 'from_node_id'] % 6 - 1
    y_index = link_df.loc[i, 'to_node_id'] % 6
    matrix[x_index, y_index] = -link_df.loc[i, 'cost']

print('原始矩阵：\n', matrix, '\n')

select_result, weight = hungarian_algorithm(matrix)
print('匹配选择结果：\n', select_result)
print('总权重：\n', -weight, '\n')
