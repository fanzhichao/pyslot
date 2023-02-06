'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   drawfigure.py
@Time    :   2022/6/8
@Desc    :   专门用来绘制RTP走势图，具体要根据大量的bet数据去生成
'''
import matplotlib.pyplot as plt

BET_LIST = [100, 150, 500, 100, 500, 50, 300,500, 100,300]
WIN_LIST = [0, 50, 200, 0, 0, 150, 600, 0, 0, 150]
RTX_MIN = 0.3
RTX_MAX = 0.6
# 坐标轴Y轴显示的起止区域
AXIS_Y_MIN = 0
AXIS_Y_MAX = 1.1
IMAGE_WITH = 1000
IMAGE_HEIGTH = 1000
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
        total_bet_list.append(total_bet / 100.0)
        total_rtp_list.append(total_rtp)
    return [total_bet_list, total_rtp_list]

def draw_total_RTP(total_bet_list, total_rtp_list, rtp_min, rtp_max):
    plt.figure(figsize=(IMAGE_WITH / 100, IMAGE_HEIGTH / 100))
    plt.title('RTP test data')
    plt.xlabel("bet")
    plt.ylabel("RTP")

    plt.axis(ymin = AXIS_Y_MIN, ymax = AXIS_Y_MAX)
    line1, = plt.plot(total_bet_list, total_rtp_list, color = 'b',linestyle = ':')
    rtp_min_list = [rtp_min] * len(total_bet_list)
    rtp_max_list = [rtp_max] * len(total_bet_list)
    line2, = plt.plot(total_bet_list, rtp_min_list, color='g', linestyle=':')
    line3, = plt.plot(total_bet_list, rtp_max_list, color='r', linestyle=':')
    plt.legend((line1,line2,line3),["line1","line2","line3"])
    # plt.savefig("1.png")
    plt.show()


if __name__ == '__main__':
    [list1, list2] = get_total_RTP(BET_LIST, WIN_LIST)
    draw_total_RTP(list1,list2, RTX_MIN, RTX_MAX)
