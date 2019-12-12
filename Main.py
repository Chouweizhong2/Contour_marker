import os
import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import MyDraw


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.area = MyDraw.MyDraw(self)
        self.area.setMouseTracking(True)
        self.area.db = [[], []]
        self.db_path = None
        self.scale = None  # 比例尺
        self.scaleMode = None
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
        open1 = QAction('打开', self)  # 为打开按钮文本
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

        #edit = my_menubar.addMenu('编辑')
        #delet_line = QAction('删除线', self)
        #edit.addAction(delet_line)
        self.abspos_Label = QLabel('坐标：')
        self.status.addPermanentWidget(self.abspos_Label, stretch=0)

        tuichu.triggered.connect(qApp.quit)
        open1.triggered.connect(self.open_file)
        save.triggered.connect(self.save_db)
        al_save.triggered.connect(self.save_db_as)
        #delet_line.triggered.connect(self.delet_line)

        # 界面布局================================
        toolLayout = QGridLayout(self)
        #mainLayout.setMargin(10)
        toolLayout.setSpacing(6)

        label1 = QLabel("文件名：")
        self.label1_fname = QLabel("未知")
        label_m = QLabel("编辑模式：")
        self.label_mode = QLabel("等待打开文件")
        label2 = QLabel("比例尺：")
        self.scaleTable = QTableWidget(2, 1)
        self.scaleTable.setVerticalHeaderLabels(['X比例尺', 'Y比例尺'])
        self.scaleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.scaleTable.horizontalHeader().setVisible(False)
        label2Button = QPushButton("单比例尺")
        label22Button = QPushButton("xy双比例尺")
        # self.label_dgx = QLabel("未知")
        label3 = QLabel("等高线")
        label3dButton = QPushButton("下方添加")
        label3uButton = QPushButton("上方添加")
        label33Button = QPushButton("删除选中")
        self.listView = QListView()

        self.entry = QStringListModel()  # 创建mode
        self.entry.setStringList(self.area.db[0])  # 将数据设置到model
        self.listView.setModel(self.entry)  # 绑定 listView 和 model
        self.listView.setEditTriggers(QTableView.NoEditTriggers)
        # listView.clicked.connect(self.clickedlist)  # listview 的点击事件
        self.listView.clicked[QModelIndex].connect(self.on_clicked)
        self.listView.doubleClicked.connect(self.Dclickedlist)

        label2Button.clicked.connect(lambda: self.scaleClicked('x'))
        label22Button.clicked.connect(lambda: self.scaleClicked('xy'))
        label3uButton.clicked.connect(lambda: self.addLine('up'))
        label3dButton.clicked.connect(lambda: self.addLine('down'))
        label33Button.clicked.connect(self.removeLine)
        self.scaleTable.clicked[QModelIndex].connect(self.scale_clicked)

        toolLayout.addWidget(label1, 1, 0)
        toolLayout.addWidget(self.label1_fname, 1, 1, 1, 3)
        toolLayout.addWidget(label_m, 2, 0)
        toolLayout.addWidget(self.label_mode, 2, 1, 1, 3)
        toolLayout.addWidget(label2, 3, 0)
        toolLayout.addWidget(self.scaleTable, 3, 1, 2, 2)
        # toolLayout.addWidget(self.label_dgx, 3, 2)
        toolLayout.addWidget(label2Button, 3, 3)
        toolLayout.addWidget(label22Button, 4, 3)
        toolLayout.addWidget(label3, 5, 0, 1, 1)
        toolLayout.addWidget(label3dButton, 5, 1, 1, 1)
        toolLayout.addWidget(label3uButton, 5, 2, 1, 1)
        toolLayout.addWidget(label33Button, 5, 3, 1, 1)
        toolLayout.addWidget(self.listView, 6, 1, 20, 3)

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
        self.area.draw_mod = index.row()
        self.area.repaint()
        self.label_mode.setText('正在编辑第{}条线:{}'.format(index.row(), self.area.db[0][index.row()]))
        # item = self.entry.itemData(index)
        # print(self.listView.selectedIndexes()[0].row())

    def scale_clicked(self, index):
        if self.scale is None:
            QMessageBox.information(self, "警告", "尚未确定比例尺")
            return None
        print('单击的是', -(index.row()+2))
        self.area.draw_mod = -(index.row()+2)
        self.label_mode.setText('正在查看比例尺，编辑请点击按钮')
        self.area.repaint()

    def Dclickedlist(self, index):
        print("双击的是：" + str(index.row()))
        # QMessageBox.information(self, "QListView", "你D选择了: " + str(self.area.db[0][index.row()]))
        # print(self.listView.selectedIndexes())
        i, okPressed = QInputDialog.getDouble(self, "等高线", "此等高线高度", 0.0, -100000.0, 100000.0, 10.0)
        if okPressed:
            self.area.db[0][index.row()] = str(i)
        self.entry.setStringList(self.area.db[0])
        self.label_mode.setText('正在编辑第{}条线:{}'.format(index.row(), self.area.db[0][index.row()]))

    def scaleClicked(self, stype:str):
        if self.db_path is None:
            QMessageBox.information(self, "警告", "尚未打开文件")
            #return None
        if stype == 'x':
            self.scaleTable.clearContents()
            self.label_mode.setText("比例尺模式：单比例尺，请选择两个点")
            self.area.draw_mod = -1
            self.area.point_list_x = []
        elif stype == 'xy':
            self.scaleTable.clearContents()
            self.scale = []
            self.label_mode.setText("比例尺模式：X 请选择两个点")
            self.area.draw_mod = -2
            self.area.point_list_x = []

        if stype == 'ok':
            i, okPressed = QInputDialog.getInt(self, "比例尺", "真实距离 米:", 0, 0, 100000, 10)
            x1 = self.area.point_list_x[0][0]
            x2 = self.area.point_list_x[1][0]
            y1 = self.area.point_list_x[0][1]
            y2 = self.area.point_list_x[1][1]
            map_length = (abs(x2 - x1) ** 2 + abs(y2 - y1) ** 2) ** 0.5
            scale_str = str(round(i / map_length, 5))
            self.scale = [scale_str, scale_str]
            # self.label_dgx.setText(str(self.scale))
            self.scaleTable.setItem(0, 0, QTableWidgetItem(self.scale[0]))
            self.scaleTable.setItem(0, 1, QTableWidgetItem(self.scale[1]))
            self.label_mode.setText('比例尺设置完成，等待编辑')

        elif stype == 'xok':
            print('into xok')
            i, okPressed = QInputDialog.getInt(self, "比例尺X", "X真实距离 米:", 0, 0, 100000, 10)
            x1 = self.area.point_list_x[0][0]
            x2 = self.area.point_list_x[1][0]
            map_length = abs(x2 - x1)
            scalex_str = str(round(i / map_length, 5))
            print(scalex_str)
            self.scale.append(scalex_str)
            self.scaleTable.setItem(0, 0, QTableWidgetItem(scalex_str))
            self.label_mode.setText("比例尺模式：Y 请选择两个点")
            self.area.draw_mod = -3
            self.area.point_list_y = []
        elif stype == 'yok':
            i, okPressed = QInputDialog.getInt(self, "比例尺Y", "Y真实距离 米:", 0, 0, 100000, 10)
            y1 = self.area.point_list_y[0][1]
            y2 = self.area.point_list_y[1][1]
            map_length = abs(y2 - y1)
            scaley_str = str(round(i / map_length, 5))
            self.scale.append(scaley_str)
            self.scaleTable.setItem(0, 1, QTableWidgetItem(self.scale[1]))
            self.label_mode.setText('比例尺设置完成，等待编辑')


        '''if len(self.area.point_list) != 2:
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
                self.label_dgx.setText(str(self.scale))'''
        '''dlg =  QtGui.QInputDialog(self)                 
dlg.setInputMode( QtGui.QInputDialog.TextInput) 
dlg.setLabelText("URL:")                        
dlg.resize(500,100)                             
ok = dlg.exec_()                                
url = dlg.textValue()'''

    def open_file(self):
        openfile_name, openfile_type = QFileDialog.getOpenFileName(self,
                                        '选择文件', './', "Image File(*.jpg *.png *.jpeg);;All file(*.*)")
        if openfile_name is '':
            return 0
        full_fname = openfile_name.split('/')[-1]
        if len(full_fname) > 15:
            full_fname = "..."+full_fname[-15:]
        self.label1_fname.setText(full_fname)
        self.setWindowTitle('Contour Marker V0.5 Editing:'+openfile_name)
        # ====================读取图片===================
        # 待解决：gif 读取， opencv没有商业权限读取gif格式
        # cvIm = cv2.imread(openfile_name)  # 通过Opencv读入一张图片
        # 解决读取中文路径问题 使用numpy包读取。
        cvIm = cv2.imdecode(np.fromfile(openfile_name, dtype=np.uint8), cv2.IMREAD_COLOR)
        print('numpy open success')
        # cv2.imshow("test", cvIm)
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
        self.area.repaint()
        # =======================读取数据库================================
        self.area.db = [[], []]  # 重置当前状态
        self.area.point = QPoint(0, 0)
        # self.label_dgx.setText('未知')
        self.scaleTable.clearContents()
        self.scale = []
        self.area.draw_mod = -10
        self.area.point_list_x = []
        self.area.point_list_y = []

        print('数据库重置成功')
        open_dict_name_s = openfile_name.split('.')
        open_dict_name_s[-1] = 'txt'
        open_dict_name = ''
        for i in open_dict_name_s:
            open_dict_name += (i + '.')
        self.db_path = open_dict_name[:-1]
        print("self.db_path", self.db_path)
        self.open_db()

    def open_db(self):
        if self.db_path is None:
            return None
        if os.path.exists(self.db_path):
            self.status.showMessage('已经打开图片及数据库')
            with open(self.db_path) as f:
                lines = f.readlines()
                if len(lines) > 0:
                    if lines[0].split('#')[1] is 'None':
                        self.scale = None
                    else:
                        # lines[0].split('#')[1]
                        self.scale = [lines[0].split('#')[1], lines[0].split('#')[2]]
                        self.scaleTable.setItem(0, 0, QTableWidgetItem(self.scale[0]))
                        self.scaleTable.setItem(0, 1, QTableWidgetItem(self.scale[1]))
                        # self.label_dgx.setText(self.scale)
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
        self.label_mode.setText('打开成功，等待编辑')

    def save_db(self):
        if self.db_path is None:
            QMessageBox.information(self, "警告", "尚未打开文件")
            return None
        with open(self.db_path, 'w') as f:
            f.write('scale#'+str(self.scale[0])+'#'+self.scale[1]+'#\n')
            for k, v in zip(self.area.db[0], self.area.db[1]):
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
            f.write('scale#'+str(self.scale[0])+'#'+self.scale[1]+'#\n')
            for k, v in zip(self.area.db[0], self.area.db[1]):
                if v != -1:
                    v_string = str(v).replace(" ","")
                    f.write(k + '\t' + v_string + '\n')
        self.status.showMessage('储存成功!')

    def addLine(self, types):

        print('addLine', types)
        if len(self.listView.selectedIndexes()) > 0:
            selected_index = self.listView.selectedIndexes()[0].row()
            if types == 'up':
                self.area.db[0].insert(selected_index, 'new line')
                self.area.db[1].insert(selected_index, [])
            elif types == 'down':
                self.area.db[0].insert(selected_index+1, 'new line')
                self.area.db[1].insert(selected_index+1, [])
        else:
            if types == 'up':
                self.area.db[0].insert(0, 'new line')
                self.area.db[1].insert(0, [])
            else:
                self.area.db[0].append('new line')
                self.area.db[1].append([])

        self.entry.setStringList(self.area.db[0])

    def removeLine(self):
        if len(self.listView.selectedIndexes()) > 0:
            selected_index = self.listView.selectedIndexes()[0].row()
            reply = QMessageBox.question(self, '删除', '确定删除{}:{}？'.format(selected_index,
                                                                         self.area.db[0][selected_index]),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.area.db[0].pop(selected_index)
                self.area.db[1].pop(selected_index)
                self.entry.setStringList(self.area.db[0])

                self.area.draw_mod = -10


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
