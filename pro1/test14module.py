#Module:소스 코드의 재사용을 가능하게 하며,
#소스 코드를 하나의 이름 공간으로 구분하고 관리.
#하나의 파일은 하나의 모듈이 된다.
#모듈의 멤버로 모듈 함수 클래스 변수 실행문이 있다.
#표준 모듈 사용자 작성 모듈 제3자 모듈(third party)로 구분 할 수 있다.

print(print.__module__) #builtins (내장모듈)기본적으로 내장되어있는 모듈

print('뭔 작업을 하다가...외부 모듈 사용하기')
import sys #표준 라이브러리 모듈을 불러오는 명령
print(sys.path) #현재 모듈의 경로 확인 
q = 'n' 
if q == 'y':
    sys.exit()
#수학관련 모듈 읽기
import math
print(math.pi)
print(math.sin(math.radians(30)))
print('종료')
#달력 출력모듈
import calendar
print(calendar.JULY)
calendar.setfirstweekday(6)
calendar.prmonth(2026,8)   #2026 ,8월 달력을 가져온다
del calendar

# import time
# print('시작')
# time.sleep(3)
# print('계속')

#난수 출력
import random
print(random.random())
print(random.randrange(1,10))

from random import random
print(random())

from random import randint, randrange, choice #일부 맴버만 로딩
print(randrange(1,5))

from random import * #전체 맴버를 로딩 (비권장)

