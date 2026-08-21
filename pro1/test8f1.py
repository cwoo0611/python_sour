# function : 여러 개의 수행문을 하나의 이름으로 묶은 실행 단위
# 함수 고유의 공간을 갖는다.
# 자원의 재활용이 가능한다
# ...

# 내장함수 : 일부 체험
print(sum([1,2,3]))
print(8,bin(8)) #bin() 2진수로 출력 0b1000
print(eval('4+5'))
print(round(1.2))
import math
print(math.ceil(1.2),'',math.ceil(1.6))
print(math.floor(1.2),'',math.floor(1.6))

b_list = [True, 1, False]
print(all(b_list)) #False
print(any(b_list)) #True

data = [10,20,30]
data2 = ['a','b']
for i in zip(data,data2): #(10, 'a')(20, 'b') zip()은 두데이터를 쌍으로 묶어줌
    print(i)

import builtins #자동 로딩
builtins.print("자동 로딩")
builtins.print(builtins.sum([2.5]))



