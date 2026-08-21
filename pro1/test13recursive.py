#재귀함수 : 함수가 자기 자신을 호출 - 반복 처리 가능

def countDown(n):
    if n == 0:
        print('완료')
        return
    else:
        print(n, end = ' ')
        countDown(n-1) #재귀

countDown(5) #5 4 3 2 1 완료

print('\n---1부터 n까지의 정수의 합 구하기----')
def totFunc(n):
    if n == 0:
        print('완료')
        return 1

    return n + totFunc(n-1) #재귀함수
result = totFunc(5)
print(result)

#팩토리얼(factorial,계승)은 1부터 어떤자연수 n까지 모든수를 곱한것
#3곱하기 2곱하기 1
def factFunc(a):
    if a == 1:return 1
    print(a)
    return a * factFunc(a-1)

result2 = factFunc(5)
print(result2)
