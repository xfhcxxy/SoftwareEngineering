import copy
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont
import glo
import sys
from db import *


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.db = DataBase()
        self.setFixedSize(400, 200)
        self.setWindowTitle('管理员登录')
        self.set_ui()

    def set_ui(self):
        # 设置字体
        login_window_font = QFont()
        login_window_font.setFamily('Consolas')
        login_window_font.setPixelSize(22)

        # 创建标签并设置文本及格式
        self.label_name = QLabel(self)
        self.label_name.setText("管理员姓名")
        self.label_name.setFont(login_window_font)
        self.label_name.move(10, 14)
        self.lable_passwd = QLabel(self)
        self.lable_passwd.setText("管理员权限码")
        self.lable_passwd.setFont(login_window_font)
        self.lable_passwd.move(10, 74)

        # 创建输入框
        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setFont(login_window_font)
        self.line_edit_name.move(150, 10)
        self.line_edit_passwd = QLineEdit(self)
        self.line_edit_passwd.setFont(login_window_font)
        self.line_edit_passwd.setEchoMode(QLineEdit.Password)
        self.line_edit_passwd.move(150, 70)

        # 创建按钮
        self.button_login = QPushButton(self)
        self.button_login.setFont(login_window_font)
        self.button_login.move(240, 150)
        self.button_login.setText("登录")
        self.button_login.clicked.connect(self.button_login_click)
        self.button_cancel = QPushButton(self)
        self.button_cancel.setFont(login_window_font)
        self.button_cancel.move(70, 150)
        self.button_cancel.setText("取消")
        self.button_cancel.clicked.connect(self.button_cancel_click)

    def button_login_click(self):
        login_name = self.line_edit_name.text()
        login_passwd = self.line_edit_passwd.text()
        data = self.db.login(login_name)
        if login_passwd and login_name:
            if data:
                if str(data[0][1]) == login_passwd:
                    QMessageBox.information(self, "登录成功", "权限确认！", QMessageBox.Yes)
                    glo.is_login = True
                    glo.login_name = login_name
                    self.close()
                else:
                    QMessageBox.information(self, "登录失败", "权限码错误！", QMessageBox.Yes)
            else:
                QMessageBox.information(self, "登录失败", "不存在的管理员姓名！", QMessageBox.Yes)
        elif login_name:
            QMessageBox.information(self, "登录失败", "请输入权限码！", QMessageBox.Yes)
        elif login_passwd:
            QMessageBox.information(self, "登录失败", "请输入姓名！", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "登录失败", "请输入姓名和权限码！", QMessageBox.Yes)

    def button_cancel_click(self):
        self.close()
