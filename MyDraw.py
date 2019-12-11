import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Main import MainWindow
import cv2


class MyDraw(QWidget):
    def __init__(self, main_window: MainWindow):
        self.father = main_window
        print('init my Draw')
        QWidget.__init__(self)
        # self.setupUi(self)
        self.resize(800, 600)
        self.pix = QPixmap(800, 600)
        self.pix.fill(QColor(255, 255, 255))
        self.point = QPoint(0, 0)
        self.endPoint = QPoint()
        self.lastPoint = QPoint()
        self.painter = QPainter()

        # ==========data
        self.Mul_num = 1
        '''Draw mod:
        0-n:对应等高线
        -1 :单比例尺
        -2 :x比例尺
        -3 :y比例尺
        -10：等待
        '''
        self.draw_mod = -10
        self.point_list = []
        self.point_list_x = []
        self.point_list_y = []
        self.db = None

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_img(painter)
        painter.end()

    def draw_img(self, painter):
        # 画地图部分缩放:
        orgx = self.pix.size().width()
        orgy = self.pix.size().height()
        scaled_size = QSize(orgx / self.Mul_num, orgy / self.Mul_num)
        scaled_img = self.pix.scaled(scaled_size)
        painter.drawPixmap(self.point, scaled_img)

        # 画点和线部分：
        show_points = None
        if self.draw_mod == -1:
            show_points = self.point_list
        elif self.draw_mod == -2:
            show_points = self.point_list_x
        elif self.draw_mod == -3:
            show_points = self.point_list_y
        elif self.draw_mod >= 0:
            show_points = self.db[1][self.draw_mod]
        else:
            show_points = []
        for i, pos in enumerate(show_points):
            cir_x = pos[0] / self.Mul_num + self.point.x() - 5
            cir_y = pos[1] / self.Mul_num + self.point.y() - 5
            painter.drawEllipse(cir_x, cir_y, 10, 10)
            if i != 0:
                start_x = show_points[i - 1][0] / self.Mul_num + self.point.x()
                start_y = show_points[i - 1][1] / self.Mul_num + self.point.y()
                end_x = pos[0] / self.Mul_num + self.point.x()
                end_y = pos[1] / self.Mul_num + self.point.y()
                painter.drawLine(start_x, start_y, end_x, end_y)

    def checkEvents222(self):
        if self.draw_mod == -1:
            if len(self.point_list) == 2:
                print('self.draw_mod', self.draw_mod)
                self.father.scaleClicked('ok')
        if self.draw_mod == -2:
            if len(self.point_list_x) == 2:
                self.father.scaleClicked('xok')
        if self.draw_mod == -3:
            if len(self.point_list_y) == 2:
                self.father.scaleClicked('yok')

    def mouseMoveEvent(self, e):  # 重写移动事件
        if e.buttons() == Qt.MidButton:
            # if self.left_click:
            self._endPos = e.pos() - self._startPos
            self.point = self.point + self._endPos
            self._startPos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.MidButton:
            self._startPos = e.pos()
        elif e.button() == Qt.LeftButton:  # 添加点
            self.add_point(e)
        elif e.button() == Qt.RightButton:  # 删除点
            self.remove_point()

    def add_point(self, e):
        if self.draw_mod == -1 and len(self.point_list) < 2:
            newpos = (e.pos() - self.point) * self.Mul_num
            self.point_list.append((newpos.x(), newpos.y()))
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()
        if self.draw_mod == -2 and len(self.point_list) < 2:
            newpos = (e.pos() - self.point) * self.Mul_num
            self.point_list_x.append((newpos.x(), newpos.y()))
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()
        if self.draw_mod == -3 and len(self.point_list) < 2:
            newpos = (e.pos() - self.point) * self.Mul_num
            self.point_list_y.append((newpos.x(), newpos.y()))
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()
        elif self.draw_mod >= 0 and self.db[1] != -1:
            newpos = (e.pos() - self.point) * self.Mul_num
            self.db[1][self.draw_mod].append((newpos.x(), newpos.y()))
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()

    def remove_point(self):
        if self.draw_mod == -1 and len(self.point_list) > 0:
            self.point_list.pop()
            self.repaint()
        elif self.draw_mod >= 0 and len(self.db[1][self.draw_mod]) > 0:
            self.self.db[1][self.draw_mod].pop()
            self.repaint()

    def mouseReleaseEvent(self, e):
        self.checkEvents222()

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            # 放大图片
            pos_x = (e.x() - self.point.x()) * 0.1/(self.Mul_num-0.1)
            pos_y = (e.y() - self.point.y()) * 0.1/(self.Mul_num-0.1)
            self.Mul_num -= 0.10
            self.point.setX(self.point.x() - pos_x)
            self.point.setY(self.point.y() - pos_y)
            self.repaint()

        elif e.angleDelta().y() < 0:
            # 缩小图片
            pos_x = (e.x() - self.point.x()) * 0.1/(self.Mul_num+0.1)
            pos_y = (e.y() - self.point.y()) * 0.1/(self.Mul_num+0.1)
            self.Mul_num += 0.10
            self.point.setX(self.point.x() + pos_x)
            self.point.setY(self.point.y() + pos_y)
            self.repaint()

    def resizeEvent(self, e):
        if self.parent is not None:
            if self.pix.size().height() > self.pix.size().width():
                self.Mul_num = self.pix.size().width() / self.size().width()
            else:
                self.Mul_num = self.pix.size().width() / self.size().width()
            # self.scaled_img = self.pix.scaled(self.size())
            self.point = QPoint(0, 0)
            self.update()
