#2번 문제



class ElecProduct:  #부모 클래스
    voulume = 0
    def volumeControl(self, volume):
        print(f"{volume}을 조절한다")


class ElecTv(ElecProduct): #자식클래스
    def volumeControl(self, volume): #오버라이딩
        print('나는 TV')
        print(f"{volume}을 리모컨으로 조절한다")

class ElecRadio(ElecProduct): #자식클래스
    def volumeControl(self, volume): #오버라이딩
        print('나는 radio')
        print(f"{volume}을 주파수로 조절한다")

if __name__ == "__main__":
    electro_product = ElecProduct()
    electro_product.volumeControl(1)
    tv = ElecTv()
    tv.volumeControl(3)
    radio = ElecRadio()
    radio.volumeControl(5)


        
