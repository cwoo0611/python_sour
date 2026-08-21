# 반복문 while 조건:    조건이 참인 동안 블럭 수행
a = 10
while a <=5:
    print(a, end = '')
    a+=1
else: # 선택적 : 조건에 따른 종료시 수행
    print('수행 성공')

print('끝')

print('1 - 100 사이의 정수 중 3의 배수의 합은?')
su = 1
hap=0
while su <=100:
    # print(su, end = '')
    if su % 3 == 0:
        # print(su, end = '')
        hap+=su
    su += 1
print('합은',hap)

print()
colors = ["r", 'g', 'b']

num = 0
while num < len(colors):
    print(colors[num])
    num += 1

print('if 블럭 내에 while 블럭 사용')
import time 
# print('a')
# time.sleep(2)
# print('b')

# sw = input('폭탄 스위치를 누를까요 ?[y/n]')

# if sw == 'Y' or sw == 'y':
#     count = 5
#     while 1 <= count:
#         print('%d초 남았어요'%count)
#         time.sleep(1)
#         count -= 1
#     print('폭발')

# elif sw == 'N' or sw == 'n':
#     print('작업 취소')
# else:
#     print('y 또는 n을 누르시오')
print('\ncontinue / break')
a = 0
while a <=10:
    a += 1
    if a == 7:
        break    #반복문 무조건 탈출
    if a == 5:
        continue
    print(a)

print('\n키보드로 정수를 입력 받아 홀수 짝수 출력(무한 반복)')
while True:
    mysu = int(input('확인할 정수 입력(예:5)'))
    if mysu == 0:
        print('프로그램 종료')
        break
    elif mysu % 2 == 0 :
        print(f'{mysu}는 짝수입니다')
        continue
    elif mysu % 2 == 1 :
        print(f'{mysu}는 홀수입니다')



print('끝')
