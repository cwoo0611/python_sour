#매개변수 유형
#위치 매개변수 : 인수와 순서대로 대응
#기본값 매개변수 : 매개변수에 입력값이 없으면 기본값
#키워드 매개변수 : 실인수와 가인수 간 동일 이름으로 대응
#가변 매개변수 : 인수의 객수가 동적인 경우


def showGugu(start, end=5):   #기본값을 넣음 기본값 매개변수 end
    for dan in range(start, end + 1,1):
        print(str(dan) + '단 출력')
        for i in range(1,10):
            print(f'{dan} * {i} = {dan * i}', end = ' ')
        print()

showGugu(2,3) #2가 start 가지고 end는 3을 가지고 호출하는게 우선순위가 있어서 3부터호출
showGugu(2) #뒤에 3과 이루어 지는게 없어서 기본매게변수인 5작용
showGugu(end=9,start=7) #showGugu(end=9,start=7) 는 순서가 아닌 이름에 대한 맵핑 (키워드 매개변수)
print()
showGugu(7,end=9)
# showGugu(start=7,9) #SyntaxError: positional argument follows keyword argument
# showGugu(end=9,7) #SyntaxError: positional argument follows keyword argumen

print('-------가변매게변수-----')
def func1(*ar): #* : 여러개의 인자를 tuple로 묶어서 받겠다는 의미 
    print(ar)
    for i in ar:
        print('밥 :' + i)

func1('김밥','비빔밥')
func1('김밥','비빔밥','공기밥','주먹밥')

print()
def func2(a, *ar):
# def func2(*ar.a): #SyntaxError: invalid syntax
    print(a)
    print(ar)
func2('김밥') 
func2('김밥','비빔밥','공기밥','주먹밥')

print()
def func3(w,h,**other):
    print(f'몸무게:{w},키:{h}')
    print(f'기타 : {other}')
func3(80, 180, irum = '신기해', nai = 33)
# func3(80, 180, {'irum' = '신기해', 'nai' = 33}) 타입에러

print()
def func4(a,b,*c,**d):
    print(a,b)
    print(c)
    print(d)
func4(1,2)
func4(1,2,3,4,5)
func4(1,2,3,4,5,kbs = 9, mbc = 11)

print()
#type hint : 함수의 인자와 반환 값에 type을 적어 가독성 향상
#type에 대한 강제성은 없다.
def typeFunc(num:int,data:list[str]): 
    print(num)
    print(data)
    result = {}
    for idx, item in enumerate(data,start=1):
        print(f'idx:{idx}, iten:{item}')
        result[item] = idx

    return result

rdata = typeFunc(1, ['일','이','삼']) #num에는 1 dat에는 리스트가들어간다
print(rdata)
print()
rdata = typeFunc('한개', [10,20,30]) 
print(rdata)


def zoo(a,b=1):
    print(a,b)
zoo(b=5,a=1)














