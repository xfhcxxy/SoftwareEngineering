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

    def update_info_with_img(self, id, user_name, user_id):
        cursor = self.db.cursor()
        fp = open("photo_register.png", 'rb')
        img = fp.read()
        fp.close()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE face_info SET FaceImg = %s, Name = %s, IdNum = %s, LastModTime = %s WHERE id = %s",
                       (MySQLdb.Binary(img), user_name, int(user_id), dt, id))
        self.db.commit()
        cursor.close()

    def update_info_without_img(self, _id, user_name, user_id):
        cursor = self.db.cursor()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE face_info SET Name = %s, IdNum = %s, LastModTime = %s WHERE id = %s",
                       (user_name, int(user_id), dt, _id))
        self.db.commit()
        cursor.close()

    def delete_info(self, _id):
        cursor = self.db.cursor()
        cursor.execute("UPDATE face_info SET IsValid = 0 WHERE Id =" + _id)
        self.db.commit()
        cursor.close()

    def get_info_before_update(self, _id):
        cursor = self.db.cursor()
        cursor.execute("SELECT FaceImg, Name, IdNum FROM face_info WHERE Id =" + _id)
        data = cursor.fetchone()
        self.db.commit()
        cursor.close()
        return data[0], str(data[1]), str(data[2])

    """
    查询所有人脸信息
    """
    def get_all_info(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM face_info")
        data = cursor.fetchall()
        self.db.commit()
        cursor.close()
        x = 0
        y = 7
        _data = []
        for info in data:  # 选出没被删除的部分
            if info[6] == b'\x01':  # bit类型的1，即该条数据未被删除
                _data.append(info)
                x += 1
        return _data, x, y


    def get_face_info_num(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM face_info")
        num = cursor.fetchone()
        self.db.commit()
        cursor.close()
        return num

    """
    获取所有操作记录信息
    """
    def get_all_ope_info(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM delete_history")
        data = cursor.fetchall()
        self.db.commit()
        cursor.close()
        x = 0
        y = 4
        _data = []
        for info in data:
            _data.append(info)
            x += 1
        return _data, x, y

    """
    增加一条操作记录，ope_type=1为删除，=0为修改
    """
    def add_ope_history(self, user_name, user_id, ope_type):
        cursor = self.db.cursor()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO delete_history VALUES(%s,%s,%s,%s)", (dt, user_name, int(user_id), ope_type))
        self.db.commit()
        cursor.close()

    """
    根据管理员姓名查询密码
    """
    def login(self, login_name):
        cursor = self.db.cursor()
        cursor.execute(u"SELECT Name, Password FROM admin_passwd WHERE Name='" + login_name + "'")
        data = cursor.fetchall()
        self.db.commit()
        cursor.close()
        return data
