class Animal:
    def move(self, moving):
        print(f"동물은 {moving}움직입니다")

class Dog(Animal):
    name = '개'
    cry = '월월'
    def move(self, moving):
        print(f"{self.name}는 {self.cry}거리면서 {moving}움직입니다")

class Cat(Animal):
    name = "고양이"
    cry = '카악'
    def move(self, moving):
        print(f"{self.name}는 {self.cry}거리면서 {moving}움직입니다")

class Wolf(Dog,Cat):
    name = "늑대"
    def move(self, moving):
        print(f"{self.name}는 {self.cry}거리면서 {moving}움직입니다")

class Fox(Cat,Dog):
    name = "여우"
    def move(self, moving):
        print(f"{self.name}는 {self.cry}거리면서 {moving}움직입니다")
    def foxMethod(self):
        print(f"{self.name}의 행동은 {super().name}의 행동과 유사하다")


if __name__ == "__main__":
    moving=input("동물의 발자국 수룰 입력하세요:ex)3발자국  ")
    yeo = Fox()
    yeo.move(moving)
    yeo.foxMethod()
    Woo = Wolf()
    Woo.move(moving)
