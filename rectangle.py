import copy
import threading
import face_recognition as fr
import glo
import cv2


"""
当镜头里的人离开或不只一个人时，清除三个标记
"""
def clear_info():
    glo.lock("face_now")
    glo.set_value("exist_one_face", False)
    glo.set_value("eye_close", False)
    glo.set_value("eve_open", False)
    glo.release("face_now")


class GetRectangle(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            glo.lock("show_img")
            r_show_img = glo.get_value("show_img")
            show_img = copy.copy(r_show_img)
            glo.release("show_img")

            rgb_show_img = show_img[:, :, ::-1]  # 从BGR转换为RBG
            rects = fr.face_locations(rgb_show_img)  # 寻找并保存人脸框的信息
            # print(len(rects))
            glo.lock("rects")
            glo.set_value("rects", rects)
            glo.release("rects")

            if len(rects) == 1:  # 当屏幕前只有一个人时保存照片
                top, right, bottom, left = rects[0]
                if bottom - top < 100 or right - left < 100:
                    print("请靠近摄像头")
                    clear_info()
                else:
                    glo.lock("face_now")
                    cv2.imwrite("face_now" + ".png", show_img)
                    glo.set_value("exist_one_face", True)
                    glo.release("face_now")
            else:
                clear_info()