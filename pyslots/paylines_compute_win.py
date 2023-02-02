
import pandas

DEBUG_ON = False
PACKAGE_NAME = 'paylines_compute_win'

# read pl and gl from excel
def get_pl_from_excel(excel_file_name):
    pl_list = []
    gl_list = []
    data = pandas.read_excel(excel_file_name, names=None)
    pl_list = data.values[:, -2].tolist()
    gl_list = data.values[:, -1].tolist()
    sum_gl = sum(gl_list)
    if sum_gl > 1 or sum_gl < 0.5:
        if DEBUG_ON:
            print(PACKAGE_NAME +": the sum of gl is wrong, result: " + str(sum_gl))
    return pl_list, gl_list

TUAN_PL_MAP = {
    '9' :[0, 0, 0, 2, 5],
    '10':[0, 0, 0, 5, 10],
    'J' :[0, 0, 2, 10, 15],
    'Q' :[0, 0, 0, 15, 20],
    'K' :[0, 0, 5, 20, 30],
    'A': [0, 0, 10, 25, 40],
    'W': [0, 0, 15, 30, 50],
    'S': [0, 0, 0, 2, 5],
}
# for pay lines games only, compute the odd of actual single pay line
# the first tuan can't be 'W'
# single_pay_line_list = ['9', 'W', '9', '9', 'W']
# 返回3个参数:第1个图案，连续图案数，这条payline的中奖金额
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
    if DEBUG_ON:
        print(str(lianxu_tuan_nums))
        print(str(lianxu_W_nums))
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
ALL_TUAN = [['9','J','9','9','J'],
            ['Q','10','K','A','S'],
            ['Q','W','Q','9','10']]
PAYLINES = [[(0,0), (2,1), (0,2), (2,3), (2,4)],
            [(2,0), (0,1), (1,2), (2,3), (2,4)],
            [(1,0), (2,1), (2,2), (2,3), (2,4)],
            [(0,0), (0,1), (1,2), (2,3), (2,4)]]
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

if __name__ == '__main__':
    EXCEL_NAME_READ_PV = r"d:py\\1.xlsx"
    singlelist = ['9','9','9','9','10']
    singlelist = ['9', 'W', '9', '9', 'W']
    r = compute_win_for_single_payline(singlelist, TUAN_PL_MAP)
    #print(str(r))

    r = get_single_payline_from_all_tuan(ALL_TUAN, PAYLINES[0])
    #print(str(r))

    r = compute_win_for_all_tuan(ALL_TUAN, PAYLINES, TUAN_PL_MAP)
    print(str(r))
    # get_pl_from_excel(EXCEL_NAME_READ_PV)