# MariaDB : jikwon table
# 직원번호, 직원명을 입력하여 로그인에 성공하면 해당직원, 부서정보 출력
import MySQLdb
import json

from dotenv import load_dotenv
import os
load_dotenv()

config = {
    'host':os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
    'port':int(os.getenv('DB_PORT')),  #port는 숫자처리
    'charset':os.getenv('DB_CHARSET')
}



def LoginFunc():
    conn = None  # finally에서 conn 참조할 수 있게 미리 선언
    try:
        conn = MySQLdb.connect(**config)  # DB 연결
        cursor = conn.cursor()  # sql 처리를 위한 객체 생성. cursor는 sql 실행을 담당

        sql = """
            Select jikwonno as 직원번호, jikwonname as 직원명, count(gogekno) as 관리고객수
from jikwon inner join gogek on jikwonno = gogekdamsano group by jikwonno;
        """

        # sql 실행 (플레이스홀더 %s 자리에 jikwon_no, jikwon_name 바인딩)
        cursor.execute(sql)

        # 로그인 성공 시 직원 정보 한 건 가져오기
        for 직원번호,직원명,관리고객수 in cursor:
            print(직원번호,직원명,관리고객수)
        

    except Exception as e:
        print('에러:', e)
    finally:
        if conn:
            conn.close()  # 연결 종료


if __name__ == "__main__":  # 이 파일을 직접 실행했을 때만 동작 (가독성/재사용성 위함)
    LoginFunc()
