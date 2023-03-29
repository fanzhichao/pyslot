#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   tools.py
@Time    :   2023/2/7 19:01
@Desc    :   工具类
'''
import sys
import json
import pandas
import codecs
import requests
import time
from copy import copy, deepcopy
from colored_logs.logger import Logger, LogType

DEBUG_ON = False
PACKAGE_NAME = 'tools'
OUT_PUT_TO_GO_FILE = r"C:\\u\\doc\\game20001.go"

log = Logger(ID=PACKAGE_NAME)
def print_success(str):
    if DEBUG_ON:
        log.success(str)


# 从excel表中读取赔率(pv)和概率(gl)数据，以及每个赔率需要生成的组合总数
def get_pl_from_excel(excel_file_name):
    pl_list = []
    gl_list = []
    pl_need_num_list = []  # 该赔率需要的组合数
    data = pandas.read_excel(excel_file_name, names=None)
    # 依次读取第1、2、5列，注意：excel的内容必须与之对应
    pl_list             = data.values[:, 0].tolist()
    gl_list             = data.values[:, 1].tolist()
    pl_need_num_list    = data.values[:, 4].tolist()
    sum_gl = sum(gl_list)
    # 各个赔率的概率总和应该在0.95-1之间
    if sum_gl > 1 or sum_gl < 0.95:
        print_success("get_pl_from_excel, 总赔率不正常 is:" + str(sum_gl))
    return pl_list, gl_list, pl_need_num_list


# 创建一个二维数组，用来保存生成的图案矩阵，每个图案的初始值都是'X'
def create_array_by_rowandcol(row,col):
    data = []
    for i in range(row):
        row_data = []
        for j in range(col):
            row_data.append('X') # 默认用'X'图案填充整个图案矩阵
        data.append(row_data)
    return data

# tuan_matrix， 需要被转置的矩阵
# reverse_reel，在翻转矩阵前，是否需要先将每列的图案倒过来
# 在paylines_create_tuan.py的update_X_with_new_tuan方法中，
# 需要将一个REEL先倒过来,再转置
def swap_matrix(tuan_matrix, reverse_reel = False):
    rows = len(tuan_matrix)
    cols = len(tuan_matrix[0])
    if reverse_reel:
        tuan_matrix = [row[::-1] for row in tuan_matrix]
    new_tuan_matrix = []
    for i in range(cols):
        single_row_tuan = []
        for j in range(rows):
            single_row_tuan.append(tuan_matrix[j][i])
        new_tuan_matrix.append(single_row_tuan)
    return new_tuan_matrix

# 这个方法处理的是包含header的tuan_matrix，其中header放在tuan_matrix最后
# 和上面方法的区别是，它会把header中的元素提取出来，放在对应REEL的最后面
def swap_matrix_with_header(tuan_matrix):
    # 一般来讲，Header比下面的matrix要少两列，所以给它的前后都补上一个'X'
    header = ['X']+tuan_matrix[-1]+['X']
    tuan_matrix_without_header = tuan_matrix[:-1:1]
    new_matrix_without_header = swap_matrix(tuan_matrix_without_header, False)
    for reel_index in range(len(new_matrix_without_header)):
        # 为'X'则代表是上面新加的元素，这个不用加到REEL对应的列里面
        if header[reel_index] != 'X':
            new_matrix_without_header[reel_index].append(header[reel_index])
    return new_matrix_without_header

# 将src_list中的值为old的元素替换为replace
def list_replace(src_list, old, replace):
    src_list = [replace if x == old else x for x in src_list]
    return src_list


# 看pl（随机生成的图案矩阵的最终赔率）是否满足需要
# 满足的条件是：它与赔率数组（excel中指定的所有赔率）中指定的某个元素对应的赔率相差不大
# 相差不大的条件是：在其0.8 - 1.2倍左右，具体是由PV_MIN 和 PV_MAX来定的
def pl_is_match(pl, pl_to_match_list, index,pl_min,pl_max):
    if index == 0:
        return False
    elif index == len(pl_to_match_list) - 1:
        if pl < pl_max * pl_to_match_list[-1] and pl > pl_to_match_list[-1]:
            return  True
    else:
        if pl > pl_min * pl_to_match_list[index] and pl < pl_max * pl_to_match_list[index]:
            return  True
    return False

# 将指定组合保存到go文件中
def save_to_go(go_filename, data):
    with codecs.open(go_filename, 'w+', encoding='utf-8') as f:
        f.writelines(str("package fruit_party") + '\n')
        f.writelines('\n')
        f.writelines(str("import \"fmt\"") + '\n')
        f.writelines('\n')
        f.writelines(str("func main() {") + '\n')
        f.writelines(str("    // 里面包含单条中奖支付线需要的数据") + '\n')
        f.writelines(str("    type PayLine struct{") + '\n')
        f.writelines(str("        TuanSingle   string  `json:\"tuan_single\"`     // 中奖的图案，如\"A\"") + '\n')
        f.writelines(str("        TuanNum      int     `json:\"tuan_num\"`        // 图案的连续数，如 2 代表有两个连续的\"A\"") + '\n')
        f.writelines(str("        TuanWin      float32 `json:\"tuan_win\"`        // 图案的中奖金额") + '\n')
        f.writelines(str("        PayLineIndex int     `json:\"pay_line_index\"`  // 这条支付线的index，从0开始") + '\n')
        f.writelines(str("    }") + '\n')
        f.writelines('\n')
        f.writelines(str("    type WinResult struct{") + '\n')
        f.writelines(str("        TotalWin    float32    `json:\"total_win\"`     // 总的中奖金额") + '\n')
        f.writelines(str("        PayLinesWin []PayLine  `json:\"pay_lines_win\"` // 保存每条中奖支付线的信息") + '\n')
        f.writelines(str("        TuanMatrix  [][]string `json:\"tuan_matrix\"`   // 保存所有的图案数据") + '\n')
        f.writelines(str("    }") + '\n')
        f.writelines('\n')
        f.writelines(str("    data := make(map[string][]WinResult)") + '\n')
        save_data_to_go(f, data)


def save_data_to_go(f, data):
    print_success(data)
    for i, value in enumerate(data):
        for j,v in enumerate(value):
            total_win       = v[0][0]
            pay_lines_win   = v[0][1]
            tuan_matrix     = v[1]
            f.writelines(formate_one_result(i,j,total_win, pay_lines_win, tuan_matrix) + '\n')
        str_end_format = "    data[\"{0}\"] = winResults{1}"
        str_end = str_end_format.format(i, i)
        f.writelines(str_end + '\n')
        f.writelines('\n')

    str1 = str("    fmt.Println(data[\"0\"])") + '\n'
    f.writelines(str1)
    str1 = str("    fmt.Println(data[\"0\"][0].TotalWin)") + '\n'
    f.writelines(str1)

    f.writelines(str("}") + '\n')
    #f.close()

def save_data_to_txt(f,data):
    for i, value in enumerate(data):
        for j, v in enumerate(value):
            total_win       = v[0][0]
            pay_lines_win   = v[0][1]
            tuan_matrix     = v[1]
            print(formate_one_result_txt(i,total_win, pay_lines_win, tuan_matrix) + '\n')
            f.writelines(formate_one_result_txt(i,total_win, pay_lines_win, tuan_matrix) + '\n')
            #f.writelines(formate_one_result_txt(i,total_win, pay_lines_win, tuan_matrix) + '\n')

def formate_one_result(i,j, total_win, pay_lines_win, tuan_matrix):
    str_beg_format = "    winResults{0}[{1}] = WinResult"
    str_beg = str_beg_format.format(i,j)
    res = str_beg+"{"+str(total_win)+","+format_go_pay_lines(pay_lines_win)+","+format_go_tuan_matrix(tuan_matrix)+"}"
    print_success(res)
    return res

# {"group":0,"total_win":0,"pay_lines_win":[{"tuan_single":"A","tuan_num":2,"tuan_win":0.2,"pay_line_index":5},{"tuan_single":"A","tuan_num":2,"tuan_win":0.2,"pay_line_index":14},{"tuan_single":"A","tuan_num":2,"tuan_win":0.2,"pay_line_index":20}],"tuan_matrix":[["G","D","C","G","H"],["A","E","H","B","D"],["E","A","B","E","E"]]}
def formate_one_result_txt(i, total_win, pay_lines_win, tuan_matrix):
    str_format = "\"group\":{0},\"total_win\":{1},\"pay_lines_win\":{2},\"tuan_matrix\":{3}"
    str = str_format.format(i,total_win,format_go_pay_lines_txt(pay_lines_win),format_go_tuan_matrix_txt(tuan_matrix))
    print_success(str)
    return "{"+str+"}"

# return []Pay_Line{Pay_Line{"J", 3, 8.1, 0}, Pay_Line{"Q", 3, 6.2,2}}
def format_go_pay_lines(pay_lines_list):
    print_success(pay_lines_list)
    str_beg = "[]PayLine{"
    str_end = "}"
    str_pay_line = "PayLine{kuohao1}\"{tuan}\",{tuan_num},{win},{payline_index}{kuohao2}"
    mid_str = ""
    if len(pay_lines_list) < 1:
        return "[]PayLine{}"
    else:
        for i,v in enumerate(pay_lines_list):
            if i != len(pay_lines_list) - 1:
                mid_str = mid_str + str_pay_line.format(kuohao1="{",kuohao2 = "},",\
                tuan = v[0], tuan_num = v[1], win = v[2], payline_index = v[3])
            else:
                mid_str = mid_str + str_pay_line.format(kuohao1="{",kuohao2 = "}",\
                tuan = v[0], tuan_num = v[1], win = v[2], payline_index = v[3])


        print_success(str_beg + mid_str + str_end)
        return(str_beg + mid_str + str_end)

def format_go_pay_lines_txt(pay_lines_list):
    str_beg = "["
    str_end = "]"
    str_pay_line = "\"tuan_single\":\"{tuan}\",\"tuan_num\":{tuan_num},\"tuan_win\":{win},\"pay_line_index\":{payline_index}"
    mid_str = ""
    if len(pay_lines_list) < 1:
        return "[]"
    else:
        for i,v in enumerate(pay_lines_list):
            if i != len(pay_lines_list) - 1:
                mid_str = mid_str + "{"+ str_pay_line.format(kuohao1="{",kuohao2 = "},",\
                tuan = v[0], tuan_num = v[1], win = v[2], payline_index = v[3]) + "},"
            else:
                mid_str = mid_str  + "{" + str_pay_line.format(kuohao1="{",kuohao2 = "}",\
                tuan = v[0], tuan_num = v[1], win = v[2], payline_index = v[3]) + "}"

        mid_str = mid_str
        print_success(str_beg + mid_str + str_end)
        return(str_beg + mid_str + str_end)

# return  [][]string{{"J", "J", "J","J", "J"}, {"J", "J", "J","J", "J"}, {"J", "J", "J","J", "J"}}
def format_go_tuan_matrix(tuan_matrix):
    str = "[][]string{kuohao1}\"{a00}\",\"{a01}\",\"{a02}\",\"{a03}\",\"{a04}\"{kuohao2}\"{a10}\",\"{a11}\",\"{a12}\",\"{a13}\",\"{a14}\"{kuohao2}\"{a20}\",\"{a21}\",\"{a22}\",\"{a23}\",\"{a24}\"{kuohao3}"
    res = str.format(kuohao1 = "{{", a00=tuan_matrix[0][0], a01=tuan_matrix[0][1], a02=tuan_matrix[0][2], \
        a03=tuan_matrix[0][3], a04=tuan_matrix[0][4], kuohao2="},{",a10=tuan_matrix[1][0], a11=tuan_matrix[1][1],\
        a12=tuan_matrix[1][2], a13=tuan_matrix[1][3], a14=tuan_matrix[1][4],a20=tuan_matrix[2][0], a21=tuan_matrix[2][1],\
        a22=tuan_matrix[2][2], a23=tuan_matrix[2][3], a24=tuan_matrix[2][4],kuohao3 ="}}")
    print_success(res)
    print_success(res)
    return res

def format_go_tuan_matrix_txt(tuan_matrix):
    str = "{kuohao1}\"{a00}\",\"{a01}\",\"{a02}\",\"{a03}\",\"{a04}\"{kuohao2}\"{a10}\",\"{a11}\",\"{a12}\",\"{a13}\",\"{a14}\"{kuohao2}\"{a20}\",\"{a21}\",\"{a22}\",\"{a23}\",\"{a24}\"{kuohao3}"
    res = str.format(kuohao1 = "[[", a00=tuan_matrix[0][0], a01=tuan_matrix[0][1], a02=tuan_matrix[0][2], \
        a03=tuan_matrix[0][3], a04=tuan_matrix[0][4], kuohao2="],[",a10=tuan_matrix[1][0], a11=tuan_matrix[1][1],\
        a12=tuan_matrix[1][2], a13=tuan_matrix[1][3], a14=tuan_matrix[1][4],a20=tuan_matrix[2][0], a21=tuan_matrix[2][1],\
        a22=tuan_matrix[2][2], a23=tuan_matrix[2][3], a24=tuan_matrix[2][4],kuohao3 ="]]")
    print_success(res)
    print_success(res)
    return res
########################  以下是单元测试用到的代码 ########################
########################           测试用例1    ########################
UNIT_TEST_MATRIX = [ ['9','S','K','9','J'],
                     ['J','Q','10','A','S'],
                     ['A','W','A','Q','10']]
UNIT_TEST_MATRIX_SWAP              = [['9','J','A'],
                                     ['S','Q','W'],
                                     ['K','10','A'],
                                     ['9','A','Q'],
                                     ['J','S','10']]
UNIT_TEST_MATRIX_SWAP_REVERSE_REEL = [['J','S','10'],
                                     ['9','A','Q'],
                                     ['K','10','A'],
                                     ['S','Q','W'],
                                     ['9','J','A']]
UNIT_TEST_MATRIX_WITH_HEADER = [ ['9','S','K','9','J'],
                                 ['J','Q','10','A','S'],
                                 ['A','W','A','Q','10'],
                                    ['10','J','Q']]
UNIT_TEST_MATRIX_WITH_HEADER_SWAP = [['9','J','A'],
                                     ['S','Q','W','10'],
                                     ['K','10','A','J'],
                                     ['9','A','Q','Q'],
                                     ['J','S','10']]

def UNIT_TEST_swap_matrix(tuan_matrix, reverse_reel,result):
    new_tuan_matrix = swap_matrix(tuan_matrix, reverse_reel)
    assert new_tuan_matrix == result

def UNIT_TEST_swap_matrix_with_header(tuan_matrix, result):
    new_tuan_matrix = swap_matrix_with_header(tuan_matrix)
    assert new_tuan_matrix == result

if __name__ == '__main__':
    # 测试读取excel
    EXCEL_NAME_READ_PV = r"d:py\\1.xlsx"
    # get_pl_from_excel(EXCEL_NAME_READ_PV)
    UNIT_TEST_swap_matrix(UNIT_TEST_MATRIX, False, UNIT_TEST_MATRIX_SWAP)
    UNIT_TEST_swap_matrix(UNIT_TEST_MATRIX, True, UNIT_TEST_MATRIX_SWAP_REVERSE_REEL)
    UNIT_TEST_swap_matrix_with_header(UNIT_TEST_MATRIX_WITH_HEADER, UNIT_TEST_MATRIX_WITH_HEADER_SWAP)
    #save_to_go(OUT_PUT_TO_GO_FILE, '')
    matrix =  [['B', 'F', 'G', 'F', 'G'], ['F', 'H', 'E', 'C', 'E'], ['F', 'G', 'A', 'B', 'G']]
    format_go_tuan_matrix(matrix)
    p_l = [['E', 3, 4, 3], ['E', 3, 4, 21]]
    format_go_pay_lines(p_l)

