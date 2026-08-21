# # 조건 판단문 if
# var = 2
# if var >=3:
#     print("크네")
#     print("흠 크군")

# if var >= 3:
#     print("크구나")
# else:
#     print("작구나")

# print()
# money = 200
# age = 35

# if money >= 500:
#     item = "사과"
#     if age <= 20:
#         msg = "참 참"
#     else:
#         msg = "참 거짓"
# else:
#     item = "복숭아"
#     if age <= 20:
#         msg = "거잣 참"
#     else:
#         msg = "거짓 거짓"
# print(f"중복 if 수행 후 결과 {item} {msg}")

# print()

# jumsu= int(input('점수입력:'))

# if jumsu >= 90:
#     print("우수")
# elif jumsu>= 80:
#     print("보통")
# else:
#     print("저조")

# print('---------')
# names=['홍길동','김찬우']
# if (count := len(names) >= 3): 
#     print(f"인원수가 {count}명 이므로 단체 할인 적용")
# else:
#     print("ㅠㅠ")

# print("끝")

# scores = [95,88,76,92,81]
# if(avg:= sum(scores)/len(scores))>=80:
#     print(f"우수반 평균 점수: {avg}")

# print('삼항 연산')
# a = 'kbs'
# b = 9 if a == 'kbs' else 11
# print('b:',b)

a=11
b = 'mbc' if a == 9 else 'kbs'
print('b:',b)
a = 3

a = 6
print(0 if a < 5 else 1 if a < 10 else 2) 
#조건이 참이면 0 조건이 거짓이면   다음 조건문 다음조건문에 참이면 1 거짓이면  2
