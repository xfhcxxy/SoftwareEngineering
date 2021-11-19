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
