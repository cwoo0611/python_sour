PRAGMA foreign_keys=ON;
-- 지역별 빈집 수: 고창 736, 양산 160
SELECT r.name,COUNT(*) AS house_count FROM vacant_houses h
JOIN regions r ON r.id=h.region_id GROUP BY r.id;
-- 양산 빈집
SELECT h.id,h.address_public,h.grade,h.structure,h.total_floor_area_m2
FROM vacant_houses h JOIN regions r ON r.id=h.region_id
WHERE r.name='경상남도 양산시' ORDER BY h.id LIMIT 20;
-- 회원 1의 관심 목록: 현재 회원이 없으므로 빈 결과
SELECT h.address_public,s.memo,s.rating FROM saved_houses s
JOIN vacant_houses h ON h.id=s.house_id WHERE s.user_id=1;
-- 저장한 빈집별 희망 업종
SELECT s.user_id,s.house_id,b.business_type FROM saved_houses s
JOIN saved_house_business_types b ON b.saved_house_id=s.id;
-- 고창: 공통 + 고창 상세
SELECT h.id,h.address_public,h.grade,h.structure,h.total_floor_area_m2,
g.house_type,g.built_year,g.land_area_m2,g.land_use_zone,g.road_access
FROM vacant_houses h JOIN gochang_house_details g ON g.house_id=h.id LIMIT 20;
-- 양산: 공통 + 양산 상세
SELECT h.id,h.address_public,h.grade,h.structure,h.total_floor_area_m2,
y.contact_agency,y.contact_phone
FROM vacant_houses h JOIN yangsan_house_details y ON y.house_id=h.id LIMIT 20;
