# 정규 표현식 : ... 
import re #정규표현식 모듈 로딩

ss = "1234 abc가나다abcABC_1234555실습중78입니다_6'Python is fun"
print(ss)
# re.findall(패턴, 대상문자열)
print(re.findall('123',ss)) 
#['123', '123']
print(re.findall(r'[0-9]',ss))
print(re.findall(r'[0 1 3]',ss)) #0,1,3 값중한개씩
print(re.findall(r'[0-9]+',ss)) #1회이상 반복되는것만
print(re.findall(r'[0-9]{2}',ss))
print(re.findall(r'[0-9]{2,3}',ss))

print(re.findall(r'\d',ss)) #모든 숫자
print(re.findall(r'\d+',ss))
print(re.findall(r'\D+',ss)) #\d 반대




print(re.findall(r'\s',ss)) #공백, 탭문자만 가지고옴
print(re.findall(r'\s+',ss))
print(re.findall(r'\S+',ss)) #반대
