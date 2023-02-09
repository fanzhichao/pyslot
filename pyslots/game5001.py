'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   game5001.py
@Time    :   2022/6/8
@Desc    :   这是一个标准的3*5的pay lines游戏的例子
'''
import time
from tqdm import tqdm
import paylines_compute_win as compute_win
import paylines_create_tuan as create_tuan
import tools
from copy import copy, deepcopy
DEBUG_ON = True
PACKAGE_NAME = 'game5001'

def pprint(str):
    if DEBUG_ON:
        print(str)
##############  保存赔率概率表的excel ####################
GAME5001_EXCEL = r"d:py\\game5001.xlsx"

# 【可改】 随机生成的图案矩阵的最终赔率是否满足需要
# 满足的条件是：它与赔率数组（excel中指定的所有赔率）中指定的某个元素对应的赔率相差不大
# 相差不大的条件是：在其0.8 - 1.2倍左右，具体是由PV_MIN 和 PV_MAX来定的
PV_MIN = 0.8
PV_MAX = 1.2
# 【必改】 定义图案的行数和列数
REEL_LENGTH = 3  # matrix的高度，rows 行数
REEL_NUM = 5    # matrix的宽度，cols 列数

#################  供生成图案用  ########################
# 所有的图案
TUAN_LIST = ['9', '10', 'J', 'Q', 'K', 'A', 'W', 'S']
# 每个REEL上面的图案出现的权重
QUANZHONG_LIST_REELS = ((0, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0),
                        (50, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0))
#################  供生成图案用  ########################

#################  供计算中奖情况用  ########################
# 图案的赔率表
TUAN_PL_MAP = {
    '9' : [0, 0, 2, 5, 10],
    '10': [0, 0, 5, 10, 15],
    'J' : [0, 0, 8, 15, 20],
    'Q' : [0, 0, 12, 20, 30],
    'K' : [0, 0, 20, 30, 50],
    'A' : [0, 0, 25, 40, 60],
    'W' : [0, 0, 0, 0, 0],
    'S' : [0, 0, 0, 0, 0],
}
# 每条支付线对应的矩阵坐标位置
PAYLINES = [[(0,0), (2,1), (0,2), (2,3), (2,4)],
            [(2,0), (0,1), (1,2), (2,3), (2,4)],
            [(1,0), (2,1), (2,2), (2,3), (2,4)],
            [(0,0), (0,1), (1,2), (2,3), (2,4)]]
#################  供计算中奖情况用  ########################




if __name__ == '__main__':
    pl_list, gl_list, pl_need_num_list = tools.get_pl_from_excel(GAME5001_EXCEL)
    num = sum(pl_need_num_list) # 需要生成的组合总数
    pl_get_num_list = [0] * len(pl_need_num_list)  # 保存一下每个赔率得到了多少个组合
    pprint("**package:" + PACKAGE_NAME + "  **funtion main: 总共需要 "+str(num) + "个组合")
    progress_bar = tqdm(total = num)
    # 跑多少组组合，一般来讲，跑满需要的赔率需要10W次以上
    for i in range(100):
        total_win = 0
        all_tuan = create_tuan.create_tuan_matrix(TUAN_LIST, QUANZHONG_LIST_REELS, REEL_LENGTH, REEL_NUM)
        win_res = compute_win.compute_win_for_tuan_matrix(all_tuan, PAYLINES, TUAN_PL_MAP)
        #pprint("**package:"+PACKAGE_NAME + "  **funtion main:"+ str(win_res))
        result = []
        # check是否中奖，如果中奖了要继续生成和计算后面的combo图案
        while(win_res[-1] > 0):
            total_win = total_win + win_res[-1]
            result.append([deepcopy(win_res), deepcopy(all_tuan)])
            # 重新生成新的comobo的图案
            old_all_tuan_with_X = create_tuan.update_tuan_matrix_with_X(all_tuan, win_res, PAYLINES)
            all_tuan = create_tuan.update_X_with_new_tuan(old_all_tuan_with_X, TUAN_LIST, QUANZHONG_LIST_REELS)
            win_res = compute_win.compute_win_for_tuan_matrix(all_tuan, PAYLINES, TUAN_PL_MAP)
        # 记录最后一个不中奖的combo的数据
        result.append([deepcopy(win_res), deepcopy(all_tuan)])
        combo_num = "combo "+str(len(result))
        result = [combo_num] + [total_win] + result
        pprint("**package:"+PACKAGE_NAME + "  **funtion main: 第 "+ str(i+1) +"局结果是:"+ str(result))

        # 如果这一局中奖了，要看这局的中奖结果要加到哪个赔率那里
        if total_win > 0 :
            for i, value in enumerate(pl_list):
                if tools.pl_is_match(total_win, pl_list,i, PV_MIN, PV_MAX):
                    # 只有某个赔率没有满的时候，才需要添加
                    if pl_get_num_list[i] < pl_need_num_list[i]:
                        pl_get_num_list[i] = pl_get_num_list[i] + 1
                        # tools.save_to_php() 需要后续完善
                        pprint("**package:" + PACKAGE_NAME + "  **funtion main: 第 "+str(i)+" 个赔率已生成组合数 "+str(pl_get_num_list[i]) + "/"+str(pl_need_num_list[i]))
                        progress_bar.update(1)  # 进度条加1
        else: # 没中奖，就加到赔率为0的列表里
            pl_get_num_list[0] = pl_get_num_list[0] + 1
            progress_bar.update(1)  # 进度条加1
            # tools.save_to_php() 需要后续完善

            pprint("**package:" + PACKAGE_NAME + "  **funtion main: 第 1 个赔率已生成组合数 " + str(
                pl_get_num_list[0]) + "/" + str(pl_need_num_list[0]))

        # 如果已经生成了所有需要的组合，则退出程序
        if sum(pl_get_num_list) >= num:
            break




