import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

#qtCreatorFile = "d:/2D_draw_scrawl.ui"

#Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)


class MyDraw(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pix = QPixmap(800, 600)
        self.pix.fill(QColor(255, 255, 255))
        self.endPoint = QPoint()
        self.lastPoint = QPoint()
        self.painter = QPainter()

    def paintEvent(self, event):
        #a = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.pix)
        self.painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.endPoint = self.lastPoint

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:       # 这里只能用buttons(), 因为button()在mouseMoveEvent()中无论
            self.endPoint = event.pos()            # 按下什么键，返回的都是Qt::NoButton
            self.painter.begin(self.pix)        # 注意这里的参数必须是self.pix，涂鸦只能在这个300*300的白板上进行
            self.painter.setPen(QColor(0, 255, 0))
            self.painter.drawLine(self.lastPoint, self.endPoint)
            self.painter.end()
            self.update()
            self.lastPoint = self.endPoint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            self.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyDraw()
    window.show()
    sys.exit(app.exec_())
