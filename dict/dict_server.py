"""
dict 服务端

功能:业务逻辑处理
模型：多进程　tcp 并发
"""
import signal  # 处理僵尸进程
import sys
from multiprocessing import *
from socket import *

from dict.mysql import Database


#服务端注册处理
def do_register(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    # 返回true表示注册成功,false表示注册失败
    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

#服务端登录
def do_login(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

#查询单词
def do_query(c,data):
    tmp= data.split(' ')
    name = tmp[1]
    word = tmp[2]

    #插入历史记录
    db.insert_history(name,word)

    #如果没查到，返回none，找到返回单词解释
    mean = db.query(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s : %s" % (word,mean)
        c.send(msg.encode())

#接受客户端请求,分配处理函数
def request(c):#循环接受链接请求
    #在每一个子进程中创建游标
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),":",data)
        if not data or data[0] == 'E':#客户端ctrl+c 异常退出，这边收到的是null
            sys.exit()#对应的子进程退出(每个客户端都对应一个子进程)
        elif data[0] == 'R':
            do_register(c,data)#服务器存客户端传来的数据,即传来的c
        elif data[0] == 'L':
            do_login(c,data)#通过data传来的name和pwd,判断是否登录成功
        elif data[0] == 'Q':
            do_query(c,data)

#全局变量
HOST = '0.0.0.0'
PORT = 8880
ADDR = (HOST,PORT)
#建立数据库对象,全局＝父进程＝所有子进程共享
db = Database(database = 'dict')

#搭建网络
def main():
    s = socket()
    #创建tcp套接字
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    #循环等待客户端链接
    print("Listen the port 8000")
    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:#按ctrl c退出
            s.close()
            db.close()#db是自己创建出来的对象,调用类中我们自己写的close方法
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue

        #创建子进程
        p = Process(target=request,args=(c,))
        p.daemon = True #父进程退出,子进程也退出
        p.start()



if __name__ == '__main__':
    main()

