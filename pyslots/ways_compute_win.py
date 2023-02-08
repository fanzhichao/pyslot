#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   ways_compute_win.py
@Time    :   2023/2/7 16:42
@Desc    :   专门用来计算ways游戏中，每局图案的中奖情况。
'''
import pandas
import tools
DEBUG_ON = True
PACKAGE_NAME = 'ways_compute_win'

def pprint(str):
    if DEBUG_ON:
        print(str)

# 以下数据只是为了说明数据格式，举例用的
# pl_map = {
#     '9' :[0, 0, 0, 2, 5,10],
#     '10':[0, 0, 0, 5, 10,20],
#     'J' :[0, 0, 2, 10, 15,25],
#     'Q' :[0, 0, 0, 15, 20,30],
#     'K' :[0, 0, 5, 20, 30,40],
#     'A': [0, 0, 10, 25, 40,60],
#     'W': [0, 0, 15, 30, 50,80],
#     'S': [0, 0, 0, 2, 5,10],
# }
# with_header 为True，表示上面还有一行，否则就没有。
# tuan_matrix =
#            [['J', 'Q', '9', 'A', 'W', 'S'],
#             ['9', 'K', 'W', 'J', 'Q', '9'],
#             ['Q', 'M', 'S', 'A', 'W', 'Q'],
#             ['K', 'K', '10', '9', '10', 'J'],
#             ['Q', 'K', 'S', '10', 'Q', '9'],
#             ['10', '9', '9', 'K', 'Q', '9'],
#             ['A', 'S', 'Q', 'J', '9', 'Q'],
#                  ['9', 'S', 'J', 'J']]
#   上面的 ['9', 'S', 'J', 'J']就是有header的情况
#  输出的结果：[['J', 1, 0], ['9', 1, 8, 3, 1, 3, 3, 2160], ['Q', 2, 1, 2, 0], ['K', 1, 3, 1, 1, 2, 180], ['10', 1, 0], ['A', 1, 0]]
#  ['9', 1, 8, 3, 1, 3, 3, 2160]表示'9'在每个REEL依次出现了1,8,3,1,3,3次，总中奖金额为720
def compute_win_for_tuan_matrix(tuan_matrix, pl_map, with_header):
    # 先得到转置，并且添加header后的图案
    tuan_matrix_swap_add_header = []
    if with_header:
        tuan_matrix_swap_add_header = tools.swap_matrix_with_header(tuan_matrix)
    else:
        tuan_matrix_swap_add_header = tools.swap_matrix(tuan_matrix,False)

    # 统计中奖情况，中奖图案必定出现在第一列
    result_list = []
    total_odd = 0
    for tuan in tuan_matrix_swap_add_header[0]:
        result = [tuan]
        # 只有这个图案没有统计过，才需要统计
        print("result_list  "+str(result_list))
        print("tuan " + str(tuan))
        if tuan not in [value[0] for value in result_list]:
            print("yes..........")
            # 统计每一个REEL上面出现的连续图案数量
            for reel in tuan_matrix_swap_add_header:
                count = reel.count(tuan) + reel.count('W')
                if count > 0:
                    result.append(count)
                else:
                    break
            # 计算奖金
            continue_count = len(result) - 1
            jiangjing = pl_map[tuan][continue_count - 1]
            for i in range(1, len(result)):
                jiangjing = jiangjing * result[i]
            result.append(jiangjing)
            total_odd = total_odd + jiangjing
            # 只有该图案中奖了，才需要记录到中奖结果中
            if jiangjing > 0:
                result_list.append(result)
    result_list.append(total_odd)
    pprint(result_list)
    return result_list


UNIT_TEST_TUAN_MATRIX = [ ['J', 'Q', '9', 'A', 'W', 'S'],
                       ['9', 'K', 'W', 'J', 'Q', '9'],
                       ['Q', 'M', 'S', 'A', 'W', 'Q'],
                       ['K', 'K', '10', '9', '10', 'J'],
                       ['Q', 'K', 'S', '10', 'Q', '9'],
                       ['10', '9', '9', 'K', 'Q', '9'],
                       ['A', 'S', 'Q', 'J', '9', 'Q'],
                            ['9', 'S', 'J', 'J']
                       ]
PL_MAP = {
            '9' :[0, 0, 0, 2, 5,10],
            '10':[0, 0, 0, 5, 10,20],
            'J' :[0, 0, 2, 10, 15,30],
            'Q' :[0, 0, 0, 15, 20,35],
            'K' :[0, 0, 5, 20, 30,50],
            'A': [0, 0, 10, 25, 40,60],
            'W': [0, 0, 15, 30, 50,80],
            'S': [0, 0, 0, 2, 5,10]}
if __name__ == '__main__':
    compute_win_for_tuan_matrix(UNIT_TEST_TUAN_MATRIX, PL_MAP, True)