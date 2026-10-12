PRAGMA foreign_keys = ON;

-- 지역별 빈집 수 및 등급
SELECT r.name, h.grade, COUNT(*) AS house_count
FROM vacant_houses h JOIN regions r ON r.id=h.region_id
GROUP BY r.id,h.grade ORDER BY r.name,h.grade;

-- 양산 빈집 상세
SELECT h.id,h.address_public,h.grade,h.structure,h.total_floor_area_m2,
       h.contact_agency,h.contact_phone,h.data_reference_period
FROM vacant_houses h JOIN regions r ON r.id=h.region_id
WHERE r.code='48330' ORDER BY h.id LIMIT 20;

-- 양산의 상가 샘플
SELECT s.name,s.industry_small_name,s.road_address,s.latitude,s.longitude
FROM commercial_stores s JOIN regions r ON r.id=s.region_id
WHERE r.code='48330';

-- 수집된 방문 통계: 지역과 유형을 항상 함께 표시
SELECT r.name,v.base_date,v.visitor_type_name,v.visitor_count
FROM regional_visitor_stats v JOIN regions r ON r.id=v.region_id;

-- 한 회원의 관심 목록 (회원 1은 현재 생성되지 않아 결과가 비어 있음)
SELECT h.address_public,h.grade,s.memo,s.rating,s.updated_at
FROM saved_houses s JOIN vacant_houses h ON h.id=s.house_id
WHERE s.user_id=1 ORDER BY s.updated_at DESC;
