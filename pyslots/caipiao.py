#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   caipiao.py
@Time    :   2023/2/11 9:08
@Desc    :
'''

import time
import random
import matplotlib.pyplot as plt
from copy import copy, deepcopy
from colored_logs.logger import Logger, LogType
DEBUG_ON = True
PACKAGE_NAME = 'caipiao'

# 定义一个盘口最重要的3个参数设置
BET_AREA_INIT_PL_LIST = [2.28, 3.44, 2.86]
BET_AREA_RTP_LIST = [0.93, 0.93, 0.93]
MAX_LOSE = 100000

# 用来模拟玩家的下注金额
BET_MONEY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 50, 100, 200, 300, 500, 1000]
BET_MONEY_QUANZHONG = [100, 80, 60, 50, 40, 35, 30, 30, 30, 25, 10, 20, 20, 15, 10, 10, 8, 5, 4, 3, 2, 1]

# 以下参数是绘制图像用
RTX_MIN = 0.93
RTX_MAX = 0.98
# 坐标轴Y轴显示的起止区域
AXIS_Y_MIN = 0
AXIS_Y_MAX = 3
IMAGE_WITH = 1000
IMAGE_HEIGTH = 600

log = Logger(ID = PACKAGE_NAME)

def pprint(str):
    if DEBUG_ON:
        print(str)

# 跟进初始赔率列表，RTP列表和盘口保证金，计算出概率列表和每个下注区域的保证金
def init_data(pl_list, rtp_list, max_lose):
    gl_list = [rtp_list[i] / pl_list[i] for i in range(len(pl_list))]
    max_lose_list = [MAX_LOSE * value for value in gl_list]
    max_bet_list = [ max_lose_list[i] / (pl_list[i] - 1) for i in range(len(max_lose_list))]
    log.success("max_lose_list:" + str(max_lose_list))
    log.success("max_bet_list:" + str(max_bet_list))
    return [gl_list, max_bet_list]

# 随机选择一个下注金额
def random_bet_money():
    return random.choices(BET_MONEY, BET_MONEY_QUANZHONG, k=1)[0]


# 模拟玩家根据当前赔率选择下注区域，该区域的赔率比初始赔率高，就多下注。反之就少下注。
def random_bet_area(init_pl_list, now_pl_list):
    bet_area_list = [i for i in range(len(init_pl_list))]
    quanzhong_list = [100] * len(init_pl_list)
    for i in range(len(init_pl_list)):
        # 赔率明显升高，其对应的下注区域的权重也升高
        bl = now_pl_list[i] / init_pl_list[i]
        if bl > 1.05 and bl <= 1.1 :
            quanzhong_list[i] = 120 * bl
        elif bl > 1.1 and bl <= 1.2 :
            quanzhong_list[i] = 140 * bl
        elif bl > 1.2 and bl <= 1.3:
            quanzhong_list[i] = 160 * bl
        elif bl > 1.3:
            quanzhong_list[i] = 200 * bl
        elif bl > 0.9 and bl <= 0.95:
            quanzhong_list[i] = 80 * bl
        elif bl > 0.8 and bl <= 0.9:
            quanzhong_list[i] = 60 * bl
        elif bl > 0.7 and bl <= 0.8:
            quanzhong_list[i] = 40 * bl
        elif bl < 0.7:
            quanzhong_list[i] = 30 * bl
    log.warning("random_bet_area quanzhong_list:"+str(quanzhong_list) +"  bl:"+str(bl))
    return random.choices(bet_area_list, quanzhong_list, k=1)[0]


# 是否各个区域的下注金额已经到达目标值了，只要有一个没达到，就返回false
def is_total_bet_enough(bet_list, max_lose_list):
    # 只要有一个下注区域没有满，就返回False
    for value1,value2 in zip(bet_list, max_lose_list):
        if value1 < value2:
            return False
    return True

def is_bet_enough(bet_list, max_lose_list,area_index):
    # 只要有一个下注区域没有满，就返回False
    return bet_list[area_index] >=  max_lose_list[area_index]

def get_winlist(all_bet_list, area_index):
    win_list = []
    win = 0
    for value in all_bet_list:
        if value[0] != area_index:
            win = 0
        else:
            win = value[1] * value[2]
        win_list.append(win)
    return win_list

# 关键算法，根据当前下注情况和初始赔率列表，得到修改过的新赔率列表
def get_new_pl_list(all_bet_list, init_pl_list, rtp_list):
    new_pl_list = deepcopy(init_pl_list)
    area_num = len(init_pl_list)
    area_total_bet_list = [0] * area_num
    area_total_win_list = [0] * area_num
    area_total_profit_list = [0] * area_num
    # 先计算总下注
    total_bet = sum([v[1] for v in all_bet_list])
    # 再计算各个下注区域的目标净利润是多大
    area_goal_profit_list = []
    for v in rtp_list:
        area_goal_profit_list.append(total_bet*(1 - v))
    # 开始计算各个下注区域的总下注和总赢,最后得到当前的总净利润
    for v in all_bet_list:
        # 得到具体的下注数据
        bet_area, bet_money, bet_pl = v[0], v[1], v[2]
        area_total_bet_list[bet_area] = area_total_bet_list[bet_area] + v[1]
        area_total_win_list[bet_area] = area_total_win_list[bet_area] + v[1]*v[2]
    for i in range(area_num):
        area_rtp = area_total_win_list[i] / total_bet
        area_total_profit_list[i] = total_bet - area_total_win_list[i]
        # 下注金额太低，不调整该区域的赔率
        if area_total_bet_list[i] < 100:
            continue
        else:
            if area_rtp < 0:
                new_pl_list[i] = init_pl_list[i] * 1.3
            elif area_rtp > 0 and area_rtp <= 0.5:
                new_pl_list[i] = init_pl_list[i] * 1.2
            elif area_rtp > 0.5 and area_rtp <= 0.8:
                new_pl_list[i] = init_pl_list[i] * 1.1
            elif area_rtp > 0.8 and area_rtp <= 0.9:
                new_pl_list[i] = init_pl_list[i] * 1.05
            elif area_rtp > 0.9 and area_rtp <= 1:
                new_pl_list[i] = init_pl_list[i]
            elif area_rtp > 1 and area_rtp <= 1.2:
                new_pl_list[i] = init_pl_list[i] * 0.98
            elif area_rtp > 1.2 and area_rtp <= 1.5:
                new_pl_list[i] = init_pl_list[i] * 0.95
            elif area_rtp > 1.5 and area_rtp <= 3:
                new_pl_list[i] = init_pl_list[i] * 0.9
            elif area_rtp > 3 and area_rtp <= 8:
                new_pl_list[i] = init_pl_list[i] * 0.8
    log.warning(" new_pl_list " + str(new_pl_list))
    return new_pl_list
# 以下方法是绘图用的
def get_total_RTP(bet_list, win_list):
    total_bet_list = []
    total_rtp_list = []
    total_bet = 0
    total_win = 0
    total_rtp = 0.0
    for i in range(len(bet_list)):
        total_bet = total_bet + bet_list[i]
        total_win = total_win + win_list[i]
        total_rtp = total_win / total_bet
        total_bet_list.append(total_bet)
        total_rtp_list.append(total_rtp)
    return [total_bet_list, total_rtp_list]

def draw_total_RTP(total_bet_list, total_rtp_list1, total_rtp_list2, total_rtp_list3, rtp_min, rtp_max):
    plt.figure(figsize=(IMAGE_WITH / 100, IMAGE_HEIGTH / 100))
    plt.title('caipiao RTP')
    plt.xlabel("bet")
    plt.ylabel("RTP")

    plt.axis(ymin = AXIS_Y_MIN, ymax = AXIS_Y_MAX)
    line1, = plt.plot(total_bet_list, total_rtp_list1, color = 'b',linestyle = ':')
    rtp_min_list = [rtp_min] * len(total_bet_list)
    rtp_max_list = [rtp_max] * len(total_bet_list)

    line2, = plt.plot(total_bet_list, total_rtp_list2, color='g', linestyle=':')
    line3, = plt.plot(total_bet_list, total_rtp_list3, color='r', linestyle=':')
    line4, = plt.plot(total_bet_list, rtp_min_list, color='y', linestyle=':')
    line5, = plt.plot(total_bet_list, rtp_max_list, color='y', linestyle=':')

    plt.legend((line1,line2,line3,line4,line5),["line1","line2","line3","line4","line5"])
    # plt.savefig("1.png")
    plt.show()



if __name__ == '__main__':
    [gl_list, max_bet_list] = init_data(BET_AREA_INIT_PL_LIST, BET_AREA_RTP_LIST, MAX_LOSE)
    area_total_bet_list = [0] * len(gl_list)
    now_pl_list = deepcopy(BET_AREA_INIT_PL_LIST)
    all_bet_list = []
    while (not is_total_bet_enough(area_total_bet_list, max_bet_list)):
        bet_area = random_bet_area(BET_AREA_INIT_PL_LIST, now_pl_list)
        bet_money = random_bet_money()
        bet_pl = now_pl_list[bet_area]
        if not is_bet_enough(area_total_bet_list, max_bet_list, bet_area):
            area_total_bet_list[bet_area] = area_total_bet_list[bet_area] + bet_money
            all_bet_list.append([bet_area, bet_money, bet_pl])
            now_pl_list = get_new_pl_list(all_bet_list, BET_AREA_INIT_PL_LIST, BET_AREA_RTP_LIST)
        #log.warning("now_pl_list:"+str(now_pl_list))
    log.success("area_total_bet_list "+str(area_total_bet_list))
    bet_list = [value[1] for value in all_bet_list]
    [list1, list2] = get_total_RTP(bet_list, get_winlist(all_bet_list, 0))
    [list3, list4] = get_total_RTP(bet_list, get_winlist(all_bet_list, 1))
    [list5, list6] = get_total_RTP(bet_list, get_winlist(all_bet_list, 2))
    draw_total_RTP(list1, list2, list4,list6,RTX_MIN, RTX_MAX)
