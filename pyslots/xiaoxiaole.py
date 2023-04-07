import numpy as np
import os.path
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import requests
import random
import datetime
import pandas as pd
import copy

COL = 8
ROW = 5
TUAN_TYPE_LIST = [1, 2, 3, 4, 5, 6]
QUANZHONG_LIST_COL1 = (5, 5, 25, 10, 20, 4)

# 游戏包括哪些图案
# src_tuan_list = ['1', '2', '3', '4', '5', '6', '7', '8']
# 每个REEL上各个图案对应的权重，下面的数据是5个REEL的情况
# quanzhong_list        = (0, 5, 25, 10, 20, 0, 0, 0)
#  最终的输出结果类似: ['10', 'J',  'J'] 对应一个REEL上的图案。
def create_one_col(tuan_list, quanzhong_list, tuan_num):
    return random.choices(tuan_list, quanzhong_list, k=tuan_num)

def create_grid(tuanlist, quanzhonglist):
    tuan_list = []
    for i in range(COL):
        list1 = create_one_col(tuanlist, quanzhonglist, ROW)
        for j in range(ROW):
            tuan_list.append([i,j, list1[j], [i,j]])
    return tuan_list

def create_init_grid():
    tuan_list = []
    for i in range(COL):
        for j in range(ROW):
            if i >= 1 and j >= 1:
                while True:
                    type = random.choice(TUAN_TYPE_LIST)
                    left_cell = tuan_list[(i - 1)* ROW + j]
                    down_cell = tuan_list[i * ROW + j - 1]
                    if type != down_cell[2] and type != left_cell[2]:
                        tuan_list.append([i, j, type, [i, j]])
                        break
            elif i >=1:
                while True:
                    type = random.choice(TUAN_TYPE_LIST)
                    left_cell = tuan_list[(i - 1)* ROW + j]
                    if type != left_cell[2]:
                        tuan_list.append([i, j, type, [i, j]])
                        break
            elif j >=1:
                while True:
                    type = random.choice(TUAN_TYPE_LIST)
                    down_cell = tuan_list[i * ROW + j - 1]
                    if type != down_cell[2]:
                        tuan_list.append([i, j, type, [i, j]])
                        break
            else:
                type = random.choice(TUAN_TYPE_LIST)
                tuan_list.append([i, j, type, [i, j]])
    print("列表数量 {0}".format(len(tuan_list)))
    return tuan_list
def refresh_liantong(grid): # 标记联通区域
    for v in grid:
        i, j = v[0],v[1]
        if i >0 and j >0 and  v[2] == grid[(i - 1)* ROW + j][2] and v[2] == grid[i* ROW + j - 1][2]:
            left_cell = grid[(i - 1)* ROW + j]
            down_cell = grid[i* ROW + j - 1]
            left_cell_index = left_cell[3][0] * COL + left_cell[3][1]
            down_cell_index = down_cell[3][0] * COL + down_cell[3][1]
            if left_cell_index < down_cell_index:
                v[3] = grid[(i - 1) * ROW + j][3]
                grid[i * ROW + j - 1][3] = v[3]
            else:
                v[3] = grid[i * ROW + j - 1][3]
                grid[(i - 1) * ROW + j][3]= v[3]
        elif i > 0 and v[2] == grid[(i - 1)* ROW + j][2]:
            v[3] = grid[(i - 1)* ROW + j][3]
        elif j > 0 and v[2] == grid[i* ROW + j - 1][2]:
            v[3] = grid[i * ROW + j - 1][3]
    return grid


# 试着交换grid中的两个cell，看能否消除联通区域，会遍历所有可能的交换情况
#COL = 8  ROW = 5
def try_to_crush(grid):
    tmpgrid = copy.deepcopy(grid)
    res = []
    for i in range(COL):
        for j in range(ROW):
            cell  = tmpgrid[i * ROW + j]
            if i >= 1 and j >= 1:
                left_cell = tmpgrid[(i - 1) * ROW + j]
                tmp = left_cell[2]
                left_cell[2] = cell[2]
                cell[2] = tmp
                tmpgrid = refresh_liantong(tmpgrid)
                quyu_list = compute_liantong_area(tmpgrid, 0, 0, None)
                if len(quyu_list) > 0:
                    tt = copy.deepcopy(tmpgrid)
                    res.append(tt)
                # 换回来
                tmpgrid = copy.deepcopy(grid)

                down_cell = tmpgrid[i * ROW + j - 1]
                tmp = down_cell[2]
                down_cell[2] = cell[2]
                cell[2] = tmp
                tmpgrid = refresh_liantong(tmpgrid)
                quyu_list = compute_liantong_area(tmpgrid, 0, 0, None)
                if len(quyu_list) > 0:
                    tt = copy.deepcopy(tmpgrid)
                    res.append(tt)
                # 换回来
                tmpgrid = copy.deepcopy(grid)

            elif i >= 1:
                left_cell = tmpgrid[(i - 1) * ROW + j]
                tmp = left_cell[2]
                left_cell[2] = cell[2]
                cell[2] = tmp
                tmpgrid = refresh_liantong(tmpgrid)
                quyu_list = compute_liantong_area(tmpgrid, 0, 0, None)
                if len(quyu_list) > 0:
                    tt = copy.deepcopy(tmpgrid)
                    res.append(tt)
                # 换回来
                tmpgrid = copy.deepcopy(grid)

            elif j >= 1:
                down_cell = tmpgrid[i * ROW + j - 1]
                tmp = down_cell[2]
                down_cell[2] = cell[2]
                cell[2] = tmp
                tmpgrid = refresh_liantong(tmpgrid)
                quyu_list = compute_liantong_area(tmpgrid, 0, 0, None)
                if len(quyu_list) > 0:
                    tt = copy.deepcopy(tmpgrid)
                    res.append(tt)
                # 换回来
                tmpgrid = copy.deepcopy(grid)
    return res


# 返回类型
# 31  三个图案一列
# 32  三个图案一行
# 33  三个图案构成直角三角形
# 41  四个图案一列
# 42  四个图案一行
# 44  四个图案构成一个正方形
def get_liantong_area_type(area):
    area_num = len(area)
    if area_num == 3:
        cell1,cell2,cell3 = area[0],area[1],area[2]
        if cell1[0] == cell2[0] and cell1[0] == cell3[0]:
            return 31
        elif cell1[1] == cell2[1] and cell1[1] == cell3[1]:
            return 32
        else:
            return 33
    elif area_num == 4:
        cell1, cell2, cell3, cell4 = area[0], area[1], area[2], area[3]
        if cell1[0] == cell2[0] and cell3[0] == cell4[0] and cell2[0] == cell3[0]:
            return 41
        elif cell1[1] == cell2[1] and cell3[1] == cell4[1] and cell2[1] == cell3[1]:
            return 42
        elif sum([cell1[0], cell2[0], cell3[0], cell4[0]]) %2 ==0 and sum([cell1[1], cell2[1], cell3[1], cell4[1]]) %2 ==0:
            return 44
        else:
            return 40
    elif area_num >= 5:
        return 50
    return 0


# 根据输入grid，计算出该grid的所有联通区域，并根据输入的image，将联通区域按类型标记到image上
def compute_liantong_area(grid, offsetX,offsetY, toImage):
    num_list = [v[3] for v in grid]
    liantong_list = []
    for v in num_list:
        if v not in liantong_list:
            liantong_list.append(v)

    area_list = []
    for v in liantong_list:
        area = []
        for v1 in grid:
            if v == v1[3]:
                area.append(v1)
        type = get_liantong_area_type(area)
        if type > 30 and type != 33:
            area_list.append(area)
    #print("联通区域的个数 {0}".format(len(quyu_list)))
    #print(quyu_list)
    if toImage != None:
        img_frame1 = Image.open("C:\\u\\pic\\frame1.png")
        img_frame2 = Image.open("C:\\u\\pic\\frame2.png")
        img_frame3 = Image.open("C:\\u\\pic\\frame3.png")
        for i in range(ROW):
            for j in range(COL):
                jj = ROW - 1 -i
                ii = j
                cell = grid[ii* ROW +jj]
                for area in area_list:
                    if cell in area:
                        if len(area) >=5:
                            toImage.paste(img_frame1, (100*j  + offsetX, 100*i +offsetY))
                        elif len(area) >=4:
                            toImage.paste(img_frame2, (100 * j + offsetX, 100 * i+offsetY))
                        else:
                            toImage.paste(img_frame3, (100 * j + offsetX, 100 * i+offsetY))
    return area_list


#COL = 8  ROW = 5
def print_grid(grid):
    for i in range(ROW):
        for j in range(COL):
            jj = ROW - 1 -i
            ii = j
            print(grid[ii* ROW +jj], end = ' ')
        print("\n")
def draw_grid(grid):
    toImage = Image.new('RGB', (COL*100, ROW*100))
    img1 = Image.open("C:\\u\\pic\\1.png")
    img2 = Image.open("C:\\u\\pic\\2.png")
    img3 = Image.open("C:\\u\\pic\\3.png")
    img4 = Image.open("C:\\u\\pic\\4.png")
    img5 = Image.open("C:\\u\\pic\\5.png")
    img6 = Image.open("C:\\u\\pic\\6.png")
    img_list = [img1,img2,img3,img4,img5,img6]
    for i in range(ROW):
        for j in range(COL):
            jj = ROW - 1 -i
            ii = j
            cell = grid[ii* ROW +jj]
            img = img_list[cell[2] - 1]
            toImage.paste(img, (100*j, 100*i))

    compute_liantong_area(grid, 0, toImage)
    plt.imshow(toImage)
    plt.show()
def draw_2_grid(grid1,grid2,grid3,grid4):
    toImage = Image.new('RGB', (2*COL*100 + 100, 2*ROW*100 + 100))
    img1 = Image.open("C:\\u\\pic\\1.png")
    img2 = Image.open("C:\\u\\pic\\2.png")
    img3 = Image.open("C:\\u\\pic\\3.png")
    img4 = Image.open("C:\\u\\pic\\4.png")
    img5 = Image.open("C:\\u\\pic\\5.png")
    img6 = Image.open("C:\\u\\pic\\6.png")
    img_list = [img1,img2,img3,img4,img5,img6]
    for i in range(ROW):
        for j in range(COL):
            jj = ROW - 1 -i
            ii = j
            cell1 = grid1[ii* ROW +jj]
            img = img_list[cell1[2] - 1]
            toImage.paste(img, (100*j, 100*i))
            if grid2 != None:
                cell2 = grid2[ii* ROW +jj]
                img = img_list[cell2[2] - 1]
                toImage.paste(img, (100*j, 100*i + 100*ROW + 100))
            if grid3 != None:
                cell3 = grid3[ii* ROW +jj]
                img = img_list[cell3[2] - 1]
                toImage.paste(img, (100*j + 100 * COL + 100, 100*i ))
            if grid4 != None:
                cell4 = grid4[ii* ROW +jj]
                img = img_list[cell4[2] - 1]
                toImage.paste(img, (100*j+ 100 * COL + 100, 100*i + + 100*ROW + 100))

    compute_liantong_area(grid1, 0, 0, toImage)
    if grid2!= None:
        compute_liantong_area(grid2, 0, 600, toImage)
    if grid3!= None:
        compute_liantong_area(grid3, 900, 0, toImage)
    if grid4!= None:
        compute_liantong_area(grid4, 900, 600, toImage)
    plt.imshow(toImage)
    plt.show()

if __name__ == '__main__':
    #grid = create_grid(TUAN_TYPE_LIST, QUANZHONG_LIST_COL1)
    #print_grid(grid)
    #grid = refresh_liantong(grid)
    #print_grid(grid)
    #draw_grid(grid)

    grid1 = create_init_grid()
    grids = try_to_crush(grid1)
    num = len(grids)
    if num == 1:
        grid2_liantong = refresh_liantong(grids[0])
        draw_2_grid(grid1,grid2_liantong,None,None)
    elif num == 2:
        grid2_liantong = refresh_liantong(grids[0])
        grid3_liantong = refresh_liantong(grids[1])
        draw_2_grid(grid1,grid2_liantong,grid3_liantong,None)
    elif num >= 3:
        grid2_liantong = refresh_liantong(grids[0])
        grid3_liantong = refresh_liantong(grids[1])
        grid4_liantong = refresh_liantong(grids[2])
        draw_2_grid(grid1,grid2_liantong,grid3_liantong,grid4_liantong)

