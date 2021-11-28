import copy
import threading
import face_recognition as fr
import glo
import cv2


"""
当镜头里的人离开或不只一个人时，清除四个标记
"""
def clear_info(name=glo.DEFAULT_NAME):
    glo.lock("face_now")
    glo.set_value("exist_one_face", False)
    glo.set_value("eye_close", False)
    glo.set_value("eve_open", False)
    glo.release("face_now")
    glo.lock("name")
    glo.set_value("name", name)
    glo.release("name")


class GetRectangle(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        clear_info()
        while True:
            glo.lock("show_img")
            r_show_img = glo.get_value("show_img")
            show_img = copy.copy(r_show_img)
            glo.release("show_img")
            rects = fr.face_locations(show_img)  # 寻找并保存人脸框的信息
            glo.lock("rects")
            glo.set_value("rects", rects)
            glo.release("rects")
            if len(rects) == 1:  # 当屏幕前只有一个人时保存照片
                top, right, bottom, left = rects[0]
                if bottom - top < 100 or right - left < 100:
                    clear_info("请靠近摄像头")
                else:
                    glo.lock("face_now")
                    cv2.imwrite("face_now" + ".png", show_img)
                    glo.set_value("exist_one_face", True)
                    glo.release("face_now")

            else:
                if len(rects) > 1:
                    clear_info("人数大于1")
                else:
                    clear_info()

            glo.lock("close")
            close = glo.get_value("close")
            glo.release("close")
            if close:
                break
