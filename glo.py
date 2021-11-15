import numpy as np
import os
import threading
import time
import cv2

"""全局常量"""
########################################################################################
"""相机参数"""
CAM_NAME = 0  # 0:系统相机/1:usb相机
WIN_NAME = "homework"

""""像素"""
CAP_WIDTH = int(640)
CAP_HEIGHT = int(480)
########################################################################################


"""全局变量"""

########################################################################################
mutex = {}
T0 = time.time()


def __init__():
    global mutex
    mutex['show_img'] = threading.Lock()
    mutex['face_now'] = threading.Lock()
    mutex['rects'] = threading.Lock()
    global _global_dict
    _global_dict = {}
    _global_dict["show_img"] = np.zeros((CAP_HEIGHT, CAP_WIDTH, 3), np.uint8)
    _global_dict["known_faces"] = os.listdir('images')
    _global_dict["rects"] = []
    _global_dict["names"] = []
    _global_dict["exist_one_face"] = False
    _global_dict["eye_close"] = False
    _global_dict["eye_open"] = False
    global T0
    T0 = time.time()


def set_value(key, value):
    _global_dict[key] = value


def get_value(key):
    try:
        return _global_dict[key]
    except:
        KeyError


def lock(val):
    mutex[val].acquire()


def release(val):
    mutex[val].release()
