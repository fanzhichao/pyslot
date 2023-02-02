import random
# for test
DEBUG_ON = True
PACKAGE_NAME = 'paylines_create_tuan'

def pprint(str):
    if DEBUG_ON:
        print(str)

# 下面的数据仅供测试用，不代表真实的数据
# 游戏包括哪些图案
TUAN_LIST = ['9', '10', 'J', 'Q', 'K', 'A', 'W', 'S']
# 每个REEL上各个图案对应的权重，下面的数据是5个REEL的情况
QUANZHONG_LIST_REELS = ((0, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0),
                        (50, 5, 25, 10, 20, 0, 0, 0),
                        (0, 5, 25, 10, 20, 0, 0, 0))

# tuan_num是指单个REEL上包含的图案总数，一般为3个
def create_one_reel_tuan(tuan_list, quanzhong_list,tuan_num):
    return random.choices(tuan_list, quanzhong_list, k=tuan_num)

# 创建一个二维数组，用来保存生成的矩阵图案
def create_array_by_rowandcol(row,col):
    data = []
    for i in range(row):
        row_data = []
        for j in range(col):
            row_data.append('X') # 默认用'X'图案填充整个图案矩阵
        data.append(row_data)
    return data

# 按照给定的权重随机生成一个矩阵图案
def create_all_tuan(tuan_list, quanzhong_list, row, col):
    reel_all_tuan = create_array_by_rowandcol(row, col)
    for index, value1 in enumerate(QUANZHONG_LIST_REELS):
        reel_tuan = create_one_reel_tuan(TUAN_LIST, value1, row)
        for j, value2 in enumerate(reel_tuan):
            reel_all_tuan[j][index] = value2
    return reel_all_tuan

# 根据当前的矩阵图案、中奖结果和支付线的位置，把中奖的图案替换为'X'，以便后续处理
def update_all_tuan_with_X(old_all_tuan, win_result,paylines):
    # 把所有中奖图案替换为 'X'
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_all_tuan_with_X, old tuan:"+str(old_all_tuan))
    for single_payline_win_result in win_result[0]:
        line_number = single_payline_win_result[-1]
        lianxu_tuan_nums = single_payline_win_result[1]
        single_payline = paylines[line_number]
        for index in range(lianxu_tuan_nums):
            i,j = single_payline[index]
            old_all_tuan[i][j] = 'X'
    # 记录每一个REEL有多少个'X'，然后生成相应的新图案，然后合成新的REEL
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_all_tuan_with_X, new tuan with 'X':"+str(old_all_tuan))
    return old_all_tuan

# 将标记为'X'的图案先删掉
# 然后'X'的图案上面的图案往下面掉落
# 接着生成新的图案，继续填补'X'图案被消除后留下的空间
def update_X_with_new_tuan(old_all_tuan_with_X, tuan_list, quanzhong_list):
    # 先将矩阵进行X Y转置，行和列换过来，从3 * 5 变成 5 * 3
    mid_all_tuan_with_X     = []    # 保存中间数据
    single_reel_tuan        = []    # 临时保存每个REEL上的数据
    rows = len(old_all_tuan_with_X)
    cols = len(old_all_tuan_with_X[0])
    for i in range(cols):
        single_reel_tuan = []
        for j in range(rows):
            single_reel_tuan.append(old_all_tuan_with_X[j][i])
        mid_all_tuan_with_X.append(single_reel_tuan)
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new matrix tuan:" + str(mid_all_tuan_with_X))

    # 生成新的随机图案，替换掉需要消除的图案，也就是被标记为'X'的图案
    # 这里需要注意的是，图案是依次向下跌落的。所以对一个REEL的数据进行处理时，要先倒着来
    mid_all_tuan_after_upate_X = [] # 保存中间数据，将'X'删掉后重新填充的图案矩阵
    for index, value in enumerate(mid_all_tuan_with_X): # 遍历每一个REEL
        reel_X_count = value.count('X')
        reel_tuan = []  # 用来保存填充后的每一个REEL的图案数据
        for i in range(len(value) - 1, -1, -1): # 倒着收集每个REEL上不为'X'的数据
            if 'X' != value[i]:
                reel_tuan.append(value[i])
        pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, old single reel:" + str(reel_tuan))
        if reel_X_count > 0:        # 如果这一列有'X'，即需要填充新的图案
            reel_add_tuan = create_one_reel_tuan(tuan_list, quanzhong_list[index], reel_X_count)
            reel_tuan.extend(reel_add_tuan)
        pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new single reel:" + str(reel_tuan))
        mid_all_tuan_after_upate_X.append(reel_tuan)
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new tuan after update X:" + str(mid_all_tuan_after_upate_X))

    # 重新转置，得到最终的新图案
    new_tuan = []
    single_row_tuan = []
    for j in range(rows - 1, -1, -1): # 在这里，再把每个REEL的数据倒过来
        single_row_tuan = []
        for i in range(cols):
            single_row_tuan.append(mid_all_tuan_after_upate_X[i][j])
        new_tuan.append(single_row_tuan)
    pprint("****package:"+PACKAGE_NAME + "  ****funtion:update_X_with_new_tuan, new tuan at last:" + str(new_tuan))
    return new_tuan

if __name__ == '__main__':
    create_all_tuan(TUAN_LIST, QUANZHONG_LIST_REELS, 3, 5)