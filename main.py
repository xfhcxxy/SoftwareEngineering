import sys
from name import *
from rectangle import *
from admin_window import *
from login_window import *


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.login_window = LoginWindow()
        self.CAM_NUM = 0
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.set_ui()
        self.slot_init()

    def set_ui(self):
        self.__layout_main = QtWidgets.QHBoxLayout()  # 采用QHBoxLayout类，按照从左到右的顺序来添加控件
        self.__layout_fun_button_1 = QtWidgets.QHBoxLayout()
        self.__layout_fun_button_2 = QHBoxLayout()
        self.__layout_fun_menu = QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()  # QVBoxLayout类垂直地摆放小部件

        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_admin_login = QtWidgets.QPushButton(u'管理员登录')
        self.button_admin_open = QtWidgets.QPushButton(u'管理员面板')
        self.button_admin_logout = QtWidgets.QPushButton(u'登出')
        self.button_close = QtWidgets.QPushButton(u'关闭系统')

        self.button_open_camera.setMinimumHeight(50)
        self.button_admin_login.setMinimumHeight(50)
        self.button_admin_open.setMinimumHeight(50)
        self.button_admin_logout.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_show_name = QtWidgets.QLabel()

        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)
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

        '''
        # 设置背景颜色
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(),QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''

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
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
                # if msg==QtGui.QMessageBox.Cancel:
                #                     pass
            else:
                glo.lock("close")
                glo.set_value("close", False)
                glo.release("close")
                self.rec = GetRectangle()
                self.name = GetName()
                self.rec.start()
                self.name.start()
                self.timer_camera.start(30)
                self.button_open_camera.setText(u'关闭相机')
        else:
            glo.lock("close")
            glo.set_value("close", True)  # 给画框线程和识别线程信号，令其停止
            glo.release("close")
            self.label_show_name.setText(glo.DEFAULT_NAME)
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
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
                print(1)
                if self.admin_window.isVisible():
                    self.admin_window.close()
                glo.is_login = False
                glo.login_name = "未登录"
        else:
            QMessageBox.information(self, "错误", "您还未登录", QMessageBox.Yes)

    def show_camera(self):
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (glo.CAP_WIDTH, glo.CAP_HEIGHT))
        glo.lock("show_img")
        glo.set_value("show_img", show)
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
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'关闭', u'是否关闭！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            glo.lock("close")
            glo.set_value("close", True)
            glo.release("close")
            if glo.is_login:
                if self.admin_window.isEnabled():
                    self.admin_window.close()
            if self.admin_window.isEnabled():
                self.admin_window.close()
            if self.cap.isOpened():
                self.cap.release()
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
