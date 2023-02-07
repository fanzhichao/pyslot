#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   ways_create_tuan.py
@Time    :   2023/2/7 11:10
@Desc    :   专门用来生成ways game的每一局的图案，包括combo1/combo2等所有的combo
'''

import random
import pytest
from tqdm import tqdm

DEBUG_ON = False
PACKAGE_NAME = 'ways_create_tuan'

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
#  最终的输出结果类似: ['10', 'J',  'J'] 对应一个REEL上的图案。
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


# 连续块的数据格式如下：
# [reel_index, block_begin_index, block_end_index, block_type, block_tuan]
#[2, 2, 3, 1, 'K'] 第3个REEL中，从上到下第[3,4,5]三个位置的'K'是一个连续块，其类型为1,也就是银框
#[0, 1, 2, 0, 'Q'] 第1个REEL中，从上到下第[2,3]两个位置的'Q'是一个连续块，其类型为1,也就是木头框
#[1, 2, 3, 2, 'Q'] 第2个REEL中，从上到下第[3,4]两个位置的'Q'是一个连续块，其类型为2,也就是金框
# 下面的方法用来创建1个Block
# reel_index_list [0,1,2,3,4,5] 表示第几个REEL
# reel_index_quanzhong_list [1,2,2,5,10,10] 对应上面的数组，表示第几个REEL的权重为
# block_length_list  [2,3,4] 表示block的长度
# block_length_quanzhong_list  [10,5,2] 对应上面的数组，表示对应的block长度的权重为
# block_type_list  [0,1,2] 表示block的种类
# block_type_quanzhong_list  [10,5,2] 对应上面的数组，表示对应的block种类的权重为
def create_one_block(reel_index_list, reel_index_quanzhong_list, block_length_list, block_length_quanzhong_list,
                      block_type_list, block_type_quanzhong_list, tuan_list, tuan_quanzhong_list,
                      row_len):
    reel_index = random.choices(reel_index_list, reel_index_quanzhong_list, k=1)[0]
    block_length = random.choices(block_length_list, block_length_quanzhong_list, k=1)[0]
    block_type = random.choices(block_type_list, block_type_quanzhong_list, k=1)[0]
    tuan = random.choices(tuan_list, tuan_quanzhong_list, k=1)[0]
    if block_length >= row_len:
        return []
    else:
        block_start_index = random.randrange(0, row_len - block_length + 1)
        res = [reel_index, block_start_index, block_start_index + block_length - 1, block_type, tuan]
        return res

# 判断两个block之间是否存在冲突
# block 格式 [5, 1, 2, 1, 'S']  [reel_index, block_begin_index, block_end_index, block_type, block_tuan]
def is_two_block_conflict(block1, block2):
    if block1[0] != block2[0]:
        return False
    elif block1[1] > block2[2] or  block2[1] > block1[2]:
        return False
    return True


# 随机创建一个block列表，里面的block不会冲突
def create_block_list(block_num_list, block_num_quanzhong_list,
                      reel_index_list, reel_index_quanzhong_list, block_length_list, block_length_quanzhong_list,
                      block_type_list, block_type_quanzhong_list, tuan_list, tuan_quanzhong_list,
                      row_len):
    block_num = random.choices(block_num_list, block_num_quanzhong_list, k=1)[0]
    block_num_get = 0
    block_list = []
    while block_num_get < block_num:
        block = create_one_block(reel_index_list, reel_index_quanzhong_list, block_length_list, block_length_quanzhong_list,
                                block_type_list, block_type_quanzhong_list, tuan_list, tuan_quanzhong_list, row_len)
        if len(block_list) == 0:
            block_list.append(block)
            block_num_get = block_num_get + 1
        else:
            conflict_num = 0
            for b in block_list:
                if is_two_block_conflict(b, block):
                    conflict_num = conflict_num + 1
                    break;
            if conflict_num == 0:
                block_list.append(block)
                block_num_get = block_num_get + 1
    print(block_list)


# 用block_list的图案覆盖掉已经创建好的图案
UNIT_TEST_TUAN = [['9', 'J', '9', '9', 'J', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', 'W', 'Q', '9', '10', 'A'],
                  ['9', 'J', '9', '9', 'J', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', 'W', 'Q', '9', '10', 'A']]
UNIT_TEST_BLOCK_LIST = [[0, 4, 5, 1, 'J'], [5, 2, 4, 1, 'Q']]
def updata_tuan_with_block_list(tuan, block_list):
    print(tuan)
    reel_num = len(tuan[0]) # 先获取有多少个REEL
    for block in block_list:
        for j in range(block[1], block[2] + 1):
            tuan[j][block[0]] = block[4]
    print(tuan)
    return tuan


# 根据当前的图案矩阵、中奖结果，把中奖的图案替换为'X'，以便后续处理
# 这个是生成combo2/combo3.../comboN的第1步（连续消除后的新图案矩阵）

# tuan_matrix = [['J', 'Q', '9', 'A', 'W', 'S'],
#                ['9', 'K', 'W', 'J', 'Q', '9'],
#                ['Q', 'M', 'S', 'A', 'W', 'Q'],
#                ['K', 'K', '10', '9', '10', 'J'],
#                ['Q', 'K', 'S', '10', 'Q', '9'],
#                ['10', '9', '9', 'K', 'Q', '9'],
#                ['A', 'S', 'Q', 'J', '9', 'Q'],
#                     ['9', 'S', 'J', 'J']]
# block_list = [[0, 4, 5, 1, 'J'], [5, 2, 4, 1, 'Q']]
# 单个block 格式 [5, 1, 2, 1, 'S']  [reel_index, block_begin_index, block_end_index, block_type, block_tuan]
# win_result:[['J', 1, 0], ['9', 1, 8, 3, 1, 3, 3, 2160], ['Q', 2, 1, 2, 0], ['K', 1, 3, 1, 1, 2, 180], ['10', 1, 0], ['A', 1, 0]]
def update_tuan_matrix_with_X(tuan_matrix, block_list, win_result):
    pprint("****package:" + PACKAGE_NAME + "  ****funtion:update_tuan_matrix_with_X, old tuan matrix:" + str(tuan_matrix))


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
UNIT_TEST_TUAN_QUANZHONG_LIST = [10, 5, 25, 10, 20, 12, 0, 5]
UNIT_TEST_REEL_INDEX_LIST =  [0,1,2,3,4,5]
UNIT_TEST_REEL_INDEX_QUANZHONG_LIST = [1,2,2,5,10,10]
UNIT_TEST_BLOCK_LENGTH_LIST = [2,3,4]
UNIT_TEST_BLOCK_LENGTH_QUANZHONG_LIST = [10,5,2]
UNIT_TEST_BLOCK_TYPE_LIST =  [0,1,2]
UNIT_TEST_BLOCK_TYPE_QUANZHONG_LIST = [10,5,2]
UNIT_TEST_BLOCK_NUM_LIST = [0, 1, 2, 3, 4]
UNIT_TEST_BLOCK_NUM_QUANZHONG_LIST = [1, 1, 2, 2, 1]
UNIT_TEST_ROW_LENGTH = 7
def UNIT_TEST_create_one_block(reel_index_list, reel_index_quanzhong_list,
                                block_length_list, block_length_quanzhong_list,
                                block_type_list, block_type_quanzhong_list,
                                tuan_list, tuan_quanzhong_list,row_len):
    for i in range(100):
        res = create_one_block(reel_index_list, reel_index_quanzhong_list,
                            block_length_list, block_length_quanzhong_list,
                            block_type_list, block_type_quanzhong_list,
                            tuan_list, tuan_quanzhong_list, row_len)
        print(res)

if __name__ == '__main__':
    # 跑1000次，确保测试结果ok
    print("****package:" + PACKAGE_NAME + "  ****funtion:main, 测试用例1")
    for i in range(1000):
        UNIT_TEST_create_tuan_matrix(UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, 3, 5)
        UNIT_TEST_create_tuan_matrix(UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, 4, 5)
    print("ok")
    # UNIT_TEST_create_one_block( UNIT_TEST_REEL_INDEX_LIST, UNIT_TEST_REEL_INDEX_QUANZHONG_LIST,
    #                             UNIT_TEST_BLOCK_LENGTH_LIST, UNIT_TEST_BLOCK_LENGTH_QUANZHONG_LIST,
    #                             UNIT_TEST_BLOCK_TYPE_LIST, UNIT_TEST_BLOCK_TYPE_QUANZHONG_LIST,
    #                             UNIT_TEST_TUAN_LIST, UNIT_TEST_TUAN_QUANZHONG_LIST, UNIT_TEST_ROW_LENGTH)

    create_block_list(UNIT_TEST_BLOCK_NUM_LIST, UNIT_TEST_BLOCK_NUM_QUANZHONG_LIST,
                      UNIT_TEST_REEL_INDEX_LIST, UNIT_TEST_REEL_INDEX_QUANZHONG_LIST,
                      UNIT_TEST_BLOCK_LENGTH_LIST, UNIT_TEST_BLOCK_LENGTH_QUANZHONG_LIST,
                      UNIT_TEST_BLOCK_TYPE_LIST, UNIT_TEST_BLOCK_TYPE_QUANZHONG_LIST,
                      UNIT_TEST_TUAN_LIST, UNIT_TEST_TUAN_QUANZHONG_LIST, UNIT_TEST_ROW_LENGTH)
    updata_tuan_with_block_list(UNIT_TEST_TUAN, UNIT_TEST_BLOCK_LIST)