# 지역별 상세를 분리한 7개 테이블

빈집 896건의 공통 항목은 vacant_houses에, 지역마다 다른 항목은 고창·양산 상세 테이블에 저장합니다. 기존 빈집 번호와 값은 모두 유지했습니다. SQLite 시제품입니다.

| 테이블 | 저장 내용 | 현재 행 수 |
|---|---|---:|
| regions | 고창·양산 지역 번호와 이름 | 2 |
| vacant_houses | 주소·등급·구조·연면적·자료 기준·원본 파일 | 896 |
| gochang_house_details | 주택 유형·준공 연도·대지면적·용도지역·도로접면 | 736 |
| yangsan_house_details | 문의 기관·문의 전화 | 160 |
| users | 회원 | 0 |
| saved_houses | 회원별 관심 빈집·메모·별점 | 0 |
| saved_house_business_types | 관심 빈집에서 선택한 희망 업종 | 0 |

## 핵심 관계

고창 빈집 1번은 vacant_houses에 공통 정보 한 행을 저장하고, gochang_house_details에 house_id=1인 상세 한 행을 저장합니다. 양산에는 고창 상세 행을 만들지 않습니다. 양산 집은 yangsan_house_details에 상세 행을 저장합니다.

각 상세 테이블의 house_id는 PK이면서 FK입니다. 따라서 같은 빈집의 상세를 두 번 넣을 수 없고, 존재하지 않는 빈집의 상세도 넣을 수 없습니다.
해당 지역과 맞는 상세 테이블을 선택하는 규칙은 적재 프로그램과 서버 코드에서 관리합니다. FK만으로 고창 집에 양산 상세를 연결하는 실수를 자동 차단하지는 않습니다. 이번 적재 결과는 지역별 상세 수와 중복 연결이 없는지 검사했습니다.

## NULL이 줄어드는 이유

양산에 없는 준공 연도·대지면적 등의 컬럼은 양산 상세 테이블에 아예 없습니다. 고창에 없는 문의처 컬럼도 고창 상세 테이블에 없습니다.
다만 원본에도 비어 있는 값은 여전히 NULL입니다. 구조 분리는 없는 정보를 만들어 채우는 작업이 아닙니다.
고창 구조·연면적과 양산 일부 등급 등은 공통 항목이지만 개별 값이 없을 수 있습니다.

## 상세 조회

고창 화면에서는 공통 정보와 고창 상세를 house_id로 JOIN합니다.

```sql
SELECT h.id,h.address_public,h.grade,h.structure,h.total_floor_area_m2,
       g.house_type,g.built_year,g.land_area_m2,g.land_use_zone,g.road_access
FROM vacant_houses h
JOIN gochang_house_details g ON g.house_id=h.id;
```

양산 화면에서는 양산 상세와 JOIN합니다.

```sql
SELECT h.id,h.address_public,h.grade,h.structure,h.total_floor_area_m2,
       y.contact_agency,y.contact_phone
FROM vacant_houses h
JOIN yangsan_house_details y ON y.house_id=h.id;
```

전체 목록에는 공통 테이블만 사용하면 됩니다. 두 상세를 모두 LEFT JOIN하면 상대 지역에 해당하지 않는 열이 조회 결과에 NULL로 보일 수 있지만 저장 구조에서는 분리되어 있습니다.

## 회원 기능

users와 vacant_houses를 saved_houses가 연결합니다. 한 회원은 여러 집을 저장하고 같은 집을 여러 회원이 저장할 수 있습니다. 메모와 별점은 회원별로 따로 저장됩니다.
저장 항목에 카페·공방을 함께 선택하면 saved_house_business_types에 두 행이 생깁니다.
업종은 카페·숙박·음식점·공방·사무실·기타로 제한하며 별점은 1~5 또는 NULL입니다.
회원·저장 항목 삭제 시 관련 업종 선택도 삭제됩니다. 빈집 삭제 시 상세 행도 삭제되지만, 관심 목록이 참조 중인 빈집은 삭제가 차단됩니다.

## 원본과 출처

고창 원본 1288행 중 빈집판정결과가 해당인 736행과 양산 160행을 유지했습니다. 현장 확인이나 거래 가능 여부를 검증한 수치는 아닙니다.
source_file과 source_row_number는 이번 원본 파일의 데이터 행을 추적합니다. 새 파일에서도 같은 집을 보장하는 식별자는 아닙니다.
원본 CSV는 프로젝트 루트, 수집한 외부 API 응답은 data 폴더에 보존합니다. 상권·업체·방문 통계·건축물대장 테이블은 이번 핵심 DB에 포함하지 않습니다. 관광자원통계는 미수집입니다.
지역은 고창·양산 시군 단위입니다. 동·리 지도 집계는 주소 정제와 하위 지역 연결이 추가로 필요합니다.
공개 주소를 복원하거나 좌표를 추정하지 않았습니다. 없는 값은 NULL, 원본의 0은 그대로 유지합니다. data_reference_period는 자료 기준이며 개별 주택의 조사일을 보장하지 않습니다.

## 관련 파일

| 파일 | 용도 |
|---|---|
| 빈집프로젝트.sqlite3 | 실제 데이터가 담긴 7개 테이블 DB |
| ERD.md | 모든 컬럼과 관계, 컬럼 한글 설명 |
| 테이블정의서.csv | 컬럼·자료형·PK·FK·필수 여부 |
| schema.sql | 7개 테이블 생성 SQL |
| seeded_database.sql | 데이터 포함 SQLite 복원 SQL |
| 조회예제.sql | 공통·고창·양산·관심 목록 조회 |
| 검증결과.json | 건수·무결성·값 보존 검증 및 백업 위치 |

이전 5개 테이블 DB와 문서는 backups/before_regional_split_...에 보관합니다. database 폴더가 현재 버전입니다.
output/tables의 엑셀과 구조 문서는 원본 수집자료 검토용이며 현재 DB 테이블 정의서가 아닙니다.

## 구현 시 주의

- SQLite 연결마다 PRAGMA foreign_keys=ON을 실행합니다.
- 상세 행의 지역 구분, 공통·상세 동시 저장은 서버 코드의 하나의 트랜잭션에서 처리합니다.
- 비밀번호는 password_hash에 안전한 해시값만 저장합니다. 인증키는 DB에 없습니다.
- 메모 변경 시 updated_at=CURRENT_TIMESTAMP도 갱신합니다.
- MySQL/MariaDB에 쓰려면 자동 증가 키·날짜 자료형 등 SQL을 맞춰야 합니다.

프로젝트 루트에서 Python으로 공통 목록을 볼 수 있습니다.

```python
import sqlite3
db=sqlite3.connect('database/빈집프로젝트.sqlite3')
db.execute('PRAGMA foreign_keys=ON')
for row in db.execute('SELECT id,address_public,grade FROM vacant_houses LIMIT 10'):
    print(row)
db.close()
```
