'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   paylines_compute_win.py
@Time    :   2022/6/8
@Desc    :   专门用来计算paylines游戏中，每局图案的中奖情况。
'''
import pandas

DEBUG_ON = False
PACKAGE_NAME = 'paylines_compute_win'

def pprint(str):
    if DEBUG_ON:
        print(str)

# read pl and gl from excel
def get_pl_from_excel(excel_file_name):
    pl_list = []
    gl_list = []
    pl_need_num_list = [] # 该赔率需要的组合数
    data = pandas.read_excel(excel_file_name, names=None)
    pl_list = data.values[:, 0].tolist()
    gl_list = data.values[:, 1].tolist()
    pl_need_num_list = data.values[:, 4].tolist()
    sum_gl = sum(gl_list)
    if sum_gl > 1 or sum_gl < 0.5:
        pprint("****package:" + PACKAGE_NAME + "  ****funtion:get_pl_from_excel, total peilv is:" + str(sum_gl))
    return pl_list, gl_list, pl_need_num_list

# 以下数据只是为了说明数据格式，举例用的
# TUAN_PL_MAP = {
#     '9' :[0, 0, 0, 2, 5],
#     '10':[0, 0, 0, 5, 10],
#     'J' :[0, 0, 2, 10, 15],
#     'Q' :[0, 0, 0, 15, 20],
#     'K' :[0, 0, 5, 20, 30],
#     'A': [0, 0, 10, 25, 40],
#     'W': [0, 0, 15, 30, 50],
#     'S': [0, 0, 0, 2, 5],
# }
# for pay lines games only, compute the odd of actual single pay line
# the first tuan can't be 'W'
# single_pay_line_list = ['9', 'W', '9', '9', 'W']
# 返回3个参数:这条payline的第1个图案，连续图案数，这条payline的中奖金额
# private方法，仅供get_result_for_all_tuan调用
def compute_win_for_single_payline(single_pay_line_list, pl_map):
    lianxu_tuan_nums = 0    # 连续非'W'图案的个数
    lianxu_W_nums = 0       # 连续'W'图案的个数
    for value in single_pay_line_list:
        if value == single_pay_line_list[0] or value == 'W':
            lianxu_tuan_nums = lianxu_tuan_nums + 1
        else:
            break
    for i in range(lianxu_tuan_nums):
        if single_pay_line_list[i] == 'W':
            lianxu_W_nums = lianxu_W_nums + 1
        else:
            break
    pprint("****package:" + PACKAGE_NAME + "  ****funtion:compute_win_for_single_payline, 连续普通图案数量 is:" + str(lianxu_tuan_nums))
    pprint("****package:" + PACKAGE_NAME + "  ****funtion:compute_win_for_single_payline, 连续Wild图案数量 is:" + str(
        lianxu_tuan_nums))
    tuan = ''
    tuan_jiangjin = 0
    if lianxu_W_nums == lianxu_tuan_nums:
        tuan = 'W'
        jiangjin = pl_map.get('W')[lianxu_W_nums]
    else:
        tuan = single_pay_line_list[0]
        jiangjin = pl_map.get(single_pay_line_list[0])[lianxu_tuan_nums - 1]
    return [tuan, lianxu_tuan_nums, jiangjin]

######################################################
# 以下数据只是为了说明数据格式，举例用的
# ALL_TUAN = [['9','J','9','9','J'],
#             ['Q','10','K','A','S'],
#             ['Q','W','Q','9','10']]
# PAYLINES = [[(0,0), (2,1), (0,2), (2,3), (2,4)],
#             [(2,0), (0,1), (1,2), (2,3), (2,4)],
#             [(1,0), (2,1), (2,2), (2,3), (2,4)],
#             [(0,0), (0,1), (1,2), (2,3), (2,4)]]
# private方法，仅供get_result_for_all_tuan调用
# 根据所有图案和单条支付线，生成单条支付线的图案调用
# 返回结果: ['9', 'W', '9', '9', 'W']
def get_single_payline_from_all_tuan(all_tuan, single_payline):
    result = []
    for value in single_payline:
        result.append(all_tuan[value[0]][value[1]])
    return result

# public方法
# 根据所有图案，所有支付线和赔率表，得到中奖结果
# 输出结果：
# [[['K', 3, 5, 0]], 5] line0中奖了
# [[], 0]  没有payline中奖
def compute_win_for_all_tuan(all_tuan, paylines, pl_map):
    result = []
    total_odd = 0
    for index,payline in enumerate(paylines):
        single_payline_tuan = get_single_payline_from_all_tuan(all_tuan, payline)
        singleline_result = compute_win_for_single_payline(single_payline_tuan, pl_map)
        if singleline_result[2] > 0:
            singleline_result.append(index)
            result.append(singleline_result)  # 记录是第几条payline
            total_odd = total_odd + singleline_result[2]
    return [result,total_odd]

########################  以下是单元测试用到的代码 ########################
########################           测试用例1    ########################
UNIT_TEST_ALL_TUAN_LIST = [ ['9','9','9','9','J'],
                            ['Q','Q','W','A','S'],
                            ['A','W','A','A','10'],
                            ['9', 'Q', 'W', 'A', 'S'],
                            ['S', 'S', 'S', 'A', '10'],
                            ]

UNIT_TEST_TUAN_PL_MAP = {
                        '9' :[0, 0, 0, 2, 5],
                        '10':[0, 0, 0, 5, 10],
                        'J' :[0, 0, 2, 10, 15],
                        'Q' :[0, 0, 10, 15, 20],
                        'K' :[0, 0, 5, 20, 30],
                        'A': [0, 0, 10, 25, 40],
                        'W': [0, 0, 15, 30, 50],
                        'S': [0, 0, 0, 2, 5],}
UNIT_TEST_RESULT_LIST = [['9', 4, 2], ['Q', 3, 10],['A', 4, 25],['9', 1, 0],['S', 3, 0]]

def UNIT_TEST_compute_win_for_single_payline(tuan_list, pl_map, result_list):
    for i in range(len(result_list)):
        res = compute_win_for_single_payline(tuan_list[i], pl_map)
        assert res ==  result_list[i]

########################           测试用例2    ########################
UNIT_TEST_TUAN1 = [['K', '10', '9', 'J', '10'], ['9', 'W', 'Q', '9', 'K'], ['J', 'A', 'K', 'Q', 'S']]
# 每条支付线对应的矩阵坐标位置
UNIT_TEST_PAYLINES1 = [[(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],
                     [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
                     [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
                     [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4)],
                     [(2, 0), (2, 1), (1, 2), (2, 3), (2, 4)]]
UNIT_TEST_WIN_RESUT1 = [[['K', 3, 5, 0], ['K', 3, 5, 3]], 10]

UNIT_TEST_TUAN2 = [['10', 'J', 'W', 'K', 'A', 'W'], ['9', 'S', 'K', 'Q', 'J',  'Q'],
                   ['J', 'W', 'Q', '9', '10', 'J'], ['Q', '9', 'J', 'K', '10',  'A']]
# 每条支付线对应的矩阵坐标位置
UNIT_TEST_PAYLINES2 = [ [(1, 0), (3, 1), (0, 2), (3, 3), (0, 4), (2, 5)],
                        [(1, 0), (3, 1), (0, 2), (2, 3), (1, 4), (3, 5)],
                        [(2, 0), (0, 1), (0, 2), (2, 3), (0, 4), (2, 5)],
                        [(2, 0), (0, 1), (1, 2), (2, 3), (1, 4), (2, 5)],]
UNIT_TEST_WIN_RESUT2 = [[['9', 4, 2, 1], ['J', 3, 2, 2]], 4]
def UNIT_TEST_compute_win_for_all_tuan(all_tuan, paylines, pl_map, result):
    res = compute_win_for_all_tuan(all_tuan, paylines, pl_map)
    assert res == result

if __name__ == '__main__':

    print("****package:" + PACKAGE_NAME + "  ****funtion:main, 测试用例1")
    UNIT_TEST_compute_win_for_single_payline(UNIT_TEST_ALL_TUAN_LIST, UNIT_TEST_TUAN_PL_MAP, UNIT_TEST_RESULT_LIST)
    print("****package:" + PACKAGE_NAME + "  ****funtion:main, 测试用例2")
    UNIT_TEST_compute_win_for_all_tuan(UNIT_TEST_TUAN1, UNIT_TEST_PAYLINES1, UNIT_TEST_TUAN_PL_MAP, UNIT_TEST_WIN_RESUT1)
    UNIT_TEST_compute_win_for_all_tuan(UNIT_TEST_TUAN2, UNIT_TEST_PAYLINES2, UNIT_TEST_TUAN_PL_MAP,
                                       UNIT_TEST_WIN_RESUT2)
    # 测试读取excel
    EXCEL_NAME_READ_PV = r"d:py\\1.xlsx"
    # get_pl_from_excel(EXCEL_NAME_READ_PV)