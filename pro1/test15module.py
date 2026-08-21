#현재 모듈은 다른 package에 있는 모듈의 멤버를 사용해 
#실행을 통해 어떤 결과를 확인할 수 있는 실행파일!!
#실행 파일은 >python 파일명.py <==이 파일은 main module

print('사용자 정의 모듈 작성 후 호출 연습 ---')
imsi = 100 #뭔가를 하다가....

print('\n경로 지정 방법1:import 모듈명')
import pack1.mymod1
print(dir(pack1.mymod1)) #사용가능 모듈 목록이 보임
print(pack1.mymod1.__file__) #경로명 및 파일명
print(pack1.mymod1.__name__) #모듈명

list = [1,2]
list2 = [3,4,5]
pack1.mymod1.lstHap(1, 2,)

print('\n경로 지정방법2:form 모듈명 improt 모듈멤법,...')
from pack1.mymod1 import kbsFunc
kbsFunc()

from pack1.mymod1 import mbcFunc, tot
mbcFunc()
print('tot:',tot)

from pack1.mymod1 import* #메모리 낭비가 심하므로 비권장

from pack1.mymod1 import kbsFunc as 케이비에스별명
케이비에스별명() # 대한민국 대표 방송

print('\n경로 지정방법3:import 하위패키지.모듈명.멤버')
import pack1.pack1sub.sbs
pack1.pack1sub.sbs.sbsMansae()
import pack1.pack1sub.sbs as 난별명
난별명.sbsMansae()

print()
from pack1_other import mymod2
imsi = mymod2.Hap(3,4)
print(imsi)
from pack1_other.mymod2 import Cha as chachacha
print(chachacha(5,2)) 

print('\n경로 지정방법4:path 설정이 된 폴더에 모듈이저장된 경우')
# #path를 설정한후
# import mymod3
# #path 설정하기전
# import pack1_other.mymod3

import numpy
print(numpy.mean(([3,5,7])))