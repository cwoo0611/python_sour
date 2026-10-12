
PRAGMA foreign_keys = ON;
CREATE TABLE data_sources (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL, source_url TEXT NOT NULL,
 reference_period TEXT, coverage_note TEXT NOT NULL
);
CREATE TABLE raw_records (
 id INTEGER PRIMARY KEY, source_id INTEGER NOT NULL REFERENCES data_sources(id),
 snapshot_row_key TEXT NOT NULL, payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
 imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(source_id, snapshot_row_key)
);
CREATE TABLE regions (
 id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT NOT NULL,
 level TEXT NOT NULL CHECK(level IN ('city','county','district'))
);
CREATE TABLE vacant_houses (
 id INTEGER PRIMARY KEY, raw_record_id INTEGER NOT NULL UNIQUE REFERENCES raw_records(id),
 region_id INTEGER NOT NULL REFERENCES regions(id), source_row_key TEXT NOT NULL,
 address_public TEXT NOT NULL, locality_name TEXT, house_type TEXT,
 grade INTEGER CHECK(grade BETWEEN 1 AND 3), structure TEXT, built_year INTEGER,
 total_floor_area_m2 NUMERIC CHECK(total_floor_area_m2 >= 0),
 building_area_m2 NUMERIC CHECK(building_area_m2 >= 0),
 land_area_m2 NUMERIC CHECK(land_area_m2 >= 0), land_use_zone TEXT, road_access TEXT,
 determination_date TEXT, grade_date TEXT, data_reference_period TEXT,
 contact_agency TEXT, contact_phone TEXT,
 latitude REAL CHECK(latitude BETWEEN -90 AND 90),
 longitude REAL CHECK(longitude BETWEEN -180 AND 180),
 CHECK((latitude IS NULL) = (longitude IS NULL))
);
CREATE TABLE building_registers (
 id INTEGER PRIMARY KEY, raw_record_id INTEGER NOT NULL UNIQUE REFERENCES raw_records(id),
 registry_pk TEXT NOT NULL UNIQUE, region_id INTEGER NOT NULL REFERENCES regions(id),
 legal_dong_code TEXT, parcel_main TEXT, parcel_sub TEXT, address_public TEXT,
 structure TEXT, main_use TEXT, total_floor_area_m2 NUMERIC, land_area_m2 NUMERIC,
 floors_above INTEGER, floors_below INTEGER, approval_date_raw TEXT,
 approval_date TEXT, approval_year INTEGER
);
CREATE TABLE house_building_links (
 house_id INTEGER NOT NULL REFERENCES vacant_houses(id),
 building_id INTEGER NOT NULL REFERENCES building_registers(id),
 evidence TEXT NOT NULL, verified_at TEXT NOT NULL,
 PRIMARY KEY(house_id, building_id)
);
CREATE TABLE commercial_stores (
 id INTEGER PRIMARY KEY, raw_record_id INTEGER NOT NULL UNIQUE REFERENCES raw_records(id),
 source_store_id TEXT NOT NULL UNIQUE, region_id INTEGER NOT NULL REFERENCES regions(id),
 name TEXT NOT NULL, branch_name TEXT, industry_large_code TEXT, industry_large_name TEXT,
 industry_medium_code TEXT, industry_medium_name TEXT,
 industry_small_code TEXT, industry_small_name TEXT,
 road_address TEXT, parcel_address TEXT, building_management_no TEXT,
 latitude REAL CHECK(latitude BETWEEN -90 AND 90),
 longitude REAL CHECK(longitude BETWEEN -180 AND 180), reference_month TEXT
);
CREATE TABLE construction_notices (
 id INTEGER PRIMARY KEY, raw_record_id INTEGER NOT NULL UNIQUE REFERENCES raw_records(id),
 source_notice_id TEXT NOT NULL UNIQUE, region_id INTEGER NOT NULL REFERENCES regions(id),
 company_name TEXT NOT NULL, business_registration_no TEXT, representative_name TEXT,
 address TEXT, phone TEXT, industry_name TEXT, industry_registration_no TEXT,
 notice_number TEXT, notice_type TEXT, registration_date TEXT, notice_date TEXT,
 change_reason TEXT
);
CREATE TABLE regional_visitor_stats (
 id INTEGER PRIMARY KEY, raw_record_id INTEGER NOT NULL UNIQUE REFERENCES raw_records(id),
 region_id INTEGER NOT NULL REFERENCES regions(id), base_date TEXT NOT NULL,
 visitor_type_code TEXT NOT NULL, visitor_type_name TEXT NOT NULL,
 visitor_count NUMERIC NOT NULL CHECK(visitor_count >= 0),
 weekday_code TEXT, weekday_name TEXT,
 UNIQUE(region_id, base_date, visitor_type_code)
);
CREATE TABLE users (
 id INTEGER PRIMARY KEY, email TEXT NOT NULL COLLATE NOCASE UNIQUE,
 password_hash TEXT NOT NULL, display_name TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE saved_houses (
 id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 house_id INTEGER NOT NULL REFERENCES vacant_houses(id), memo TEXT,
 rating INTEGER CHECK(rating BETWEEN 1 AND 5),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(user_id, house_id)
);
CREATE TABLE business_types (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE saved_house_business_types (
 saved_house_id INTEGER NOT NULL REFERENCES saved_houses(id) ON DELETE CASCADE,
 business_type_id INTEGER NOT NULL REFERENCES business_types(id),
 PRIMARY KEY(saved_house_id, business_type_id)
);
CREATE INDEX idx_houses_region_grade ON vacant_houses(region_id, grade);
CREATE INDEX idx_stores_region_industry ON commercial_stores(region_id, industry_small_code);
CREATE INDEX idx_notices_region_industry ON construction_notices(region_id, industry_name);
CREATE INDEX idx_visitors_region_date ON regional_visitor_stats(region_id, base_date);
