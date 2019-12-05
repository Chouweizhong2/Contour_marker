import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import MyDraw


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.area = MyDraw.MyDraw()
        self.area.db = [['添加..',], [-1,]]
        self.db_path = None
        self.scale = None  # 比例尺
        self.status = self.statusBar()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.resize(1000, 600)
        # self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle('Contour Marker V0.5')
        # self.setWindowIcon(QIcon(r"E:\\1.jpg"))
        # 设置状态栏
        self.status.showMessage('欢迎使用，请使用菜单打开文件')

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
        save.triggered.connect(self.save_db)
        al_save.triggered.connect(self.save_db_as)

        # 界面布局================================
        toolLayout = QGridLayout(self)
        #mainLayout.setMargin(10)
        toolLayout.setSpacing(6)
        '''toolLayout.setColumnStretch(0, 1)
        toolLayout.setColumnStretch(1, 3)
        toolLayout.setColumnStretch(2, 1)'''

        label1 = QLabel("文件名：")
        self.label11 = QLabel("未知")
        label2 = QLabel("比例尺：")
        label2Button = QPushButton("更改")
        self.label22 = QLabel("未知")
        label3 = QLabel("等高线")

        self.listView = QListView()
        self.entry = QStringListModel()  # 创建mode
        # self.qList = ['添加..']  # 添加的数组数据
        self.entry.setStringList(self.area.db[0])  # 将数据设置到model
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
        # listView.clicked.connect(self.clickedlist)  # listview 的点击事件
        self.listView.clicked[QModelIndex].connect(self.on_clicked)
        self.listView.doubleClicked.connect(self.Dclickedlist)
        label2Button.clicked.connect(self.label2ButtonClicked)

        toolLayout.addWidget(label1, 1, 0)
        toolLayout.addWidget(self.label11, 1, 1)
        toolLayout.addWidget(label2, 2, 0)
        toolLayout.addWidget(self.label22, 2, 1)
        toolLayout.addWidget(label2Button, 2, 2)
        toolLayout.addWidget(label3,3,0,1,1)
        toolLayout.addWidget(self.listView,3,1,2,15)

        toolQW = QWidget()
        toolQW.setLayout(toolLayout)
        layout = QSplitter(Qt.Horizontal)
        layout.addWidget(self.area)
        layout.addWidget(toolQW)

        fin_layout = QHBoxLayout()
        fin_layout.addWidget(layout)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(fin_layout)

    def on_clicked(self, index):
        if self.scale is None:
            QMessageBox.information(self, "警告", "尚未确定比例尺")
            return None
        print('单击的是', index.row())
        if self.area.db[1][index.row()] != -1:
            self.area.draw_mod = index.row()
            self.area.repaint()
        else:
            self.area.draw_mod = -2
            self.area.repaint()
        # item = self.entry.itemData(index)
        # print(self.listView.selectedIndexes()[0].row())

    def Dclickedlist(self, index):
        print("双击的是：" + str(index.row()))
        # QMessageBox.information(self, "QListView", "你D选择了: " + str(self.area.db[0][index.row()]))
        # print(self.listView.selectedIndexes())

        if self.area.db[1][index.row()] == -1:
            self.area.db[0].insert(index.row(), 'new line')
            self.area.db[1].insert(index.row(), [])
        else:
            i, okPressed = QInputDialog.getInt(self, "等高线", "此等高线高度", 0, 0, 100000, 10)
            if okPressed:
                self.area.db[0][index.row()] = str(i)


        self.entry.setStringList(self.area.db[0])

    def label2ButtonClicked(self):
        if self.db_path is None:
            QMessageBox.information(self, "警告", "尚未打开文件")
            #return None
        if len(self.area.point_list) != 2:
            QMessageBox.information(self, "比例尺", "请先在地图选择两个点")
            return None
        else:
            i, okPressed = QInputDialog.getInt(self, "比例尺", "真实距离 m :", 0, 0, 100000, 10)
            if okPressed:
                x1 = self.area.point_list[0][0]
                x2 = self.area.point_list[1][0]
                y1 = self.area.point_list[0][1]
                y2 = self.area.point_list[1][1]
                map_length = (abs(x2-x1)**2+abs(y2-y1)**2)**0.5
                self.scale = round(i/map_length, 5)
                self.label22.setText(str(self.scale))
        '''dlg =  QtGui.QInputDialog(self)                 
dlg.setInputMode( QtGui.QInputDialog.TextInput) 
dlg.setLabelText("URL:")                        
dlg.resize(500,100)                             
ok = dlg.exec_()                                
url = dlg.textValue()'''

    def open_file(self):

        openfile_name, openfile_type = QFileDialog.getOpenFileName(self, '选择文件', './')
        print(openfile_name)
        self.label11.setText(openfile_name.split('/')[-1])
        self.setWindowTitle('Contour Marker V0.5 Editing:'+openfile_name)
        # ====================读取图片===================
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
        # =======================读取数据库================================
        self.area.db = [['添加..', ], [-1, ]]  # 重置当前状态
        self.label22.setText('未知')
        self.scale = None
        self.area.draw_mod = -1
        self.area.point_list = []

        print('数据库重置成功')
        open_dict_name_s = openfile_name.split('.')
        open_dict_name_s[-1] = 'txt'
        open_dict_name = ''
        for i in open_dict_name_s:
            open_dict_name += (i + '.')
        self.db_path = open_dict_name[:-1]
        self.open_db()


    def open_db(self):
        if self.db_path is None:
            return None
        if os.path.exists(self.db_path):
            self.status.showMessage('已经打开图片及数据库')
            with open(self.db_path) as f:
                lines = f.readlines()
                if len(lines) >1:
                    if lines[0].split('#')[1] is 'None':
                        self.scale = None
                    else:
                        self.scale = lines[0].split('#')[1]
                        self.label22.setText(self.scale)
                    for i in range(len(lines)-1):
                        self.area.db[0].insert(i, lines[i + 1].split('\t')[0])
                        list_point = []
                        print(lines[i + 1].split('\t')[1][2:-3])
                        for j in lines[i + 1].split('\t')[1][2:-3].split('),('):
                            list_point.append(tuple(eval(j)))
                        self.area.db[1].insert(i, list_point)
            self.entry.setStringList(self.area.db[0])

        else:
            with open(self.db_path, 'w') as f:
                f.close()
                self.status.showMessage('数据库为空，已新建数据库'+self.db_path)

    def save_db(self):
        if self.db_path is None:
            QMessageBox.information(self, "警告", "尚未打开文件")
            return None
        with open(self.db_path, 'w') as f:
            f.write('scale#'+str(self.scale)+'#\n')
            for k, v in zip(self.area.db[0],self.area.db[1]):
                if v != -1:
                    v_string = str(v).replace(" ","")
                    f.write(k + '\t' + v_string + '\n')
        self.status.showMessage('储存成功!')

    def save_db_as(self):
        savefile_name, openfile_type = QFileDialog.getSaveFileName(self, '选择文件', './', "Text Files (*.txt)")
        if self.db_path is None:
            QMessageBox.information(self, "警告", "尚未打开文件")
            return None
        with open(savefile_name, 'w') as f:
            f.write('scale#' + str(self.scale) + '#\n')
            for k, v in zip(self.area.db[0],self.area.db[1]):
                if v != -1:
                    v_string = str(v).replace(" ","")
                    f.write(k + '\t' + v_string + '\n')
        self.status.showMessage('储存成功!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
