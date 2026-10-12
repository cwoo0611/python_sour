# 건물 위치 정보를 추가한 9개 테이블 ERD

```mermaid
erDiagram
 regions ||--o{ vacant_houses : "지역의 빈집"
 vacant_houses ||--o| gochang_house_details : "고창이면 상세 1행"
 vacant_houses ||--o| yangsan_house_details : "양산이면 상세 1행"
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
  INTEGER grade  "등급"
  TEXT structure  "구조"
  NUMERIC total_floor_area_m2  "연면적"
  TEXT data_reference_period  "자료 기준 시점"
  TEXT source_file  "원본 파일"
  INTEGER source_row_number  "원본 데이터 행 번호"
 }
 gochang_house_details {
  INTEGER house_id PK,FK "빈집 번호"
  TEXT house_type  "주택 유형"
  INTEGER built_year  "준공 연도"
  NUMERIC land_area_m2  "대지면적"
  TEXT land_use_zone  "용도지역"
  TEXT road_access  "도로접면"
 }
 yangsan_house_details {
  INTEGER house_id PK,FK "빈집 번호"
  TEXT contact_agency  "문의 기관"
  TEXT contact_phone  "문의 전화"
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
 regions ||--o{ buildings : "지역의 건물"
 vacant_houses ||--o{ house_building_links : "확인된 연결"
 buildings ||--o{ house_building_links : "연결된 건물"
 buildings {
  INTEGER id PK "번호"
  INTEGER region_id FK "지역 번호"
  TEXT source_ufid UK "브이월드 건물 식별번호"
  TEXT parcel_code  "필지번호 PNU"
  TEXT building_register_id  "건축물대장 식별번호"
  INTEGER ground_floors  "지상 층수"
  INTEGER underground_floors  "지하 층수"
  NUMERIC building_area_m2  "건축면적 제곱미터"
  NUMERIC total_floor_area_m2  "연면적 제곱미터"
  TEXT approval_date_raw  "사용승인일 원본"
  TEXT geometry_geojson  "건물 윤곽 좌표 EPSG4326 GeoJSON"
  TEXT fetched_at  "수집 시각 UTC"
 }
 house_building_links {
  INTEGER house_id PK,FK "빈집 번호"
  INTEGER building_id PK,FK "건물 번호"
  TEXT evidence  "연결 확인 근거"
  TEXT verified_at  "연결 확인 시각"
 }
```

PK는 행 번호를 식별하는 기본키, FK는 다른 테이블 번호를 참조하는 외래키입니다.
한 회원은 여러 빈집을 저장할 수 있고, 같은 빈집도 여러 회원이 저장할 수 있습니다.
관심 항목에 카페와 공방을 선택하면 희망 업종 테이블에는 두 행이 생깁니다.
중복 금지: regions.name, users.email, saved_houses(user_id,house_id), vacant_houses(source_file,source_row_number).
buildings는 일반 건물 정보입니다. 빈집 여부를 뜻하지 않습니다. 현재 건물 5건, 확인된 빈집 연결 0건입니다. geometry_geojson은 건물 테두리 좌표이며 좌표계는 EPSG:4326, 순서는 경도·위도입니다.
