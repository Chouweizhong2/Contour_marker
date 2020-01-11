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
        self.enable_draw = False

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
        self.draw_all = 0
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
        if self.father.hide_map == 0:
            painter.drawPixmap(self.point, scaled_img)

        # 画点和线部分：
        show_points = None
        if self.draw_mod == -1:
            self.draw_line(painter, self.point_list_x)
            self.draw_line(painter, self.point_list_y)
        elif self.draw_mod == -2:
            self.draw_line(painter, self.point_list_x)
        elif self.draw_mod == -3:
            self.draw_line(painter, self.point_list_y)
        elif self.draw_mod >= 0:
            if self.draw_all == 1:
                for i in range(len(self.db[0])):
                    self.draw_line(painter, self.db[1][i],
                                   self.db[2][i][0],
                                   self.db[2][i][1])
            else:
                self.draw_line(painter, self.db[1][self.draw_mod],
                               self.db[2][self.draw_mod][0],
                               self.db[2][self.draw_mod][1])

    def draw_line(self, painter, show_points, color=QColor(0, 0, 0), pen_type='实线'):
        if show_points is None:
            return 0
        painter.setBrush(color)
        if pen_type == '实线':
            pen_type = Qt.SolidLine
        else:
            pen_type = Qt.DashLine
        pen = QPen(color, 1, pen_type)
        painter.setPen(pen)
        for i, pos in enumerate(show_points):
            cir_x = pos[0] / self.Mul_num + self.point.x() - 3
            cir_y = pos[1] / self.Mul_num + self.point.y() - 3
            painter.drawEllipse(cir_x, cir_y, 6, 6)
            if i != 0:
                start_x = show_points[i - 1][0] / self.Mul_num + self.point.x()
                start_y = show_points[i - 1][1] / self.Mul_num + self.point.y()
                end_x = pos[0] / self.Mul_num + self.point.x()
                end_y = pos[1] / self.Mul_num + self.point.y()
                painter.drawLine(start_x, start_y, end_x, end_y)
            if self.father.edit_mode == 0:
                start_x = show_points[-1][0] / self.Mul_num + self.point.x()
                start_y = show_points[-1][1] / self.Mul_num + self.point.y()
                end_x = show_points[0][0] / self.Mul_num + self.point.x()
                end_y = show_points[0][1] / self.Mul_num + self.point.y()
                painter.drawLine(start_x, start_y, end_x, end_y)

    def checkEvents_scale(self):
        if self.draw_mod == -2:
            if len(self.point_list_x) == 2:
                self.father.scale_changed('xok')
        if self.draw_mod == -3:
            if len(self.point_list_y) == 2:
                self.father.scale_changed('yok')

    def mouseMoveEvent(self, e):  # 重写移动事件
        if e.buttons() == Qt.MidButton:
            # if self.left_click:
            self._endPos = e.pos() - self._startPos
            self.point = self.point + self._endPos
            self._startPos = e.pos()
            self.repaint()
        else:
            orgx = self.pix.size().width()
            orgy = self.pix.size().height()
            abs_pos_x = e.x() - self.point.x()
            abs_pos_y = e.y() - self.point.y()
            if 0 < abs_pos_x < orgx / self.Mul_num and 0 < abs_pos_y < orgy / self.Mul_num:
                self.father.abspos_Label.setText('坐标 (' + str(round(abs_pos_x * self.Mul_num, 6))
                                                 + ',' + str(round(abs_pos_y * self.Mul_num, 6)) + ')')
            else:
                self.father.abspos_Label.setText('坐标 出界')

    def mousePressEvent(self, e):
        if e.button() == Qt.MidButton:
            self._startPos = e.pos()
        if self.father.edit_mode == 1:
            if e.button() == Qt.LeftButton:  # 添加点
                self.add_point(e)
                self.father.change_saved = 0
            elif e.button() == Qt.RightButton:  # 删除点
                self.remove_point()
                self.father.change_saved = 0

    def add_point(self, e):
        if self.draw_mod == -2 and len(self.point_list_x) < 2:
            newpos = (e.pos() - self.point) * self.Mul_num
            self.point_list_x.append((newpos.x(), newpos.y()))
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()
            self.checkEvents_scale()
        if self.draw_mod == -3 and len(self.point_list_y) < 2:
            newpos = (e.pos() - self.point) * self.Mul_num
            self.point_list_y.append((newpos.x(), newpos.y()))
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()
            self.checkEvents_scale()
        elif self.draw_mod >= 0 and self.db[1] != -1:
            newpos = (e.pos() - self.point) * self.Mul_num
            self.db[1][self.draw_mod].append((newpos.x(), newpos.y()))
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()

    def remove_point(self):
        if self.draw_mod == -2 and len(self.point_list_x) > 0:
            self.father.scaleTable.setItem(0, 0, None)
            self.point_list_x.pop()
            self.repaint()
        if self.draw_mod == -3 and len(self.point_list_y) > 0:
            self.father.scaleTable.setItem(0, 1, None)
            self.point_list_y.pop()
            self.repaint()
        elif self.draw_mod >= 0 and len(self.db[1][self.draw_mod]) > 0:
            self.db[1][self.draw_mod].pop()
            print("pop success")
            self.repaint()

    def mouseReleaseEvent(self, e):
        pass

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            # 放大图片
            pos_x = (e.x() - self.point.x()) * 0.1 / (self.Mul_num - 0.1)
            pos_y = (e.y() - self.point.y()) * 0.1 / (self.Mul_num - 0.1)
            if self.Mul_num > 0.3:
                self.Mul_num -= 0.10
                self.point.setX(self.point.x() - pos_x)
                self.point.setY(self.point.y() - pos_y)
                self.repaint()

        elif e.angleDelta().y() < 0:
            # 缩小图片
            pos_x = (e.x() - self.point.x()) * 0.1 / (self.Mul_num + 0.1)
            pos_y = (e.y() - self.point.y()) * 0.1 / (self.Mul_num + 0.1)
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
