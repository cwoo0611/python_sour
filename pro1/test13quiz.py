def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas


# 급여 처리
def processfunc(datas):
    # 현재 연도 자동으로 가져오기
    # current_year = datetime.now().year
    current_year = 2026

    # 직원별 급여 계산
    for data in datas:
        emp_no, name, base_pay, hire_year = data

        # 근무 연수 계산
        work_years = current_year - hire_year

        # 근속 수당 계산
        if work_years <= 3:
            bonus = 150000
        elif work_years <= 8:
            bonus = 450000
        else:
            bonus = 1000000

        # 총 급여
        salary = base_pay + bonus

        # 공제율 결정
        if salary >= 3000000:
            tax_rate = 0.5
        elif salary >= 2000000:
            tax_rate = 0.3
        else:
            tax_rate = 0.15

        # 공제액
        tax = int(salary * tax_rate)

        # 실수령액
        net_pay = salary - tax

        # 계산 결과 추가
        data.extend([
            work_years,
            bonus,
            tax,
            net_pay
        ])

    # 결과 출력
    print("사번  이름    기본급    근무년수  근속수당  공제액    수령액")
    print("-" * 70)

    for data in datas:
        print(
            f"{data[0]:<4} "
            f"{data[1]:<6} "
            f"{data[2]:<8} "
            f"{data[4]:<8} "
            f"{data[5]:<8} "
            f"{data[6]:<8} "
            f"{data[7]}"
        )

    print("-" * 70)
    print(f"처리 건수 : {len(datas)}건")


# 프로그램 실행
datas = inputfunc()
processfunc(datas)

# 문제 2 ---------------------------------
def inputfunc():
    datas = [
        "새우깡,15",
        "감자깡,20",
        "양파깡,10",
        "새우깡,30",
        "감자깡,25",
        "양파깡,40",
        "새우깡,40",
        "감자깡,10",
        "양파깡,35",
        "새우깡,50",
        "감자깡,60",
        "양파깡,20",
    ]
    return datas


def solution_func():
    # 상품별 단가
    price_by_name = {
        "새우깡": 450,
        "감자깡": 300,
        "양파깡": 450
    }

    # 주문 데이터
    arr_items = inputfunc()

    # 상품별 총 수량 : {key표현식: value표현식 for 변수 in 반복가능객체}
    count_by_name = {name: 0 for name in price_by_name}

    # 상품별 총 금액
    amount_by_name = {name: 0 for name in price_by_name}

    # 주문별 결과를 저장할 리스트
    order_table = []

    # 주문 데이터 처리
    for item in arr_items:
        # "새우깡,15" → "새우깡", "15"
        name, count = item.split(",")

        count = int(count)
        price = price_by_name[name]
        amount = count * price

        # 상품별 누적 수량
        count_by_name[name] += count

        # 상품별 누적 금액
        amount_by_name[name] += amount
        # 주문별 결과 저장
        order_table.append([name,count,price,amount])

    # 주문 내역 출력
    print("출력 형태:")
    print(f"{'상품명':<6} {'수량':>6} {'단가':>6} {'금액':>8}")
    print("-" * 35)

    for item in order_table:
        print(
            f"{item[0]:<6} "
            f"{item[1]:>6} "
            f"{item[2]:>6} "
            f"{item[3]:>8}"
        )

    # 상품별 소계
    print("\n소계")
    total_count = 0
    total_amount = 0

    for name in price_by_name:
        print(
            f"{name} : "
            f"{count_by_name[name]}개   "
            f"소계액 : {amount_by_name[name]}원"
        )

        total_count += count_by_name[name]
        total_amount += amount_by_name[name]

    # 전체 총계
    print("\n총계")
    print(f"총 수량 : {total_count}")
    print(f"총 액   : {total_amount}")

solution_func()


# 문제 3 ---------------------------------
products = { "노트북": 1500000, "모니터": 350000, "키보드": 80000, "마우스": 50000 } 

# 할인 함수 
discount10 = lambda price: int(price * 0.9) 
discount20 = lambda price: int(price * 0.8) 

def order(product, count, discount_func=None): 
    price = products[product] 
    total = price * count 
    if discount_func is not None: 
        total = discount_func(total) 

    return total 

print(order("노트북", 1)) 
print(order("키보드", 2, discount10)) 
print(order("모니터", 2, discount20))

orders = [ ("노트북", 1), ("키보드", 3), ("모니터", 2), ("마우스", 5) ]

result = sorted( orders, key=lambda x: products[x[0]] * x[1], reverse=True ) 
print(result)




# 연습문제 - 재귀 :  정수들이 저장된 리스트에서 재귀함수를 작성해 최대값을 구하는 코드를 작성하시오.
# for문으로
def find_max_for(v):
    max_value = v[0]

    for i in range(1, len(v)):
        if v[i] > max_value:
            max_value = v[i]

    return max_value

v = [7, 9, 15, 43, 32, 21]
print(find_max_for(v))

print('------------')
def find_max(v, n):
    if n == 1: 
        return v[0]   # 리스트의 첫 번째 값을 반환하고 재귀 종료

    # 재귀 호출
    prev_max = find_max(v, n - 1)  # 앞의 (n-1)개 원소 중 최대값을 구함. 이 호출이 끝나야 아래 코드로 내려옴

    # 마지막 값과 비교
    if v[n - 1] > prev_max:
        # 현재 단계에서 마지막 원소 v[n-1]과 이전 단계에서 구한 최대값(prev_max)을 비교
        return v[n - 1]  # 마지막 값이 더 크면 그 값을 최대값으로 반환
    else:
        return prev_max 

v = [7, 9, 15, 43, 32, 21] 
print(find_max(v, len(v)))

print('-- 좀 더 파이썬 스럽게 ---')
def find_max(v, n):
    if n == 1:
        return v[0]    

    return max(
        v[n - 1],               #  현재 단계의 마지막 원소
        find_max(v, n - 1)  #  앞의 (n-1)개 중 최대값을 재귀로 구함
    )   # 두 값 중 큰 값을 반환

print(find_max(v, len(v)))
