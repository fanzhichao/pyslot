'''
@Author  :   Frank
@License :   (C) Copyright 2023-2028
@Contact :
@Software:   slot
@File    :   game20001.py
@Time    :   2023/2/24
@Desc    :   这是一个标准的3*5的pay lines游戏的例子
'''
import time
from tqdm import tqdm
import paylines_compute_win as compute_win
import paylines_create_tuan as create_tuan
import tools
from copy import copy, deepcopy
DEBUG_ON = False
PACKAGE_NAME = 'game5001'
from colored_logs.logger import Logger, LogType


log = Logger(ID=PACKAGE_NAME)
def print_success(str):
    if DEBUG_ON:
        log.success(str)

def print_error(str):
    if DEBUG_ON:
        log.error(str)

##############  保存赔率概率表的excel ####################
GAME20001_EXCEL = r"C:\\u\\doc\\game20001.xlsx"
GAME20001_OUT_PUT_TXT = r"C:\\u\\doc\\game20001.txt"
# 【可改】 随机生成的图案矩阵的最终赔率是否满足需要
# 满足的条件是：它与赔率数组（excel中指定的所有赔率）中指定的某个元素对应的赔率相差不大
# 相差不大的条件是：在其0.9 - 1.1倍左右，具体是由PV_MIN 和 PV_MAX来定的
PV_MIN = 0.9
PV_MAX = 1.1
# 【必改】 定义图案的行数和列数
REEL_LENGTH = 3  # matrix的高度，rows 行数
REEL_NUM = 5    # matrix的宽度，cols 列数

#################  供生成图案用  ########################
# 所有的图案
# 'A':樱桃   'B':柠檬  'C':橙子  'D':西梅
# 'E':西瓜   'F':葡萄  'G':星星  'H':7
TUAN_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# 每个REEL上面的图案出现的权重
QUANZHONG_LIST_REELS = ((20, 15, 10, 20, 25, 25, 25, 15),
                        (15, 15, 10, 20, 25, 25, 25, 15),
                        (10, 20, 20, 20, 25, 20, 25, 15),
                        (8, 20, 20, 20, 25, 25, 20, 10),
                        (8, 10, 20, 25, 25, 20, 25, 10))

QUANZHONG_LIST_REELS_RICH = ((0, 0, 0, 20, 35, 25, 25, 15),
                             (0, 0, 0, 20, 35, 25, 25, 15),
                             (0, 0, 0, 20, 35, 25, 25, 15),
                             (0, 0, 0, 20, 35, 25, 25, 15),
                             (0, 0, 0, 0, 35, 25, 25, 15))

#################  供生成图案用  ########################

#################  供计算中奖情况用  ########################
# 图案的赔率表
TUAN_PL_MAP = {
    'A' : [0, 0.2, 0.8, 2, 5],
    'B' : [0, 0, 1, 2, 5],
    'C' : [0, 0, 2, 4, 10],
    'D' : [0, 0, 3, 6, 15],
    'E' : [0, 0, 4, 8, 20],
    'F' : [0, 0, 6, 12, 30],
    'G' : [0, 0, 10, 20, 50],
    'H' : [0, 0, 25, 50, 200]
}
"""
TUAN_PL_MAP = {
    'A' : [0, 0.2, 0.8, 2, 8],
    'B' : [0, 0, 0.8, 2, 8],
    'C' : [0, 0, 0.8, 2, 8],
    'D' : [0, 0, 0.8, 2, 8],
    'E' : [0, 0, 2, 8, 20],
    'F' : [0, 0, 2, 8, 20],
    'G' : [0, 0, 2, 10, 50],
    'H' : [0, 0, 4, 40, 200]
}
"""
# 每条支付线对应的矩阵坐标位置
PAYLINES = [[(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],
            [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],

            [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)],
            [(1, 0), (0, 1), (0, 2), (0, 3), (1, 4)],
            [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],
            [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],
            [(0, 0), (1, 1), (1, 2), (1, 3), (0, 4)],

            [(2, 0), (1, 1), (1, 2), (1, 3), (2, 4)],
            [(0, 0), (1, 1), (0, 2), (1, 3), (0, 4)],
            [(2, 0), (1, 1), (2, 2), (1, 3), (2, 4)],
            [(1, 0), (0, 1), (1, 2), (0, 3), (1, 4)],
            [(1, 0), (2, 1), (1, 2), (2, 3), (1, 4)],

            [(1, 0), (1, 1), (0, 2), (1, 3), (1, 4)],
            [(1, 0), (1, 1), (2, 2), (1, 3), (1, 4)],
            [(0, 0), (2, 1), (0, 2), (2, 3), (0, 4)],
            [(2, 0), (0, 1), (2, 2), (0, 3), (2, 4)],
            [(1, 0), (0, 1), (2, 2), (0, 3), (1, 4)],

            [(1, 0), (2, 1), (0, 2), (2, 3), (1, 4)],
            [(0, 0), (0, 1), (2, 2), (0, 3), (0, 4)],
            [(2, 0), (2, 1), (0, 2), (2, 3), (2, 4)],
            [(0, 0), (2, 1), (2, 2), (2, 3), (0, 4)],
            [(2, 0), (0, 1), (0, 2), (0, 3), (2, 4)],]
#################  供计算中奖情况用  ########################




if __name__ == '__main__':
    pl_list, gl_list, pl_need_num_list = tools.get_pl_from_excel(GAME20001_EXCEL)
    num = sum(pl_need_num_list) # 需要生成的组合总数
    pl_get_num_list = [0] * len(pl_need_num_list)  # 保存一下每个赔率得到了多少个组合
    print_success("main: 总共需要 " + str(num) + "个组合")

    # 初始化进度条相关的资源
    progress_bar_list = []
    progress_bar_total = tqdm(total = num, desc="生成总的组合")
    progress_bar_list.append(progress_bar_total)
    for i,v in enumerate(pl_need_num_list):
        progress_bar = tqdm(total = v, desc="生成赔率为{0}组合".format(pl_list[i]))
        progress_bar_list.append(progress_bar)

    # 跑多少组组合，一般来讲，跑满需要的赔率需要10W次以上
    go_data = [[]]*len(pl_list)
    for i in range(len(go_data)):
        go_data[i] = []
    with open(GAME20001_OUT_PUT_TXT,'w') as f:
        for i in range(200000):
            quzhang_list = QUANZHONG_LIST_REELS
            if i > 100000: # 换组合，可以更大概率产生高赔率
                quzhang_list = QUANZHONG_LIST_REELS_RICH
            all_tuan = create_tuan.create_tuan_matrix(TUAN_LIST, quzhang_list, REEL_LENGTH, REEL_NUM)
            win_res = compute_win.compute_win_for_tuan_matrix(all_tuan, PAYLINES, TUAN_PL_MAP)
            result = [deepcopy(win_res), deepcopy(all_tuan)]
            # 写到文本文件里，只是用来快速查看数据
            f.writelines(str(result) +'\n')
            total_win = win_res[0]
            # 如果这一局中奖了，要看这局的中奖结果要加到哪个赔率那里
            if total_win > 0 :
                for i, value in enumerate(pl_list):
                    if tools.pl_is_match(total_win, pl_list,i, PV_MIN, PV_MAX):
                        # 只有某个赔率没有满的时候，才需要添加
                        if pl_get_num_list[i] < pl_need_num_list[i]:
                            pl_get_num_list[i] = pl_get_num_list[i] + 1
                            go_data[i].append(result)
                            progress_bar_total.update(1)  # 总的进度条加1
                            progress_bar_list[i + 1].update(1) # 对应赔率的进度条加1
            else: # 没中奖，就加到赔率为0的列表里
                if pl_get_num_list[0] < pl_need_num_list[0]:
                    pl_get_num_list[0] = pl_get_num_list[0] + 1
                    go_data[0].append(result)
                    progress_bar_total.update(1)  # 总的进度条加1
                    progress_bar_list[1].update(1)  # 赔率为0的进度条加1
                    print_success("第1个赔率已生成组合数 {0}/{1}".format(pl_get_num_list[0],pl_need_num_list[0]))
            # 如果已经生成了所有需要的组合，则退出程序
            if sum(pl_get_num_list) >= num:
                break
    # 将所有得到的结果保存到go文件中
    tools.save_to_go(r"C:\\u\\doc\\game20001.go",go_data)

