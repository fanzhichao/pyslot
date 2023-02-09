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
import tools
from tqdm import tqdm
from colored_logs.logger import Logger, LogType

DEBUG_ON = False
PACKAGE_NAME = 'ways_create_tuan'
log = Logger(ID = PACKAGE_NAME)
def pprint(str):
    if DEBUG_ON:
        log.warning(str)

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


# 按照给定的权重随机生成一个图案矩阵，这个仅限于生成每一局的combo1的图案
# 即从0开始，没有任何先决条件，生成一个图案矩阵
def create_tuan_matrix_without_header(tuan_list, quanzhong_list, row, col):
    reel_all_tuan = tools.create_array_by_rowandcol(row, col)
    for index, value1 in enumerate(quanzhong_list):
        reel_tuan = create_one_reel_tuan(tuan_list, value1, row)
        for j, value2 in enumerate(reel_tuan):
            reel_all_tuan[j][index] = value2
    return reel_all_tuan

def create_header(header_tuan_list, header_quanzhong, header_len):
    res = create_one_reel_tuan(header_tuan_list, header_quanzhong, header_len)
    return res
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
                      reel_len):
    reel_index = random.choices(reel_index_list, reel_index_quanzhong_list, k=1)[0]
    block_length = random.choices(block_length_list, block_length_quanzhong_list, k=1)[0]
    block_type = random.choices(block_type_list, block_type_quanzhong_list, k=1)[0]
    tuan = random.choices(tuan_list, tuan_quanzhong_list, k=1)[0]
    if block_length >= reel_len:
        return []
    else:
        block_start_index = random.randrange(0, reel_len - block_length + 1)
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
                      reel_index_list, reel_index_quanzhong_list,
                      block_length_list, block_length_quanzhong_list,
                      block_type_list, block_type_quanzhong_list,
                      tuan_list, tuan_quanzhong_list,
                      reel_len):
    block_num = random.choices(block_num_list, block_num_quanzhong_list, k=1)[0]
    block_num_get = 0
    block_list = []
    while block_num_get < block_num:
        block = create_one_block(reel_index_list, reel_index_quanzhong_list, block_length_list, block_length_quanzhong_list,
                                block_type_list, block_type_quanzhong_list, tuan_list, tuan_quanzhong_list, reel_len)
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
    log.warning("function: create_block_list,  block_list  " + str(block_list))
    return block_list


# 用block_list的图案覆盖掉已经创建好的图案
UNIT_TEST_TUAN_WITHOUT_HEADER = [['9', 'J', '9', '9', 'J', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', 'W', 'Q', '9', '10', 'A'],
                  ['9', 'J', '9', '9', 'J', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', 'W', 'Q', '9', '10', 'A']]
UNIT_TEST_TUAN_WITH_HEADER = [['9', 'J', '9', '9', 'J', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', 'W', 'Q', '9', '10', 'A'],
                  ['9', 'J', '9', '9', 'J', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', '10', 'K', 'A', 'S', 'A'],
                  ['Q', 'W', 'Q', '9', '10', 'A'],
                       ['9', '10', '9', '10']]
UNIT_TEST_BLOCK_LIST = [[0, 4, 5, 1, 'J'], [5, 2, 4, 1, 'Q']]

# 更新不带header的普通matrix图案
def updata_tuan_with_block_list(tuan, block_list):
    for block in block_list:
        for j in range(block[1], block[2] + 1):
            tuan[j][block[0]] = block[4]
    return tuan

#  更新转置过后的matrix图案，此时是带header的
#  因为有可能block升级以后会消失（拆开成为单个Wild图案）
#  所以这里还需要返回一个新的new_block_list
def updata_swap_tuan_with_block_list(tuan, block_list):
    new_block_list = []
    for block in block_list:
        block_need_to_save = True
        for j in range(block[1], block[2] + 1):
            if block[-2] > 2:  # 如果框已经升到第3级了，那么所有图案变成wild
                tuan[block[0]][j] = 'W'
                block_need_to_save = False
            else:
                tuan[block[0]][j] = block[4]
        if block_need_to_save:
            new_block_list.append(block)
    pprint("updata_swap_tuan_with_block_list, new_tuan  " + str(tuan))
    pprint("updata_swap_tuan_with_block_list, new_block_list  " + str(new_block_list))
    return [tuan, new_block_list]


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
# win_result:[['J', 1, 0], ['9', 1, 2, 3, 1, 3, 3, 540], ['Q', 2, 1, 2, 0], ['K', 1, 3, 1, 1, 2, 180], ['10', 1, 0], ['A', 1, 0]]
def update_tuan_matrix_with_X(tuan_matrix, block_list, win_result_list):
    pprint("****package:" + PACKAGE_NAME + "  ****funtion:update_tuan_matrix_with_X, old tuan matrix:" + str(tuan_matrix))
    # 以下处理的都是带header的图案
    # 先将图案去掉header后转置，再加上header，变成按REEL(列)组织的数据
    # 然后将其中中奖的图案用‘X’替换掉
    header = tuan_matrix[-1]
    tuan_matrix_without_header = tuan_matrix[:-1:1]
    swap_matrix_with_header = tools.swap_matrix_with_header(tuan_matrix)
    for win_result in win_result_list:
        if win_result[-1] > 0: # 只处理中奖图案
            zhongjiang_tuan = win_result[0]
            reel_end_index = len(win_result) -2
            # 将中奖的所有图案替换为'X'
            for i in range(0, reel_end_index):
                swap_matrix_with_header[i] = tools.list_replace(swap_matrix_with_header[i], zhongjiang_tuan, 'X')
                swap_matrix_with_header[i] = tools.list_replace(swap_matrix_with_header[i], 'W', 'X')
    pprint("update_tuan_matrix_with_X, new matrix:"+ str(swap_matrix_with_header))
    header_with_X = [swap_matrix_with_header[i][-1] for i in range(1, len(swap_matrix_with_header) - 1)]
    pprint("update_tuan_matrix_with_X, header_with_X:" + str(header_with_X))
    # 接下来，对block_list及图案进行处理。
    # 如果该block不在中奖路径上，则不管它，否则，对其按游戏规则进行升级处理
    swap_matrix_after_update_X = []
    new_block_list = []
    for win_result in win_result_list:
        if win_result[-1] > 0: # 只处理中奖图案
            zhongjiang_tuan = win_result[0]
            reel_end_index = len(win_result) - 2
            for block in block_list:
                if block[-1] == zhongjiang_tuan and  block[0] < reel_end_index:
                    # 对位于中奖区域的block进行升级处理
                    block[-2] = block[-2] + 1
            # 将之前可能被替换为'X'的图案再替换回来
            [swap_matrix_after_update_X, new_block_list] = updata_swap_tuan_with_block_list(swap_matrix_with_header, block_list)
    swap_matrix_after_update_X_without_header = []
    for value in swap_matrix_after_update_X:
        if len(value) > len(swap_matrix_after_update_X[0]):
            swap_matrix_after_update_X_without_header.append(value[:-1:1])
        else:
            swap_matrix_after_update_X_without_header.append(value)
    return [swap_matrix_after_update_X_without_header, header_with_X, new_block_list]


# 这个是生成combo2/combo3.../comboN的第2步（连续消除后的新图案矩阵），具体分为3步:
# 1. 将标记为'X'的图案先删掉
# 2. 然后'X'的图案上面的图案往下面掉落
# 3. 接着生成新的图案，继续填补'X'图案被消除后留下的空间
# 注意: 和paylines_create_tuan.py不同的是，这个方法的第一个输入参数是转置后的矩阵
# 另外，header需要单独处理，所以第1个参数是不包含header的
def update_X_with_new_tuan(tuan_swap_matrix_with_X, tuan_list, quanzhong_list, header, header_quanzhong_list):
    pprint("update_X_with_new_tuan, tuan_swap_matrix_with_X:" + str(tuan_swap_matrix_with_X))
    # 生成新的随机图案，替换掉需要消除的图案，也就是被标记为'X'的图案
    # 这里需要注意的是，图案是依次向下跌落的。所以对一个REEL的数据进行处理时，要先倒着来
    mid_tuan_matrix_after_upate_X = [] # 保存中间数据，将'X'删掉后重新填充的图案矩阵
    for index, value in enumerate(tuan_swap_matrix_with_X): # 遍历每一个REEL
        reel_X_count = value.count('X')
        # 倒着收集每个REEL上不为'X'的数据, 最终会变成填充后的每一个REEL的图案数据
        reel_tuan = [v for v in reversed(value) if 'X' != v]
        pprint("update_X_with_new_tuan, old single reel:" + str(reel_tuan))
        if reel_X_count > 0:        # 如果这一列有'X'，即需要填充新的图案
            reel_add_tuan = create_one_reel_tuan(tuan_list, quanzhong_list[index], reel_X_count)
            reel_tuan.extend(reel_add_tuan)
        pprint("update_X_with_new_tuan, new single reel:" + str(reel_tuan))
        mid_tuan_matrix_after_upate_X.append(reel_tuan)
    pprint("update_X_with_new_tuan, new tuan after update X:" + str(mid_tuan_matrix_after_upate_X))

    # 将矩阵重新转置一下，同时在转置前先将每个REEL上的数据倒过来
    new_tuan = tools.swap_matrix(mid_tuan_matrix_after_upate_X, True)
    pprint("update_X_with_new_tuan, new tuan at last:" + str(new_tuan))

    # 接下来用同样的方式处理header
    reel_X_count = header.count('X')
    pprint("update_X_with_new_tuan, header:" + str(header))
    # 倒着收集每个REEL上不为'X'的数据, 最终会变成填充后的每一个REEL的图案数据
    new_header = [v for v in header if 'X' != v]
    if reel_X_count > 0:  # 如果这一列有'X'，即需要填充新的图案
        reel_add_tuan = create_one_reel_tuan(tuan_list, header_quanzhong_list, reel_X_count)
        new_header.extend(reel_add_tuan)
    pprint("update_X_with_new_tuan, new_header:" + str(new_header))
    return [new_tuan, new_header]







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

def UNIT_TEST_create_tuan_matrix_without_header(src_tuan_list, src_quanzhong_list, row, col):
    tuan_list = create_tuan_matrix_without_header(src_tuan_list, src_quanzhong_list, row, col)
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
UNIT_TEST_REEL_LENGTH = 7
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

########################           测试用例3    ########################
UNIT_TEST_WIN_RESULT_LIST = [['J', 1, 0], ['9', 1, 2, 3, 1, 3, 3, 540], ['Q', 2, 1, 2, 0], ['K', 1, 3, 1, 1, 2, 180], ['10', 1, 0], ['A', 1, 0]]

if __name__ == '__main__':
    # 跑1000次，确保测试结果ok
    pprint("main, 测试用例1")
    for i in range(1000):
        UNIT_TEST_create_tuan_matrix_without_header(UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, 3, 5)
        UNIT_TEST_create_tuan_matrix_without_header(UNIT_TEST_TUAN_LIST, UNIT_TEST_QUANZHONG_LIST_REELS, 4, 5)
    # UNIT_TEST_create_one_block( UNIT_TEST_REEL_INDEX_LIST, UNIT_TEST_REEL_INDEX_QUANZHONG_LIST,
    #                             UNIT_TEST_BLOCK_LENGTH_LIST, UNIT_TEST_BLOCK_LENGTH_QUANZHONG_LIST,
    #                             UNIT_TEST_BLOCK_TYPE_LIST, UNIT_TEST_BLOCK_TYPE_QUANZHONG_LIST,
    #                             UNIT_TEST_TUAN_LIST, UNIT_TEST_TUAN_QUANZHONG_LIST, UNIT_TEST_ROW_LENGTH)

    create_block_list(UNIT_TEST_BLOCK_NUM_LIST, UNIT_TEST_BLOCK_NUM_QUANZHONG_LIST,
                      UNIT_TEST_REEL_INDEX_LIST, UNIT_TEST_REEL_INDEX_QUANZHONG_LIST,
                      UNIT_TEST_BLOCK_LENGTH_LIST, UNIT_TEST_BLOCK_LENGTH_QUANZHONG_LIST,
                      UNIT_TEST_BLOCK_TYPE_LIST, UNIT_TEST_BLOCK_TYPE_QUANZHONG_LIST,
                      UNIT_TEST_TUAN_LIST, UNIT_TEST_TUAN_QUANZHONG_LIST, UNIT_TEST_REEL_LENGTH)
    updata_tuan_with_block_list(UNIT_TEST_TUAN_WITHOUT_HEADER, UNIT_TEST_BLOCK_LIST)

    update_tuan_matrix_with_X(UNIT_TEST_TUAN_WITH_HEADER, UNIT_TEST_BLOCK_LIST, UNIT_TEST_WIN_RESULT_LIST)