#배열 연산
#기본 수학함수는 배열에 요소별로 적용되고
#  +,-,*,/ 나 또는 add, subtract, multiply, 함수를 사용
# 벡터화 연산을 하므로 for문을 사용하지 않고 바로 배열에 대한 연산 

import numpy as np

# x = np.array([[1,2],[3,4]], dtype=np.float32)
x = np.array([[.1,2],[3,4]])

print(x, ' ', x.dtype) # [[1,2],[3,4]] float32

# y=np.arange(5,9)
y=np.arange(5,9).reshape(2,2) #2행2열로 변환 1처원을 2차원으로 바꿔준다
y = y.astype(np.float32) #타입변경
print(y,' ',y.dtype)

print(x.ndim,' ',y.ndim) #2 2

print()

print(x+y) #파이썬 연산자 사용
print(np.add(x,y)) #넘파이 함수(유니버설 함수) - 위보다 연산속도가 빠름
print()
print(x-y)
print(np.subtract(x,y))
print()
print(x*y)
print(np.multiply(x,y))
print()
print(x/y)
print(np.divide(x,y))
print()
print(np.sqrt(x), ' ', np.exp(x), ' ',np.log(x), ' ', np.cos(x))