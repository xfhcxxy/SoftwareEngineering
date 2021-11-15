import copy
import threading
import cv2
import os
import face_recognition as fr
import numpy as np
import time
from name import *
from rectangle import *
import glo


class OpcvCapture(threading.Thread):
    def __init__(self, win_name, cam_name):
        super().__init__()
        self.cam_name = cam_name
        self.win_name = win_name

    def run(self):
        capture = cv2.VideoCapture(glo.CAM_NAME)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, glo.CAP_WIDTH)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, glo.CAP_HEIGHT)
        while True:            # 获取一帧
            ret, frame = capture.read()            # 获取的帧送入检测，绘制检测结果后返回,自拍模式做镜像
            # frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            show_img = cv2.flip(frame, flipCode=1)

            glo.lock("show_img")
            glo.set_value("show_img", show_img)
            glo.release("show_img")

            glo.lock("rects")
            r_rects = glo.get_value("rects")
            rects = copy.copy(r_rects)
            glo.release("rects")

            show_img2 = copy.copy(show_img)

            for rect in rects:
                top, right, bottom, left = rect
                cv2.rectangle(show_img2, (left, bottom), (right, top), [255, 0, 0], thickness=2) #画框圈出脸部
            cv2.imshow(glo.WIN_NAME, show_img2)
            cv2.waitKey(int(1000/60))  # 1000/帧数


if __name__ == "__main__":
    glo.__init__()
    cam = OpcvCapture("camera1", 0)
    rec = GetRectangle()
    name = GetName()
    cam.start()
    rec.start()
    name.start()
