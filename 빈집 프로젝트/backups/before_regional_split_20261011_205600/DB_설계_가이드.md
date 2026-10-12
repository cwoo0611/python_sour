# 핵심 5개 테이블 DB 설계

기존 13개에서 5개로 축소했습니다. 실제 빈집 896건과 빈집 번호를 유지한 SQLite 시제품입니다.

| 테이블 | 뜻 | 한 행의 의미 |
|---|---|---|
| regions | 지역 | 고창 또는 양산 |
| vacant_houses | 빈집 | 빈집 한 채의 원본 기록 |
| users | 회원 | 회원 한 명 |
| saved_houses | 관심 빈집 | 한 회원이 저장한 집과 메모·별점 |
| saved_house_business_types | 희망 업종 | 한 관심 항목에 선택한 업종 하나 |

## 관계를 이해하는 예시

회원 1번 민수가 빈집 10번을 저장하면 saved_houses에 user_id=1, house_id=10을 넣습니다.
그 저장 항목이 3번이면 희망 업종 테이블에 (3, 카페), (3, 공방)을 넣을 수 있습니다.
예시 회원은 DB에 생성하지 않았습니다.

## 줄인 내용

- data_sources와 raw_records를 제거했습니다. 원본은 루트의 CSV와 data 폴더의 API 응답 파일로 보관합니다.
- regions에는 id와 name만 남겼습니다. 고창·양산 두 지역만 있습니다.
- source_file과 source_row_number를 빈집에 넣어 이번 원본 파일의 데이터 행을 찾을 수 있습니다. 갱신된 파일에서도 같은 집을 보장하는 번호는 아닙니다.
- 상권·건축물대장·건설업체 공시·방문 통계 및 건축물 연결 테이블은 제거했습니다. 원본 파일은 보존하며 해당 기능 구현 시 테이블을 추가할 수 있습니다.
- 업종 6개는 고정 목록 CHECK 조건으로 관리하므로 business_types 기준 테이블이 없어도 됩니다.

## 데이터

고창은 원본 1288행 중 빈집판정결과가 해당인 736행, 양산은 160행입니다. 총 896행이며 현장 확인이나 거래 가능 여부를 검증한 수치는 아닙니다.
회원·관심·업종 선택은 사용자 입력 전이므로 비어 있습니다. 등급·구조·면적·문의처 등 기존 핵심 값과 ID는 유지했습니다.
없는 값은 NULL이고 원본의 0은 보존합니다. 가려진 주소를 복원하거나 좌표를 추정하지 않았습니다.
data_reference_period는 자료의 기준 시점이며 개별 주택의 조사일을 보장하지 않습니다.
현재 지역은 시군 단위입니다. 동·리별 지도 집계는 주소 정제와 하위 지역 연결이 추가로 필요합니다.
상권 등 외부 정보 연결 기능은 이번 핵심 DB 범위에서 제외했습니다. 관광자원통계는 미수집입니다.

## 규칙

- 회원과 빈집의 조합은 중복 저장할 수 없습니다.
- 별점은 1~5 또는 미입력 NULL입니다.
- 희망 업종은 카페·숙박·음식점·공방·사무실·기타입니다. 같은 업종 중복 선택은 금지합니다.
- 회원 삭제 시 관심 항목 및 희망 업종도 삭제됩니다. 참조 중인 빈집 삭제는 차단됩니다.
- 비밀번호는 password_hash에 해시값만 저장하며 인증키는 DB에 없습니다.
- 메모 수정 시 서버 코드에서 updated_at=CURRENT_TIMESTAMP도 갱신해야 합니다.
- SQLite 연결마다 PRAGMA foreign_keys=ON을 실행해야 FK 검사가 적용됩니다.

## 관련 파일

| 파일 | 역할 |
|---|---|
| 빈집프로젝트.sqlite3 | 실제 데이터 DB |
| ERD.md | 전체 관계도와 컬럼 한글 설명 |
| 테이블정의서.csv | 모든 컬럼·자료형·키·참조 |
| schema.sql | 5개 테이블 생성 SQL |
| seeded_database.sql | 실제 데이터 포함 SQLite 복원 SQL |
| 조회예제.sql | 지역별 빈집·관심 목록 조회 |
| 검증결과.json | 검증 결과 및 이전 버전 백업 위치 |

이전 버전은 backups/before_simplification_...에 보관했습니다. 활성 DB는 database 폴더의 파일입니다.
output/tables 엑셀은 원본 데이터 검토용이므로 활성 DB 테이블 목록과 다릅니다.
MySQL/MariaDB에 적용하려면 자동 증가 키와 날짜 자료형 등 SQL을 해당 DB에 맞게 변환해야 합니다.

프로젝트 루트에서 다음으로 조회할 수 있습니다.

```python
import sqlite3
db=sqlite3.connect('database/빈집프로젝트.sqlite3')
db.execute('PRAGMA foreign_keys=ON')
for row in db.execute('SELECT id,address_public,grade FROM vacant_houses LIMIT 10'):
    print(row)
db.close()
```
