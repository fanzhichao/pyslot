#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   6001.py
@Time    :   2023/2/8 15:27
@Desc    :   这是一个标准的ways 游戏的例子
'''
import time
from tqdm import tqdm
import ways_compute_win as compute_win
import ways_create_tuan as create_tuan
import tools
DEBUG_ON = True
PACKAGE_NAME = 'game5001'
PV_MIN = 0.8
PV_MAX = 1.2
# just for test

def pprint(str):
    if DEBUG_ON:
        print(str)
##############  保存赔率概率表的excel ####################
GAME5001_EXCEL = r"d:py\\game5001.xlsx"

#################  供生成图案用  ########################
# 所有的图案
TUAN_LIST = ['9', '10', 'J', 'Q', 'K', 'A', 'W', 'S']
# 每个REEL上面的图案出现的权重，其元素个数必须和REEL_NUM相等
TUAN_QUANZHONG_LIST = ((0, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0),
                        (50, 5, 25, 10, 20, 0, 0, 0),
                        (50, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0))
# header区域的权重
HEADER_QUANZHONG = (0, 5, 25, 10, 20, 0, 0, 0)

#################  供计算中奖情况用  ########################
# 图案的赔率表
TUAN_PL_MAP = {
    '9' : [0, 0, 0, 2, 5, 10],
    '10': [0, 0, 0, 5, 10, 20],
    'J' : [0, 0, 0, 10, 15, 25],
    'Q' : [0, 0, 0, 15, 20, 30],
    'K' : [0, 0, 5, 20, 30, 40],
    'A' : [0, 0, 10, 25, 40, 50],
    'W' : [0, 0, 15, 30, 50,60],
    'S' : [0, 0, 0, 2, 5, 10],
}
BLOCK_TUAN_QUANZHONG = (0, 5, 25, 10, 20, 0, 0, 0)
REEL_INDEX_LIST =  [0,1,2,3,4,5]
REEL_INDEX_QUANZHONG_LIST = [1,2,2,5,10,10]
BLOCK_LENGTH_LIST = [2,3,4]
BLOCK_LENGTH_QUANZHONG_LIST = [10,5,2]
BLOCK_TYPE_LIST =  [0,1,2]
BLOCK_TYPE_QUANZHONG_LIST = [10,5,2]
BLOCK_NUM_LIST = [0, 1, 2, 3, 4]
BLOCK_NUM_QUANZHONG_LIST = [1, 1, 2, 2, 1]
REEL_LENGTH = 7  # 去掉header的matrix的高度，rows
REEL_NUM = 6     # 去掉header的matrix的宽度，cols


def pl_is_match(pl, pl_to_match_list, index):
    if index == 0:
        return False
    elif index == len(pl_to_match_list) - 1:
        if pl < PV_MAX * pl_to_match_list[-1] and pl > pl_to_match_list[-1]:
            return  True
    else:
        if pl > PV_MIN * pl_to_match_list[index] and pl < PV_MAX * pl_to_match_list[index]:
            return  True
    return False


if __name__ == '__main__':
    pl_list, gl_list, pl_need_num_list = tools.get_pl_from_excel(GAME5001_EXCEL)
    num = sum(pl_need_num_list) # 需要生成的组合总数
    pl_get_num_list = [0] * len(pl_need_num_list)  # 保存一下每个赔率得到了多少个组合
    pprint("总共需要 "+str(num) + "组组合")
    progress_bar = tqdm(total = num)
    for i in range(10):
        total_win = 0
        all_tuan = create_tuan.create_tuan_matrix_without_header(TUAN_LIST, TUAN_QUANZHONG_LIST, REEL_LENGTH, REEL_NUM)
        block_list = create_tuan.create_block_list(BLOCK_NUM_LIST, BLOCK_NUM_QUANZHONG_LIST,
                                                    REEL_INDEX_LIST, REEL_INDEX_QUANZHONG_LIST,
                                                    BLOCK_LENGTH_LIST, BLOCK_LENGTH_QUANZHONG_LIST,
                                                    BLOCK_TYPE_LIST, BLOCK_TYPE_QUANZHONG_LIST,
                                                    TUAN_LIST, BLOCK_TUAN_QUANZHONG, REEL_LENGTH)
        all_tuan = create_tuan.updata_tuan_with_block_list(all_tuan, block_list)
        header = create_tuan.create_header(TUAN_LIST, HEADER_QUANZHONG, REEL_LENGTH - 2)
        all_tuan.append(header)
        win_res = compute_win.compute_win_for_tuan_matrix(all_tuan, TUAN_PL_MAP, True)

        pprint("****package:"+PACKAGE_NAME + "  ****funtion main:"+ str(win_res))

        result = []
        single_combo_result = []
        # check是否中奖，如果中奖了要继续生成和计算后面的combo图案
        while(win_res[-1] > 0):
            total_win = total_win + win_res[-1]
            single_combo_result = [win_res, all_tuan]
            result.append(single_combo_result)
            # 重新生成新的combo的图案
            [old_all_tuan_with_X, new_block_list] = create_tuan.update_tuan_matrix_with_X(all_tuan, block_list, win_res[:-1:1])
            [all_tuan, new_header] = create_tuan.update_X_with_new_tuan(old_all_tuan_with_X, TUAN_LIST, TUAN_QUANZHONG_LIST, TUAN_LIST, HEADER_QUANZHONG)
            all_tuan = create_tuan.updata_tuan_with_block_list(all_tuan, new_block_list)
            all_tuan.append(new_header)
            win_res = compute_win.compute_win_for_tuan_matrix(all_tuan, TUAN_PL_MAP, True)
            #pprint("****package:" + PACKAGE_NAME + "  ****funtion main: win_res " + str(win_res))
        # 记录最后一个不中奖的combo的数据
        single_combo_result = [win_res, all_tuan]
        result.append(single_combo_result)
        combo_num = "combo "+str(len(result))
        result = [combo_num] + [total_win] + result
        pprint("****package:"+PACKAGE_NAME + "  ****funtion main: the "+ str(i) + str(result))

        # 如果这一局中奖了，要看这局的中奖结果要加到哪里
        if total_win > 0 :
            for i, value in enumerate(pl_list):
                if pl_is_match(total_win, pl_list,i):
                    # 只有某个赔率没有满的时候，才需要添加
                    if pl_get_num_list[i] < pl_need_num_list[i]:
                        pl_get_num_list[i] = pl_get_num_list[i] + 1
                        print(" 第 "+str(i)+"  有了 "+str(pl_get_num_list[i]))
                        progress_bar.update(1)  # 进度条加1
        else:
            pl_get_num_list[0] = pl_get_num_list[0] + 1
            progress_bar.update(1)  # 进度条加1

        # 如果已经生成了所有需要的组合，则退出程序
        if sum(pl_get_num_list) >= num:
            break

