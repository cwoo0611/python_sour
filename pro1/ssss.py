def showGugu(start, end=5):   #기본값을 넣음 기본값 매개변수 end
    for dan in range(start, end + 1,1):
        print(str(dan) + '단 출력')
        for i in range(1,10):
            print(f'{dan} * {i} = {dan * i}', end = ' ')
        print()

showGugu(1,3)