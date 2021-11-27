import copy
import threading
import time
import os
import glo
import face_recognition as fr
from scipy.spatial import distance as dist
import numpy as np
from db import *
import cv2
from keras.preprocessing import image
from keras.models import load_model


class GetName(threading.Thread):
    def __init__(self):
        super().__init__()
        self.db = DataBase()
        self.load()
        self.model = load_model("train_mask/model/maskAndNoMask1.h5")
        """
        for image in self.images:
            current_image = fr.load_image_file("images/" + image)
            self.current_images_encoded.append(fr.face_encodings(current_image)[0])
        """

    def load(self):
        self.current_images_encoded = []
        self.images = []
        data, x, y = self.db.get_all_info()
        for i in range(x):
            self.images.append(data[i][2])
            fout = open("temporary.png", "wb")
            fout.write(data[i][1])
            current_image = fr.load_image_file("temporary.png")
            self.current_images_encoded.append(fr.face_encodings(current_image)[0])

    """
    计算眼睛纵横比
    """
    def get_ear(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def set_name(self, name):
        glo.lock("name")
        glo.lock("face_now")
        r_exist_one_face = glo.get_value("exist_one_face")
        exist_one_face = copy.copy(r_exist_one_face)
        glo.release("face_now")
        if exist_one_face:
            glo.set_value("name", name)
        glo.release("name")

    def run(self):
        while True:
            """
            三个标记，是否是有且仅有一个人，是否有监测到睁眼和闭眼这两个状态
            """
            glo.lock("face_now")
            r_exist_one_face = glo.get_value("exist_one_face")
            r_face_img = fr.load_image_file("face_now.png")
            r_face_gbr = cv2.imread("face_now.png")
            r_eye_close = glo.get_value('eye_close')
            r_eye_open = glo.get_value('eye_open')
            exist_one_face = copy.copy(r_exist_one_face)
            face_img = copy.copy(r_face_img)
            face_gbr = copy.copy(r_face_gbr)
            eye_close = copy.copy(r_eye_close)
            eye_open = copy.copy(r_eye_open)

            glo.release("face_now")

            """
            有且仅有一个人脸入镜时开始监测
            先判断是否有睁眼和闭眼两个状态
            两个状态都有时代表为活体，再进行人脸匹配
            """
            if exist_one_face:
                rects = fr.face_locations(face_img)
                if len(rects) == 0:
                    continue
                top, right, bottom, left = rects[0]
                height = bottom - top
                width  = right - left
                top = max(0, top - int(height*0.3))
                #bottom = min(glo.CAP_HEIGHT, bottom + int(height*0.3))
                left = max(0, left - int(width*0.3))
                right = min(glo.CAP_WIDTH, right + int(width*0.3))
                mask_dec = face_gbr[top:bottom, left:right]
                cv2.imwrite("mask_dec.png", mask_dec)
                #cv2.imshow("test", mask_dec)
                img = image.load_img("mask_dec.png", target_size=(150, 150))
                img_tensor = image.img_to_array(img) / 255.0
                img_tensor = np.expand_dims(img_tensor, axis=0)
                prediction = self.model.predict(img_tensor)
                #print(prediction)
                if prediction[0][0] < 0.5:
                    self.set_name("请取下口罩")
                    continue
                if eye_open and eye_close:
                    faces_img_encoded = fr.face_encodings(face_img)
                    if len(faces_img_encoded) == 0:
                        continue
                    face_img_encoded = faces_img_encoded[0]
                    get_name = False
                    for i in range(len(self.images)):
                        result = fr.compare_faces([face_img_encoded], self.current_images_encoded[i], tolerance=0.39)
                        if result[0]:
                            self.set_name("匹配：" + self.images[i])
                            get_name = True
                            break
                    if not get_name:
                        self.set_name("未匹配")
                else:
                    face_landmark_list = fr.face_landmarks(face_img)
                    if len(face_landmark_list) == 0:
                        continue
                    self.set_name("请眨眼")
                    face_landmark = face_landmark_list[0]
                    left_eye = face_landmark['left_eye']
                    right_eye = face_landmark['right_eye']
                    ear_left = self.get_ear(left_eye)
                    ear_right = self.get_ear(right_eye)
                    closed = ear_left < 0.2 and ear_right < 0.2
                    eye_close = eye_close or closed
                    eye_open = eye_open or not closed
                    glo.lock("face_now")
                    r_exist_one_face = glo.get_value("exist_one_face")
                    exist_one_face = copy.copy(r_exist_one_face)
                    if exist_one_face:
                        glo.set_value('eye_close', eye_close)
                        glo.set_value('eye_open', eye_open)
                    glo.release("face_now")



            glo.lock("close")
            close = glo.get_value("close")
            glo.release("close")
            if close:
                break
