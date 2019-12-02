import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.status = self.statusBar()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.resize(1000, 600)
        # self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle('Contour Marker V0.01')
        # self.setWindowIcon(QIcon(r"E:\\1.jpg"))
        # 设置状态栏
        self.status.showMessage('欢迎使用，请使用菜单打开文件', 5000)

        my_menubar = self.menuBar()
        file = my_menubar.addMenu('文件')
        # 设置菜单================================
        open1 = QAction('打开', self)  # 为打开按钮设置图标，显示文本
        open1.setShortcut('ctrl+o')  # 设置快捷键
        file.addAction(open1)  # 添加打开按钮
        file.addSeparator()  # 添加间隔，好看
        save = QAction('保存', self)
        save.setShortcut('ctrl+s')
        al_save = QAction('另存为..', self)
        tuichu = QAction('退出', self)

        file.addAction(save)
        file.addAction(al_save)
        file.addSeparator()
        file.addAction(tuichu)

        tuichu.triggered.connect(qApp.quit)
        open1.triggered.connect(self.open_file)
        # 界面布局================================
        toolLayout = QGridLayout(self)
        #mainLayout.setMargin(10)
        toolLayout.setSpacing(6)
        '''toolLayout.setColumnStretch(0, 1)
        toolLayout.setColumnStretch(1, 3)
        toolLayout.setColumnStretch(2, 1)'''

        label1 = QLabel("文件名：")
        label11 = QLabel("未知")
        label2 = QLabel("比例尺：")
        label2Button = QPushButton("更改")
        label22 = QLabel("未知")
        label3 = QLabel("等高线")

        self.listView = QListView()
        self.entry = QStringListModel()  # 创建mode
        self.qList = ['Line 1', 'Line 2', 'Line 3', 'Line 4', '添加..']  # 添加的数组数据
        self.entry.setStringList(self.qList)  # 将数据设置到model
        self.listView.setModel(self.entry)  ##绑定 listView 和 model
        '''
        self.itemOld = QStandardItem("text")
        self.entry = QStandardItemModel()
        self.qList = ['Line 1', 'Line 2', 'Line 3', 'Line 4', '添加..']
        self.listView.setModel(self.entry)
        for text in self.qList:
            it = QStandardItem(text)
            self.entry.appendRow(it)
        
        slm = QStringListModel()  # 创建mode
        self.qList = ['Line 1', 'Line 2', 'Line 3', 'Line 4', '添加..']  # 添加的数组数据
        slm.setStringList(self.qList)  # 将数据设置到model
        self.listView.setModel(slm)  ##绑定 listView 和 model
        '''
        self.listView.setEditTriggers(QTableView.NoEditTriggers)

        #listView.clicked.connect(self.clickedlist)  # listview 的点击事件
        self.listView.clicked[QModelIndex].connect(self.on_clicked)
        self.listView.doubleClicked.connect(self.Dclickedlist)

        toolLayout.addWidget(label1, 1, 0)
        toolLayout.addWidget(label11, 1, 1)
        toolLayout.addWidget(label2, 2, 0)
        toolLayout.addWidget(label22, 2, 1)
        toolLayout.addWidget(label2Button, 2, 2)
        toolLayout.addWidget(label3,3,0,1,1)
        toolLayout.addWidget(self.listView,3,1,2,15)

        toolQW = QWidget()
        toolQW.setLayout(toolLayout)
        self.area = MyDraw()
        layout = QSplitter(Qt.Horizontal)
        layout.addWidget(self.area)
        layout.addWidget(toolQW)

        fin_layout = QHBoxLayout()
        fin_layout.addWidget(layout)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(fin_layout)

    def on_clicked(self, index):
        print(index.row())
        item = self.entry.itemData(index)
        # print(self.listView.selectedIndexes()[0].row())

    def Dclickedlist(self, index):
        QMessageBox.information(self, "QListView", "你D选择了: " + self.qList[index.row()])
        print("点击的是：" + str(index.row()))
        print(self.listView.selectedIndexes())

    def open_file(self):
        openfile_name, openfile_type = QFileDialog.getOpenFileName(self, '选择文件', './')
        print(openfile_name)
        # filename = r"C:/Users/Cjay/PycharmProjects/Contour_marker/data/Material/mc-enep.jpg"
        cvIm = cv2.imread(openfile_name, -1)  # 通过Opencv读入一张图片
        image_height, image_width, image_depth = cvIm.shape  # 获取图像的高，宽以及深度。
        print(image_height, image_width)
        # QIm = cv2.cvtColor(Im, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        QIm = QImage(cvIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                     image_width * image_depth,
                     QImage.Format_RGB888).rgbSwapped()
        self.area.pix = QPixmap.fromImage(QIm)  # 将QImage显示在之前创建的QLabel控件中
        if image_height > image_width:
            self.area.Mul_num = image_height/600
        else:
            self.area.Mul_num = image_width/600
        # self.area.scaled_size = QSize(image_width/self.area.Mul_num, image_height/self.area.Mul_num)
        self.area.repaint()


class MyDraw(QWidget):
    def __init__(self):
        print('init my Draw')
        QWidget.__init__(self)
        #self.setupUi(self)
        self.resize(800,600)
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
        self.point_list = []
        self.Mul_num = 1

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
        scaled_size = QSize(orgx/self.Mul_num, orgy/self.Mul_num)
        scaled_img = self.pix.scaled(scaled_size)
        painter.drawPixmap(self.point, scaled_img)
        for i, pos in enumerate(self.point_list):
            cir_x = pos.x()/self.Mul_num + self.point.x()-5
            cir_y = pos.y()/self.Mul_num + self.point.y()-5
            painter.drawEllipse(cir_x, cir_y, 10, 10)
            if i != 0:
                start_x = self.point_list[i-1].x()/self.Mul_num + self.point.x()
                start_y = self.point_list[i-1].y()/self.Mul_num + self.point.y()
                end_x = pos.x()/self.Mul_num + self.point.x()
                end_y = pos.y()/self.Mul_num + self.point.y()
                painter.drawLine(start_x, start_y, end_x, end_y)

    def mouseMoveEvent(self, e):  # 重写移动事件
        if e.buttons() == Qt.MidButton:
        #if self.left_click:
            self._endPos = e.pos() - self._startPos
            self.point = self.point + self._endPos
            self._startPos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.MidButton:
            self._startPos = e.pos()
        elif e.button() == Qt.LeftButton:  # 添加点
            newpos = (e.pos() - self.point) * self.Mul_num
            self.point_list.append(newpos)
            print("Add: ", newpos.x(), newpos.y())
            self.repaint()
        elif e.button() == Qt.RightButton:  # 删除点
            self.point_list.pop()
            self.repaint()

    def mouseReleaseEvent(self, e):
        '''if e.button() == Qt.RightButton:
            self.point = QPoint(0, 0)
            self.scaled_img = self.pix.scaled(self.size())
            self.repaint()'''

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            # 放大图片
            #self.scaled_size = QSize(self.scaled_size.width()-15, self.scaled_size.height()-15)
            self.Mul_num -= 0.15
            #new_w = e.x() - (self.pix.width()/self.Mul_num * (e.x() - self.point.x())) / (self.pix.width()/self.Mul_num + self.pix.width()/self.Mul_num*15)
            #new_h = e.y() - (self.pix.height()/self.Mul_num * (e.y() - self.point.y())) / (self.pix.height()/self.Mul_num + self.pix.width()/self.Mul_num*15)
            #self.point = QPoint(new_w, new_h)
            self.repaint()

        elif e.angleDelta().y() < 0:
            # 缩小图片
            self.Mul_num += 0.15
            #self.scaled_size = QSize(self.scaled_size.width() + 15, self.scaled_size.height() + 15)
            #new_w = e.x() - (self.pix.width()/self.Mul_num * (e.x() - self.point.x())) / (self.pix.width()/self.Mul_num - self.pix.width()/self.Mul_num*0.15)
            #new_h = e.y() - (self.pix.height()/self.Mul_num * (e.y() - self.point.y())) / (self.pix.height()/self.Mul_num - self.pix.width()/self.Mul_num*15)
            #self.point = QPoint(new_w, new_h)
            self.repaint()

    def resizeEvent(self, e):
        if self.parent is not None:
            if self.pix.size().height() > self.pix.size().width():
                self.Mul_num = self.pix.size().width()/self.size().width()
            else:
                self.Mul_num = self.pix.size().width()/self.size().width()
            #self.scaled_img = self.pix.scaled(self.size())
            self.point = QPoint(0, 0)
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
