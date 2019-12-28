import pickle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os


'''def get_point(str_points):
    list_point = []
    str_points_list = str_points.split('),(')
    for i in str_points_list:
        list_point.append(tuple(eval(i)))
    return list_point

os.makedirs



db = [['添加..',], [-1,]]
dbpath = "C:/Users/Cjay/PycharmProjects/Contour_marker/data/Material/mf-banefo.txt"
with open(dbpath) as f:
    i = 0
    lines = f.readlines()
    for line in lines:
        if line[0] !='#':
            if 'User_name' in line:
                print(line.split(' ')[-1][:-1])
                # self.user_name.setText(line.split(' ')[-1][:-2])
            elif 'Scale_type' in line:
                print(int(line.split(' ')[-1][:-1]))
                # self.scaleMode = int(line.split(' ')[-1][:-1])
            elif 'Scale_num' in line:
                scal_nums = line.split(' ')[-1][2:-3].split("','")

            elif 'Scale_points' in line:
                points = get_point(line.split(' ')[-1][2:-3])
                print(points)
        else:
            parts = line.split('-')
            rgba = eval(parts[1])
            color = QColor(rgba[0],rgba[1],rgba[2],rgba[3])
            height = parts[0][1:]
            line_type = parts[2]
            points = get_point(parts[3][2:-3])
'''
mystr = ''
mystr_list = mystr.split('),(')
print(mystr_list)