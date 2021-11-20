import copy
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont
import glo
from db import *


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.db = DataBase()
        self.id = -1
        self.init_ui()
        self.slot_init()

    def init_ui(self):
        self.setWindowTitle("管理员")
        self.setFixedSize(1920, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_design()
        self.right_design()
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)

        self.button_left_1.clicked.connect(self.button_left_1_click)
        self.button_left_2.clicked.connect(self.button_left_2_click)
        self.button_left_3.clicked.connect(self.button_left_3_click)
        self.button_left_4.clicked.connect(self.button_left_4_click)
        self.button_left_5.clicked.connect(self.button_left_5_click)
        self.button_left_6.clicked.connect(self.button_left_6_click)
        self.button_left_7.clicked.connect(self.button_left_7_click)
        self.button_left_8.clicked.connect(self.button_left_8_click)

        self.button_ask_1.clicked.connect(self.take_photo_1)

        self.button_ask_4.clicked.connect(self.show_to_mod_face_info)
        self.button_ask_5.clicked.connect(self.show_data_face_info)

    """
    左窗口
    """
    def left_design(self):

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.label_left_1 = QtWidgets.QLabel("管理员功能")
        self.label_left_1.setObjectName('admin_label')
        self.label_left_1.setMaximumHeight(50)

        self.button_left_1 = QtWidgets.QPushButton("增加人像信息")
        self.button_left_1.setObjectName('left_button')
        self.button_left_2 = QtWidgets.QPushButton("删除人像信息")
        self.button_left_2.setObjectName('left_button')
        self.button_left_3 = QtWidgets.QPushButton("查询人像信息")
        self.button_left_3.setObjectName('left_button')
        self.button_left_4 = QtWidgets.QPushButton("修改人像信息")
        self.button_left_4.setObjectName('left_button')
        self.button_left_5 = QtWidgets.QPushButton("查看已有人像")
        self.button_left_5.setObjectName('left_button')
        self.button_left_6 = QtWidgets.QPushButton("查看删改记录")
        self.button_left_6.setObjectName('left_button')
        self.button_left_7 = QtWidgets.QPushButton("查询删改记录")
        self.button_left_7.setObjectName('left_button')
        self.button_left_8 = QtWidgets.QPushButton("关于我们")
        self.button_left_8.setObjectName('left_button')

        self.left_layout.addWidget(self.label_left_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_4, 5, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_5, 6, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_6, 7, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_7, 8, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_8, 9, 0, 1, 3)

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)

    """
    右窗口
    """
    def right_design(self):
        self.right_widget_1 = QtWidgets.QWidget()  # 增加人像信息
        self.right_widget_1.setObjectName('right_widget')
        self.right_layout_1 = QtWidgets.QGridLayout()
        self.right_widget_1.setLayout(self.right_layout_1)
        self.right_widget_2 = QtWidgets.QWidget()  # 删除人像信息
        self.right_widget_2.setObjectName('right_widget')
        self.right_layout_2 = QtWidgets.QGridLayout()
        self.right_widget_2.setLayout(self.right_layout_2)
        self.right_widget_3 = QtWidgets.QWidget()  # 查询人像信息
        self.right_widget_3.setObjectName('right_widget')
        self.right_layout_3 = QtWidgets.QGridLayout()
        self.right_widget_3.setLayout(self.right_layout_3)
        self.right_widget_4 = QtWidgets.QWidget()  # 修改人像信息
        self.right_widget_4.setObjectName('right_widget')
        self.right_layout_4 = QtWidgets.QGridLayout()
        self.right_widget_4.setLayout(self.right_layout_4)
        self.right_widget_update_4 = QtWidgets.QWidget()  # 修改人像信息-xiu gai zhong
        self.right_widget_update_4.setObjectName('right_widget')
        self.right_layout_update_4 = QtWidgets.QGridLayout()
        self.right_widget_update_4.setLayout(self.right_layout_update_4)
        self.right_widget_5 = QtWidgets.QWidget()  # 查看已有人像
        self.right_widget_5.setObjectName('right_widget')
        self.right_layout_5 = QtWidgets.QGridLayout()
        self.right_widget_5.setLayout(self.right_layout_5)
        self.right_widget_6 = QtWidgets.QWidget()  # 查看删改记录
        self.right_widget_6.setObjectName('right_widget')
        self.right_layout_6 = QtWidgets.QGridLayout()
        self.right_widget_6.setLayout(self.right_layout_6)
        self.right_widget_7 = QtWidgets.QWidget()  # 查询删改记录
        self.right_widget_7.setObjectName('right_widget')
        self.right_layout_7 = QtWidgets.QGridLayout()
        self.right_widget_7.setLayout(self.right_layout_7)
        self.right_widget_8 = QtWidgets.QWidget()  # 关于我们
        self.right_widget_8.setObjectName('right_widget')
        self.right_layout_8 = QtWidgets.QGridLayout()
        self.right_widget_8.setLayout(self.right_layout_8)

        self.main_layout.addWidget(self.right_widget_1, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_2, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_3, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_4, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_5, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_6, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_7, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_8, 0, 2, 12, 10)

        self.set_right_widget_1()
        self.set_right_widget_2()
        self.set_right_widget_3()
        self.set_right_widget_4()
        self.set_right_widget_5()
        self.set_right_widget_6()
        self.set_right_widget_7()
        self.set_right_widget_8()

    def set_right_widget_1(self):

        self.label_name_1 = QtWidgets.QLabel()
        self.label_name_1.setText("请输入姓名：")
        self.line_edit_name_1 = QtWidgets.QLineEdit()

        self.label_id_1 = QtWidgets.QLabel()
        self.label_id_1.setText("请输入ID：")
        self.line_edit_id_1 = QtWidgets.QLineEdit()

        self.label_show_camera = QtWidgets.QLabel()
        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.button_ask_1 = QtWidgets.QPushButton(u'打开相机')


        self.right_layout_1.addWidget(self.label_name_1, 0, 2, 1, 2)
        self.right_layout_1.addWidget(self.line_edit_name_1, 0, 4, 1, 6)
        self.right_layout_1.addWidget(self.label_id_1, 2, 2, 1, 2)
        self.right_layout_1.addWidget(self.line_edit_id_1, 2, 4, 1, 6)
        self.right_layout_1.addWidget(self.label_show_camera, 4, 2, 1, 10)
        self.right_layout_1.addWidget(self.button_ask_1, 5, 5, 1, 2)


    def set_right_widget_2(self):
        print("待写2")

    def set_right_widget_3(self):
        print("待写3")

    def set_right_widget_4(self):
        self.table_4 = QtWidgets.QTableWidget()
        self.button_ask_4 = QtWidgets.QPushButton(u"查看")
        self.right_layout_4.addWidget(self.table_4, 0, 2, 10, 10)
        self.right_layout_4.addWidget(self.button_ask_4, 11, 5, 1, 2)

    def set_right_widget_update_4(self, id):
        self.label_name_4 = QtWidgets.QLabel()
        self.label_name_4.setText("请输入修改后姓名：")
        self.line_edit_name_4 = QtWidgets.QLineEdit()
        self.line_edit_name_4.setFont(QFont('Arial', 14))
        self.line_edit_name_4.setText(self.db.get_name(id))

        self.label_id_4 = QtWidgets.QLabel()
        self.label_id_4.setText("请输入修改后ID：")
        self.line_edit_id_4 = QtWidgets.QLineEdit()
        self.line_edit_id_4.setFont(QFont('Arial', 14))
        self.line_edit_id_4.setText(self.db.get_id_num(id))

        self.label_show_camera = QtWidgets.QLabel()
        self.label_show_camera.setFixedSize(320, 240)
        self.label_show_camera.setAutoFillBackground(False)
        self.label_show_pic_4 = QtWidgets.QLabel()
        self.label_show_pic_4.setFixedSize(320, 240)
        self.label_show_pic_4.setAutoFillBackground(False)
        face_img = self.db.get_face_img(id)
        face_info_img = QtGui.QImage.fromData(face_img)
        face_info_pixmap = QtGui.QPixmap.fromImage(face_info_img)
        self.label_show_pic_4.setScaledContents(True)
        self.label_show_pic_4.setPixmap(face_info_pixmap)

        self.id = id

        self.button_cam_4 = QtWidgets.QPushButton(u'打开相机')

        self.right_layout_update_4.addWidget(self.label_name_4, 0, 2, 1, 2)
        self.right_layout_update_4.addWidget(self.line_edit_name_4, 0, 4, 1, 6)
        self.right_layout_update_4.addWidget(self.label_id_4, 2, 2, 1, 2)
        self.right_layout_update_4.addWidget(self.line_edit_id_4, 2, 4, 1, 6)
        self.right_layout_update_4.addWidget(self.label_show_pic_4, 4, 1, 1, 10)
        self.right_layout_update_4.addWidget(self.label_show_camera, 4, 12, 1, 10)
        self.right_layout_update_4.addWidget(self.button_cam_4, 5, 5, 1, 2)


    def set_right_widget_5(self):
        self.table_5 = QtWidgets.QTableWidget()
        self.button_ask_5 = QtWidgets.QPushButton(u"查看")
        self.right_layout_5.addWidget(self.table_5, 0, 2, 10, 10)
        self.right_layout_5.addWidget(self.button_ask_5, 11, 5, 1, 2)

    def set_right_widget_6(self):
        print("待写6")

    def set_right_widget_7(self):
        print("待写7")

    def set_right_widget_8(self):
        print("待写8")

    def button_left_1_click(self):
        self.right_widget_1.show()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_update_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_2_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.show()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_update_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_3_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.show()
        self.right_widget_4.hide()
        self.right_widget_update_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_4_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.show()
        self.right_widget_update_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_5_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_update_4.hide()
        self.right_widget_5.show()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_6_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_update_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.show()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_7_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_update_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.show()
        self.right_widget_8.hide()

    def button_left_8_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_update_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.show()

    def take_photo_1(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(glo.CAM_NAME)
            print(flag)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
                # if msg==QtGui.QMessageBox.Cancel:
                #                     pass
            else:
                self.timer_camera.start(30)
                self.button_ask_1.setText(u'确定')
        else:
            self.timer_camera.stop()
            self.cap.release()
            #self.label_show_camera.clear()
            self.button_ask_1.setText(u'打开相机')
            user_name = self.line_edit_name_1.text()
            user_id = self.line_edit_id_1.text()
            if user_name != "" and user_id != "" and str.isdigit(user_id):
                cv2.imwrite("photo_register.png", self.image)
                self.db.add_photo(user_name, user_id)
            else:
                msg_text = ""
                if user_id == "" or user_name == "":
                    msg_text = "姓名或密码不能为空"
                else:
                    msg_text = "密码只能为数字"
                msg = QtWidgets.QMessageBox.information(self, "警告！！！", msg_text, QMessageBox.Yes)

    def take_photo_4(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(glo.CAM_NAME)
            print(flag)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
                # if msg==QtGui.QMessageBox.Cancel:
                #                     pass
            else:
                self.timer_camera.start(30)
                self.button_cam_4.setText(u'确定')
        else:
            self.timer_camera.stop()
            self.cap.release()
            #self.label_show_camera.clear()
            self.button_cam_4.setText(u'打开相机')
            user_name = self.line_edit_name_4.text()
            user_id = self.line_edit_id_4.text()
            if user_name != "" and user_id != "" and str.isdigit(user_id):
                cv2.imwrite("photo_register.png", self.image)
                self.db.update_info(self.id, user_name, user_id)
                self.show_to_mod_face_info()
            else:
                msg_text = ""
                if user_id == "" or user_name == "":
                    msg_text = "姓名或密码不能为空"
                else:
                    msg_text = "密码只能为数字"
                msg = QtWidgets.QMessageBox.information(self, "警告！！！", msg_text, QMessageBox.Yes)

    def show_camera(self):
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (glo.CAP_WIDTH, glo.CAP_HEIGHT))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def show_data_face_info(self, _name=None, _id=None, _create_time=None, _last_mod_time=None):
        data, x, y = self.db.get_all_info()
        self.table_5.setRowCount(x)
        self.table_5.setColumnCount(y-1)
        for i in range(x):
            for j in range(y):
                if j != 1:  # 1是BLOB格式照片
                    temp_data = QTableWidgetItem(str(data[i][j]))
                    self.table_5.setItem(i, j, temp_data)
                else:
                    face_info_img = QtGui.QImage.fromData(data[i][j])
                    face_info_pixmap = QtGui.QPixmap.fromImage(face_info_img)
                    face_info_label = QtWidgets.QLabel()
                    face_info_label.setScaledContents(True)
                    face_info_label.setPixmap(face_info_pixmap)
                    face_info_label.setMaximumSize(200, 200)
                    self.table_5.setCellWidget(i, j, face_info_label)

        self.table_5.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_5.setHorizontalHeaderLabels(['编号', '照片', '姓名', 'ID号', '录入时间', '最后修改时间', '操作'])
        self.table_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动分配列宽
        self.table_5.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_5.verticalHeader().setDefaultSectionSize(200)

    def show_to_mod_face_info(self, _name=None, _id=None, _create_time=None, _last_mod_time=None):
        data, x, y = self.db.get_all_info()
        self.table_4.setRowCount(x)
        self.table_4.setColumnCount(y)
        for i in range(x):
           for j in range(y):
                if j == 1:  # 1是BLOB格式照片
                    face_info_img = QtGui.QImage.fromData(data[i][j])
                    face_info_pixmap = QtGui.QPixmap.fromImage(face_info_img)
                    face_info_label = QtWidgets.QLabel()
                    face_info_label.setScaledContents(True)
                    face_info_label.setPixmap(face_info_pixmap)
                    face_info_label.setMaximumSize(200, 200)
                    self.table_4.setCellWidget(i, j, face_info_label)
                elif j == y - 1:
                    self.table_4.setCellWidget(i, j, self.buttonForRow(str(data[i][0])))
                else:
                    temp_data = QTableWidgetItem(str(data[i][j]))
                    self.table_4.setItem(i, j, temp_data)

        self.table_4.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_4.setHorizontalHeaderLabels(['编号', '照片', '姓名', 'ID号', '录入时间', '最后修改时间', '操作'])
        self.table_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动分配列宽
        self.table_4.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_4.verticalHeader().setDefaultSectionSize(200)

    def buttonForRow(self,id):
        widget = QtWidgets.QWidget()
        # 修改
        self.button_update = QtWidgets.QPushButton(u'修改')
        self.button_update.setStyleSheet(''' text-align : center;
                                          background-color : NavajoWhite;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  ''')
        self.button_update.clicked.connect(self.button_update_click)

        # 删除
        self.button_delete = QtWidgets.QPushButton(u'删除')
        self.button_delete.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')
        self.button_delete.clicked.connect(self.button_delete_click)

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.button_update)
        hLayout.addWidget(self.button_delete)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def button_update_click(self):
        button = self.sender()
        id = ''
        if button:
            # 确定位置的时候这里是关键
            row = self.table_4.indexAt(button.parent().pos()).row()
            id = str(self.table_4.takeItem(row, 0).text())
        self.set_right_widget_update_4(id)
        self.button_cam_4.clicked.connect(self.take_photo_4)
        self.right_widget_update_4.show()


    def button_delete_click(self):
        button = self.sender()
        if button:
            # 确定位置的时候这里是关键
            row = self.table_4.indexAt(button.parent().pos()).row()
            id = str(self.table_4.takeItem(row, 0).text())
            self.db.delete_info(id)
            self.show_to_mod_face_info()

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        if self.timer_camera.isActive():
            self.timer_camera.stop()
        event.accept()
