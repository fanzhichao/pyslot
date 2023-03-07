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
from copy import copy, deepcopy
from colored_logs.logger import Logger, LogType

DEBUG_ON = True
PACKAGE_NAME = 'game6001'

def pprint(str):
    if DEBUG_ON:
        print(str)
##############  保存赔率概率表的excel ####################
GAME6001_EXCEL = r"C:\\u\\doc\\game5001.xlsx"

#################  供生成图案用  ########################
# 【必改】 定义去掉header后图案的行数和列数
REEL_LENGTH = 5  # 去掉header的matrix的高度，rows 行数
REEL_NUM = 6     # 去掉header的matrix的宽度，cols 列数

# 【可改】 随机生成的图案矩阵的最终赔率是否满足需要
# 满足的条件是：它与赔率数组（excel中指定的所有赔率）中指定的某个元素对应的赔率相差不大
# 相差不大的条件是：在其0.8 - 1.2倍左右，具体是由PV_MIN 和 PV_MAX来定的
PV_MIN = 0.8
PV_MAX = 1.2

# 【必改】所有的图案，不同的游戏这里肯定不同，这个列表是第1个要修改的
TUAN_LIST = ['9', '10', 'J', 'Q', 'K', 'A', 'B', 'C', 'W', 'S']
# 每个REEL上面的图案出现的权重，其元素个数必须和REEL_NUM相等
# 【必改】TUAN_LIST修改后，要增加或减少对应图案的权重，即cols要跟着变
# 【必改】REEL_NUM修改后，要增加或减少对应REEL的权重列表，即rows要跟着变
TUAN_QUANZHONG_LIST = ( (20, 10, 15, 10, 8, 16,  18, 12, 0, 0),
                        (10, 20, 15, 15, 12, 10, 8,  5, 5, 3),
                        (8, 8, 20, 15, 12, 10, 12,  10, 5, 10),
                        (10, 15, 15, 15, 12, 12, 15, 12, 5, 10),
                        (20, 20, 15, 15, 12, 10, 12, 10, 5, 20),
                        (20, 20, 15, 15, 12, 10, 12, 10, 8, 10))
#  header区域的权重
# 【必改】TUAN_LIST修改后，要增加或减少对应图案的权重，即cols要跟着变
HEADER_QUANZHONG = (8, 15, 20, 15, 8, 6,  8, 6, 0, 0)

#################  供计算中奖情况用  ########################
# 图案的赔率表
# 【必改】TUAN_LIST修改后，要增加或减少对应图案的赔率字典
#  注意:下面每个value对应的数组长度要和上面定义的REEL_NUM一样
TUAN_PL_MAP = {
    '9' : [0, 0, 0, 2, 5, 10],
    '10': [0, 0, 0, 5, 10, 20],
    'J' : [0, 0, 0, 10, 15, 25],
    'Q' : [0, 0, 0, 15, 20, 30],
    'K' : [0, 0, 0, 20, 30, 40],
    'A' : [0, 0, 0, 25, 40, 50],
    'B' : [0, 0, 0, 20, 30, 40],
    'C' : [0, 0, 0, 25, 40, 50],
    'W' : [0, 0, 0, 0, 0, 0],
    'S' : [0, 0, 0, 0, 0, 0],
}

# 以下定义都是针对block的，即游戏中出现的长条连续图案（一般包含2-4个图案）
# 【必改】TUAN_LIST修改后，要增加或减少对应图案的权重，即cols要跟着变
# block 不能为'W' 或者 'S'
BLOCK_TUAN_QUANZHONG = (15, 20, 12, 10, 8, 6, 8, 6, 0, 0)
# 【可改】下面分别定义了block出现在第几个REEL上，及其权重
REEL_INDEX_LIST =  [0,1,2,3,4,5]
REEL_INDEX_QUANZHONG_LIST = [0,15,10,5,10,10]
# 【可改】下面分别定义了block的长度（包含多少个图案），及其权重
BLOCK_LENGTH_LIST = [2,3,4]
BLOCK_LENGTH_QUANZHONG_LIST = [10,5,2]
# 【可改】下面分别定义了block的种类（木框、银框、金框），及其权重
BLOCK_TYPE_LIST =  [0,1,2]
BLOCK_TYPE_QUANZHONG_LIST = [10,5,1]
# 【可改】下面分别定义了一局的图案中block的数量，及其权重
BLOCK_NUM_LIST = [0, 1, 2, 3, 4]
BLOCK_NUM_QUANZHONG_LIST = [12, 5, 5, 2, 1]


if __name__ == '__main__':
    log = Logger(ID = PACKAGE_NAME)
    pl_list, gl_list, pl_need_num_list = tools.get_pl_from_excel(GAME6001_EXCEL)
    num = sum(pl_need_num_list) # 需要生成的组合总数
    pl_get_num_list = [0] * len(pl_need_num_list)  # 保存一下每个赔率得到了多少个组合
    log.success("main: 总共需要 "+str(num) + "个组合")
    progress_bar = tqdm(total = num)
    # 跑多少组组合，一般来讲，跑满需要的赔率需要10W次以上
    for i in range(10):
        total_win = 0
        all_tuan = create_tuan.create_tuan_matrix_without_header(TUAN_LIST, TUAN_QUANZHONG_LIST, REEL_LENGTH, REEL_NUM)
        new_block_list = create_tuan.create_block_list(BLOCK_NUM_LIST, BLOCK_NUM_QUANZHONG_LIST,
                                                    REEL_INDEX_LIST, REEL_INDEX_QUANZHONG_LIST,
                                                    BLOCK_LENGTH_LIST, BLOCK_LENGTH_QUANZHONG_LIST,
                                                    BLOCK_TYPE_LIST, BLOCK_TYPE_QUANZHONG_LIST,
                                                    TUAN_LIST, BLOCK_TUAN_QUANZHONG, REEL_LENGTH)
        all_tuan = create_tuan.updata_tuan_with_block_list(all_tuan, new_block_list)
        header = create_tuan.create_header(TUAN_LIST, HEADER_QUANZHONG, REEL_NUM - 2)
        all_tuan.append(header)
        win_res = compute_win.compute_win_for_tuan_matrix(all_tuan, TUAN_PL_MAP, True)
        result = []
        single_combo_result = []
        # check是否中奖，如果中奖了要继续生成和计算后面的combo图案
        while(win_res[-1] > 0):
            total_win = total_win + win_res[-1]
            result.append([deepcopy(win_res), deepcopy(all_tuan), deepcopy(new_block_list)])
            # 重新生成新的combo的图案
            [old_all_tuan_with_X, header_with_X, new_block_list] = create_tuan.update_tuan_matrix_with_X(all_tuan, new_block_list, win_res[:-1:1])
            [all_tuan, new_header] = create_tuan.update_X_with_new_tuan(old_all_tuan_with_X, TUAN_LIST, TUAN_QUANZHONG_LIST, header_with_X, HEADER_QUANZHONG)
            all_tuan = create_tuan.updata_tuan_with_block_list(all_tuan, new_block_list)
            all_tuan.append(deepcopy(new_header))
            win_res = compute_win.compute_win_for_tuan_matrix(all_tuan, TUAN_PL_MAP, True)
        # 记录最后一个不中奖的combo的数据
        result.append([deepcopy(win_res), deepcopy(all_tuan), deepcopy(new_block_list)])
        combo_num = "combo "+str(len(result))
        result = [combo_num] + [total_win] + result
        log.success("main: 得到一局结果 "+ str(combo_num))
        pprint("main: 这一局的详细数据是 " + str(result))

        # 如果这一局中奖了，要看这局的中奖结果要加到哪里
        if total_win > 0 :
            for i, value in enumerate(pl_list):
                if tools.pl_is_match(total_win, pl_list, i, PV_MIN, PV_MAX):
                    # 只有某个赔率没有满的时候，才需要添加
                    if pl_get_num_list[i] < pl_need_num_list[i]:
                        pl_get_num_list[i] = pl_get_num_list[i] + 1
                        log.success("main: 第" + str(
                            i) + "个赔率已生成组合数 " + str(pl_get_num_list[i]) + "/" + str(pl_need_num_list[i]))
                        progress_bar.update(1)  # 进度条加1
        else:
            pl_get_num_list[0] = pl_get_num_list[0] + 1
            progress_bar.update(1)  # 进度条加1
            log.success("main: 第1个赔率已生成组合数 " + str(pl_get_num_list[0]) + "/" + str(pl_need_num_list[0]))

        # 如果已经生成了所有需要的组合，则退出程序
        if sum(pl_get_num_list) >= num:
            break

