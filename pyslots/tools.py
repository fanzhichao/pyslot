#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   tools.py
@Time    :   2023/2/7 19:01
@Desc    :
'''

import pandas

DEBUG_ON = False
PACKAGE_NAME = 'tools'

def pprint(str):
    if DEBUG_ON:
        print(str)


# read pl and gl from excel
def get_pl_from_excel(excel_file_name):
    pl_list = []
    gl_list = []
    pl_need_num_list = []  # 该赔率需要的组合数
    data = pandas.read_excel(excel_file_name, names=None)
    pl_list = data.values[:, 0].tolist()
    gl_list = data.values[:, 1].tolist()
    pl_need_num_list = data.values[:, 4].tolist()
    sum_gl = sum(gl_list)
    if sum_gl > 1 or sum_gl < 0.5:
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
# 在paylines_create_tuan的update_X_with_new_tuan方法中，
# 需要将一个REEL先倒过来,再转置
def swap_matrix(tuan_matrix, reverse_reel = False):
    print(tuan_matrix)
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

def swap_matrix_with_header(tuan_matrix):
    # 前后两列补齐，一般来讲，Header比下面的matrix要少两列
    header = ['X']+tuan_matrix[-1]+['X']
    tuan_matrix_without_header = tuan_matrix[:-1:1]
    new_matrix_without_header = swap_matrix(tuan_matrix_without_header, False)
    for reel_index in range(len(new_matrix_without_header)):
        if header[reel_index] != 'X': # 比较粗暴的判断方式，但是简单易懂
            new_matrix_without_header[reel_index].append(header[reel_index])
    return new_matrix_without_header

def list_replace(src_list, old, replace):
    src_list = [replace if x == old else x for x in src_list]
    return src_list

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
def UNIT_TEST_swap_matrix(tuan_matrix, reverse_reel,result):
    new_tuan_matrix = swap_matrix(tuan_matrix, reverse_reel)
    assert new_tuan_matrix == result
if __name__ == '__main__':
    # 测试读取excel
    EXCEL_NAME_READ_PV = r"d:py\\1.xlsx"
    # get_pl_from_excel(EXCEL_NAME_READ_PV)
    UNIT_TEST_swap_matrix(UNIT_TEST_MATRIX, False, UNIT_TEST_MATRIX_SWAP)
    UNIT_TEST_swap_matrix(UNIT_TEST_MATRIX, True, UNIT_TEST_MATRIX_SWAP_REVERSE_REEL)
    swap_matrix_with_header(UNIT_TEST_MATRIX)
