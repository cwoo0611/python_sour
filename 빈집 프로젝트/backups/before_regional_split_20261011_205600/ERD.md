# 핵심 5개 테이블 ERD

```mermaid
erDiagram
 regions ||--o{ vacant_houses : "지역의 빈집"
 users ||--o{ saved_houses : "회원이 저장"
 vacant_houses ||--o{ saved_houses : "저장 대상"
 saved_houses ||--o{ saved_house_business_types : "희망 업종"
 regions {
  INTEGER id PK "번호"
  TEXT name  "지역 이름"
 }
 vacant_houses {
  INTEGER id PK "번호"
  INTEGER region_id FK "지역 번호"
  TEXT address_public  "공개 주소"
  TEXT house_type  "주택 유형"
  INTEGER grade  "등급"
  TEXT structure  "구조"
  INTEGER built_year  "준공 연도"
  NUMERIC total_floor_area_m2  "연면적"
  NUMERIC land_area_m2  "대지면적"
  TEXT land_use_zone  "용도지역"
  TEXT road_access  "도로접면"
  TEXT contact_agency  "문의 기관"
  TEXT contact_phone  "문의 전화"
  TEXT data_reference_period  "자료 기준 시점"
  TEXT source_file  "원본 파일"
  INTEGER source_row_number  "원본 데이터 행 번호"
 }
 users {
  INTEGER id PK "번호"
  TEXT email  "이메일"
  TEXT password_hash  "비밀번호 해시"
  TEXT display_name  "이름"
  TEXT created_at  "생성 시각"
 }
 saved_houses {
  INTEGER id PK "번호"
  INTEGER user_id FK "회원 번호"
  INTEGER house_id FK "빈집 번호"
  TEXT memo  "메모"
  INTEGER rating  "별점"
  TEXT created_at  "생성 시각"
  TEXT updated_at  "수정 시각"
 }
 saved_house_business_types {
  INTEGER saved_house_id PK,FK "관심 저장 번호"
  TEXT business_type PK "희망 업종"
 }
```

PK는 행 번호를 식별하는 기본키, FK는 다른 테이블 번호를 참조하는 외래키입니다.
한 회원은 여러 빈집을 저장할 수 있고, 같은 빈집도 여러 회원이 저장할 수 있습니다.
관심 항목에 카페와 공방을 선택하면 희망 업종 테이블에는 두 행이 생깁니다.
중복 금지: regions.name, users.email, saved_houses(user_id,house_id), vacant_houses(source_file,source_row_number).