class Car:
    handle = 1                 #속성 즉 맴버 두기
    speed = 0

    def __init__(self, name, speed):
        self.name = name    #현재 객체의 name에게 name(지역변수)인자값 치환
        self.speed = speed

    def showData(self):
        km = "킬로미터"
        msg = "속도:" + str(self.speed) + km       #그냥 speed 하면 showdata에서 찾음 
        return msg

    def printHandle(self):
        return self.handle

print(Car.handle) #원형(prototype) 클래스의 맴버호출 #1
print()
car1 = Car('tom',10) #생성자 호출을 통해 객체를 생성(인스턴스화)
print('car1 객체 주소:',car1)
print('car1 : ', car1.name, ' ', car1.speed,' ',car1.handle)
car1.color = '파랑'  #원래 car1 객체에 없는 color 맴버를 추가할수있다
print('carl.color: ', car1.color)
print('-------')
car2 = Car('oscar',20) #생성자
print('car2 객체 주소:',car2)
print('car2 : ', car2.name, ' ', car2.speed,' ',car2.handle)
print(id(Car),id(car1),id(car2))
#2575306402528 2575304249024 2575304166928
print(car1.__dict__) #{'name': 'tom', 'speed': 10, 'color': '파랑'}
print(car2.__dict__) #{'name': 'oscar', 'speed': 20}

print('-------------- 메소드-------------')
print('car1 speed:', car1.showData())        #속도:10킬로미터
print('car2 speed:', car2.showData())        #속도:20킬로미터

car1.speed = 60     
car2.speed = 110
print('car1 speed:', car1.showData())        #속도:60킬로미터
print('car2 speed:', car2.showData())        #속도:110킬로미터

print()
print('car1 handle : ', car1.printHandle()) #1 hande이 객체에 안담겨져있기 떄문에 원형타입으로 가서 값을 가지고옴
print('car2 handle : ', car2.printHandle()) #1 hande이 객체에 안담겨져있기 떄문에 원형타입으로 가서 값을 가지고옴
Car.handle = 2 #원형 클래스의 멤버 변수 값 수정
print('car1 handle : ', car1.printHandle()) #1 hande이 객체에 안담겨져있기 떄문에 원형타입으로 가서 값을 가지고옴
print('car2 handle : ', car2.printHandle()) #1 hande이 객체에 안담겨져있기 떄문에 원형타입으로 가서 값을 가지고옴
