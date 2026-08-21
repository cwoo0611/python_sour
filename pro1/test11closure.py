#Clousre : Scope에 제약을 받지 않는 변수들을 포함하고 있는 코드블럭이다.
#내부 함수의 주소를 반환해 함수 밖에서 함수 내의 멤버를 참조하기

def funcTimes(a,b):
    c = a * b
    print('c:', c )
    return c
print(funcTimes(2,3))

# print(c) #NameError: name 'c' is not defined

kbs = funcTimes(2,3)   #실행결과를 kbs 대입
print(kbs)
kbs = funcTimes    #kbs에 주소를 넣는것 
print(kbs(2,3))    #따라서 실행할떄는 이렇게 

mbc = sbs = kbs
del funcTimes  #functimes 함수명 삭제 (참조 변수 삭제)
# aa = funcTimes(2,3) #NameError: name 'funcTimes' is not defined
print(kbs(3,4))
print(sbs(3,4))
print(mbc(3,4))

print('\n--- 클로저를 사용하지 않는 경우--------')
def out():
    count = 0
    def inn():
        nonlocal count 
        count += 1
        return count
    print(inn())
# print(count) #err global이 아니아서
out()
out()

print('\n--- 클로저를 사용한 경우--------')
def outer():
    count = 0
    def inner():
        nonlocal count 
        count += 1
        return count
    return inner #요것이 클로저: 내부 함수의 주소를 반환함 inner함수의 주소 리턴

var1 =outer()
print('var1 주소 :',var1) #var1 주소 : <function outer.<locals>.inner at 0x00000173DB373480>
print('count:',var1())
print('count:',var1())
print(var1.__closure__) #_명령_: 파이썬 고육 명령
myvar = var1()
print(myvar)
var2 = outer() #새로운 객체(inner 함수) 생성
print(var2())
print(var2())

print('\n수량 * 단가 * 세금한 결과를 출력하기 ---')
def outer2(tax):
    def inner2(su, dan):
        amount = su * dan * tax
        return amount
    return inner2

#1분기에는 금액:su * dan에 대한 tax는 0.1 부과
q1 = outer2(0.1)
result1 = q1(5,50000)
print('resi;t1:',result1) 
result2 = q1(2,40000)
print('resi;t1:',result2) 

#2분기에는 금액:su * dan에 대한 tax는 0.05 부과
q2 = outer2(0.05)
result3 = q2(5,50000)
print('resi;t1:',result1) 
result4 = q2(2,40000)
print('resi;t1:',result2) 

print('\n\n일급함수(객체): 함수안에 함수, 인자로 함수 전달, 반환 값이 함수')
def func1(a,b):
    return a + b
func2 = func1 #함수를 변수나 상수에 저장
print(func1(3,4))
print(func2(3,4))
print()
def func3(fu):# 인자로 함수 전달
    def func4(): #함수안에 함수 선언
        print('나는 내부함수야')
    func4()
    return fu # 반환 값이 함수

mbc = func3(func1) #인자로 함수 전달함
print(mbc(6,7))

print('\n축약함수(Lamda function):여러줄의 함수 정의를 한줄로 간단하게 줄여서 쓰는 함수')
#형식---lamda 매개변수,...:표현식   <==return 없이 결과 반환
def hapFunc(x,y): #프로그램 종료시 까지 메모리를 유지
    return x + y
print(hapFunc(1,2))
#위에꺼를 람다로
print((lambda x,y:x+y)(1,2)) #휘발성
gg = lambda x,y:x+y
print(gg(1,2))
gg2 = lambda x,y:x+y
print(id(gg),id(gg2))

print()
kbs = lambda a, su=10: a + su
print(kbs(5,6))
print(kbs(5))

sbs = lambda a, *tu, **di : print(a,tu,di)
sbs(1,2,3,var=4,var2=5)  #1 (2, 3) {'var': 4, 'var2': 5}

# filter() :반복 가능한 객체에서 특정 조건에 맞는 요소만 골라낸다
#기본 구조는 filter(함수,반복 가능한 객체)
print(list(filter(lambda a:a < 5, range(10)))) #[0, 1, 2, 3, 4]
print(list(filter(lambda a:a % 2, range(10)))) #[1, 3, 5, 7, 9]

#filter를 이용해 1~100 사이의 정수 중 5의 배수이거나 7의 배수만 출력(리스트)
print(list(filter(lambda x:x % 5 == 0 or x % 7 == 0, range(101) )))

#함수 장식자