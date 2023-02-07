#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   paylines_create_tuan.py
@Time    :   2022/6/8
@Desc    :   专门用来生成paylines game的每一局的图案，包括combo1/combo2等所有的combo
'''
import random
import pytest
from tqdm import tqdm

DEBUG_ON = False
PACKAGE_NAME = 'paylines_create_tuan'

def pprint(str):
    if DEBUG_ON:
        print(str)

# 下面的数据仅用来举个例子，不代表真实的数据
# 游戏包括哪些图案
# src_tuan_list = ['9', '10', 'J', 'Q', 'K', 'A', 'W', 'S']
# 每个REEL上各个图案对应的权重，下面的数据是5个REEL的情况
# quanzhong_list        = ((0, 5, 25, 10, 20, 0, 0, 0),
#                         (0, 5, 25, 10, 20, 0, 0, 0),
#                         (0, 5, 25, 10, 20, 0, 0, 0),
#                         (50, 5, 25, 10, 20, 0, 0, 0),
#                         (0, 5, 25, 10, 20, 0, 0, 0))

# tuan_num是指单个REEL上包含的图案总数，也就是每一列的图案个数，一般为3个
def create_one_reel_tuan(src_tuan_list, quanzhong_list,tuan_num):
    return random.choices(src_tuan_list, quanzhong_list, k=tuan_num)

# 创建一个二维数组，用来保存生成的图案矩阵，每个图案的初始值都是'X'
def create_array_by_rowandcol(row,col):
    data = []
    for i in range(row):
        row_data = []
        for j in range(col):
            row_data.append('X') # 默认用'X'图案填充整个图案矩阵
        data.append(row_data)
    return data

# 按照给定的权重随机生成一个图案矩阵，这个仅限于生成每一局的combo1的图案
# 即从0开始，没有任何先决条件，生成一个图案矩阵
def create_tuan_matrix(tuan_list, quanzhong_list, row, col):
    reel_all_tuan = create_array_by_rowandcol(row, col)
    for index, value1 in enumerate(quanzhong_list):
        reel_tuan = create_one_reel_tuan(tuan_list, value1, row)
        for j, value2 in enumerate(reel_tuan):
            reel_all_tuan[j][index] = value2
    return reel_all_tuan

# 根据当前的图案矩阵、中奖结果和支付线的位置，把中奖的图案替换为'X'，以便后续处理
# 这个是生成combo2/combo3.../comboN的第1步（连续消除后的新图案矩阵）
def update_tuan_matrix_with_X(tuan_matrix, win_result,paylines):
    # 把所有中奖图案替换为 'X'
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_tuan_matrix_with_X, old tuan:"+str(tuan_matrix))
    for single_payline_win_result in win_result[0]:
        line_number = single_payline_win_result[-1]
        lianxu_tuan_nums = single_payline_win_result[1]
        single_payline = paylines[line_number]
        for index in range(lianxu_tuan_nums):
            i,j = single_payline[index]
            tuan_matrix[i][j] = 'X'
    # 记录每一个REEL有多少个'X'，然后生成相应的新图案，然后合成新的REEL
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_tuan_matrix_with_X, new tuan with 'X':"+str(tuan_matrix))
    return tuan_matrix

# 这个是生成combo2/combo3.../comboN的第2步（连续消除后的新图案矩阵），具体分为3步:
# 1. 将标记为'X'的图案先删掉
# 2. 然后'X'的图案上面的图案往下面掉落
# 3. 接着生成新的图案，继续填补'X'图案被消除后留下的空间
def update_X_with_new_tuan(tuan_matrix_with_X, tuan_list, quanzhong_list):
    # 先将矩阵进行X Y转置，行和列换过来，从3 * 5 变成 5 * 3
    mid_tuan_matrix_with_X     = []    # 保存中间数据
    single_reel_tuan        = []    # 临时保存每个REEL上的数据
    rows = len(tuan_matrix_with_X)
    cols = len(tuan_matrix_with_X[0])
    for i in range(cols):
        single_reel_tuan = []
        for j in range(rows):
            single_reel_tuan.append(tuan_matrix_with_X[j][i])
        mid_tuan_matrix_with_X.append(single_reel_tuan)
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new matrix tuan:" + str(mid_tuan_matrix_with_X))

    # 生成新的随机图案，替换掉需要消除的图案，也就是被标记为'X'的图案
    # 这里需要注意的是，图案是依次向下跌落的。所以对一个REEL的数据进行处理时，要先倒着来
    mid_tuan_matrix_after_upate_X = [] # 保存中间数据，将'X'删掉后重新填充的图案矩阵
    for index, value in enumerate(mid_tuan_matrix_with_X): # 遍历每一个REEL
        reel_X_count = value.count('X')
        reel_tuan = []  # 用来保存填充后的每一个REEL的图案数据
        for i in range(len(value) - 1, -1, -1): # 倒着收集每个REEL上不为'X'的数据
            if 'X' != value[i]:
                reel_tuan.append(value[i])
        pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, old single reel:" + str(reel_tuan))
        if reel_X_count > 0:        # 如果这一列有'X'，即需要填充新的图案
            reel_add_tuan = create_one_reel_tuan(tuan_list, quanzhong_list[index], reel_X_count)
            reel_tuan.extend(reel_add_tuan)
        pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new single reel:" + str(reel_tuan))
        mid_tuan_matrix_after_upate_X.append(reel_tuan)
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new tuan after update X:" + str(mid_tuan_matrix_after_upate_X))

    # 重新转置，得到最终的新图案
    new_tuan = []
    single_row_tuan = []
    for j in range(rows - 1, -1, -1): # 在这里，再把每个REEL的数据倒过来
        single_row_tuan = []
        for i in range(cols):
            single_row_tuan.append(mid_tuan_matrix_after_upate_X[i][j])
        new_tuan.append(single_row_tuan)
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new tuan at last:" + str(new_tuan))
    return new_tuan

########################  以下是单元测试用到的代码 ########################
########################           测试用例1    ########################

# 游戏包括哪些图案
UNIT_TEST_TUAN_LIST = ['9', '10', 'J', 'Q', 'K', 'A', 'W', 'S']
# 每个REEL上各个图案对应的权重，下面的数据是5个REEL的情况
UNIT_TEST_QUANZHONG_LIST_REELS = ((10, 5, 25, 10, 20, 12, 0, 5),
                                  (10, 15, 0, 10, 20, 10, 10, 10),
                                  (10, 25, 25, 10, 0, 12, 10, 20),
                                  (50, 15, 25, 10, 20, 0, 20, 10),
                                  (0, 15, 25, 10, 20, 20, 30, 10))


def UNIT_TEST_create_tuan_matrix(src_tuan_list, src_quanzhong_list, row, col):
    tuan_list = create_tuan_matrix(src_tuan_list, src_quanzhong_list, row, col)
    tuan_count = 0
    pprint("****package:" + PACKAGE_NAME + "  ****funtion:UNIT_TEST_create_all_tuan, new tuan matrix:" + str(tuan_list))
    # 首先测试一下，看有没有非法图案，即所有图案都是图案数组中的
    for tuan in UNIT_TEST_TUAN_LIST:
        for row_tuan in tuan_list:
            tuan_count = tuan_count + row_tuan.count(tuan)
    assert tuan_count == row * col
    # 再测试一下，第1个REEL不能产生Wild字符
    reel1_tuan = [reel[0] for reel in tuan_list]
    wild_num_of_reel1 = reel1_tuan.count('W')
    assert wild_num_of_reel1 == 0
    # 再测试一下，第2个REEL不能产生"J"字符
    reel2_tuan = [reel[1] for reel in tuan_list]
    J_num_of_reel2 = reel2_tuan.count('J')
    assert J_num_of_reel2 == 0
    # 再测试一下，第3个REEL不能产生"J"字符
    reel3_tuan = [reel[2] for reel in tuan_list]
    K_num_of_reel3 = reel3_tuan.count('K')
    assert K_num_of_reel3 == 0
    # 再测试一下，第4个REEL不能产生"A"字符
    reel4_tuan = [reel[3] for reel in tuan_list]
    A_num_of_reel4 = reel4_tuan.count('A')
    assert A_num_of_reel4 == 0
    # 再测试一下，第45个REEL不能产生"9"字符
    reel5_tuan = [reel[4] for reel in tuan_list]
    A_num_of_reel5 = reel5_tuan.count('9')
    assert A_num_of_reel5 == 0

########################           测试用例2    ########################
UNIT_TEST_OLD_ALL_TUAN = [['K', '10', '9', 'J', '10'], ['9', 'W', 'Q', '9', 'K'], ['J', 'A', 'K', 'Q', 'S']]
# 每条支付线对应的矩阵坐标位置
UNIT_TEST_PAYLINES = [[(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],
                     [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
                     [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
                     [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4)],
                     [(2, 0), (2, 1), (1, 2), (2, 3), (2, 4)]]
UNIT_TEST_WIN_RESUT1 = [[['K', 3, 5, 0]], 4]
UNIT_TEST_RESULT_TUAN_AFTER_UP_X_1 = [['X', '10', '9', 'J', '10'], ['9', 'X', 'Q', '9', 'K'], ['J', 'A', 'X', 'Q', 'S']]
UNIT_TEST_WIN_RESUT2 = [[['K', 3, 5, 1], ['J', 4, 10, 3]], 4]
UNIT_TEST_RESULT_TUAN_AFTER_UP_X_2 = [['X', '10', 'X', 'J', '10'], ['9', 'X', 'Q', '9', 'K'], ['X', 'A', 'X', 'X', 'S']]

def UNIT_TEST_update_tuan_matrix_with_X(old_tuan, win_result, pay_lines, result):
    new_tuan = update_tuan_matrix_with_X(old_tuan, win_result, pay_lines)
    for i, row in enumerate(new_tuan):
        for j in range(len(row)):
            assert new_tuan[i][j] == result[i][j]


########################           测试用例3    ########################
UNIT_TEST_OLD_TUAN1 = [['X', '10', '9', 'J', '10'], ['9', 'X', 'Q', '9', 'K'], ['J', 'A', 'X', 'Q', 'S']]
UNIT_TEST_NEW_TUAN1 = [['M', 'M', 'M', 'J', '10'], ['9', '10', '9', '9', 'K'], ['J', 'A', 'Q', 'Q', 'S']]

UNIT_TEST_OLD_TUAN2 = [['9', 'K', 'X', 'J', 'X'], ['Q', 'W', 'S', 'A', 'W'], ['X', 'K', 'X', '9', 'X'], ['K', 'X', '10', 'X', '10']]
UNIT_TEST_NEW_TUAN2 = [['M', 'M', 'M', 'M', 'M'], ['9', 'K', 'M', 'J', 'M'], ['Q', 'W', 'S', 'A', 'W'], ['K', 'K', '10', '9', '10']]
def UNIT_TEST_update_X_with_new_tuan(old_all_tuan_with_X, tuan_list, quanzhong_list, result):
    new_tuan = update_X_with_new_tuan(old_all_tuan_with_X, tuan_list, quanzhong_list)
    for i, row in enumerate(result):
        for j in range(len(row)):
            if result[i][j] != 'M':
                assert new_tuan[i][j] == result[i][j]




if __name__ == '__main__':
    # 跑1000次，确保测试结果ok
    print("****package:" + PACKAGE_NAME + "  ****funtion:main, 测试用例1")
    for i in range(1000):
        UNIT_TEST_create_tuan_matrix(UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, 3, 5)
        UNIT_TEST_create_tuan_matrix(UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, 4, 5)
    print("****package:" + PACKAGE_NAME + "  ****funtion:main, 测试用例2")
    UNIT_TEST_update_tuan_matrix_with_X(UNIT_TEST_OLD_ALL_TUAN, UNIT_TEST_WIN_RESUT1, UNIT_TEST_PAYLINES, UNIT_TEST_RESULT_TUAN_AFTER_UP_X_1)
    UNIT_TEST_update_tuan_matrix_with_X(UNIT_TEST_OLD_ALL_TUAN, UNIT_TEST_WIN_RESUT2, UNIT_TEST_PAYLINES, UNIT_TEST_RESULT_TUAN_AFTER_UP_X_2)
    print("****package:" + PACKAGE_NAME + "  ****funtion:main, 测试用例3")
    UNIT_TEST_update_X_with_new_tuan(UNIT_TEST_OLD_TUAN1, UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, UNIT_TEST_NEW_TUAN1)
    UNIT_TEST_update_X_with_new_tuan(UNIT_TEST_OLD_TUAN2, UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, UNIT_TEST_NEW_TUAN2)
