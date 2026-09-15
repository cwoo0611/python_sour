from socket import *

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect(('192.168.0.29', 7788))
clientsock.send("안녕 반가워".encode())
print('수신자료:', clientsock.recv(1024).decode())
clientsock.close()

