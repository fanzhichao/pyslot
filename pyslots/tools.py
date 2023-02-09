#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   tools.py
@Time    :   2023/2/7 19:01
@Desc    :   工具类
'''

import pandas
from copy import copy, deepcopy
DEBUG_ON = False
PACKAGE_NAME = 'tools'

def pprint(str):
    if DEBUG_ON:
        print(str)


# 从excel表中读取赔率(pv)和概率(gl)数据，以及每个赔率需要生成的组合总数
def get_pl_from_excel(excel_file_name):
    pl_list = []
    gl_list = []
    pl_need_num_list = []  # 该赔率需要的组合数
    data = pandas.read_excel(excel_file_name, names=None)
    # 依次读取第1、2、5列，注意：excel的内容必须与之对应
    pl_list             = data.values[:, 0].tolist()
    gl_list             = data.values[:, 1].tolist()
    pl_need_num_list    = data.values[:, 4].tolist()
    sum_gl = sum(gl_list)
    # 各个赔率的概率总和应该在0.95-1之间
    if sum_gl > 1 or sum_gl < 0.95:
        pprint("****package:" + PACKAGE_NAME + "  ****funtion:get_pl_from_excel, total peilv is:" + str(sum_gl))
    return pl_list, gl_list, pl_need_num_list


# 创建一个二维数组，用来保存生成的图案矩阵，每个图案的初始值都是'X'
def create_array_by_rowandcol(row,col):
    data = []
    for i in range(row):
        row_data = []
        for j in range(col):
            row_data.append('X') # 默认用'X'图案填充整个图案矩阵
        data.append(row_data)
    return data

# tuan_matrix， 需要被转置的矩阵
# reverse_reel，在翻转矩阵前，是否需要先将每列的图案倒过来
# 在paylines_create_tuan.py的update_X_with_new_tuan方法中，
# 需要将一个REEL先倒过来,再转置
def swap_matrix(tuan_matrix, reverse_reel = False):
    rows = len(tuan_matrix)
    cols = len(tuan_matrix[0])
    if reverse_reel:
        tuan_matrix = [row[::-1] for row in tuan_matrix]
    new_tuan_matrix = []
    for i in range(cols):
        single_row_tuan = []
        for j in range(rows):
            single_row_tuan.append(tuan_matrix[j][i])
        new_tuan_matrix.append(single_row_tuan)
    return new_tuan_matrix

# 这个方法处理的是包含header的tuan_matrix，其中header放在tuan_matrix最后
# 和上面方法的区别是，它会把header中的元素提取出来，放在对应REEL的最后面
def swap_matrix_with_header(tuan_matrix):
    # 一般来讲，Header比下面的matrix要少两列，所以给它的前后都补上一个'X'
    header = ['X']+tuan_matrix[-1]+['X']
    tuan_matrix_without_header = tuan_matrix[:-1:1]
    new_matrix_without_header = swap_matrix(tuan_matrix_without_header, False)
    for reel_index in range(len(new_matrix_without_header)):
        # 为'X'则代表是上面新加的元素，这个不用加到REEL对应的列里面
        if header[reel_index] != 'X':
            new_matrix_without_header[reel_index].append(header[reel_index])
    return new_matrix_without_header

# 将src_list中的值为old的元素替换为replace
def list_replace(src_list, old, replace):
    src_list = [replace if x == old else x for x in src_list]
    return src_list


# 看pl（随机生成的图案矩阵的最终赔率）是否满足需要
# 满足的条件是：它与赔率数组（excel中指定的所有赔率）中指定的某个元素对应的赔率相差不大
# 相差不大的条件是：在其0.8 - 1.2倍左右，具体是由PV_MIN 和 PV_MAX来定的
def pl_is_match(pl, pl_to_match_list, index,pl_min,pl_max):
    if index == 0:
        return False
    elif index == len(pl_to_match_list) - 1:
        if pl < pl_max * pl_to_match_list[-1] and pl > pl_to_match_list[-1]:
            return  True
    else:
        if pl > pl_min * pl_to_match_list[index] and pl < pl_max * pl_to_match_list[index]:
            return  True
    return False

# 将指定组合保存到php文件中
# result为这一局的数据，pl是这一局对应的赔率，pl_index是pl在赔率数组中的index
def save_to_php(php_filename, result, pl_index, pl):
    # 需要后续更新完善
    i = 1
########################  以下是单元测试用到的代码 ########################
########################           测试用例1    ########################
UNIT_TEST_MATRIX = [ ['9','S','K','9','J'],
                     ['J','Q','10','A','S'],
                     ['A','W','A','Q','10']]
UNIT_TEST_MATRIX_SWAP              = [['9','J','A'],
                                     ['S','Q','W'],
                                     ['K','10','A'],
                                     ['9','A','Q'],
                                     ['J','S','10']]
UNIT_TEST_MATRIX_SWAP_REVERSE_REEL = [['J','S','10'],
                                     ['9','A','Q'],
                                     ['K','10','A'],
                                     ['S','Q','W'],
                                     ['9','J','A']]
UNIT_TEST_MATRIX_WITH_HEADER = [ ['9','S','K','9','J'],
                                 ['J','Q','10','A','S'],
                                 ['A','W','A','Q','10'],
                                    ['10','J','Q']]
UNIT_TEST_MATRIX_WITH_HEADER_SWAP = [['9','J','A'],
                                     ['S','Q','W','10'],
                                     ['K','10','A','J'],
                                     ['9','A','Q','Q'],
                                     ['J','S','10']]

def UNIT_TEST_swap_matrix(tuan_matrix, reverse_reel,result):
    new_tuan_matrix = swap_matrix(tuan_matrix, reverse_reel)
    assert new_tuan_matrix == result

def UNIT_TEST_swap_matrix_with_header(tuan_matrix, result):
    new_tuan_matrix = swap_matrix_with_header(tuan_matrix)
    assert new_tuan_matrix == result

if __name__ == '__main__':
    # 测试读取excel
    EXCEL_NAME_READ_PV = r"d:py\\1.xlsx"
    # get_pl_from_excel(EXCEL_NAME_READ_PV)
    UNIT_TEST_swap_matrix(UNIT_TEST_MATRIX, False, UNIT_TEST_MATRIX_SWAP)
    UNIT_TEST_swap_matrix(UNIT_TEST_MATRIX, True, UNIT_TEST_MATRIX_SWAP_REVERSE_REEL)
    UNIT_TEST_swap_matrix_with_header(UNIT_TEST_MATRIX_WITH_HEADER, UNIT_TEST_MATRIX_WITH_HEADER_SWAP)

