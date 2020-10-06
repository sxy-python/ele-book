import pymysql
import hashlib
SALT = "#&Aid_"

class Datebase:
    def __init__(self,host='localhost',port=3306,user='root',
                 passwd='123456',charset='utf8',database=None
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.database = database
        self.connect_database()


    def connect_database(self):
        self.db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             database='dict',
                             charset='utf8')
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.db.close()

    def register(self,name,passwd):
        sql = "select * from user where name = '%s'" % name#这种传值得加'',通过execute传值不用加(系统加了)
        self.cur.execute(sql)
        r = self.cur.fetchone()#fetchone查找到返回一个元祖，查找失败返回null
        if r:
            return False #用户存在

        hash = hashlib.md5((name+SALT).encode())#名字加盐
        hash.update(passwd.encode())
        passwd = hash.hexdigest()#加密后的密码

        #执行到这说明不存在
        sql = "insert into user (name,passwd) VALUES (%s,%s)"

        try:  # 插入是写操作,加上try
            self.cur.execute(sql,[name,passwd])#只有写的时候的execute才会又[]参数
            self.db.commit()#提交,不提交不生效
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        hash = hashlib.md5((name + SALT).encode())  # 名字加盐
        hash.update(passwd.encode())
        passwd = hash.hexdigest()  # 加密后的密码

        sql = "select * from user where name = '%s' and passwd = '%s'"\
              % (name,passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()


        if r:
            return True #用户存在

    def query(self,word):
        sql = "select mean from words where word = '%s' " % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 如果找到,r是一个元祖，里面装mean
        if r:
            return r[0]  # r[0]是解释

