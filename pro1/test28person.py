class Person:    #용도 부모클래스로 사용  
    say = '난 사람이야~~~~' # 접근권환 : public
    nai = '20'
    __msg = 'good : private 멤버 - 현재 클래서에서만 유효'

    def __init__(self, nai):
        print('Person 생성자')
        self.nai = nai

    def printInfo(self):    # 접근권환 : public
        print(f'나이:{self.nai},이야기:{self.say}')

    def helloMethod(self):
        print('안녕')
        print('hello:', self.say, self.nai, self.__msg)   # 콤마 추가함

print(Person.say, Person.nai)  #원형 클래스로 멤버 호출(비권장)
# Person.printinfo() #TypeError
per = Person('25')  #객체 변수로 멤버 호출 (권장)
per.printInfo()
per.helloMethod()

print('---'*5)
class Employee(Person):
    subject = '근로자'
    say = '일하는 동물'     #hiding  
    def __init__(self):
        print('Employee 생성자')

    def printInfo(self):      #메소드 오버라이딩(부모의 메소드를 자식이 똑같은 명을 가지고있음)
        print('Employee 클래스의 printInfo()호출됨')

    def eprintInfo(self):
        print(self.subject, self.say, self.nai)
        # print(self.__msg) AttributeError: 'Employee' object has no attribute '_Employee__msg'
        self.helloMethod()
        self.printInfo()    #현재 클래스에서 먼저 검색 후 없으면 부모 메소드 호출 
        super().printInfo() #super()는 현재 클래스가 아니라 부모 메소드로 바로 호출하고 싶을떄사용한다
        print(self.say, super().say)
emp = Employee()
print(emp.subject, emp.nai, emp.say)
emp.printInfo()
emp.eprintInfo()


print('---' * 5)
class Worker(Person):
    # def __init__(self, nai):
    #     pass
    def __init__(self, nai):
        print('Worker 생성자')
        super().__init__(nai) #부모 클래스의 생성자 호출
    def wPrintInfo(self):
        print('Worker - wPrintInfo()처리')
        self.printInfo
        super().printInfo()

wor = Worker('30')
print(wor.say,wor.nai)
wor.wPrintInfo()

print('==='* 5)
class Programmer(Worker):
    def __init__(self, nai):
        print('Programmer 생성자')
        super().__init__(nai) #Bound method call
        Worker.__init__(self, nai)  #unBound method call

    def pPrintInfo(self):
        print('Programmer - pPrintInfo()처리함')

    def wPrintInfo(self):
        print('Programmer 클래스에서 오버라이딩')

pro = Programmer(35)
print(pro.say, pro.nai)
pro.pPrintInfo()
pro.wPrintInfo()

print('\n 클래스 타입 확인------------')
a= 3; print(type(a)) #<class 'int'> ㅡMaker가 만든 기본타입
print(type(pro)) #<class '__main__.Programmer'>
print(type(wor)) #<class '__main__.Worker'>

print(Person.__bases__) #(<class 'object'>
print(Employee.__bases__) #(<class '__main__.Person'>,)
print(Worker.__bases__) #(<class '__main__.Person'>,)
print(Programmer.__bases__) #(<class '__main__.Worker'>)



