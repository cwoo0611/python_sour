# cgi-bin/sangpum.py : 웹용 파이썬 - Maria DB에 
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 한글 깨짐 방지

import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv() #env 파일은 sangpum.py와 같은 폴더 위치에 있어야 함
config= {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT')),
    'charset': os.getenv('DB_CHARSET')
}

# print("Contet-Type:text/html; charset=utf-8") # 얘는 꼭 라인스킵하고 띄어쓰기 조심
# print() #무조건 라인스킵
# print("<html>")
# print("<body>")
# print("<h2>*상품정보*</h2>")
# print("<table border='1'>")
# print("<tr><td>코드</td><td>품명</td><td>수량</td><td>단가</td></tr>")

# print("</table>")
# print("</body>")
# print("</html>")

print("""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>상품정보</title>
</head>
<body>
    <h2>*상품정보*</h2>
""")
conn = None
try:
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        select code,sang,su,dan from sangdata
    """)

    datas = cursor.fetchall()
    print("<table border='1'>")
    print("<tr><td>코드</td><td>품명</td><td>수량</td><td>단가</td></tr>")
    for data in datas:
        print("<tr>")
        print(f"<td>{data[0]}</td>")
        print(f"<td>{data[1]}</td>")
        print(f"<td>{data[2]}</td>")
        print(f"<td>{data[3]}</td>")
        print("</tr>")
    print("</table>")
    cursor.close()
except Exception as e:
    print("오류:" + str(e))
finally:
    if conn:
        conn.close()