# 빈집 프로젝트 ERD

실제 생성된 SQLite 스키마를 기준으로 작성했습니다. PK는 기본키, FK는 외래키, UK는 중복 금지 키입니다.

```mermaid
erDiagram
    data_sources ||--o{ raw_records : "원본 출처"
    raw_records ||--o| vacant_houses : "빈집 판정 후 정제"
    raw_records ||--o| building_registers : "건축물대장 정제"
    raw_records ||--o| commercial_stores : "상가 정제"
    raw_records ||--o| construction_notices : "등록공시 정제"
    raw_records ||--o| regional_visitor_stats : "방문 통계 정제"
    regions ||--o{ vacant_houses : "소재 지역"
    regions ||--o{ building_registers : "소재 지역"
    regions ||--o{ commercial_stores : "소재 지역"
    regions ||--o{ construction_notices : "등록 지역"
    regions ||--o{ regional_visitor_stats : "집계 지역"
    vacant_houses ||--o{ house_building_links : "확인된 연결"
    building_registers ||--o{ house_building_links : "확인된 연결"
    users ||--o{ saved_houses : "관심 저장"
    vacant_houses ||--o{ saved_houses : "관심 대상"
    saved_houses ||--o{ saved_house_business_types : "희망 업종"
    business_types ||--o{ saved_house_business_types : "업종 선택"

    data_sources {
        INTEGER id PK
        TEXT name
        TEXT source_url
        TEXT reference_period
        TEXT coverage_note
    }
    raw_records {
        INTEGER id PK
        INTEGER source_id FK
        TEXT snapshot_row_key
        TEXT payload_json
        TEXT imported_at
    }
    regions {
        INTEGER id PK
        TEXT code UK
        TEXT name
        TEXT level
    }
    vacant_houses {
        INTEGER id PK
        INTEGER raw_record_id FK,UK
        INTEGER region_id FK
        TEXT source_row_key
        TEXT address_public
        TEXT locality_name
        INTEGER grade
        TEXT structure
        INTEGER built_year
        NUMERIC total_floor_area_m2
        NUMERIC land_area_m2
        TEXT data_reference_period
        REAL latitude
        REAL longitude
    }
    building_registers {
        INTEGER id PK
        INTEGER raw_record_id FK,UK
        TEXT registry_pk UK
        INTEGER region_id FK
        TEXT legal_dong_code
        TEXT parcel_main
        TEXT parcel_sub
        TEXT approval_date_raw
        TEXT approval_date
        INTEGER approval_year
    }
    house_building_links {
        INTEGER house_id PK,FK
        INTEGER building_id PK,FK
        TEXT evidence
        TEXT verified_at
    }
    commercial_stores {
        INTEGER id PK
        INTEGER raw_record_id FK,UK
        TEXT source_store_id UK
        INTEGER region_id FK
        TEXT name
        TEXT industry_small_code
        TEXT industry_small_name
        REAL latitude
        REAL longitude
        TEXT reference_month
    }
    construction_notices {
        INTEGER id PK
        INTEGER raw_record_id FK,UK
        TEXT source_notice_id UK
        INTEGER region_id FK
        TEXT company_name
        TEXT business_registration_no
        TEXT industry_registration_no
        TEXT notice_type
        TEXT notice_date
    }
    regional_visitor_stats {
        INTEGER id PK
        INTEGER raw_record_id FK,UK
        INTEGER region_id FK
        TEXT base_date
        TEXT visitor_type_code
        TEXT visitor_type_name
        NUMERIC visitor_count
    }
    users {
        INTEGER id PK
        TEXT email UK
        TEXT password_hash
        TEXT display_name
        TEXT created_at
    }
    saved_houses {
        INTEGER id PK
        INTEGER user_id FK
        INTEGER house_id FK
        TEXT memo
        INTEGER rating
        TEXT created_at
        TEXT updated_at
    }
    business_types {
        INTEGER id PK
        TEXT name UK
    }
    saved_house_business_types {
        INTEGER saved_house_id PK,FK
        INTEGER business_type_id PK,FK
    }
```

빈집·건축물대장·상권·공시의 상세 컬럼 전체는 `테이블정의서.csv` 및 `schema.sql`에서 확인할 수 있습니다.

추가 복합 UNIQUE: raw_records(source_id, snapshot_row_key), saved_houses(user_id, house_id), regional_visitor_stats(region_id, base_date, visitor_type_code).

raw_records에서 정제 테이블로 가는 1:0..1 관계는 해당 자료의 정제 경로를 표현합니다. 현재 스키마는 정제 테이블별 raw_record_id 중복을 막지만 서로 다른 정제 테이블 사이의 배타성은 적재 프로그램에서 관리합니다.
