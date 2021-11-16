import MySQLdb
import datetime
import base64

db = MySQLdb.connect("localhost", "test", "123456", "team5", charset='utf8')
cursor = db.cursor()
fp = open("images/xiangyu.png", 'rb')
img = fp.read()
fp.close()
print('==============================================================')
dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# sql = "INSERT INTO face_info(FaceImg,Name, IdNum, CreateTime, lastModTime, IsValid) VALUES(%s, '向宇', 2019141460246, '" + dt + "', '" + dt+ "', 1)"


# cursor.execute("INSERT INTO face_info VALUES(%s,%s,%s,%s,%s,%s,%s)", (MySQLdb.Binary(img), 'test',23,None,None,1,124))
cursor.execute("SELECT FaceImg FROM face_info where Id = 124")
d = cursor.fetchone()[0]
cursor.close()


f = open("test.png", "wb")
f.write(d)
f.close()

db.commit()
db.close()


