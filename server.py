import socket
import time

s = socket.socket()
host = "127.0.0.1" #socket.gethostname()
port = 12345
s.bind((host,port))
s.listen(5)
while True:
    c, addr = s.accept()
    print("Connection accepted from " + repr(addr[1]))

    c.send("Server approved connection\n")
    c.send("Server approved connection\n")
    for line in open('payload.txt','r').readlines():
    	time.sleep(0.0125)
    	c.send(line)

c.close()
