import copy
import cv2
import face_recognition as fr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
import glo
from db import *
import name


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, admin_name="未登录"):
        super().__init__()
        self.WIDTH = 200
        self.HEIGHT = 150
        self.id = -1
        self.open_camera_1 = False
        self.open_camera_2 = False
        self.admin_name = admin_name
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.db = DataBase()
        self.init_ui()
        self.slot_init()
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_3.hide()

    def init_ui(self):
        self.setWindowTitle("管理员")
        self.setFixedSize(1800, 700)
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

        self.button_ask_1.clicked.connect(self.take_photo_1)
        self.button_ok_1.clicked.connect(self.take_photo_ok_1)
        self.button_ask_2.clicked.connect(self.show_to_mod_face_info)
        self.button_ask_3.clicked.connect(self.show_ope_history)

    """
    左窗口
    """

    def left_design(self):

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.label_left_1 = QtWidgets.QLabel("您好，" + self.admin_name)
        self.label_left_1.setAlignment(Qt.AlignCenter)
        self.label_left_1.setObjectName('admin_label')
        self.label_left_1.setMaximumHeight(50)

        self.button_left_1 = QtWidgets.QPushButton("增加人像信息")
        self.button_left_1.setObjectName('left_button')
        self.button_left_2 = QtWidgets.QPushButton("管理人像信息")
        self.button_left_2.setObjectName('left_button')
        self.button_left_3 = QtWidgets.QPushButton("浏览操作记录")
        self.button_left_3.setObjectName('left_button')
        self.button_left_4 = QtWidgets.QPushButton("关闭")
        self.button_left_4.setObjectName('left_button')

        self.button_left_1.setMinimumHeight(50)
        self.button_left_2.setMinimumHeight(50)
        self.button_left_3.setMinimumHeight(50)
        self.button_left_4.setMinimumHeight(50)

        self.left_layout.addWidget(self.label_left_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_3, 7, 0, 1, 3)
        self.left_layout.addWidget(self.button_left_4, 10, 0, 1, 3)

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)

    """
    右窗口
    """

    def right_design(self):
        self.right_widget_1 = QtWidgets.QWidget()  # 增加人像信息
        self.right_widget_1.setObjectName('right_widget')
        self.right_layout_1 = QtWidgets.QGridLayout()
        self.right_widget_1.setLayout(self.right_layout_1)
        self.right_widget_2 = QtWidgets.QWidget()  # 修改人像信息
        self.right_widget_2.setObjectName('right_widget')
        self.right_layout_2 = QtWidgets.QGridLayout()
        self.right_widget_2.setLayout(self.right_layout_2)
        self.right_widget_update_2 = QtWidgets.QWidget()  # 修改人像信息-xiu gai zhong
        # self.right_widget_update_2.setObjectName('right_widget')
        self.right_layout_update_2 = QtWidgets.QGridLayout()
        self.right_widget_update_2.setLayout(self.right_layout_update_2)
        self.right_widget_3 = QtWidgets.QWidget()  # 查看删改记录
        self.right_widget_3.setObjectName('right_widget')
        self.right_layout_3 = QtWidgets.QGridLayout()
        self.right_widget_3.setLayout(self.right_layout_3)

        self.main_layout.addWidget(self.right_widget_1, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_2, 0, 2, 12, 10)
        self.main_layout.addWidget(self.right_widget_3, 0, 2, 12, 10)

        self.set_right_widget_1()
        self.set_right_widget_2()
        self.set_right_widget_3()

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
        self.button_ok_1 = QPushButton(u'确认添加')

        self.right_layout_1.addWidget(self.label_name_1, 0, 1, 1, 2)
        self.right_layout_1.addWidget(self.line_edit_name_1, 0, 6, 1, 6)
        self.right_layout_1.addWidget(self.label_id_1, 2, 1, 1, 2)
        self.right_layout_1.addWidget(self.line_edit_id_1, 2, 6, 1, 6)
        self.right_layout_1.addWidget(self.label_show_camera_1, 4, 6, 1, 10)
        self.right_layout_1.addWidget(self.button_ask_1, 5, 5, 1, 2)
        self.right_layout_1.addWidget(self.button_ok_1, 5, 9, 1, 2)

    def set_right_widget_2(self):
        self.table_2 = QtWidgets.QTableWidget()
        self.button_ask_2 = QtWidgets.QPushButton(u"查看")
        self.right_layout_2.addWidget(self.table_2, 0, 2, 10, 10)
        self.right_layout_2.addWidget(self.button_ask_2, 11, 6, 1, 2)

        self.label_show_camera_2 = QtWidgets.QLabel()
        self.label_show_camera_2.setFixedSize(self.WIDTH, self.HEIGHT)
        self.label_show_camera_2.setAutoFillBackground(False)

    def set_right_widget_update_2(self, _id):
        face_img, name_before, id_num_before = self.db.get_info_before_update(_id)

        self.label_name_2 = QtWidgets.QLabel()
        self.label_name_2.setText("请输入修改后姓名：")
        self.line_edit_name_2 = QtWidgets.QLineEdit()
        self.line_edit_name_2.setFont(QFont('Arial', 14))
        self.line_edit_name_2.setText(name_before)

        self.label_id_2 = QtWidgets.QLabel()
        self.label_id_2.setText("请输入修改后ID：")
        self.line_edit_id_2 = QtWidgets.QLineEdit()
        self.line_edit_id_2.setFont(QFont('Arial', 14))
        self.line_edit_id_2.setText(id_num_before)

        self.label_show_pic_2 = QtWidgets.QLabel()
        self.label_show_pic_2.setFixedSize(self.WIDTH, self.HEIGHT)
        self.label_show_pic_2.setAutoFillBackground(False)
        face_info_img = QtGui.QImage.fromData(face_img)
        face_info_pixmap = QtGui.QPixmap.fromImage(face_info_img)
        self.label_show_pic_2.setScaledContents(True)
        self.label_show_pic_2.setPixmap(face_info_pixmap)

        self.id = _id

        self.button_cam_2 = QtWidgets.QPushButton(u'打开相机')
        self.button_ok_2 = QPushButton(u'确认修改')
        self.button_ok_2.clicked.connect(self.take_photo_ok_2)

        self.right_layout_update_2.addWidget(self.label_name_2, 0, 2, 1, 2)
        self.right_layout_update_2.addWidget(self.line_edit_name_2, 0, 4, 1, 6)
        self.right_layout_update_2.addWidget(self.label_id_2, 2, 2, 1, 2)
        self.right_layout_update_2.addWidget(self.line_edit_id_2, 2, 4, 1, 6)
        self.right_layout_update_2.addWidget(self.label_show_pic_2, 4, 1, 1, 10)
        self.right_layout_update_2.addWidget(self.label_show_camera_2, 4, 12, 1, 10)
        self.right_layout_update_2.addWidget(self.button_cam_2, 5, 5, 1, 2)
        self.right_layout_update_2.addWidget(self.button_ok_2, 5, 9, 1, 2)

    def set_right_widget_3(self):
        self.table_3 = QtWidgets.QTableWidget()
        self.button_ask_3 = QtWidgets.QPushButton(u"查看")
        self.right_layout_3.addWidget(self.table_3, 0, 2, 10, 10)
        self.right_layout_3.addWidget(self.button_ask_3, 11, 6, 1, 2)

    def button_left_1_click(self):
        self.right_widget_1.show()
        self.right_widget_2.hide()
        self.right_widget_update_2.hide()
        self.right_widget_3.hide()

    def button_left_2_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.show()
        self.right_widget_update_2.hide()
        self.right_widget_3.hide()

    def button_left_3_click(self):
        self.right_widget_1.hide()
        self.right_widget_2.hide()
        self.right_widget_update_2.hide()
        self.right_widget_3.show()

    def button_left_4_click(self):
        self.close()

    def take_photo_1(self):
        if not self.open_camera_1:
            self.open_camera_1 = True
            self.timer_camera.start(30)
            self.button_ask_1.setText(u'确定')
        else:
            self.open_camera_1 = False
            self.timer_camera.stop()
            self.button_ask_1.setText(u'打开相机')

    def take_photo_ok_1(self):
        user_name = self.line_edit_name_1.text()
        user_id = self.line_edit_id_1.text()
        user_face_img = self.label_show_camera_1.pixmap()
        msg_text = ""
        if user_face_img:
            image_encoded = fr.face_encodings(self.image)
            num = len(image_encoded)
            if num == 1 and user_name and user_id and user_face_img and str.isdigit(user_id):
                result = QMessageBox.question(self, "警告", "您确定要添加此信息吗", QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    cv2.imwrite("photo_register.png", self.image)
                    self.db.add_photo(user_name, user_id)
                    name.load()
            else:
                if user_id == "" or user_name == "":
                    msg_text = "姓名不能为空"
                elif user_name == "":
                    msg_text = "ID号不能为空"
                elif not str.isdigit(user_id):
                    msg_text = "ID号只能为数字"
                elif num == 0:
                    msg_text = "未识别到人脸"
                elif num > 1:
                    msg_text = "人数大于1"
                msg = QMessageBox.information(self, "警告！！！", msg_text, QMessageBox.Yes)
        else:
            msg_text = "请录入人脸"
            msg = QMessageBox.information(self, "警告！！！", msg_text, QMessageBox.Yes)

    def take_photo_2(self):
        if not self.open_camera_2:
            self.open_camera_2 = True
            self.timer_camera.start(30)
            self.button_cam_2.setText(u'确定')
        else:
            self.open_camera_2 = False
            self.timer_camera.stop()
            self.button_cam_2.setText(u'打开相机')

    def take_photo_ok_2(self):
        user_name = self.line_edit_name_2.text()
        user_id = self.line_edit_id_2.text()
        user_face_img = self.label_show_camera_2.pixmap()
        msg_text = ""
        if user_face_img:
            image_encoded = fr.face_encodings(self.image)
            num = len(image_encoded)
            if num == 1 and user_name and user_id and user_face_img and str.isdigit(user_id):
                result = QMessageBox.question(self, "警告", "您确定要修改此信息吗", QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    cv2.imwrite("photo_register.png", self.image)
                    self.db.update_info_with_img(self.id, user_name, user_id)
                    self.db.add_ope_history(self.label_left_1.text().split("，")[1], self.id, 0)
                    self.right_widget_update_2.close()
                    self.show_to_mod_face_info()
                    name.load()
            else:
                if user_id == "" or user_name == "":
                    msg_text = "姓名不能为空"
                elif user_name == "":
                    msg_text = "ID号不能为空"
                elif not str.isdigit(user_id):
                    msg_text = "ID号只能为数字"
                elif num == 0:
                    msg_text = "未识别到人脸"
                elif num > 1:
                    msg_text = "人数大于1"
                msg = QMessageBox.information(self, "警告！！！", msg_text, QMessageBox.Yes)
        else:
            if user_name and user_id and str.isdigit(user_id):
                result = QMessageBox.question(self, "警告", "您确定要修改此信息吗", QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    self.db.update_info_without_img(self.id, user_name, user_id)
                    self.db.add_ope_history(self.label_left_1.text().split("，")[1], self.id, 0)
                    self.right_widget_update_2.close()
                    self.show_to_mod_face_info()
                    name.load()
            else:
                if user_id == "" or user_name == "":
                    msg_text = "姓名不能为空"
                elif user_id == "":
                    msg_text = "ID号不能为空"
                else:
                    msg_text = "ID号只能为数字"
                msg = QtWidgets.QMessageBox.information(self, "警告！！！", msg_text, QMessageBox.Yes)

    def show_camera(self):
        glo.lock("show_img")
        r_show_1 = glo.get_value("show_img")
        show_1 = copy.copy(r_show_1)
        glo.release("show_img")
        self.image = show_1
        show_2 = copy.copy(show_1)
        show_1 = cv2.cvtColor(show_1, cv2.COLOR_BGR2RGB)
        showImage_1 = QtGui.QImage(show_1.data, show_1.shape[1], show_1.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera_1.setPixmap(QtGui.QPixmap.fromImage(showImage_1))
        show_2 = cv2.resize(show_2, (self.WIDTH, self.HEIGHT))
        show_2 = cv2.cvtColor(show_2, cv2.COLOR_BGR2RGB)
        showImage_2 = QtGui.QImage(show_2.data, show_2.shape[1], show_2.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera_2.setPixmap(QtGui.QPixmap.fromImage(showImage_2))

    def show_to_mod_face_info(self, _name=None, _id=None, _create_time=None, _last_mod_time=None):
        data, x, y = self.db.get_all_info()
        self.table_2.setRowCount(x)
        self.table_2.setColumnCount(y)
        for i in range(x):
            for j in range(y):
                if j == 1:  # 1是BLOB格式照片
                    face_info_img = QtGui.QImage.fromData(data[i][j])
                    face_info_pixmap = QtGui.QPixmap.fromImage(face_info_img)
                    face_info_label = QtWidgets.QLabel()
                    face_info_label.setScaledContents(True)
                    face_info_label.setPixmap(face_info_pixmap)
                    face_info_label.setMaximumSize(self.WIDTH, self.HEIGHT)
                    self.table_2.setCellWidget(i, j, face_info_label)
                elif j == y - 1:
                    self.table_2.setCellWidget(i, j, self.buttonForRow())
                else:
                    temp_data = QTableWidgetItem(str(data[i][j]))
                    self.table_2.setItem(i, j, temp_data)

        self.table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_2.setHorizontalHeaderLabels(['编号', '照片', '姓名', 'ID号', '录入时间', '最后修改时间', '操作'])
        self.table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动分配列宽
        self.table_2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_2.verticalHeader().setDefaultSectionSize(self.HEIGHT)

    def buttonForRow(self):
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
        _id = ''
        if button:
            # 确定位置的时候这里是关键
            row = self.table_2.indexAt(button.parent().pos()).row()
            _id = str(self.table_2.item(row, 0).text())

        self.set_right_widget_update_2(_id)
        self.button_cam_2.clicked.connect(self.take_photo_2)
        self.right_widget_update_2.show()

    def button_delete_click(self):
        button = self.sender()
        if button:
            # 确定位置的时候这里是关键
            row = self.table_2.indexAt(button.parent().pos()).row()
            id = str(self.table_2.item(row, 0).text())
            result = QMessageBox.question(self, "警告", "您确定要删除此信息吗", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.db.delete_info(id)
                self.db.add_ope_history(self.label_left_1.text().split("，")[1], id, 1)
                self.show_to_mod_face_info()

    def show_ope_history(self, _OpeTime=None, _Name=None, _Ope_Id=None):
        data, x, y = self.db.get_all_ope_info()
        self.table_3.setRowCount(x)
        self.table_3.setColumnCount(y)
        for i in range(x):
            for j in range(y):
                info = ""
                if j == 3:
                    if data[i][3] == b"\x01":
                        info = "删除"
                    else:
                        info = "修改"
                else:
                    info = str(data[i][j])
                temp_data = QTableWidgetItem(info)
                self.table_3.setItem(i, j, temp_data)
        self.table_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_3.setHorizontalHeaderLabels(['操作时间', '操作管理员姓名', '被操作人脸信息编号', '操作类型'])
        self.table_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动分配列宽
        self.table_3.verticalHeader().setDefaultSectionSize(self.HEIGHT)

    def closeEvent(self, event):
        if self.timer_camera.isActive():
            self.timer_camera.stop()
        event.accept()
