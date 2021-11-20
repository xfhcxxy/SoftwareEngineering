import MySQLdb
import datetime


class DataBase:
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "test", "123456", "team5", charset='utf8')

    def add_photo(self, user_name, user_id):
        cursor = self.db.cursor()
        fp = open("photo_register.png", 'rb')
        img = fp.read()
        fp.close()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO face_info VALUES(%s,_binary %s,%s,%s,%s,%s,%s)", (None, MySQLdb.Binary(img), user_name, int(user_id), dt, dt, 1))
        self.db.commit()
        cursor.close()

    def update_info(self, id, user_name, user_id):
        cursor = self.db.cursor()
        fp = open("photo_register.png", 'rb')
        img = fp.read()
        fp.close()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE face_info SET FaceImg = %s, Name = %s, IdNum = %s, LastModTime = %s WHERE id = %s",
                       (MySQLdb.Binary(img), user_name, int(user_id), dt, id))
        self.db.commit()
        cursor.close()

    def delete_info(self, id):
        cursor = self.db.cursor()
        cursor.execute("UPDATE face_info SET IsValid = 0 WHERE Id =" + id)
        self.db.commit()
        cursor.close()

    def get_name(self, id):
        cursor = self.db.cursor()
        cursor.execute("SELECT Name FROM face_info WHERE Id =" + id)
        # cursor.execute("SELECT Name FROM face_info WHERE Id = 1")
        name = cursor.fetchone()
        cursor.close()
        return str(name[0])

    def get_id_num(self, id):
        cursor = self.db.cursor()
        cursor.execute("SELECT IdNum FROM face_info WHERE Id =" + id)
        # cursor.execute("SELECT Name FROM face_info WHERE Id = 1")
        id_num = cursor.fetchone()
        cursor.close()
        return str(id_num[0])

    def get_face_img(self, id):
        cursor = self.db.cursor()
        cursor.execute("SELECT FaceImg FROM face_info WHERE Id =" + id)
        # cursor.execute("SELECT Name FROM face_info WHERE Id = 1")
        face_img = cursor.fetchone()
        cursor.close()
        return face_img[0]

    def get_all_info(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM face_info")
        data = cursor.fetchall()
        x = 0
        y = 7
        _data = []
        for info in data:  # 选出没被删除的部分
            if info[6] == b'\x01':  # bit类型的1，即该条数据未被删除
                _data.append(info)
                x += 1
        return _data, x, y


# if __name__ == '__main__':
#     db = DataBase()
#     db.get_name()
