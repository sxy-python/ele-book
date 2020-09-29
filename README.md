#电子词典
在线词典

1. 需求分析
   * 确定并发方案  (Process多进程)
   * 确定网络传输方法  tcp网络
   * 确定具体细节(注册都有那些信息,显示所有历史记录还是最近10个)
     用户名密码, 显示最近10条历史记录

   * 二级界面,界面间的跳转怎么完成

2. 数据库设计 : 存什么  几个表  表字段和类型
   dict

   建立数据表
   words --> id  word  mean  单词表
   user --> id  name  passwd  用户

   create table user (id int primary key auto_increment,name varchar(32) not null,passwd char(128) not null);

   hist --> id  name word  time  历史记录

   create table hist (id int primary key auto_increment,name varchar(32) not null,word varchar(28),time datetime default now());


3. 模块设计: 几个模块,每个模块做什么,封装方法

   * 客户端
   * 服务端
   * 数据库操作

4. 搭建并发网络,完成通信测试


5. 分析具体功能,进行实现
   注册
   登录
   查单词
   历史记录

cookie:

   import getpass

   getpass.getpass()
   功能:　隐藏输入内容
   参数:  提示行

进行密码加密

In [3]: import hashlib

In [4]: passwd = 'abc123'

生成加密对象
hash = hashlib.md5()

hash = hashlib.md5(b"#-the,L")　＃ 加盐处理


进行密码加密
In [6]: hash.update(passwd.encode())

获取加密后的内容
In [7]: hash.hexdigest()