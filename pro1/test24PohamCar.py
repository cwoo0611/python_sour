#여러 개의 부품 객체를 조립해 완성차 생성
#클래스의 포함 관계 사용(자원의 재활용)
#포홤 관계 : 다른 클래스(객체)를 마치 자신의 맴버 처럼 선언하고 사용

# import test24PohamHandle 
from test24PohamHandle import PohamHandle

class PohamCar:           
    turnSohwMessage = "정지"   #turnshow는 포함카의 고유맴버

    def __init__(self, ownerName):
        self.ownerName = ownerName
        self.handle = PohamHandle() #클래스의 포함관계

    def turnHandle(self, q):
        # 회전량(q):양수면 우회전,회전량(q):음수면, 좌회전,0이면 직진이라고 가정
        if q > 0:
            self.turnSohwMessage = self.handle.rightTurn(q)
        elif q < 0 :
            self.turnSohwMessage = self.handle.leftTurn(q)
        elif q ==0:
            self.turnSohwMessage = "직진"
            

if __name__ == "__main__":
    tom = PohamCar("미스터 톰")
    tom.turnHandle(10)
    print(tom.ownerName + "의 회전량은 " + tom.turnSohwMessage + " " + \
      str(tom.handle.quantity))

    print()
    suji = PohamCar("미스 수지")
    suji.turnHandle(-20)
    print(suji.ownerName + "의 회전량은 " + suji.turnSohwMessage + " " + \
      str(suji.handle.quantity))

    suji.turnHandle(0)
    print(suji.ownerName + "의 회전량은 " + suji.turnSohwMessage + "0")