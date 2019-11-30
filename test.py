# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
'''

from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


class UI_Main(QWidget):
    def __init__(self):
        super(UI_Main, self).__init__()
        self.setWindowTitle('主窗口')


def Main():
    app = QtWidgets.QApplication(sys.argv)
    u = UI_Main()
    u.show()
    time.sleep(10000)
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    d = QtWidgets.DialogUI()
    d.show()
    # Main()
    # 使用qdarkstyle渲染模式
    app.setStyleSheet(QtWidgets.qdarkstyle.load_stylesheet_pyqt5())
    sys.exit(app.exec())
'''

import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time

12345


# 登陆对话框
class DialogUI(QWidget):
    def __init__(self, parent=None):
        super(DialogUI, self).__init__(parent)

        self.setWindowTitle("登陆")
        # self.resize(350,150)
        # 输入密码框
        flo = QFormLayout()
        e1 = QLineEdit()
        BtnOk = QPushButton("  确   定   ")
        BtnCancel = QPushButton(" 取 消 ")
        BtnCancel.clicked.connect(self.close)  # 点击取消关闭窗口
        e1.setEchoMode(QLineEdit.Password)  # 设置密码不可见
        e1.textChanged.connect(self.textchanged)
        flo.addRow("请输入密码：", e1)
        flo.addRow(BtnOk, BtnCancel)
        self.setLayout(flo)

    # 核对密码是否正确
    def textchanged(self, text):
        if text == "12345":
            self.close()  # 关闭登陆界面
            WindowShow.show()
            print("输入正确,跳转至主界面")


# 主窗口
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1274, 860)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
'''
        #self.retranslateUi(Dialog)
        #self.buttonBox.accepted.connect(Dialog.accept)
        #self.buttonBox.rejected.connect(Dialog.reject)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
'''


class WindowShow(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self):
        super(WindowShow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('主窗口')
        self.setWindowIcon(QIcon('icon.png'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = DialogUI()
    d.show()
    WindowShow = WindowShow()  # 生成主窗口的实例
    # 使用qdarkstyle渲染模式
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    sys.exit(app.exec())
