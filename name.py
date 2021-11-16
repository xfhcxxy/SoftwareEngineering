import copy
import threading
import time
import os
import glo
import face_recognition as fr
from scipy.spatial import distance as dist


class GetName(threading.Thread):
    def __init__(self):
        super().__init__()
        self.current_images_encoded = []
        self.images = os.listdir('images')
        for image in self.images:
            current_image = fr.load_image_file("images/" + image)
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

    def run(self):
        while True:
            """
            三个标记，是否是有且仅有一个人，是否有监测到睁眼和闭眼这两个状态
            """
            glo.lock("face_now")
            r_exist_one_face = glo.get_value("exist_one_face")
            r_face_img = fr.load_image_file("face_now.png")
            r_eye_close = glo.get_value('eye_close')
            r_eye_open = glo.get_value('eye_open')
            exist_one_face = copy.copy(r_exist_one_face)
            face_img = copy.copy(r_face_img)
            eye_close = copy.copy(r_eye_close)
            eye_open = copy.copy(r_eye_open)
            glo.release("face_now")

            """
            有且仅有一个人脸入镜时开始监测
            先判断是否有睁眼和闭眼两个状态
            两个状态都有时代表为活体，再进行人脸匹配
            """
            if exist_one_face:
                if eye_open and eye_close:
                    faces_img_encoded = fr.face_encodings(face_img)
                    if len(faces_img_encoded) == 0:
                        continue
                    face_img_encoded = faces_img_encoded[0]
                    for i in range(len(self.images)):
                        result = fr.compare_faces([face_img_encoded], self.current_images_encoded[i], tolerance=0.39)
                        if result[0]:
                            print("匹配：" + self.images[i][:-4])
                else:
                    face_landmark_list = fr.face_landmarks(face_img)
                    if len(face_landmark_list) == 0:
                        continue
                    face_landmark = face_landmark_list[0]
                    left_eye = face_landmark['left_eye']
                    right_eye = face_landmark['right_eye']
                    ear_left = self.get_ear(left_eye)
                    ear_right = self.get_ear(right_eye)
                    closed = ear_left < 0.2 and ear_right < 0.2
                    eye_close = eye_close or closed
                    eye_open = eye_open or not closed
                    print("睁眼："+str(eye_open)+" "+"闭眼："+str(eye_close))
                    glo.lock("face_now")
                    glo.set_value('eye_close', eye_close)
                    glo.set_value('eye_open', eye_open)
                    glo.release("face_now")

            """
            start = time.time()
            while True:
                if time.time() - start > 2:
                    break
            """
            glo.lock("close")
            close = glo.get_value("close")
            glo.release("close")
            if close:
                break;