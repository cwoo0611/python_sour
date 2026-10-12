PRAGMA foreign_keys=ON;
CREATE TABLE buildings (
 id INTEGER PRIMARY KEY,
 region_id INTEGER NOT NULL REFERENCES regions(id),
 source_ufid TEXT NOT NULL UNIQUE,
 parcel_code TEXT,
 building_register_id TEXT,
 ground_floors INTEGER,
 underground_floors INTEGER,
 building_area_m2 NUMERIC CHECK(building_area_m2>=0),
 total_floor_area_m2 NUMERIC CHECK(total_floor_area_m2>=0),
 approval_date_raw TEXT,
 geometry_geojson TEXT NOT NULL CHECK(json_valid(geometry_geojson)),
 fetched_at TEXT NOT NULL
);
CREATE TABLE gochang_house_details(
 house_id INTEGER PRIMARY KEY REFERENCES vacant_houses(id) ON DELETE CASCADE,
 house_type TEXT,built_year INTEGER,land_area_m2 NUMERIC CHECK(land_area_m2>=0),
 land_use_zone TEXT,road_access TEXT);
CREATE TABLE house_building_links (
 house_id INTEGER NOT NULL REFERENCES vacant_houses(id) ON DELETE CASCADE,
 building_id INTEGER NOT NULL REFERENCES buildings(id),
 evidence TEXT NOT NULL CHECK(length(trim(evidence))>0),
 verified_at TEXT NOT NULL,
 PRIMARY KEY(house_id,building_id)
);
CREATE TABLE regions(id INTEGER PRIMARY KEY,name TEXT NOT NULL UNIQUE);
CREATE TABLE saved_house_business_types(
 saved_house_id INTEGER NOT NULL REFERENCES saved_houses(id) ON DELETE CASCADE,
 business_type TEXT NOT NULL CHECK(business_type IN ('카페','숙박','음식점','공방','사무실','기타')),
 PRIMARY KEY(saved_house_id,business_type));
CREATE TABLE saved_houses(id INTEGER PRIMARY KEY,user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 house_id INTEGER NOT NULL REFERENCES vacant_houses(id),memo TEXT,rating INTEGER CHECK(rating BETWEEN 1 AND 5),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,UNIQUE(user_id,house_id));
CREATE TABLE users(id INTEGER PRIMARY KEY,email TEXT NOT NULL COLLATE NOCASE UNIQUE,
 password_hash TEXT NOT NULL,display_name TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE vacant_houses(
 id INTEGER PRIMARY KEY,region_id INTEGER NOT NULL REFERENCES regions(id),
 address_public TEXT NOT NULL,grade INTEGER CHECK(grade BETWEEN 1 AND 3),
 structure TEXT,total_floor_area_m2 NUMERIC CHECK(total_floor_area_m2>=0),data_reference_period TEXT,
 source_file TEXT NOT NULL,source_row_number INTEGER NOT NULL,UNIQUE(source_file,source_row_number));
CREATE TABLE yangsan_house_details(
 house_id INTEGER PRIMARY KEY REFERENCES vacant_houses(id) ON DELETE CASCADE,
 contact_agency TEXT,contact_phone TEXT);
CREATE INDEX idx_buildings_parcel ON buildings(parcel_code);
CREATE INDEX idx_buildings_register ON buildings(building_register_id);
CREATE INDEX idx_houses_region_grade ON vacant_houses(region_id,grade);
