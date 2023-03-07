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
import requests
import random
import time
BET_LIST = [100, 150, 500, 100, 500, 50, 300,500, 100,300]
WIN_LIST = [0, 50, 200, 0, 0, 150, 600, 0, 0, 150]
RTX_MIN = 0.3
RTX_MAX = 0.6
# 坐标轴Y轴显示的起止区域
AXIS_Y_MIN = 0
AXIS_Y_MAX = 1.1
IMAGE_WITH = 1000
IMAGE_HEIGTH = 1000

# 通过HTTP请求，获取每一局spin的结果数据，然后统计结果数据。
def get_result_from_url():
    bet_array = [1,2,5,10,15,20,50,100]
    userid_array = [1, 2, 5, 10, 15, 20, 50, 100]
    bet_list = []
    win_list = []
    url = "http://127.0.0.1:4523/m1/2311909-0-default/cash"
    for i in range(10):
        bet = random.choice(bet_array)
        userid = random.choice(userid_array)
        params = {"userid": userid, "bet":bet}
        # 这里要解析一下收到的结果，得到每一局的win
        res = requests.post(url, data=params)
        bet_list.append(bet)
        win_list.append(userid)
    return bet_list, win_list
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
    res = get_result_from_url()
    print(res)