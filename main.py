import sys
from camera import *
from name import *
from rectangle import *
from admin_window import *
from login_window import *


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.cam = Camera()
        self.rec = GetRectangle()
        self.name = GetName()
        self.cam.start()
        self.rec.start()
        self.name.start()
        self.open_camera = False
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.login_window = LoginWindow()
        self.set_ui()
        self.slot_init()

    def set_ui(self):
        self.__layout_main = QHBoxLayout()  # 采用QHBoxLayout类，按照从左到右的顺序来添加控件
        self.__layout_fun_button_1 = QHBoxLayout()
        self.__layout_fun_button_2 = QHBoxLayout()
        self.__layout_fun_menu = QVBoxLayout()
        self.__layout_data_show = QVBoxLayout()  # QVBoxLayout类垂直地摆放小部件

        self.button_open_camera = QPushButton(u'打开相机')
        self.button_admin_login = QPushButton(u'管理员登录')
        self.button_admin_open = QPushButton(u'管理员面板')
        self.button_admin_logout = QPushButton(u'管理员登出')
        self.button_close = QPushButton(u'关闭系统')

        self.button_open_camera.setMinimumHeight(50)
        self.button_admin_login.setMinimumHeight(50)
        self.button_admin_open.setMinimumHeight(50)
        self.button_admin_logout.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)

        # 信息显示
        self.label_show_camera = QLabel()
        self.label_show_name = QLabel()

        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(glo.close_img))
        self.label_show_name.setFixedSize(150, 50)
        self.label_show_name.setText("未检测到人脸")

        """
        布局
        """
        self.__layout_fun_button_1.addWidget(self.button_open_camera)
        self.__layout_fun_button_1.addWidget(self.button_admin_login)
        self.__layout_fun_button_1.addWidget(self.button_close)
        self.__layout_fun_button_2.addWidget(self.button_admin_open)
        self.__layout_fun_button_2.addWidget(self.button_admin_logout)
        self.__layout_fun_menu.addLayout(self.__layout_fun_button_1)
        self.__layout_fun_menu.addLayout(self.__layout_fun_button_2)
        self.__layout_data_show.addWidget(self.label_show_name)
        self.__layout_data_show.addLayout(self.__layout_fun_menu)
        self.__layout_main.addStretch(1)
        self.__layout_main.addWidget(self.label_show_camera)
        self.__layout_main.addLayout(self.__layout_data_show)


        self.setLayout(self.__layout_main)
        self.setWindowTitle(u'Team5-耿申奥、刘欣龙、向宇')

    def slot_init(self):  # 建立通信连接
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.button_admin_login.clicked.connect(self.button_admin_login_click)
        self.button_admin_open.clicked.connect(self.button_admin_open_click)
        self.button_admin_logout.clicked.connect(self.button_admin_logout_click)
        self.button_close.clicked.connect(self.button_close_clicked)

        self.timer_camera.timeout.connect(self.show_camera)

    def button_close_clicked(self):
        self.close()

    def button_open_camera_click(self):
        if not self.open_camera:
            self.open_camera = True
            self.timer_camera.start(30)
            self.button_open_camera.setText(u'关闭相机')
        else:
            self.open_camera = False
            self.label_show_name.setText(glo.DEFAULT_NAME)
            self.timer_camera.stop()
            self.label_show_camera.clear()
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(glo.close_img))
            self.button_open_camera.setText(u'打开相机')

    def button_admin_open_click(self):
        if glo.is_login:
            self.admin_window = AdminWindow(glo.login_name)
            self.admin_window.show()
        else:
            QMessageBox.information(self, "错误", "请先登录！", QMessageBox.Yes)

    def button_admin_login_click(self):
        if not glo.is_login:
            self.login_window.show()
        else:
            QMessageBox.information(self, "错误", "您已登录！", QMessageBox.Yes)

    def button_admin_logout_click(self):
        if glo.is_login:
            result = QMessageBox.question(self, "警告", "您确定要登出吗", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                if self.admin_window.isVisible():
                    self.admin_window.close()
                glo.is_login = False
                glo.login_name = "未登录"
        else:
            QMessageBox.information(self, "错误", "您还未登录", QMessageBox.Yes)

    def show_camera(self):
        glo.lock("show_img")
        r_show = glo.get_value("show_img")
        show = copy.copy(r_show)
        glo.release("show_img")
        glo.lock("rects")
        r_rects = glo.get_value("rects")
        rects = copy.copy(r_rects)
        glo.release("rects")
        for rect in rects:
            top, right, bottom, left = rect
            cv2.rectangle(show, (left, bottom), (right, top), [255, 0, 0], thickness=2)  # 画框圈出脸部
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        glo.lock("name")
        r_name = glo.get_value("name")
        name = copy.copy(r_name)
        glo.release("name")
        self.label_show_name.setText(name)

    def closeEvent(self, event):
        ok = QPushButton()
        cancel = QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'关闭', u'是否关闭！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')
        glo.lock("close")
        glo.set_value("close", True)
        glo.release("close")
        while True:
            if not self.name.is_alive():
                break
        while True:
            if not self.rec.is_alive():
                break
        while True:
            if not self.cam.is_alive():
                break
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if glo.is_login:
                if self.admin_window.isEnabled():
                    self.admin_window.close()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()


if __name__ == '__main__':
    glo.__init__()
    App = QApplication(sys.argv)
    App.setStyleSheet(open('styleSheet.qss', encoding='utf-8').read())
    win = Ui_MainWindow()
    win.show()
    sys.exit(App.exec_())
