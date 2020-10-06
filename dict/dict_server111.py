import signal
import sys
from multiprocessing import *
from socket import *

from dict.mysql111 import *

HOST = '127.0.0.1'
PORT = 8882
ADDR = (HOST,PORT)
db = Datebase(database = 'user')

    
def do_register(c, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]

    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

def do_login(c, data) :
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]

    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

def do_query(c, data):
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]
    mean = db.query(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s : %s" % (word, mean)
        c.send(msg.encode())

def request(c):
    while True:
        db.create_cursor()

        data = c.recv(1024).decode()
        print(c.getpeername(), ":", data)
        if not data or data[0] == 'E':
            sys.exit()
        elif data[0] == 'R':
            do_register(c, data)  # c是用来传递数据的套接字
        elif data[0] == 'L':
            do_login(c, data)  # 通过data传来的name和pwd,判断是否登录成功
        elif data[0] == 'Q':
            do_query(c, data)

def main():
    s = socket()
    s.bind(ADDR)
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端链接
    print("Listen the port 8989")
    while True:
        #主线程只负责写链接的关闭和接受
        try:
            c,addr = s.accept()
            print("data form : ",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()  # db是自己创建出来的对象,调用类中我们自己写的close方法
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue

        p = Process(target=request, args=(c,))
        p.daemon = True  # 父进程退出,子进程也退出
        p.start()

main()