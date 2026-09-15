# 네트워크:두대 이상의 컴퓨터나 장치를 서로 연결하여 데이터를 주고 받을수 있도록 구성한 통신환경
#있도록 구성한 통신환경
# 네트워크:네트워크를 만들고,연결하고,통신하게 하는 모든 활동
#        :PC와 서버연결,tcp/ip통신,소캣통신,인터넷연결

# socket:소캣(socket)은 프로세스가 네트워크 세계로 데이터를 보내거나
# 혹은 그 세계로부터데이터를 받기 위한 실제적인 청구 역할을 한다.
# 그러므로 프로세스가 데이터를 보내거나 받기 위해서는 반드시 소캣을 열어서
# 소캣에 데이터를 써보내거나 소켓으로부터 데이터를 읽어들어야 한다.
# 프로그램과 프로그램이 네트워크를 통해 데이터를 주고받기 위해 사용하는 
# 연결지점 + socket이란 tcp/ip의 프로그래머 인터페이스이다.
# socket이란 tcp ip의 프로그래퍼 인터페이스 이다.
# 통신 기기간 대화가 가능하도록 하는 통신방식으로 클라이언트/서버 모델에 기초한다

#tcp:연결을 맺고 신뢰성있게 데이터를 전달하는 연결지향 프로토콜
#   :클라이언트 프로그램(socket)->네트워크(socket)서버프로그램
# udp:연결 없이 빠르게 데이터를 전달하는 비연결지향 프로토콜

# socket 통신확인
import socket
#서비스 이름과 프로토콜 이름을 사용해 서비스 기본포트 확인
print(socket.getservbyname('http','tcp')) #80 www
print(socket.getservbyname('https','tcp')) #443
print(socket.getservbyname('ftp','tcp')) #21 파일전송
print(socket.getservbyname('ssh','tcp')) #22 원격 컴퓨터 접속
print(socket.getservbyname('smtp','tcp')) #25 메일 송수신
print(socket.getservbyname('pop3','tcp')) #110 이메일 
print()
# 특정 웹서버의 ip address확인
print(socket.getaddrinfo('www.daum.net',80,proto=socket.SOL_TCP)) 
#[(<AddressFamily.AF_INET: 2>, 0, 6, '', ('121.53.105.193', 80))]
#       주소체계,        소캣타입 프로토콜번호,실제접속주소

print(socket.getaddrinfo('www.naver.com',443,proto=socket.SOL_TCP)) 
#[(<AddressFamily.AF_INET: 2>, 0, 6, '', ('223.130.200.219', 443)), (<AddressFamily.AF_INET: 2>, 0, 6, '', ('223.130.192.248', 443)), (<AddressFamily.AF_INET: 2>, 0, 6, '', ('223.130.192.247', 443)), (<AddressFamily.AF_INET: 2>, 0, 6, '', ('223.130.200.236', 443))]

