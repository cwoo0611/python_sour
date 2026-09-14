# MariaDB : jikwon table
# 직원번호, 직원명을 입력하여 로그인에 성공하면 해당직원, 부서정보 출력
import MySQLdb
import json

# DB 연결 정보 읽기 1 : json 파일읽기
# with open('dbconnect.json', mode='r', encoding='utf-8') as f:
#     config = json.load(f)

# DB 접속 정보 읽기 2: .env 파일 읽기 
#pip install python-dotenv
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

        jikwon_no = input("직원번호:")
        jikwon_name = input("직원이름:")

        # 입력값 검증: 하나라도 비어있으면 함수 종료
        if jikwon_no == "" or jikwon_name == "":
            print("로그인 정보를 입력하세요")
            return

        # 참고용 예전 버전 (format 방식) - SQL 인젝션에 취약해서 사용 안 함
        # sql = """
        #         select jikwonno as 직원번호,jikwonname as 직원명,
        #         buserloc as 근무지역,jikwonjik as 직급,jikwongen as 성별
        #         from jikwon
        #         left outer join buser on jikwon.busernum = buser.buserno
        #         where jikwonno={0} and jikwonname={1}
        #     """.format(jikwon_no,jikwon_name)

        # 직원번호, 직원명, 부서정보(근무지역), 직급, 성별을 조회
        # %s는 파라미터 플레이스홀더 (execute의 두번째 인자로 값 전달)
        sql = """
            select j.jikwonno as 직원번호, j.jikwonname as 직원명,
            b.busername as 부서명, b.busertel as 부서전화,j.jikwonjik as 직급, j.jikwongen as 성별
            from jikwon j
            left outer join buser b on j.busernum = b.buserno
            where j.jikwonno=%s and j.jikwonname=%s
        """

        # sql 실행 (플레이스홀더 %s 자리에 jikwon_no, jikwon_name 바인딩)
        cursor.execute(sql, (jikwon_no, jikwon_name))

        # 로그인 성공 시 직원 정보 한 건 가져오기
        data = cursor.fetchone()

        if data:
            print("로그인 성공")
            print("직원번호:", data[0])
            print("직원명:", data[1])
            print("부서명:", data[2])
            print("부서전화:", data[3])
            print("직급:", data[4])
            print("성별:", data[5])
        else:
            print("로그인 실패: 입력자료 확인하세요")

    except Exception as e:
        print('에러:', e)
    finally:
        if conn:
            conn.close()  # 연결 종료


if __name__ == "__main__":  # 이 파일을 직접 실행했을 때만 동작 (가독성/재사용성 위함)
    LoginFunc()

