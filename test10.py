cnt = 0
hap = 0
for i in range(101):
    if i % 3 == 0:
        print(i, end = ' ')
        hap +=i
        cnt += 1
    elif i % 4 == 0:
        if i % 7 != 0:
            print(i, end = ' ')
            hap +=i
            cnt += 1
print()
print(f'건수:{cnt}')
print(f'배수의 총합:{hap}')
    