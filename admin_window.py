import copy
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import glo
from db import *


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.init_ui()
        self.slot_init()
        self.db = DataBase()

    def init_ui(self):
        self.setWindowTitle("管理员")
        self.setFixedSize(960, 700)
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

        self.label_show_camera_1 = QtWidgets.QLabel()
        self.label_show_camera_1.setFixedSize(641, 481)
        self.label_show_camera_1.setAutoFillBackground(False)

        self.button_ask_1 = QtWidgets.QPushButton(u'打开相机')


        self.right_layout_1.addWidget(self.label_name_1, 0, 2, 1, 2)
        self.right_layout_1.addWidget(self.line_edit_name_1, 0, 4, 1, 6)
        self.right_layout_1.addWidget(self.label_id_1, 2, 2, 1, 2)
        self.right_layout_1.addWidget(self.line_edit_id_1, 2, 4, 1, 6)
        self.right_layout_1.addWidget(self.label_show_camera_1, 4, 2, 1, 10)
        self.right_layout_1.addWidget(self.button_ask_1, 5, 5, 1, 2)


    def set_right_widget_2(self):
        print("待写2")

    def set_right_widget_3(self):
        print("待写3")

    def set_right_widget_4(self):
        print("待写4")

    def set_right_widget_5(self):
        print("待写5")

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
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_2_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.show()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_3_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.show()
        self.right_widget_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_4_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.show()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_5_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_5.show()
        self.right_widget_6.hide()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_6_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.show()
        self.right_widget_7.hide()
        self.right_widget_8.hide()

    def button_left_7_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
        self.right_widget_5.hide()
        self.right_widget_6.hide()
        self.right_widget_7.show()
        self.right_widget_8.hide()

    def button_left_8_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()
        self.right_widget_4.hide()
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











    def show_camera(self):
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (glo.CAP_WIDTH, glo.CAP_HEIGHT))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera_1.setPixmap(QtGui.QPixmap.fromImage(showImage))

