'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   drawfigure.py
@Time    :   2023/3/28
@Desc    :   专门用来绘制RTP走势图，具体要根据大量的bet数据去生成
'''
import os.path
import shutil

import matplotlib.pyplot as plt
import requests
import random
import datetime
import pandas as pd
from threading import Thread

# 下面的参数都是为了绘制RTP走势图用
# 绘制RTP走势图时，指定的RTP上下限，会绘制两条直线
RTX_MIN = 0.92
RTX_MAX = 0.96
# 坐标轴Y轴显示的起止区域，也就是RTP范围
AXIS_Y_MIN = 0
AXIS_Y_MAX = 1.5
# RTP走势图的宽度和高度
IMAGE_WITH = 1000
IMAGE_HEIGTH = 1000

# 全局变量，用来保存玩家所有的下注信息，里面一条记录就是一条下注信息
single_player_result_list = []

# 通过HTTP请求，获取每一局spin的结果数据，然后统计结果数据。
# 向服务端请求N次数据，这个是需要放在多线程里面执行的
def get_result_from_url(times, user_array):
    # 该游戏玩家可选的下注档位
    bet_array = [100, 1000, 5000, 10000]
    # 请求游戏的URL
    url = "http://api.ahleen.live/ftestapi/echo-api/fruit_party/test_game?token=20210129&uid={0}&dontencode=2019&sign=n_e_m_o&ttx=1&bet_coin={1}&roomid=123456"
    for i in range(times):
        bet = random.choice(bet_array)
        userid = user_array[i % len(user_array)]
        time_beg = datetime.datetime.now()
        # 这里要解析一下收到的结果，得到每一局的win
        res = requests.post(url.format(userid, bet))
        time_end = datetime.datetime.now()
        time_end_str = time_end.strftime("  %H:%M:%S.%f")
        # print("等服务端结果的时间为 "+ str((time_end - time_beg).microseconds/100000) +" 秒")
        # 解析一下数据
        jsondata = res.json()
        if "data" in jsondata:
            win= res.json()["data"]
            single_player_result_list.append([userid, bet, win])
        else:
            print("\033[0;31;1m 服务器返回数据错误！\033[0m")
    return
def get_total_RTP():
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

def output_single_user_rtp(excel_name):
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
    dataframe = dataframe.sort_values(by=["局数","rtp"], ascending=False)
    l,m,n = 0,0,0
    for index, row in dataframe.iterrows():
        if index == 0:
            continue
        if row['rtp'] > RTX_MAX:
            l = l + 1
            print("\033[0;31;1m userid {:10d}   rtp {:.3f}  bet {:10d}  局数 {:6d}\033[0m".format(int(row['id']), row['rtp'], int(row['bet']), int(row['局数'])))
        elif row['rtp'] < RTX_MIN:
            m = m + 1
            print("\033[0;34;1m userid {:10d}   rtp {:.3f}  bet {:10d}  局数 {:6d}\033[0m".format(int(row['id']), row['rtp'], int(row['bet']) , int(row['局数'])))
        else:
            n = n + 1
            print(" userid {:10d}   rtp {:.3f}  bet {:10d}  局数 {:6d}".format(int(row['id']), row['rtp'], int(row['bet']) , int(row['局数'])))
    #print("rtp>0.94 {:f}   rtp<0.9 {:f}  rtp正常 {:f}".format(l / (l + m + n), m / (l + m + n), n / (l + m + n)))
    dataframe.to_excel(excel_name, index = False)
    return

# turns 代表跑几轮, times代表每轮每个线程跑多少次，线程总数 x times才是最终的局数
# dirpath是一个文件夹的名称，代表这一次的所有结果会保存到哪个文件夹下
def run_shuzhi(turns, times, dirpath):
    # 确保保存图片和excel的目录是可用的
    pic_path = "C:\\u\\doc\\{0}".format(dirpath)
    if os.path.expandvars(pic_path):
        shutil.rmtree(pic_path, ignore_errors=True)
    os.mkdir(pic_path)
    # 开启多线程模式，向服务器请求数据，并等待所有线程全部运行完成
    for i in range(turns):
        user_array = [  [80037982, 80078694, 80072693, 97069997, 81042539, 80068208, 80022576, 81042207, 81047868, 81037699, ],
                        [81057343, 81062234, 80076449, 80096819, 80075878, 81030360, 81057456, 81037421, 80072380, 81059798, ],
                        [81061847, 80056505, 81035930, 80092434, 81035567, 81015269, 81043456, 81020719, 81055106, 80029927, ],
                        [81056427, 80074899, 81005675, 80072309, 81068092, 80091172, 81004997, 81057451, 80073838, 81012997, ],
                        [81032413, 80066825, 80068974, 81044700, 81059325, 80069036, 80067642, 80074611, 80080914, 81021946, 81028373],
                        [80024048, 80084665, 81064713, 81016418, 81010106, 81004476, 80067183, 80071036, 80067537, 81038892, 80081051],
                        [80096458, 80064217, 81036480, 81045964, 80066588, 80065386, 80074873, 81067935, 80090005, 80053661, 80089450],
                        [81069078, 81053886, 81008670, 80069714, 81057112, 80073429, 81056063, 80071968, 81058026, 80097380, 80070398],
                        [80079014, 80081031, 80066151, 80088190, 80098476, 80086449, 80048802, 80086481, 80094307, 80083060], ]
        thread_list = []
        for v in user_array:
            t = Thread(target=get_result_from_url, args=(times, v))
            thread_list.append(t)
            t.start()
        for t in thread_list:
            t.join()

        pic_name = "C:\\u\\doc\\{0}\\{1}.png".format(dirpath, i + 1)
        excel_name = "C:\\u\\doc\\{0}\\{1}.xlsx".format(dirpath, i + 1)
        print(str("=============================第{0}轮测试================================").format(i + 1))
        output_single_user_rtp(excel_name)
        print(str("=====================================================================").format(i + 1))
        total_bet_list, total_rtp_list = get_total_RTP()
        draw_total_RTP(total_bet_list, total_rtp_list, RTX_MIN, RTX_MAX, pic_name)
        single_player_result_list.clear()

if __name__ == '__main__':
    run_shuzhi(5, 10, "1")





