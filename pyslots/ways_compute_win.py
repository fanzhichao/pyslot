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
# all_tuan = [['J', 'Q', '9', 'A', 'W', 'S'],
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
def compute_win_for_all_tuan(all_tuan, pl_map, with_header):
    all_tuan_by_reel = []
    for reel_index in range(len(all_tuan[0])):
        rows = len(all_tuan)
        reel_tuan = []
        if with_header:
            rows = len(all_tuan) - 1
        for row in range(rows):
            reel_tuan.append(all_tuan[row][reel_index])
            if with_header:
                if reel_index >=1 and reel_index < len(all_tuan[0]) - 1:
                    reel_tuan.append(all_tuan[rows][reel_index -1])
        all_tuan_by_reel.append(reel_tuan)
    pprint(all_tuan_by_reel)
    result_list = []
    for tuan in all_tuan_by_reel[0]:
        result = [tuan]
        if tuan in [value[0] for value in result_list]:# 已经计算这个图案的中奖情况了
            continue
        # 统计每一个REEL上面出现的连续图案树木
        for reel in all_tuan_by_reel:
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
        result_list.append(result)
    pprint(result_list)
    return result


UNIT_TEST_ALL_TUAN = [ ['J', 'Q', '9', 'A', 'W', 'S'],
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
    compute_win_for_all_tuan(UNIT_TEST_ALL_TUAN, PL_MAP, True)