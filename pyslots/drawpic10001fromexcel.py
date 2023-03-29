'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   drawpic10001fromexcel.py
@Time    :   2023/3/21
@Desc    :   专门用来绘制RTP走势图，具体要根据大量的bet数据去生成
'''
import matplotlib.pyplot as plt
import requests
import random
import datetime
import json
import pandas
import codecs
import time
import pandas as pd

# 下面的参数都是为了绘制RTP走势图用
# 绘制RTP走势图时，指定的RTP上下限，会绘制两条直线
RTX_MIN = 0.92
RTX_MAX = 0.94
# 坐标轴Y轴显示的起止区域，也就是RTP范围
AXIS_Y_MIN = 0
AXIS_Y_MAX = 1.5
IMAGE_WITH = 1000
IMAGE_HEIGTH = 1000

GAME10001_EXCEL = r"C:\\u\\doc\\slots_record_0327.xlsx"
# 通过HTTP请求，获取每一局spin的结果数据，然后统计结果数据。
def get_result_from_excel():
    user_list = []
    bet_list = []
    win_list = []
    single_player_result_list = []
    data = pandas.read_excel(GAME10001_EXCEL, names=None)
    # 依次读取第1、2、5列，注意：excel的内容必须与之对应
    user_list = data.values[:, 1].tolist()
    bet_list = data.values[:, 3].tolist()
    win_list = data.values[:, 5].tolist()
    for i in range(len(user_list)):
        single_player_result_list.append([user_list[i], bet_list[i], win_list[i]])
    return single_player_result_list
def get_total_RTP(single_player_result_list):
    total_bet_list = []
    total_rtp_list = []
    total_bet = 0
    total_win = 0
    total_rtp = 0.0
    for i in range(len(single_player_result_list)):
        total_bet = total_bet + single_player_result_list[i][1]
        total_win = total_win + single_player_result_list[i][2]
        total_rtp = total_win / total_bet
        total_bet_list.append(total_bet / 100.0)
        total_rtp_list.append(total_rtp)
    return [total_bet_list, total_rtp_list]

def draw_total_RTP(total_bet_list, total_rtp_list, rtp_min, rtp_max, save_pic):
    plt.figure(figsize=(IMAGE_WITH / 100, IMAGE_HEIGTH / 100))
    plt.title('RTP test data')
    plt.xlabel("bet money")
    plt.ylabel("RTP")

    plt.axis(ymin = AXIS_Y_MIN, ymax = AXIS_Y_MAX)
    line1, = plt.plot(total_bet_list, total_rtp_list, color = 'b',linestyle = ':')
    rtp_min_list = [rtp_min] * len(total_bet_list)
    rtp_max_list = [rtp_max] * len(total_bet_list)
    line2, = plt.plot(total_bet_list, rtp_min_list, color='g', linestyle=':')
    line3, = plt.plot(total_bet_list, rtp_max_list, color='r', linestyle=':')
    plt.legend((line1,line2,line3),["RTP",str(RTX_MIN),str(RTX_MAX)])
    plt.savefig(save_pic)
    #plt.show()

def get_single_user_rtp(single_player_result_list):
    userid_list = []
    user_bet_list = []
    user_win_list = []
    user_rtp_list = []
    user_bet_count_list = []
    for v in single_player_result_list:
        if v[0] not in userid_list:
            userid_list.append(v[0])
    for v in userid_list:
        bet_list  = [s[1] for s in single_player_result_list if s[0] == v]
        win_list  = [s[2] for s in single_player_result_list if s[0] == v]
        total_bet = sum(bet_list)
        total_win = sum(win_list)
        user_bet_list.append(total_bet)
        user_win_list.append(total_win)
        user_rtp_list.append(1.0 * total_win/ total_bet)
        user_bet_count_list.append(len(bet_list))

    datalist = []
    for i in range(len(userid_list)):
        datalist.append([userid_list[i], user_rtp_list[i], user_bet_list[i], user_bet_count_list[i]])
    dataframe = pd.DataFrame(datalist, columns=['id', 'rtp', 'bet', '局数'])
    dataframe = dataframe.sort_values(by=["局数"], ascending=False)
    l,m,n = 0,0,0
    for index, row in dataframe.iterrows():
        if index == 0:
            continue
        if row['rtp'] > 0.95:
            l = l + 1
            print("\033[0;31;1m userid {:10d}   rtp {:.3f}  bet {:10d}  局数 {:6d}\033[0m".format(int(row['id']), row['rtp'], int(row['bet']), int(row['局数'])))
        elif row['rtp'] < 0.91:
            m = m + 1
            print("\033[0;34;1m userid {:10d}   rtp {:.3f}  bet {:10d}  局数 {:6d}\033[0m".format(int(row['id']), row['rtp'], int(row['bet']) , int(row['局数'])))
        else:
            n = n + 1
            print(" userid {:10d}   rtp {:.3f}  bet {:10d}  局数 {:6d}".format(int(row['id']), row['rtp'], int(row['bet']) , int(row['局数'])))
    print("rtp>0.94 {:f}   rtp<0.9 {:f}  rtp正常 {:f}".format(l / (l + m + n), m / (l + m + n), n / (l + m + n)))
    return

if __name__ == '__main__':
    list1 = get_result_from_excel()
    total_bet_list, total_rtp_list = get_total_RTP(list1)
    res = get_single_user_rtp(list1)
    pic_name = "C:\\u\\doc\\exceldata.png"
    draw_total_RTP(total_bet_list,total_rtp_list, RTX_MIN, RTX_MAX, pic_name)

