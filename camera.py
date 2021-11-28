import threading
import cv2

import glo


class Camera(threading.Thread):
    def __init__(self):
        super().__init__()
        self.CAM_NUM = 0
        self.cap = cv2.VideoCapture()  # 初始化摄像头

    def run(self):
        self.cap.open(self.CAM_NUM)
        while True:
            flag, self.image = self.cap.read()
            show = cv2.resize(self.image, (glo.CAP_WIDTH, glo.CAP_HEIGHT))
            glo.lock("show_img")
            glo.set_value("show_img", show)
            glo.release("show_img")
            cv2.waitKey(int(1000/60))

            glo.lock("close")
            close = glo.get_value("close")
            glo.release("close")
            if close:
                break
