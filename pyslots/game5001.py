
import paylines_compute_win as compute_win
import paylines_create_tuan as create_tuan
DEBUG_ON = True
PACKAGE_NAME = 'game5001'
# just for test

def pprint(str):
    if DEBUG_ON:
        print(str)
##############  保存赔率概率表的excel ####################
GAME5001_EXCEL = r"d:py\\game5001.xlsx"

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
    '9' : [0, 0, 0, 2, 5],
    '10': [0, 0, 0, 5, 10],
    'J' : [0, 0, 0, 10, 15],
    'Q' : [0, 0, 0, 15, 20],
    'K' : [0, 0, 5, 20, 30],
    'A' : [0, 0, 10, 25, 40],
    'W' : [0, 0, 15, 30, 50],
    'S' : [0, 0, 0, 2, 5],
}
# 每条支付线对应的矩阵坐标位置
PAYLINES = [[(0,0), (2,1), (0,2), (2,3), (2,4)],
            [(2,0), (0,1), (1,2), (2,3), (2,4)],
            [(1,0), (2,1), (2,2), (2,3), (2,4)],
            [(0,0), (0,1), (1,2), (2,3), (2,4)]]
#################  供计算中奖情况用  ########################


if __name__ == '__main__':
    pl_list, gl_list = compute_win.get_pl_from_excel(GAME5001_EXCEL)
    for i in range(2000):
        all_tuan = create_tuan.create_all_tuan(TUAN_LIST, QUANZHONG_LIST_REELS, 3, 5)
        win_res = compute_win.compute_win_for_all_tuan(all_tuan, PAYLINES, TUAN_PL_MAP)

        #pprint("****package:"+PACKAGE_NAME + "  ****funtion main:"+ str(win_res))

        result = []
        single_combo_result = []
        # check是否中奖，如果中奖了要继续生成和计算后面的combo图案
        while(win_res[-1] > 0):
            single_combo_result = [win_res, all_tuan]
            result.append(single_combo_result)
            # 重新生成新的comobo的图案
            old_all_tuan_with_X = create_tuan.update_all_tuan_with_X(all_tuan, win_res, PAYLINES)
            all_tuan = create_tuan.update_X_with_new_tuan(old_all_tuan_with_X, TUAN_LIST, QUANZHONG_LIST_REELS)
            win_res = compute_win.compute_win_for_all_tuan(all_tuan, PAYLINES, TUAN_PL_MAP)
            pprint("****package:" + PACKAGE_NAME + "  ****funtion main: win_res " + str(win_res))
        # 记录最后一个不中奖的combo的数据
        single_combo_result = [win_res, all_tuan]
        result.append(single_combo_result)
        combo_num = "combo "+str(len(result))
        result = [combo_num] + result
        pprint("****package:"+PACKAGE_NAME + "  ****funtion main: the "+ str(i) + str(result))




