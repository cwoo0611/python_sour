#함수 장식자 기존 함수를 건드리지 않고 겉에 기능을 덧씌워주는 문법이에요. "함수를 꾸며준다"는 이름 그대로예요.
# 특정기능 추가, 코드중복줄이기, 가독성 향상 

#기본작동 원리:장식자는 함수를 인자로 받아 내부에서 새로운 함수를 써서(wrapper) 반환.

def make2(fn):
    return lambda:'안녕' + fn()
def make1(fn):
    return lambda:'반가워' + fn()

def helloFunc():
    return '홍길동'

hi = make2(make1(helloFunc)) #decorator 없이 실행 (장식자)x
print(hi()) #안녕반가워홍길동


@make2
@make1
def helloFunc2():
    return '고길동'
print(helloFunc2()) #장식자 활용


