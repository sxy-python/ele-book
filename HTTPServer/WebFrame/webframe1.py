from socket import *
import json

socked = socket()
socked.bind(('0.0.0.0',8080))
socked.listen(3)

while True:
    c,addr = socked.accept()
    data = c.recv(1024).decode()
    print(json.loads(data))
    d = {"status":'200','data':'xxxxxx'}
    c.send(json.dumps(d).encode())