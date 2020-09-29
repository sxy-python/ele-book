import getpass #隐藏输入
import hashlib #转换加密

#输入隐藏,只能通过终端输入
pwd = getpass.getpass("PW:")#用法和input完全一样,只不过输入不会显示内容
print(pwd)

#算法加盐
hash = hashlib.md5('*#06l'.encode())#返回一个hash对象
hash.update(pwd.encode())#加密处理
pwd = hash.hexdigest()#通过接口函数可以获得加密后的密码
print(pwd)