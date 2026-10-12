"""Add verified VWorld samples and optional house/building links to the prototype."""
import csv
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
OUT = ROOT / 'database'
DB = OUT / '빈집프로젝트.sqlite3'
SQL = '''
CREATE TABLE IF NOT EXISTS buildings (
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
CREATE INDEX IF NOT EXISTS idx_buildings_register ON buildings(building_register_id);
CREATE INDEX IF NOT EXISTS idx_buildings_parcel ON buildings(parcel_code);
CREATE TABLE IF NOT EXISTS house_building_links (
 house_id INTEGER NOT NULL REFERENCES vacant_houses(id) ON DELETE CASCADE,
 building_id INTEGER NOT NULL REFERENCES buildings(id),
 evidence TEXT NOT NULL CHECK(length(trim(evidence))>0),
 verified_at TEXT NOT NULL,
 PRIMARY KEY(house_id,building_id)
);
'''
labels = {'id':'번호','region_id':'지역 번호','source_ufid':'브이월드 건물 식별번호','parcel_code':'필지번호 PNU','building_register_id':'건축물대장 식별번호','ground_floors':'지상 층수','underground_floors':'지하 층수','building_area_m2':'건축면적 제곱미터','total_floor_area_m2':'연면적 제곱미터','approval_date_raw':'사용승인일 원본','geometry_geojson':'건물 윤곽 좌표 EPSG4326 GeoJSON','fetched_at':'수집 시각 UTC','house_id':'빈집 번호','building_id':'건물 번호','evidence':'연결 확인 근거','verified_at':'연결 확인 시각'}

def main():
    c=sqlite3.connect(DB)
    c.execute('PRAGMA foreign_keys=ON')
    existing=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    before={t:c.execute('SELECT * FROM '+t+' ORDER BY rowid').fetchall() for t in existing}
    backup=ROOT/'backups'/('before_buildings_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
    backup.mkdir(parents=True)
    with sqlite3.connect(backup/DB.name) as dest:c.backup(dest)
    for p in OUT.iterdir():
        if p.is_file() and p.name!=DB.name:shutil.copy2(p,backup/p.name)
    payload=json.loads((ROOT/'data/api_samples/vworld_response.txt').read_text(encoding='utf-8'))
    assert payload['crs']['properties']['name'].endswith('4326')
    c.executescript(SQL)
    rid=c.execute("SELECT id FROM regions WHERE name LIKE '%양산%'").fetchone()[0]
    now=datetime.now(timezone.utc).isoformat()
    for f in payload['features']:
        p=f['properties'];g=f['geometry']
        assert p['col_adm_se']=='48330' and g['type'] in ('Polygon','MultiPolygon')
        c.execute('''INSERT INTO buildings(region_id,source_ufid,parcel_code,building_register_id,ground_floors,underground_floors,building_area_m2,total_floor_area_m2,approval_date_raw,geometry_geojson,fetched_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(source_ufid) DO NOTHING''',
        (rid,p['ufid'],p.get('pnu'),p.get('bldrgst_pk'),p.get('grnd_flr'),p.get('ugrnd_flr'),p.get('archarea'),p.get('totalarea'),p.get('useapr_day'),json.dumps(g,separators=(',',':')),now))
    c.commit()
    for t,rows in before.items():assert rows==c.execute('SELECT * FROM '+t+' ORDER BY rowid').fetchall()
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not c.execute('PRAGMA foreign_key_check').fetchall()
    # Confirm foreign keys and nonempty evidence prevent unsupported links.
    c.execute('SAVEPOINT validation')
    rejected=0
    for args in [(999999,1,'test',now),(1,999999,'test',now),(1,1,'',now)]:
        try:c.execute('INSERT INTO house_building_links VALUES(?,?,?,?)',args)
        except sqlite3.IntegrityError:rejected+=1
    assert rejected==3
    c.execute('ROLLBACK TO validation');c.execute('RELEASE validation')
    tables=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    schema='PRAGMA foreign_keys=ON;\n'+';\n'.join(r[0] for r in c.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' ORDER BY type DESC,name"))+';\n'
    dump='\n'.join(c.iterdump())+'\n'
    restored=sqlite3.connect(':memory:');restored.executescript(dump)
    for t in tables:assert c.execute('SELECT * FROM '+t+' ORDER BY rowid').fetchall()==restored.execute('SELECT * FROM '+t+' ORDER BY rowid').fetchall()
    restored.execute('PRAGMA foreign_keys=ON');assert not restored.execute('PRAGMA foreign_key_check').fetchall()
    (OUT/'schema.sql').write_text(schema,encoding='utf-8-sig')
    (OUT/'seeded_database.sql').write_text(dump,encoding='utf-8-sig')
    erd=(OUT/'ERD.md').read_text(encoding='utf-8-sig')
    erd=erd.replace('지역별 상세를 분리한 7개 테이블 ERD','건물 위치 정보를 추가한 9개 테이블 ERD')
    if ' buildings {' not in erd:
        block=' regions ||--o{ buildings : "지역의 건물"\n vacant_houses ||--o{ house_building_links : "확인된 연결"\n buildings ||--o{ house_building_links : "연결된 건물"\n'
        for t in ['buildings','house_building_links']:
            block+=' '+t+' {\n'
            fks={r[3] for r in c.execute('PRAGMA foreign_key_list('+t+')')}
            for _,name,typ,nn,default,pk in c.execute('PRAGMA table_info('+t+')'):
                keys=','.join(k for k,yes in [('PK',pk),('FK',name in fks),('UK',name=='source_ufid')] if yes)
                block+=f'  {typ} {name} {keys} "{labels.get(name,name)}"\n'
            block+=' }\n'
        erd=erd.replace('\n```\n','\n'+block+'```\n',1)
        erd+='\nbuildings는 일반 건물 정보입니다. 빈집 여부를 뜻하지 않습니다. 현재 건물 5건, 확인된 빈집 연결 0건입니다. geometry_geojson은 건물 테두리 좌표이며 좌표계는 EPSG:4326, 순서는 경도·위도입니다.\n'
    (OUT/'ERD.md').write_text(erd,encoding='utf-8-sig')
    guide=(OUT/'DB_설계_가이드.md').read_text(encoding='utf-8-sig').replace('7개 테이블','9개 테이블')
    if '## 건물 좌표 추가' not in guide:
        guide+='''
## 건물 좌표 추가

기존 7개 테이블에 buildings와 house_building_links 두 개를 추가했습니다. 기존 빈집 896건과 지역 상세 값은 그대로 유지했습니다.

| 추가 테이블 | 저장 내용 | 현재 행 수 |
|---|---|---:|
| buildings | 브이월드에서 조회한 양산 일반 건물과 윤곽 좌표 | 5 |
| house_building_links | 실제로 확인된 빈집과 건물의 연결 | 0 |

buildings의 한 행은 건물 하나입니다. 원본 ufid→source_ufid, pnu→parcel_code, bldrgst_pk→building_register_id, grnd_flr→ground_floors, ugrnd_flr→underground_floors, archarea→building_area_m2, totalarea→total_floor_area_m2, useapr_day→approval_date_raw, geometry→geometry_geojson으로 가져왔습니다. id·region_id·fetched_at은 프로젝트에서 부여합니다. fetched_at은 수집 시각이며 자료 조사일이 아닙니다. 원본의 나머지 속성은 API 응답 파일에 보관합니다.

geometry_geojson은 테이블이 아니라 건물 테두리를 표현하는 좌표 묶음을 담은 TEXT 컬럼입니다. 좌표계는 EPSG:4326이고 [경도, 위도] 순서입니다. 지도 핀용 대표점은 아직 계산하지 않았습니다. 지도 라이브러리로 건물 윤곽을 그릴 수 있습니다. 이번 DB는 SQLite이며 본격 공간 검색에는 PostGIS 등 별도 공간 기능이 필요합니다.

house_building_links는 빈집 번호와 건물 번호를 연결합니다. 한 필지에 여러 동이 있을 수 있어 여러 건물 연결을 허용합니다. 연결할 때 evidence에 확인 근거, verified_at에 확인 시각을 기록합니다. 근거의 실제 타당성은 사람이 확인하거나 서버에서 검증해야 합니다. 외래키만으로 같은 지역·같은 실제 건물인지 검증하지는 못합니다.

현재 5건은 좌표 API 작동을 확인한 일반 건물 샘플입니다. 빈집임을 확인한 데이터가 아니므로 연결을 만들지 않았습니다. 주소가 가려진 빈집은 임의로 연결하지 않습니다. 건축물대장 식별번호나 정확한 주소·필지번호를 확보해 대조한 뒤 연결해야 합니다. 건축물대장 샘플 자체를 추가 적재하지는 않았습니다.

빈집과 건물 사이에는 LEFT JOIN을 사용하면 위치가 없는 빈집도 목록에 남습니다. 연결이 없는 현재 상태에서는 건물 값이 NULL로 조회되는 것이 정상입니다. 없는 좌표를 추정해서 채우지 않았습니다.

백업은 backups/before_buildings_... 폴더에 있습니다. add_building_database.py는 이번 변경과 샘플 적재를 수행하는 스크립트입니다. 기존 build_database.py는 과거 5→7개 테이블 변경용이므로 현재 DB에 실행하지 않습니다.
'''
    (OUT/'DB_설계_가이드.md').write_text(guide,encoding='utf-8-sig')
    query=(OUT/'조회예제.sql').read_text(encoding='utf-8-sig')
    if '-- 건물 좌표' not in query:
        query+='''
-- 건물 좌표: 일반 건물 샘플이며 빈집 확정 자료가 아닙니다.
SELECT id,parcel_code,building_register_id,ground_floors,total_floor_area_m2,geometry_geojson FROM buildings LIMIT 5;
-- 확인된 연결만 조회. 현재 연결 0건이므로 건물 컬럼은 NULL입니다.
SELECT h.id,h.address_public,b.id AS building_id,b.geometry_geojson
FROM vacant_houses h
LEFT JOIN house_building_links l ON l.house_id=h.id
LEFT JOIN buildings b ON b.id=l.building_id;
'''
    (OUT/'조회예제.sql').write_text(query,encoding='utf-8-sig')
    with (OUT/'테이블정의서.csv').open(encoding='utf-8-sig',newline='') as f:oldrows=list(csv.reader(f))
    # Preserve the previous dictionary layout and append fields with explicit metadata.
    newrows=[['테이블','컬럼','자료형','키','참조','필수','설명']]
    for t in tables:
        fks={r[3]:r[2]+'.'+r[4] for r in c.execute('PRAGMA foreign_key_list('+t+')')}
        for _,name,typ,nn,default,pk in c.execute('PRAGMA table_info('+t+')'):
            newrows.append([t,name,typ,','.join(k for k,yes in [('PK',pk),('FK',name in fks),('UK',name=='source_ufid')] if yes),fks.get(name,''),'예' if nn or pk else '아니오',labels.get(name,name)])
    # Read existing ERD labels for the original columns.
    import re
    for row in newrows[1:]:
        if row[0] in ('buildings','house_building_links'):continue
        match=re.search(r'\b'+re.escape(row[1])+r'\s+(?:[A-Z,]+\s+)?"([^"]+)"',erd)
        if match:row[-1]=match.group(1)
    with (OUT/'테이블정의서.csv').open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows(newrows)
    report={'table_counts':{t:c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in tables},'integrity_check':'ok','foreign_key_check':[],'all_existing_values_preserved':True,'dump_restore_verified':True,'invalid_links_rejected':rejected,'geometry_crs':'EPSG:4326','unverified_house_links_created':0,'backup':str(backup)}
    (OUT/'검증결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    c.close()
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
