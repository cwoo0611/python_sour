# 사용자 정의 함수
"""
def 함수면(가인수,,,): #dummy argument
    #...
    return 반환값 # 1개만 반환, return이 없으면 return None
함수명(실인수,,,) #함수 호출 #actual argument
"""
print( '뭔가를 실행')
#함수 선언
def doFunc1():
    print('doFunc1 수행')
    return None # 생략가능

def doFunc2(name):
    print('name : ', name)

def doFunc3(arg1, arg2):
    res = arg1 + arg2
    return res

def doFunc4(a1,a2):
    imsi = a1 + a2
    if imsi % 2 == 1:
        return      #함수 내에 return 은 함수의 무조건 탈출 
    else:
        return imsi


#함수 호출
doFunc1()
print('어떤 작업 처리')
doFunc1()
print('함수 주소는',doFunc1)
print('함수 주소는', id(doFunc1))
imsi = doFunc1 #함수의 주소를 치환
imsi()
imsi2 = doFunc1() # 함수 실행 결과를 기억
print(imsi2) # 실행 결과를 출력 
print(doFunc1())
print( '뭔가를 종료')
print('---------------')
# doFunc2() #TypeError: doFunc2() missing 1 required positional argument: 'name'
doFunc2(7) #name 이어도 숫자를 집어넣어도 된다 넣은값에 맞게 타입이 바뀜
doFunc2('홍길동')
print('--------------')
doFunc3("대한", "민국")
print(doFunc3("대한", "민국"))

print('---------------')
doFunc4(3,5) 
print(doFunc4(3,5)) #8



print('**'*30)
def triArea(a,b):
    c = a * b / 2
    triAreaPrint(c)    #함수 내에서 다른 함수를 호출

def triAreaPrint(arg):
    print('삼각형의 면적은', arg)

triArea(20,30)

print()
def passResult(kor, eng):
    ss = kor + eng
    if ss >= 50:
        return True
    else:
        return False

if passResult(20,50):
    print('합격')
else:
    print('불합격')
print()
def swapFunc(a,b):
    return b,a  #return(b,a) 반환값은 반드시 1개
a = 10; b = 20
print(a, ' ',b)
print(swapFunc(a,b))



print()
def funcTest():
    print('funcTest  멤버 처리')
    def funcInner():
        print('내부함수 funcInner 실행')

    funcInner()

funcTest()

print()
# if 조건식 안에 함수 적용
def isOdd(para):
    return para % 2 == 1 #홀수이면 True 반환

mydict = {x:x for x in range(11) if isOdd(x)}
print(mydict)


print('\n변수의 생존 범위(scope rule)')
# 변수가 저장되는 이름공간은 변수가 어디에서 선언 되었는가에 따라 생존 시간이 다른다.
#전역,지역변수
#Local > Enclosing function(내부) >Global(전역) > Built - in(내장)
player = '전국대표' #전역변수(현재 파일(모듈)어디서든 호출 가능)
name = '신기해'

def funcSoccer():
    name = '이기자' #지역 변수(현재 함수 내에서만 유효)
    city = '서울'
    print(f"이름은 {name} 수준은 {player}")
    print(f"지역은 {city}")

funcSoccer()
print('작업종료') 
# print(f"지역은 {city}") #NameError: name 'city' is not defined

print()
a = 10; b = 20; c = 30     #전역변수 
print(f"foo 수행 전 a:{a}, b:{b}, c:{c}")

def foo():
    a = 7 
    b = 100

    def bar():
        global c #bar의 맴버가 아니라 모듈의 맴버 됨(전역)
        nonlocal b
        b = 87
        print(f"bar 수행 중 a:{a}, b:{b}, c:{c}")
        c = 92 
        #b = 200 #bar 수준 지역 변수 
        b = 300 #nonlocal b를 쓰는 순간 foo 수준 지역 변수 
    bar()
    print(f"bar 수행 후 a:{a}, b:{b}, c:{c}")

foo()
print(f"foo 수행 후 a:{a}, b:{b}, c:{c}")

# foo 수행 전 a:10, b:20, c:30
# bar 수행 중 a:7, b:87, c:30
# bar 수행 후 a:7, b:300, c:92
# foo 수행 후 a:10, b:20, c:92

print()
g = 1
print('g:',g) #1
def func():
    global g
    a = g 
    g = 2
    return a
print (func())
print('g:',g) #2   





    
    













