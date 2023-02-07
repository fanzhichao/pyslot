#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Frank
@License :   (C) Copyright 2019-2025, StarryFun
@Contact :   fanzhichao1983@gmail.com
@Software:   slot
@File    :   tools.py
@Time    :   2023/2/7 19:01
@Desc    :
'''

import pandas

DEBUG_ON = False
PACKAGE_NAME = 'tools'

def pprint(str):
    if DEBUG_ON:
        print(str)


# read pl and gl from excel
def get_pl_from_excel(excel_file_name):
    pl_list = []
    gl_list = []
    pl_need_num_list = []  # 该赔率需要的组合数
    data = pandas.read_excel(excel_file_name, names=None)
    pl_list = data.values[:, 0].tolist()
    gl_list = data.values[:, 1].tolist()
    pl_need_num_list = data.values[:, 4].tolist()
    sum_gl = sum(gl_list)
    if sum_gl > 1 or sum_gl < 0.5:
        pprint("****package:" + PACKAGE_NAME + "  ****funtion:get_pl_from_excel, total peilv is:" + str(sum_gl))
    return pl_list, gl_list, pl_need_num_list

if __name__ == '__main__':
    # 测试读取excel
    EXCEL_NAME_READ_PV = r"d:py\\1.xlsx"
    # get_pl_from_excel(EXCEL_NAME_READ_PV)