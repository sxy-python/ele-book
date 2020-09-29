"""
数据库操作模块
思路：
将数据库操作封装成一个类，将dict_server需要的数据库操作写成方法,在dict_server中
实例化对象,需要什么方法直接调用
"""
import pymysql
import hashlib

SALT = "#&Aid_" #盐

class Database:
    #这些参数不传入的话,用默认值
    def __init__(self,host='localhost',port=3306,user='root',
                 passwd='123456',charset='utf8',database=None
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.database = database
        self.connect_database()#链接数据库(创建对象过程中自动进行数据库链接)

    def connect_database(self):
        #链接数据库
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset
                                  )
    #关闭数据库
    def close(self):
        self.db.close()

    #创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    #注册操作
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

    #登录操作
    def login(self,name,passwd):
        hash = hashlib.md5((name + SALT).encode())  # 名字加盐
        hash.update(passwd.encode())
        passwd = hash.hexdigest()  # 加密后的密码

        sql = "select * from user where name = '%s' and passwd = '%s'" % (name,passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    def query(self,word):
        sql = "select mean from words where word = '%s' " % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        #如果找到,r是一个元祖，里面装mean
        if r:
            return r[0]#r[0]是解释
        #后面不写了,没找到就是自然结束,自然结束就是返回null

    def insert_history(self,name,word):
        sql = "insert into hist (name,word) VALUES (%s,%s)"
        try:#插入得try一下
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception:
            self.db.rollback()

if __name__ == '__main__':
    db = Database(database='dict')
    db.create_cursor()
    if db.register('sxy96','0501'):
        print("插入成功")
    else:
        print("失败")