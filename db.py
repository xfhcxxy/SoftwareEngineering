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
        print(user_name, int(user_id))
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO face_info VALUES(%s,%s,%s,%s,%s,%s,%s)", (MySQLdb.Binary(img), user_name, int(user_id), dt, dt, 1, None))
        self.db.commit()
        cursor.close()

