# opp : 객체지향(중심)적인 프로그래밍 가능. 상속, 포함, 다향성 등의 기법 구사 가능
# class : 멤 버변수(필드),멤버 메소드로 구성
# 인스턴스에 의해 새로운 이름공간을 갖는다.
import math

a = 2
print(a)

def func():
    print('ok')

class TestClass:    #클래스의 헤더              # 부모가 없으면 바로막는다 
    aa = 1  #멤버 변수(필드) 현재 클래스 내에서 전역

    def __init__(self): #특별한 메소드. method의 첫 인자는 반드시 self
        print('생성자: 객체 생성시 가장 먼저 1회만 호출 - 초기화 담당')

    def __del__(self): #특별 메소드
        print('소멸자:프로그램 종ㄹ시 자동실행. 마무리 작업')

    def showMessage(self): #일반 메소드 
        name = '한국인' #지역변수: showMessage 에서 유효
        print(name) 
        print(self.aa) #그냥 aa를 하면 showMessage에서 찾는 따라서 클래스 내에 맴버를 지정할떄는 self.aa라한다


print(TestClass) #<class '__main__.TestClass'>
print('클래스 멤버 :', TestClass.aa) #클래스 멤버 : 1
#클래스 생성자를 이용해 객체 생성후 해당 객체의 주소를 객체변수에 치환
test = TestClass()  #생성자 호출. instance를 하는것 ->object(객체)가 만들어진다
#1. Bound Method call
print('클래스 멤버 :', test.aa)
test.showMessage() #자동으로 객체변수 test가 메소드의 인수로담겨 호출이 된다

print()
print(type(1)) #<class 'int'>
print(type(1.0))
print(type('ok'))
print(type(test)) #<class '__main__.TestClass'>

print(id(test)) #2900699008704
print(id(TestClass)) #2900701159056
test2 = TestClass() #객체 생성 한개 더생성 
print(id(test)) #2900699008704
