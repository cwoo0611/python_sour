"""Split the five-table prototype into seven tables, preserving existing data."""
import csv,json,shutil,sqlite3,sys
from pathlib import Path
from datetime import datetime
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
OUT=ROOT/'database';DB=OUT/'빈집프로젝트.sqlite3'
SCHEMA='''PRAGMA foreign_keys=ON;
CREATE TABLE regions(id INTEGER PRIMARY KEY,name TEXT NOT NULL UNIQUE);
CREATE TABLE vacant_houses(
 id INTEGER PRIMARY KEY,region_id INTEGER NOT NULL REFERENCES regions(id),
 address_public TEXT NOT NULL,grade INTEGER CHECK(grade BETWEEN 1 AND 3),
 structure TEXT,total_floor_area_m2 NUMERIC CHECK(total_floor_area_m2>=0),data_reference_period TEXT,
 source_file TEXT NOT NULL,source_row_number INTEGER NOT NULL,UNIQUE(source_file,source_row_number));
CREATE TABLE gochang_house_details(
 house_id INTEGER PRIMARY KEY REFERENCES vacant_houses(id) ON DELETE CASCADE,
 house_type TEXT,built_year INTEGER,land_area_m2 NUMERIC CHECK(land_area_m2>=0),
 land_use_zone TEXT,road_access TEXT);
CREATE TABLE yangsan_house_details(
 house_id INTEGER PRIMARY KEY REFERENCES vacant_houses(id) ON DELETE CASCADE,
 contact_agency TEXT,contact_phone TEXT);
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
'''
NAMES={'regions':'지역','vacant_houses':'빈집 공통','gochang_house_details':'고창 빈집 상세','yangsan_house_details':'양산 빈집 상세','users':'회원','saved_houses':'관심 빈집','saved_house_business_types':'희망 업종'}
FIELDS={'id':'번호','name':'지역 이름','region_id':'지역 번호','address_public':'공개 주소','house_type':'주택 유형','grade':'등급','structure':'구조','built_year':'준공 연도','total_floor_area_m2':'연면적','land_area_m2':'대지면적','land_use_zone':'용도지역','road_access':'도로접면','contact_agency':'문의 기관','contact_phone':'문의 전화','data_reference_period':'자료 기준 시점','source_file':'원본 파일','source_row_number':'원본 데이터 행 번호','email':'이메일','password_hash':'비밀번호 해시','display_name':'이름','created_at':'생성 시각','updated_at':'수정 시각','user_id':'회원 번호','house_id':'빈집 번호','memo':'메모','rating':'별점','saved_house_id':'관심 저장 번호','business_type':'희망 업종'}
def main():
 old=sqlite3.connect(DB);old.row_factory=sqlite3.Row
 if old.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='buildings'").fetchone():raise SystemExit('Current database includes buildings. Historical migration is disabled.')
 if {r[0] for r in old.execute("SELECT name FROM sqlite_master WHERE type='table'")}==set(NAMES):raise SystemExit('Already split into seven tables.')
 records={t:[dict(r) for r in old.execute('SELECT * FROM '+t)] for t in ['vacant_houses','users','saved_houses']}
 regions=[dict(r) for r in old.execute('SELECT id,name FROM regions WHERE id IN(SELECT region_id FROM vacant_houses)')]
 choices=[dict(r) for r in old.execute('SELECT * FROM saved_house_business_types')]
 backup=ROOT/'backups'/('before_regional_split_'+datetime.now().strftime('%Y%m%d_%H%M%S'));backup.mkdir(parents=True)
 with sqlite3.connect(backup/DB.name) as b:old.backup(b)
 for p in OUT.iterdir():
  if p.is_file() and p.name!=DB.name:shutil.copy2(p,backup/p.name)
 old.close()
 temp=OUT/'simplified_build.sqlite3'
 if temp.exists():raise RuntimeError('Temporary database exists')
 c=sqlite3.connect(temp);c.executescript(SCHEMA)
 def insert(t,r):c.execute(f"INSERT INTO {t} ({','.join(r)}) VALUES ({','.join('?' for _ in r)})",list(r.values()))
 for r in regions:insert('regions',r)
 cols=[r[1] for r in c.execute('PRAGMA table_info(vacant_houses)')]
 for h in records['vacant_houses']:
  insert('vacant_houses',{k:h[k] for k in cols})
  if h['source_file'].startswith('전북'):
   insert('gochang_house_details',dict(house_id=h['id'],**{k:h[k] for k in ['house_type','built_year','land_area_m2','land_use_zone','road_access']}))
  elif h['source_file'].startswith('경상'):
   insert('yangsan_house_details',dict(house_id=h['id'],**{k:h[k] for k in ['contact_agency','contact_phone']}))
  else:raise AssertionError('Unknown source region')
 for t in ['users','saved_houses']:
  for r in records[t]:insert(t,r)
 for r in choices:insert('saved_house_business_types',r)
 c.commit()
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert not c.execute('PRAGMA foreign_key_check').fetchall()
 assert c.execute('SELECT COUNT(*) FROM vacant_houses').fetchone()[0]==896
 assert c.execute('SELECT COUNT(*) FROM gochang_house_details').fetchone()[0]==736
 assert c.execute('SELECT COUNT(*) FROM yangsan_house_details').fetchone()[0]==160
 assert c.execute('SELECT COUNT(*) FROM gochang_house_details g JOIN yangsan_house_details y ON g.house_id=y.house_id').fetchone()[0]==0
 # Reconstruct every old house and compare each field to the previous database.
 c.row_factory=sqlite3.Row
 rebuilt=[dict(r) for r in c.execute('SELECT h.*,g.house_type,g.built_year,g.land_area_m2,g.land_use_zone,g.road_access,y.contact_agency,y.contact_phone FROM vacant_houses h LEFT JOIN gochang_house_details g ON g.house_id=h.id LEFT JOIN yangsan_house_details y ON y.house_id=h.id ORDER BY h.id')]
 assert rebuilt==sorted(records['vacant_houses'],key=lambda r:r['id'])
 c.row_factory=None
 c.execute('SAVEPOINT validation')
 uid=c.execute("INSERT INTO users(email,password_hash,display_name) VALUES('test@example.invalid','test','검증')").lastrowid
 sid=c.execute('INSERT INTO saved_houses(user_id,house_id,rating) VALUES(?,?,5)',(uid,1)).lastrowid
 c.execute('INSERT INTO saved_house_business_types VALUES(?,?)',(sid,'카페'))
 for sql,args in [('INSERT INTO gochang_house_details(house_id) VALUES(?)',(1,)),('INSERT INTO gochang_house_details(house_id) VALUES(?)',(999999,)),('INSERT INTO saved_houses(user_id,house_id) VALUES(?,?)',(uid,1)),('INSERT INTO saved_houses(user_id,house_id,rating) VALUES(?,?,6)',(uid,2)),('INSERT INTO saved_houses(user_id,house_id) VALUES(?,?)',(uid,999999)),('INSERT INTO saved_house_business_types VALUES(?,?)',(sid,'없는업종')),('INSERT INTO saved_house_business_types VALUES(?,?)',(sid,'카페'))]:
  try:c.execute(sql,args)
  except sqlite3.IntegrityError:pass
  else:raise AssertionError('Invalid input accepted')
 c.execute('DELETE FROM users WHERE id=?',(uid,))
 assert not c.execute('SELECT 1 FROM saved_houses WHERE id=?',(sid,)).fetchone()
 assert not c.execute('SELECT 1 FROM saved_house_business_types WHERE saved_house_id=?',(sid,)).fetchone()
 c.execute('DELETE FROM vacant_houses WHERE id=2')
 assert not c.execute('SELECT 1 FROM gochang_house_details WHERE house_id=2').fetchone()
 c.execute('ROLLBACK TO validation');c.execute('RELEASE validation')
 counts={t:c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in NAMES}
 dump='\n'.join(c.iterdump())
 restored=sqlite3.connect(':memory:');restored.executescript(dump)
 assert restored.execute('SELECT COUNT(*) FROM vacant_houses').fetchone()[0]==896
 assert restored.execute('SELECT COUNT(*) FROM gochang_house_details').fetchone()[0]==736
 assert restored.execute('SELECT COUNT(*) FROM yangsan_house_details').fetchone()[0]==160
 assert not restored.execute('PRAGMA foreign_key_check').fetchall();restored.close()
 definitions=[];erd=['# 지역별 상세를 분리한 7개 테이블 ERD','','```mermaid','erDiagram',' regions ||--o{ vacant_houses : "지역의 빈집"',' vacant_houses ||--o| gochang_house_details : "고창이면 상세 1행"',' vacant_houses ||--o| yangsan_house_details : "양산이면 상세 1행"',' users ||--o{ saved_houses : "회원이 저장"',' vacant_houses ||--o{ saved_houses : "저장 대상"',' saved_houses ||--o{ saved_house_business_types : "희망 업종"']
 for t in NAMES:
  erd.append(' '+t+' {')
  fks={r[3]:r[2]+'.'+r[4] for r in c.execute('PRAGMA foreign_key_list('+t+')')}
  for _,name,typ,required,default,pk in c.execute('PRAGMA table_info('+t+')'):
   flags=','.join(x for x in ['PK' if pk else '', 'FK' if name in fks else ''] if x)
   erd.append(f'  {typ} {name} {flags} "{FIELDS[name]}"')
   definitions.append([t,NAMES[t],name,FIELDS[name],typ,flags,fks.get(name,''),'필수' if required or pk else '선택',default])
  erd.append(' }')
 erd+=['```','','PK는 행 번호를 식별하는 기본키, FK는 다른 테이블 번호를 참조하는 외래키입니다.','한 회원은 여러 빈집을 저장할 수 있고, 같은 빈집도 여러 회원이 저장할 수 있습니다.','관심 항목에 카페와 공방을 선택하면 희망 업종 테이블에는 두 행이 생깁니다.','중복 금지: regions.name, users.email, saved_houses(user_id,house_id), vacant_houses(source_file,source_row_number).']
 report=dict(tables=counts,integrity='ok',foreign_keys='ok',constraint_tests='passed',cascade_delete='passed',sql_restore='passed',all_house_values_preserved=True,regional_details_disjoint=True,backup=str(backup))
 c.close();temp.replace(DB)
 for name,text in [('schema.sql',SCHEMA),('seeded_database.sql',dump),('ERD.md','\n'.join(erd)),('검증결과.json',json.dumps(report,ensure_ascii=False,indent=2))]:
  (OUT/name).write_text(text,encoding='utf-8')
 with (OUT/'테이블정의서.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['테이블','뜻','컬럼','한글 설명','자료형','키','참조','필수 여부','기본값']);w.writerows(definitions)
 shutil.copy2(ROOT/'tmp/simple_db_guide.md',OUT/'DB_설계_가이드.md')
 shutil.copy2(ROOT/'tmp/simple_queries.sql',OUT/'조회예제.sql')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
