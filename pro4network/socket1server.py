#1회용 서버
from socket import *

# socket 객체 생성
serversock = socket(AF_INET,SOCK_STREAM)   #형식 socket(소켓종류,소켓유형)
#socket을 이용해 특정 컴과 바인딩(서버의 ip와 port 연결)
# 포트 번호는 컴퓨터(IP 주소) 안에서 실행되는 특정 프로그램이나 서비스를 구분하기 위한 16비트 논리적 주소입니다
serversock.bind(('192.168.0.29',8888)) #cmd에서 ipconfig로 ip확인

#연결 대기상테로 전환. 리스너 설정(연결 정보수 최대 5개까지 허용)
serversock.listen(5)
print('서버 서비스 중...')

#클라이언트의 접속
conn, addr = serversock.accept() #수동적으로 연결을 받음
print('client addr: ' ,addr) 

#클라이언트가 보낸 데이터 수신
msg = conn.recv(1024).decode() # 1kb 단위로 수신된 데이터를 문자열로 변환
print('from client message:',msg)

# 연결종료
conn.close()
serversock.close()

