
    
    
class CoinIn:
    def culc(self, coin, count):
        self.coin = coin
        self.count = count
        self.cupcount = 0
        self.change = 0

        if self.coin >= 200:
            if self.coin % 200 == 0:
                self.change = self.coin - (self.count*200) 
                return (self.count, self.change)
            elif self.coin % 200 != 0:
                self.change = self.coin - (self.count*200) 
                return (self.count, self.change)
        elif self.coin == 200:
            self.change = self.coin - (self.count*200) 
            return (self.count, self.change)      
        elif self.coin < 200:
            print("요금이 부족합니다.")

class Machine:
    def showdata(self):
        self.show = CoinIn()
        coin = int(input('돈을 넣어주세요'))
        count = int(input('잔갯수를 입력하세요'))
        
        successful = self.show.culc(coin,count)
        print(successful)

KIM = Machine()
KIM.showdata()


    
    




    

        
