PRAGMA foreign_keys=ON;
CREATE TABLE regions(id INTEGER PRIMARY KEY,name TEXT NOT NULL UNIQUE);
CREATE TABLE vacant_houses(
 id INTEGER PRIMARY KEY,region_id INTEGER NOT NULL REFERENCES regions(id),
 address_public TEXT NOT NULL,house_type TEXT,grade INTEGER CHECK(grade BETWEEN 1 AND 3),
 structure TEXT,built_year INTEGER,total_floor_area_m2 NUMERIC CHECK(total_floor_area_m2>=0),
 land_area_m2 NUMERIC CHECK(land_area_m2>=0),land_use_zone TEXT,road_access TEXT,
 contact_agency TEXT,contact_phone TEXT,data_reference_period TEXT,
 source_file TEXT NOT NULL,source_row_number INTEGER NOT NULL,UNIQUE(source_file,source_row_number));
CREATE TABLE users(id INTEGER PRIMARY KEY,email TEXT NOT NULL COLLATE NOCASE UNIQUE,
 password_hash TEXT NOT NULL,display_name TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE saved_houses(id INTEGER PRIMARY KEY,user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 house_id INTEGER NOT NULL REFERENCES vacant_houses(id),memo TEXT,rating INTEGER CHECK(rating BETWEEN 1 AND 5),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,UNIQUE(user_id,house_id));
CREATE TABLE saved_house_business_types(
 saved_house_id INTEGER NOT NULL REFERENCES saved_houses(id) ON DELETE CASCADE,
 business_type TEXT NOT NULL CHECK(business_type IN ('카페','숙박','음식점','공방','사무실','기타')),
 PRIMARY KEY(saved_house_id,business_type));
CREATE INDEX idx_houses_region_grade ON vacant_houses(region_id,grade);
