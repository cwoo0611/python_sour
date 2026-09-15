# client
from socket import *

clientsock = socket(AF_INET,SOCK_STREAM)
clientsock.connect(('192.168.0.29',8888))#connect하는순간 
clientsock.send("안녕서버".encode())

clientsock.close()

# server 실행중 -client 실행 - sever가 메시지 수신 후 종료