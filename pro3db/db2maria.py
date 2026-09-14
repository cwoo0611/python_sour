# 원격 데이터 베이스와 연동 프로그래밍
# MariaDB : 
# 준비 1)ip(네트워크에서 컴퓨터나 장치를 구분 규약) 주소가 필요
# 준비 2)연결용 driver file이 필요

# pip install mysqlclient

import MySQLdb

# 연결방법1
# conn = MySQLdb.connect( # db연결담당
#     host='127.0.0.1',  #192.168.0.29, localhost
#     user='root',
#     password='123',
#     database='test',
#     port=3306    #mariadb/mysql 서버가 기본적으로 사용하는 포트번호
# )


# 연결방법2
# config_data = {
#     'host':'127.0.0.1',
#     'user':'root',
#     'password':'123',
#     'database':'test',
#     'port':3306,
#     'charset':'utf8'

# 

# 연결방법3
# 별도 저장된 json 파일 읽기
import json

with open('dbconnect.json', mode='r',encoding='utf-8') as f:
    config_data = json.load(f) #저장된 JSON 텍스트를 파이썬 객체로 변환해 가져온다는 뜻이에요.



def myFunc():
    try:
        conn = MySQLdb.connect(**config_data)
        conn.autocommit(True) #자동 커밋
        conn.autocommit(False) #수동 커밋:기본값
        cursor = conn.cursor() #sql 처리를 위한 객체 생성. cusor는 sql 실행을 담당

        #자료 추가
        
        # # isql = "insert into sangdata(code,sang,su,dan) values(5,'마스크',5,'3000')"
        # isql = "insert into sangdata(code,sang,su,dan) values(%s,%s,%s,%s)"
        # ins_data = (6,'커피',10,5000)
        # cursor.execute(isql,ins_data)
        # conn.commit() #원격 db에 저장됨 

        # 자료수정
        # usql = "update sangdata set sang=%s,su=%s,dan=%s where code =%s"
        # up_data = '물티슈',3,1000,5 #('물티슈',3,1000,5) 
        # cursor.execute(usql,up_data) 
        # conn.commit()   

        # usql = "update sangdata set sang=%s,su=%s,dan=%s where code =%s"
        # up_data = '콜라',11,3000,6 
        # #insert,update,delete 성공하면 성공 갯수,실패하면 0을 반환
        # cou = cursor.execute(usql,up_data) 
        # print("수정갯수:",cou)
        # conn.commit() 

        #자료삭제
        code = '6';
        dsql = "delete from sangdata where code=%s"
        cou = cursor.execute(dsql,(code,)) #반환값 얻기
        if cou !=0:
            print('삭제성공')
        else:
            print("삭제실패")

        conn.commit()

        #참고 : secure coding 가이드라인에 맞게 프로그래밍 해야 한다. 
        # 해킹 위험: sql 인젝션은 사용자의 입력값을 검증하지 않는 웹 애플리케이션이

        print(dsql)


        # 자료 읽기
        sql = "select * from sangdata"
        cursor.execute(sql) #sql 읽기
        for data in cursor.fetchall():
                    # print(data)
            print("%s %s %s %s" %data)

        print()
        cursor.execute(sql)
        for data in cursor:
            print(data[0],data[1],data[2],data[3])

        print()
        cursor.execute(sql)
        for code,sang,su,dan in cursor:
            print(code,sang,su,dan)

        print()
        cursor.execute(sql)
        for a,b,수량,단가 in cursor:
            print(a,b,수량,단가)

    except Exception as e:
        print('처리 오류: ',e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':   #main것을 알려줌 가독성을 올려준다
    myFunc()
