from socket import *
import sys
from threading import Thread
import json,re
from config import *

# httpserver功能
class HTTPServer:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.create_socket() #和浏览器交互
        self.connect_socket()#链接webframe
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,
                               SO_REUSEADDR,
                               DEBUG)
        #这句是在测试的时候，防止端口重用等待，实际部署中不用这个，DEBUG等于0或1表示能不能用

    #创建和webframe交互的套接字
    def connect_socket(self):
        self.connect_sockfd = socket()
        frame_addr = (frame_ip,frame_port)
        try:
            #链接web后端应用
            self.connect_sockfd.connect(frame_addr)
        except Exception as e:
            print(e)
            sys.exit()

    # 绑定地址
    def bind(self):
        self.address = (self.host,self.port)
        self.sockfd.bind(self.address)

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(5)
        print("Start the http server:%d"%self.port)
        while True:
            #不能加self.connfd．因为connfd是全局的，一直存在，而要是写成self.的形式
            #就会创建一个线程产生一个connfd，假如上一个进程正在运行，此时终止了connfd，就崩了
            connfd,addr = self.sockfd.accept()
            client = Thread(target=self.handle,
                            args=(connfd,))
            client.setDaemon(True)
            client.start()
            
    #具体处理客户端请求任务
    def handle(self,connfd):
        #request是获取的http请求
        request = connfd.recv(4096).decode()
        #[A-Z]+ 是请求类型　　\s+　是空格　\S*　是除了空格的全部元素(暴力拆解)
        #再组成子组
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            #re.match匹配 字符串的开始位置
            #groupdict()返回捕获组的组名及内容的字典
            env = re.match(pattern,request).groupdict()
        except:
            #客户端断开
            connfd.close()
            return
        #没有被捕获异常的情况下，新建一个套接字和webFrame进行交互
        else:
            #将字典转成为json
            data = json.dumps(env)
            #将解析后的请求发送给webframe
            self.connect_sockfd.send(data.encode())
            #接收来自webframe的数据
            data = self.connect_sockfd.recv(4096*100).decode()
            self.response(connfd,json.loads(data))

    #给浏览器发送数据
    def response(self,connfd,data):
        #data此时是字典
        if data['status'] == '200':
            #响应行
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            #响应头
            responseHeaders += 'Content-Type:text/html\r\n'
            responseHeaders += '\r\n'
            #响应体
            responseBody = data['data']
        elif data['status'] == '404':
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += 'Content-Type:text/html\r\n'
            responseHeaders += '\r\n'
            responseBody = data['data']
        elif data['status'] == '302':
            pass

        # 将数据发送给浏览器
        data = responseHeaders + responseBody
        connfd.send(data.encode())

if __name__ == '__main__':
    httpd = HTTPServer()
    httpd.serve_forever() # 启动服务