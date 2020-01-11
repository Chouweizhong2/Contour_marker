import os
import sys
from time import strftime, localtime
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
        self.area.db = [[], [], []]
        self.db_path = None
        self.scale = [None, None]  # 比例尺
        self.edit_mode = 1
        self.change_saved = 1
        self.status = self.statusBar()
        self.init_ui()
        self.hide_map = 0
        self.show_all_temp = -99

    def init_ui(self):
        # 设置窗口属性
        self.resize(1000, 600)
        # self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle('Contour Marker V0.7')
        # self.setWindowIcon(QIcon(r"E:\\1.jpg"))
        # 设置状态栏
        self.status.showMessage('欢迎使用，请使用菜单打开文件')

        my_menubar = self.menuBar()
        file = my_menubar.addMenu('文件')
        # 设置菜单================================
        open1 = QAction('打开', self)  # 为打开按钮文本
        open1.setShortcut('ctrl+o')  # 设置快捷键
        open_img = QAction('打开图', self)
        open_db = QAction('打开数据库', self)
        file.addAction(open1)  # 添加打开按钮
        file.addAction(open_img)
        file.addAction(open_db)
        file.addSeparator()  # 添加间隔，好看
        save = QAction('保存', self)
        save.setShortcut('ctrl+s')
        al_save = QAction('另存为..', self)
        tuichu = QAction('退出', self)

        file.addAction(save)
        file.addAction(al_save)
        file.addSeparator()
        file.addAction(tuichu)

        # edit = my_menubar.addMenu('编辑')
        # delet_line = QAction('删除线', self)
        # edit.addAction(delet_line)
        self.abspos_Label = QLabel('坐标：')
        self.status.addPermanentWidget(self.abspos_Label, stretch=0)
        tuichu.triggered.connect(qApp.quit)
        open1.triggered.connect(self.open_file)
        open_img.triggered.connect(lambda: self.open_file(True))
        open_db.triggered.connect(lambda: self.clean_db(None, True))
        save.triggered.connect(lambda: self.save_db(self.db_path))
        al_save.triggered.connect(lambda: self.save_db('as'))
        # delet_line.triggered.connect(self.delet_line)

        # 界面布局================================
        toolLayout = QGridLayout(self)
        # mainLayout.setMargin(10)
        toolLayout.setSpacing(6)

        label1 = QLabel("用户名：")
        self.user_name = QLineEdit()
        self.user_name.setPlaceholderText('请输入用户名')
        label_m = QLabel("模式：")
        self.label_mode = QLabel("编辑模式")
        self.btn_mode = QPushButton('浏览模式(E)')
        label2 = QLabel("比例尺：")
        self.scale_unit = QComboBox()
        self.scale_unit.addItems(['比例尺单位', 'm', 'km', 'degree', '其他'])
        self.scaleTable = QTableWidget(2, 1)
        self.scaleTable.setVerticalHeaderLabels(['X比例尺', 'Y比例尺'])
        self.scaleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.scaleTable.horizontalHeader().setVisible(False)
        label2Button = QPushButton("显示比例尺")
        label22Button = QPushButton("修改比例尺")
        # self.label_dgx = QLabel("未知")
        label3 = QLabel("等高线")
        label3dButton = QPushButton("下方添加")
        label3uButton = QPushButton("上方添加")
        label33Button = QPushButton("删除选中")
        self.listView = QListView()
        self.show_all = QPushButton("显示所有(S)")
        btn_hide_map = QPushButton("隐藏地图")

        self.entry = QStringListModel()  # 创建mode
        self.entry.setStringList(self.area.db[0])  # 将数据设置到model
        self.listView.setModel(self.entry)  # 绑定 listView 和 model
        self.listView.setEditTriggers(QTableView.NoEditTriggers)
        # listView.clicked.connect(self.clickedlist)  # listview 的点击事件
        self.listView.clicked[QModelIndex].connect(self.on_clicked)
        self.listView.doubleClicked.connect(self.Dclickedlist)
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)

        label2Button.clicked.connect(lambda: self.show_scaleClicked('show'))
        label22Button.clicked.connect(lambda: self.show_scaleClicked('edit'))
        label3uButton.clicked.connect(lambda: self.addLine('up'))
        label3dButton.clicked.connect(lambda: self.addLine('down'))
        label33Button.clicked.connect(self.removeLine)
        self.btn_mode.clicked.connect(self.mode_change)
        self.btn_mode.setShortcut('E')
        self.scaleTable.clicked[QModelIndex].connect(self.scale_clicked)
        # QObject.connect(self.scaleTable, pyqtSignal("customContextMenuRequested (const QPoint&)", slotFunc))
        self.listView.customContextMenuRequested[QPoint].connect(self.change_color_meun)
        self.show_all.clicked.connect(self.show_all_clicked)
        self.show_all.setShortcut('S')
        btn_hide_map.clicked.connect(self.hide_map_clicked)
        self.scale_unit.currentIndexChanged.connect(self.scale_unit_clicked)

        toolLayout.addWidget(label1, 1, 0)
        toolLayout.addWidget(self.user_name, 1, 1, 1, 3)
        toolLayout.addWidget(label_m, 2, 0)
        toolLayout.addWidget(self.label_mode, 2, 1, 1, 2)
        toolLayout.addWidget(self.btn_mode, 2, 3, 1, 1)
        toolLayout.addWidget(label2, 3, 0)
        toolLayout.addWidget(self.scaleTable, 3, 1, 2, 2)
        # toolLayout.addWidget(self.label_dgx, 3, 2)
        toolLayout.addWidget(label2Button, 3, 3)
        toolLayout.addWidget(self.scale_unit, 4, 0, 1, 1)
        toolLayout.addWidget(label22Button, 4, 3)
        toolLayout.addWidget(label3, 5, 0, 1, 1)
        toolLayout.addWidget(label3dButton, 5, 1, 1, 1)
        toolLayout.addWidget(label3uButton, 5, 2, 1, 1)
        toolLayout.addWidget(label33Button, 5, 3, 1, 1)
        toolLayout.addWidget(self.listView, 6, 1, 20, 3)
        toolLayout.addWidget(self.show_all, 6, 0, 1, 1)
        toolLayout.addWidget(btn_hide_map, 8, 0, 1, 1)

        toolQW = QWidget()
        toolQW.setLayout(toolLayout)
        layout = QSplitter(Qt.Horizontal)
        layout.setStyleSheet("QSplitter::handle{background-color: lightgray}")
        layout.setHandleWidth(1)
        layout.addWidget(self.area)
        layout.addWidget(toolQW)

        fin_layout = QHBoxLayout()
        fin_layout.addWidget(layout)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(fin_layout)

    def scale_unit_clicked(self):
        if self.scale_unit.currentIndex() == 4:
            i, okPressed = QInputDialog.getText(self, "比例尺", "此比例尺单位")
            if okPressed:
                self.scale_unit.clear()
                self.scale_unit.addItems(['比例尺单位', 'm', 'km', 'degree', '其他'])
                self.scale_unit.addItem(i)
                self.scale_unit.setCurrentIndex(5)
        self.change_saved = 0
        print(self.scale_unit.currentIndex())

    def hide_map_clicked(self):
        if self.hide_map == 0:
            self.hide_map = 1
            self.area.repaint()
        else:
            self.hide_map = 0
            self.area.repaint()

    def show_all_clicked(self):
        if self.area.draw_all == 1:
            self.area.draw_all = 0
            self.area.repaint()
        else:
            self.area.draw_all = 1
            self.area.repaint()

    def mode_change(self):
        if self.edit_mode == 0:
            self.label_mode.setText('编辑模式')
            self.btn_mode.setText('浏览模式(E)')
            self.btn_mode.setShortcut('E')
            self.edit_mode = 1
            self.area.repaint()
        else:
            self.label_mode.setText('浏览模式')
            self.btn_mode.setText('编辑模式(E)')
            self.btn_mode.setShortcut('E')
            self.edit_mode = 0
            self.area.repaint()

    def change_color_meun(self, point):
        popupmenu = QMenu(self.listView)
        index = self.listView.indexAt(point)
        # print("change_color_meun", index.row())
        ##### 添加菜单
        change_color = QAction('更改颜色', self.listView)
        change_color.triggered.connect(lambda: self.change_color(index))
        popupmenu.addAction(change_color)
        popupmenu.exec(QCursor.pos())

    def change_color(self, index):
        # print('Change color clicked:{}'.format(index.row()))
        color = QColorDialog.getColor(Qt.blue)  # 参数Qt.blue：调色盘选取颜色默认停在蓝色
        self.area.db[2][index.row()] = (color, self.area.db[2][index.row()][1])
        self.change_saved = 0

    def on_clicked(self, index):
        if self.scale[0] is None:
            QMessageBox.information(self, "警告", "尚未确定比例尺")
            return None
        print('单击的是', index.row())
        if self.edit_mode == 0:
            self.label_mode.setText('正在查看第{}条线:{}'.format(index.row(), self.area.db[0][index.row()]))
            self.area.enable_draw = False
            self.area.draw_mod = index.row()
            self.area.repaint()
        else:
            self.label_mode.setText('正在编辑第{}条线:{}'.format(index.row(), self.area.db[0][index.row()]))
            self.area.enable_draw = True
            self.area.draw_mod = index.row()
            self.area.repaint()
        # item = self.entry.itemData(index)
        # print(self.listView.selectedIndexes()[0].row())

    def scale_clicked(self, index):
        print('单击的是', -(index.row() + 2))
        if self.scale[index.row()] is None:
            self.area.draw_mod = -(index.row() + 2)
            if index.row() == 0:
                self.label_mode.setText("比例尺X 请选择两个点")
            if index.row() == 1:
                self.label_mode.setText('比例尺Y 请选择两个点')
            self.area.repaint()

    def scale_changed(self, which_changed):
        if which_changed == 'xok':
            print('into xok')
            i, okPressed = QInputDialog.getDouble(self, "比例尺X", "X真实距离:", 0, 0, 100000, 10)
            print('scale_changed point_list_x', self.area.point_list_x)
           # scalex_str = self.get_scal(self.area.point_list_x, i)
            print('scale_changed scalex_str', i)
            self.scale[0] = str(i)
            self.scaleTable.setItem(0, 0, QTableWidgetItem(self.scale[0]))
            self.change_saved = 0
        elif which_changed == 'yok':
            i, okPressed = QInputDialog.getDouble(self, "比例尺Y", "Y真实距离:", 0, 0, 100000, 10)
            # scaley_str = self.get_scal(self.area.point_list_y, i)
            self.scale[1] = str(i)
            self.scaleTable.setItem(0, 1, QTableWidgetItem(self.scale[1]))
            self.label_mode.setText('比例尺设置完成，等待编辑')
            self.change_saved = 0

    def show_scaleClicked(self, do_type):
        if do_type == 'show':
            if self.scale[0] is None:
                QMessageBox.information(self, "警告", "请点击表格添加比例尺")
                return None
            self.area.draw_mod = -1
            self.label_mode.setText('正在查看比例尺')
            self.area.repaint()
        elif do_type == 'edit':
            if self.scale[0] is None:
                QMessageBox.information(self, "警告", "请直接点击表格添加比例尺")
                return None
            else:
                reply = QMessageBox.question(self, '警告', '你确认要删除现有比例尺吗？',
                                     QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    return None
                else:
                    self.area.point_list_y = []
                    self.area.point_list_x = []
                    self.scale = [None, None]
                    self.scaleTable.clearContents()


    def Dclickedlist(self, index):
        print("双击的是：" + str(index.row()))
        # QMessageBox.information(self, "QListView", "你D选择了: " + str(self.area.db[0][index.row()]))
        # print(self.listView.selectedIndexes())
        i, okPressed = QInputDialog.getDouble(self, "等高线", "此等高线高度", 0.0, -100000.0, 100000.0, 10.0)
        if okPressed:
            self.area.db[0][index.row()] = str(i)
        self.entry.setStringList(self.area.db[0])

    def get_scal(self, point_list, real_length):
        x1 = point_list[0][0]
        x2 = point_list[1][0]
        y1 = point_list[0][1]
        y2 = point_list[1][1]
        map_length = (abs(x2 - x1) ** 2 + abs(y2 - y1) ** 2) ** 0.5
        scale_str = str(round(real_length / map_length, 5))
        return scale_str

    def open_file(self, only_img=False):
        if self.change_saved == 0:
            reply = QMessageBox.question(self, '警告', '尚未保存,\n你确认要打开新文件吗？',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                return 0

        self.change_saved = 1
        openfile_name, openfile_type = QFileDialog.getOpenFileName(self,
                                                                   '选择文件', './',
                                                                   "Image File(*.jpg *.png *.jpeg);;All file(*.*)")
        if openfile_name is '':
            return 0
        '''full_fname = openfile_name.split('/')[-1]
        if len(full_fname) > 15:
            full_fname = "..."+full_fname[-15:]
        self.label1_fname.setText(full_fname)'''
        self.setWindowTitle('Contour Marker V0.5 Editing:' + openfile_name)
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
            self.area.Mul_num = image_height / 600
        else:
            self.area.Mul_num = image_width / 600
        self.area.repaint()
        if not only_img:
            self.clean_db(openfile_name)

    def clean_db(self, openfile_name, only_db=False):
        if self.change_saved == 0:
            reply = QMessageBox.question(self, '警告', '尚未保存,\n你确认要打开新文件吗？',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                return 0
        # =======================读取数据库================================
        self.area.db = [[], [], []]  # 重置当前状态
        self.entry.setStringList(self.area.db[0])
        self.area.point = QPoint(0, 0)
        # self.label_dgx.setText('未知')
        self.scaleTable.clearContents()
        self.scale = [None, None]
        self.area.draw_mod = -10
        self.area.point_list_x = []
        self.area.point_list_y = []
        self.scale_unit.clear()
        self.scale_unit.addItems(['比例尺单位', 'm', 'km', 'degree', '其他'])
        if not only_db:
            print('数据库重置成功')
            open_dict_name_s = openfile_name.split('.')
            open_dict_name_s[-1] = 'txt'
            open_dict_name = ''
            for i in open_dict_name_s:
                open_dict_name += (i + '.')
            self.db_path = open_dict_name[:-1]
        else:
            openfile_name, openfile_type = QFileDialog.getOpenFileName(self,
                                                                       '选择文件', './',
                                                                       "DB File(*.txt);;All file(*.*)")
            if openfile_name is '':
                return 0
            self.db_path = openfile_name
        print("self.db_path", self.db_path)
        self.open_db()

    def open_db(self):
        def get_point(str_points):
            list_point = []
            str_points_list = str_points.split('),(')
            for i in str_points_list:
                if i is not '':
                    list_point.append(tuple(eval(i)))
            return list_point

        if self.db_path is None:
            return None
        if os.path.exists(self.db_path):
            self.status.showMessage('已经打开图片及数据库')
            with open(self.db_path, 'r', encoding='utf-8') as f:
                i = 0
                lines = f.readlines()
                for line in lines:
                    if line[0] != '#':
                        if 'User_name' in line:
                            self.user_name.setText(line.split(' ')[-1][:-1])
                        elif 'Scale_unit' in line:
                            self.scale_unit.addItem(line.split(' ')[-1][:-1])
                            self.scale_unit.setCurrentIndex(5)
                        elif 'Scale_num' in line:
                            self.scale = line.split(' ')[-1][1:-2].split(",")
                            for i in range(2):
                                if self.scale[i] == 'None':
                                    self.scale[i] = None
                                else:
                                    self.scale[i] = self.scale[i][1:-1]
                            self.scaleTable.setItem(0, 0, QTableWidgetItem(self.scale[0]))
                            self.scaleTable.setItem(0, 1, QTableWidgetItem(self.scale[1]))
                        elif 'Scale_points' in line:
                            points = get_point(line.split(' ')[-1][2:-3])
                            if len(points) == 2:
                                self.area.point_list_x = [points[0], points[1]]
                            elif len(points) == 4:
                                self.area.point_list_x = [points[0], points[1]]
                                self.area.point_list_y = [points[2], points[3]]
                    else:
                        minus = False
                        if line[1] == '-':
                            minus = True
                            line = line[0] + line[2:]
                        parts = line.split('-')
                        rgba = eval(parts[1])
                        color = QColor(rgba[0], rgba[1], rgba[2], rgba[3])
                        if minus:
                            height = '-' + parts[0][1:]
                        else:
                            height = parts[0][1:]
                        line_type = parts[2]
                        points = get_point(parts[3][2:-3])
                        self.area.db[0].insert(i, height)
                        self.area.db[1].insert(i, points)
                        self.area.db[2].insert(i, (color, line_type))
                        i += 1

            self.entry.setStringList(self.area.db[0])
            self.area.draw_mod = -1
            self.area.repaint()

        self.change_saved = 1
        self.label_mode.setText('打开成功，等待编辑')

    def save_db(self, save_path):
        if self.user_name.text() is '':
            QMessageBox.information(self, "警告", "尚未填写用户名")
            return None
        if save_path == 'as':
            savefile_name, openfile_type = QFileDialog.getSaveFileName(self, '选择文件', './', "Text Files (*.txt)")
            if savefile_name is '':
                return 0
            self.db_path = savefile_name
        else:
            savefile_name = self.db_path
        if savefile_name is None:
            QMessageBox.information(self, "警告", "尚未打开文件")
            return None

        with open(savefile_name, 'w', encoding='utf-8') as f:
            f.write("User_name {}\n".format(self.user_name.text()))
            f.write("Last_time {}\n".format(strftime("%Y/%m/%d-%H:%M:%S", localtime())))
            if len(self.area.point_list_y) != 2:
                write_list = self.area.point_list_x
            else:
                write_list = self.area.point_list_x + self.area.point_list_y
            f.write('Scale_num {}\n'.format(str(self.scale).replace(" ", "")))
            f.write('Scale_unit {}\n'.format(self.scale_unit.currentText()))
            f.write('Scale_points {}\n'.format(str(write_list).replace(" ", "")))
            for name, points, c_t in zip(self.area.db[0], self.area.db[1], self.area.db[2]):
                c_str = str(c_t[0].getRgb()).replace(" ", "")
                n_str = str(points).replace(" ", "")
                f.write('#' + name + '-' + c_str + '-' + c_t[1] + '-' + n_str + '\n')
        self.status.showMessage('储存成功!')
        self.change_saved = 1

    def addLine(self, types):

        print('addLine', types)
        if len(self.listView.selectedIndexes()) > 0:
            selected_index = self.listView.selectedIndexes()[0].row()
            if types == 'up':
                self.area.db[0].insert(selected_index, 'new line')
                self.area.db[1].insert(selected_index, [])
                self.area.db[2].insert(selected_index, (QColor(0, 0, 0), '实线'))
            elif types == 'down':
                self.area.db[0].insert(selected_index + 1, 'new line')
                self.area.db[1].insert(selected_index + 1, [])
                self.area.db[2].insert(selected_index + 1, (QColor(0, 0, 0), '实线'))
        else:
            if types == 'up':
                self.area.db[0].insert(0, 'new line')
                self.area.db[1].insert(0, [])
                self.area.db[2].insert(0, (QColor(0, 0, 0), '实线'))
            else:
                self.area.db[0].append('new line')
                self.area.db[1].append([])
                self.area.db[2].append((QColor(0, 0, 0), '实线'))

        self.entry.setStringList(self.area.db[0])
        self.change_saved = 0

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

                self.area.draw_mod = -1
                self.change_saved = 0
                self.area.repaint()

    def closeEvent(self, event):
        if self.change_saved == 1:
            event.accept()
        else:
            reply = QMessageBox.question(self, '警告', '尚未保存,\n你确认要退出吗？',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
