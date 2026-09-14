# --- DB(RDBMS) 연동 관련 ------------------------------------------
# 문1) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
# 직원번호 입력 : _______
# 직원명 입력 : _______
# 직원번호 직원명 부서명 부서전화 직급 성별
#     1         홍길동 총무부 111-1111 이사 남           <== 홍길동으로 로그인한 경우


# pip install python-dotenv   설치
# env 파일로 db 연결 정보 읽기
# DB_HOST = 127.0.0.1
# DB_USER=root
# DB_PASSWORD=123
# DB_NAME=test
# DB_PORT=3306
# DB_CHARSET=utf8
import MySQLdb

from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'host':os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
    'port':int(os.getenv('DB_PORT')),     # port는 수자 처리 
    'charset':os.getenv('DB_CHARSET'),
    }

def loginfunc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)  # DB 연결  # dict여서 **를 붙인다.
        cursor = conn.cursor()  # SQL 처리를 위한 객체 생성
        jikwonno = input('직원번호 입력 : ')
        jikwonname = input('직원명 입력 : ')
        if jikwonno == '' or jikwonname == '':
            print('로그인 정보를 입력하세요')
            return

        sql = """
        select 
        j.jikwonno as 직원번호, j.jikwonname as 직원명,
        b.busername as 부서명, b.busertel as 부서전화, j.jikwonjik as 직급, j.jikwongen as 성별      
        from jikwon j
        left outer join buser b on j.busernum = b.buserno
        where j.jikwonno=%s and j.jikwonname=%s
        """

        # sql 실행
        cursor.execute(sql, (jikwonno, jikwonname))  # sql 실행  # %s자리에 입력값이 들어감 

        # 로그인 성공 직원 정보 출력
        data = cursor.fetchone()


        # 로그인 성공시

        if data:
            print('로그인 성공')
            print('직원번호','직원명','부서명','부서전화','직급','성별')
            print(data[0],'      ',data[1],data[2],data[3],data[4],data[5])

        else:
            print('로그인 실패 : 다시 확인해주세요')

    except Exception as e:
        print('에러 : ', e)
    finally:
        if conn:
            conn.close()     # conn이 있으면 연결종료 



if __name__ == '__main__':
    loginfunc()