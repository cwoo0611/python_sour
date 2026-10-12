"""Build a reviewable SQLite prototype from the collected source snapshots."""
import csv
import hashlib
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'database'
OUT.mkdir(exist_ok=True)
SCHEMA = '''
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
'''

def clean(v):
    if v is None:return None
    value=str(v).strip()
    return value if value and value != '-' else None
def number(v):
    v=clean(v)
    return float(v) if v and re.fullmatch(r'\d+(\.\d+)?',v) else None
def integer(v):
    v=number(v)
    return int(v) if v is not None and v.is_integer() else None
def date(v):
    v=clean(v)
    if not v:return None
    from datetime import datetime
    for fmt in ('%Y%m%d','%Y-%m-%d','%Y.%m.%d'):
        try:return datetime.strptime(v,fmt).date().isoformat()
        except ValueError:pass
    return None
def grade(v):
    match=re.fullmatch(r'([123])등급',clean(v) or '')
    return int(match[1]) if match else None

def main():
    # An existing database is never overwritten.
    db=OUT/'빈집프로젝트.sqlite3'
    if db.exists():raise SystemExit('Database already exists. Keep the existing database and choose a new output name.')
    conn=sqlite3.connect(db)
    conn.executescript(SCHEMA)
    def insert(table, row):
        keys=list(row)
        cur=conn.execute(f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join('?' for _ in keys)})",[row[k] for k in keys])
        return cur.lastrowid
    def raw(source,key,row):
        return insert('raw_records',dict(source_id=source,snapshot_row_key=str(key),payload_json=json.dumps(row,ensure_ascii=False)))
    regions={}
    def region(code,name,level='city'):
        if code not in regions:regions[code]=insert('regions',dict(code=code,name=name,level=level))
        return regions[code]
    gochang=region('52790','전북특별자치도 고창군','county')
    yangsan=region('48330','경상남도 양산시')
    sources=[
      ('고창 빈집현황','https://www.data.go.kr/data/15151879/fileData.do','2025-11-10','원본 1288행 중 빈집판정결과 해당 736행 적재'),
      ('양산 빈집현황','https://www.data.go.kr/data/15144630/fileData.do','2026-09-08','원본 160행'),
      ('양산 상권 샘플','https://www.data.go.kr/data/15012005/openapi.do','2026-06','양산 5건, 전체 상권 아님'),
      ('건축물대장 표제부 샘플','https://www.data.go.kr/data/15134735/openapi.do',None,'양산 남부동 조회 첫 5건. 빈집과 미연결'),
      ('키스콘 등록공시 샘플','https://www.data.go.kr/data/15061362/openapi.do','2025-01-01 ~ 2025-12-31','양산 등록공시 첫 5건. 현재 영업 업체 전체 아님'),
      ('지역별 방문자수 샘플','https://www.data.go.kr/data/15101972/openapi.do','2025-01-01','첫 5건. 고창 및 양산 자료 아님'),
    ]
    for name,url,period,note in sources:insert('data_sources',dict(name=name,source_url=url,reference_period=period,coverage_note=note))
    with next(ROOT.glob('전북*.csv')).open(encoding='utf-8-sig',newline='') as stream:
        for n,r in enumerate(csv.DictReader(stream),1):
            rid=raw(1,n,r)
            if r['빈집판정결과'].strip()!='해당':continue
            insert('vacant_houses',dict(raw_record_id=rid,region_id=gochang,source_row_key=str(n),address_public=r['소재지(바뀐후)'],locality_name=clean(r['법정동']),house_type=clean(r['주택유형']),grade=grade(r['등급판정결과']),structure=clean(r['건축물대장 주구조']),built_year=integer(r['건축년도']),total_floor_area_m2=number(r['연면적']),building_area_m2=number(r['건축면적']),land_area_m2=number(r['대지면적']),land_use_zone=clean(r['용도지역']),road_access=clean(r['도로접면']),determination_date=date(r['빈집판정일자']),grade_date=date(r['등급산정일자']),data_reference_period='2025-11-10'))
    with next(ROOT.glob('경상*.csv')).open(encoding='cp949',newline='') as stream:
        for n,r in enumerate(csv.DictReader(stream),1):
            insert('vacant_houses',dict(raw_record_id=raw(2,n,r),region_id=yangsan,source_row_key=str(n),address_public=r['소재지'],grade=grade(r['빈집등급']),structure=clean(r['건축물구조']),total_floor_area_m2=number(r['연면적']),data_reference_period=clean(r['데이터기준일']),contact_agency=clean(r['관리기관명']),contact_phone=clean(r['관리기관전화번호'])))
    p=json.loads((ROOT/'data/commercial_yangsan_sample.json').read_text(encoding='utf-8'))
    for r in p['body']['items']:
        insert('commercial_stores',dict(raw_record_id=raw(3,r['bizesId'],r),source_store_id=str(r['bizesId']),region_id=yangsan,name=r['bizesNm'],branch_name=clean(r.get('brchNm')),industry_large_code=r['indsLclsCd'],industry_large_name=r['indsLclsNm'],industry_medium_code=r['indsMclsCd'],industry_medium_name=r['indsMclsNm'],industry_small_code=r['indsSclsCd'],industry_small_name=r['indsSclsNm'],road_address=clean(r['rdnmAdr']),parcel_address=clean(r['lnoAdr']),building_management_no=clean(r.get('bldMngNo')),latitude=number(r['lat']),longitude=number(r['lon']),reference_month=str(p['header']['stdrYm'])))
    for r in json.loads((ROOT/'data/api_samples/building_items.json').read_text(encoding='utf-8')):
        approval=clean(r.get('useAprDay'))
        insert('building_registers',dict(raw_record_id=raw(4,r['mgmBldrgstPk'],r),registry_pk=str(r['mgmBldrgstPk']),region_id=yangsan,legal_dong_code=clean(r['bjdongCd']),parcel_main=clean(r['bun']),parcel_sub=clean(r['ji']),address_public=clean(r['platPlc']),structure=clean(r['strctCdNm']),main_use=clean(r['mainPurpsCdNm']),total_floor_area_m2=number(r['totArea']),land_area_m2=number(r['platArea']),floors_above=integer(r['grndFlrCnt']),floors_below=integer(r['ugrndFlrCnt']),approval_date_raw=approval,approval_date=date(approval),approval_year=int(approval[:4]) if approval and re.match(r'^\d{4}',approval) else None))
    for r in json.loads((ROOT/'data/api_samples/kiscon_items.json').read_text(encoding='utf-8')):
        insert('construction_notices',dict(raw_record_id=raw(5,r['ncrGsSeq'],r),source_notice_id=str(r['ncrGsSeq']),region_id=yangsan,company_name=r['ncrGsKname'],business_registration_no=clean(r.get('ncrMasterNum')),representative_name=clean(r.get('ncrGsMaster')),address=clean(r['ncrGsAddr']),phone=clean(r['ncrOffTel']),industry_name=clean(r['ncrItemName']),industry_registration_no=clean(r['ncrItemregno']),notice_number=clean(r['ncrGsNumber']),notice_type=clean(r['ncrGsFlag']),registration_date=date(r['ncrGsDate']),notice_date=date(r['ncrGsRegdate']),change_reason=clean(r['ncrGsReason'])))
    vp=ROOT/'data/api_samples/visitors_items.json'
    if not vp.exists():vp=Path('C:/works/projects/빈집 프로젝트/data/api_samples/visitors_items.json')
    for n,r in enumerate(json.loads(vp.read_text(encoding='utf-8')),1):
        insert('regional_visitor_stats',dict(raw_record_id=raw(6,n,r),region_id=region(r['signguCode'],r['signguNm'],'district'),base_date=date(r['baseYmd']),visitor_type_code=r['touDivCd'],visitor_type_name=r['touDivNm'],visitor_count=number(r['touNum']),weekday_code=r['daywkDivCd'],weekday_name=r['daywkDivNm']))
    for name in ['카페','숙박','음식점','공방','사무실','기타']:insert('business_types',dict(name=name))
    conn.commit()
    counts={r[0]:conn.execute(f'SELECT COUNT(*) FROM {r[0]}').fetchone()[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert counts['vacant_houses']==896
    assert counts['raw_records']==1468
    assert conn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not conn.execute('PRAGMA foreign_key_check').fetchall()
    assert conn.execute('SELECT COUNT(*) FROM house_building_links').fetchone()[0]==0
    # Prove user constraints reject duplicates, invalid ratings and orphan links.
    conn.execute('SAVEPOINT validation')
    u=insert('users',dict(email='test@example.invalid',password_hash='test-only',display_name='검증용'))
    insert('saved_houses',dict(user_id=u,house_id=1,rating=5))
    for row in [dict(user_id=u,house_id=1),dict(user_id=u,house_id=2,rating=6),dict(user_id=u,house_id=999999)]:
        try:insert('saved_houses',row)
        except sqlite3.IntegrityError:pass
        else:raise AssertionError('Constraint did not reject invalid data')
    conn.execute('ROLLBACK TO validation');conn.execute('RELEASE validation')
    (OUT/'schema.sql').write_text(SCHEMA,encoding='utf-8')
    (OUT/'seeded_database.sql').write_text('\n'.join(conn.iterdump()),encoding='utf-8')
    report=dict(tables=counts,integrity='ok',foreign_keys='ok',constraint_tests='passed',house_building_links=0)
    (OUT/'검증결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    columns=[]
    for table in counts:
        for _,name,typ,notnull,default,pk in conn.execute(f'PRAGMA table_info({table})'):
            columns.append([table,name,typ,'PK' if pk else '',bool(notnull),default])
    with (OUT/'테이블정의서.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['테이블','컬럼','자료형','기본키','NOT NULL','기본값']);writer.writerows(columns)
    conn.close()
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
