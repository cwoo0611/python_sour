# aa = {1,2,3,4,5,5,5,5,5}
# for i in aa:
#     #pass
#     print(i, end = ' ')

# print('분산/표준편차')
# numbers = [1,3,5,7,9] #합은 25, 평균은 5.0
# # numbers = [3,4,5,6,7] #합은 25, 평균은 5.0
numbers = [-3,4,5,7,12] #합은 25, 평균은 5.0
tot = 0
for a in numbers:
    tot += a

print(f"합은 {tot}, 평균은 {tot / len(numbers)}")

avg = tot / len(numbers)

#편차 제곱의 합 
hap = 0
for i in numbers:
    hap += (i - avg)**2
print(f"편차 제곱의 합: {hap}")
vari =  hap / len(numbers)
print(f"분산은 {vari}")
print(f"표준편차는 {vari**0.5}")

print()
colors = ['빨강','초록','파랑']
for v in colors:
    print(v, end = ' ')
print()

print('iter() : 반복 가능한 객체를 하나씩 꺼낼 수 있는 상태로 만들어 주는 함수')
iterator = iter(colors) 
for v in iterator:
     print(v, end = ' ')

print()
for idx, d in enumerate(colors,start=1):   #1부터 시작
    print(idx, ' ', d)

print('\n 사전형 ---')
datas = {'python' : '만능언어', 'java':'웹용언어', 'mariadb':'RDBMS'}
print(datas.items()) #([('python', '만능언어'), ('java', '웹용언어'), ('mariadb', 'RDBMS')]) 리스트 안에 튜플ㄹ 되어있음
for i in datas.items():
    print(i[0]) #키만나온다

for k, v in datas.items(): #키랑 값을 묶어주는 함수이다
    print(k, '--', v)

    
for k in datas.keys(): #키만 찍는다
    print(k, end = ' ')
print()

for v in datas.values():  #값만 찍는다
    print(v, end = ' ')

print('\n 다중  for ------------') #다중 for 문
for n in [2,3]:
    print(f'{n}단 ~~~ ')
    for su in [1,2,3,4,5,6,7,8,9]:
        print(f'{n} * {su} = {n*su}')

print('\nfor:continue, break ------------')

print('\n\n정규표현식 + for 연습 ---')
message = """
펠리시아!!!!!!노와 콴자 존스 부부의 샌디에이고 인수를 승인했다.펠리시아!!!!!!노와 콴자 존스 부부의 샌디에이고 인수를 승인했다.펠리시아!!!!!!노와 콴자 존스 부부의 샌디에이고 인수를 승인했다.
펠리시아!!!!!!노와 콴자 존스 부부의 샌디에이고 인수를 승인했다.
"""
import re #정규표현식 라이브러리를 주기억장치에 안착
message2 = re.sub(r'[^가-힣\s]','',message)  #패턴과 일치하는 문자열을 다른 문자열로 치환
print(message2)
message3 = message2.split(' ') #공백을 기준으로 문자열 분리
print(message3, ' ', len(message3))

# 단어별 빈도수 출력: dict 사용 
cou = {}
for i in message3:
    if i in cou:
        cou[i] += 1 #같은 단어가 있으면 누적
    else:
        cou[i]=1 # 최초 단어일 경우 '단어':1

print('\ncomprehension:반복문 + 조건문 + 값 생성을 한줄로 표현')
a = [1,2,3,4,5,6,7,8,9,10]
li = []
for i in a:
    if i % 2 == 0:
        li.append(i)
print(li)

print(list(i for i in a if i % 2 == 0))  #조건이 참이면 맨왼쪽 i로감ㄴ

print()
id_name = {1:'tom', 2:'james'}
name_id = {val:key for key, val in id_name.items()}
print(name_id) #{'tom': 1, 'james': 2}

print()
aa = [(1,2),(3,4),(5,6)]
for a,b in aa:
    print(a + b)

print([a+b for a, b in aa]) #[3, 7, 11]

print(*[1,2,3])


print("\n수열 생성: range(start, stop. step)") #range 기본형식
print(list(range(1, 6))) #[1, 2, 3, 4, 5]
print(list(range(1, 6, 1))) #[1, 2, 3, 4, 5]
print(list(range(1, 6, 2))) #[1, 3, 5]
print(tuple(range(1, 6, 2))) #(1, 3, 5)
print(tuple(range(0, 6, 1))) #(0, 1, 2, 3, 4, 5)
print(tuple(range(6))) #(0, 1, 2, 3, 4, 5)
print(list(range(-10,-100,-20))) #[-10, -30, -50, -70, -90]
print()
for i in range(6):
    print(i,end = ",")

for _ in range(6):
    print('반복')

print('1~10까지 정수 합')
tot = 0
for i in range(1,11):
    tot += i 
print('tot :',tot)

for i in range(1,10):
    print(f'2 * {i} = {2 * i}')

print('2~9 구구단 출력(단은 행단위 출력)')
for i in range(2,10):
    for j in range(1,10):
         print(f'{i}*{j} = {j * i}', end=' ')
    print()

print('주사위를 두 번 던져 낭ㄴ 숫자들의 합이 4의 배수가 되는 경우만 출력')
for i in range(6):
    n1 = i + 1
    for j in range(6):
        n2 = j + 1
        n = n1 + n2
        if n%4 == 0 :
            print(n1,n2)
print()
for i in range(1,7,1):
    for j in range(1,7):
        hap = i + j 
        if hap%4 == 0 :
            print(i,j)






