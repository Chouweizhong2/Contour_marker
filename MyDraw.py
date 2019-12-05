import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2


class MyDraw(QWidget):
    def __init__(self):
        print('init my Draw')
        QWidget.__init__(self)
        # self.setupUi(self)
        self.resize(800, 600)
        '''filename = r"C:/Users/Cjay/PycharmProjects/Contour_marker/data/Material/mc-enep.jpg"
        cvIm = cv2.imread(filename, -1)  # 通过Opencv读入一张图片
        image_height, image_width, image_depth = cvIm.shape  # 获取图像的高，宽以及深度。
        print(image_height, image_width)
        # QIm = cv2.cvtColor(Im, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        QIm = QImage(cvIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                     image_width * image_depth,
                     QImage.Format_RGB888).rgbSwapped()
        self.pix = QPixmap.fromImage(QIm)
        self.scaled_size = self.size()
        self.scaled_img = self.pix.scaled(self.scaled_size)'''
        self.pix = QPixmap(800, 600)
        self.pix.fill(QColor(255, 255, 255))
        self.point = QPoint(0, 0)
        self.endPoint = QPoint()
        self.lastPoint = QPoint()
        self.painter = QPainter()
        # ==========data
        self.Mul_num = 1
        self.draw_mod = -1
        self.point_list = []
        self.db = None

    def paintEvent(self, event):
        '''self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.pix)
        self.painter.end()'''

        painter = QPainter()
        painter.begin(self)
        self.draw_img(painter)
        painter.end()

    def draw_img(self, painter):
        orgx = self.pix.size().width()

        orgy = self.pix.size().height()
        scaled_size = QSize(orgx / self.Mul_num, orgy / self.Mul_num)
        scaled_img = self.pix.scaled(scaled_size)
        painter.drawPixmap(self.point, scaled_img)
        show_points = None
        if self.draw_mod == -1:
            show_points = self.point_list
        elif self.draw_mod >= 0 and self.db[1][self.draw_mod] != -1:
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
        '''if e.button() == Qt.RightButton:
            self.point = QPoint(0, 0)
            self.scaled_img = self.pix.scaled(self.size())
            self.repaint()'''

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            # 放大图片
            # self.scaled_size = QSize(self.scaled_size.width()-15, self.scaled_size.height()-15)
            self.Mul_num -= 0.15
            # new_w = e.x() - (self.pix.width()/self.Mul_num * (e.x() -
            # self.point.x())) / (self.pix.width()/self.Mul_num + self.pix.width()/self.Mul_num*15)
            # new_h = e.y() - (self.pix.height()/self.Mul_num * (e.y() -
            # self.point.y())) / (self.pix.height()/self.Mul_num + self.pix.width()/self.Mul_num*15)
            # self.point = QPoint(new_w, new_h)
            self.repaint()

        elif e.angleDelta().y() < 0:
            # 缩小图片
            self.Mul_num += 0.15
            # self.scaled_size = QSize(self.scaled_size.width() + 15, self.scaled_size.height() + 15)
            # new_w = e.x() - (self.pix.width()/self.Mul_num * (e.x() -
            # self.point.x())) / (self.pix.width()/self.Mul_num - self.pix.width()/self.Mul_num*0.15)
            # new_h = e.y() - (self.pix.height()/self.Mul_num * (e.y() -
            # self.point.y())) / (self.pix.height()/self.Mul_num - self.pix.width()/self.Mul_num*15)
            # self.point = QPoint(new_w, new_h)
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
