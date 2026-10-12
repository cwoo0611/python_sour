"""Check VWorld building geometry; never log the authentication key."""
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parent
key = next(line.split('=', 1)[1].strip().strip('\"\'') for line in (ROOT / '.env.local').read_text(encoding='utf-8-sig').splitlines() if line.startswith('VWORLD_API_KEY='))
out = ROOT / 'data' / 'api_samples'
out.mkdir(parents=True, exist_ok=True)
params = dict(SERVICE='WFS', REQUEST='GetFeature', VERSION='1.1.0', TYPENAME='lt_c_bldginfo', BBOX='129.02,35.32,129.04,35.35', SRSNAME='EPSG:4326', MAXFEATURES='5', OUTPUT='application/json', KEY=key, DOMAIN='http://localhost:5000')
try:
    req = Request('https://api.vworld.kr/req/wfs?' + urlencode(params), headers={'Referer': 'http://localhost:5000/'})
    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read().decode('utf-8-sig', errors='replace')
            status = response.status
    except HTTPError as error:
        status = error.code
        raw = error.read().decode('utf-8-sig', errors='replace')
    raw = raw.replace(key, '[REDACTED]')
    (out / 'vworld_response.txt').write_text(raw, encoding='utf-8')
    try:
        data = json.loads(raw)
        features = data.get('features', [])
        report = dict(http_status=status, count=len(features), geometry_types=[f.get('geometry', {}).get('type') for f in features], property_fields=list(features[0].get('properties', {})) if features else [], response_summary=data if not features else None)
    except ValueError:
        report = dict(http_status=status, count=0, response_summary=raw[:2000])
    (out / 'vworld_status.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
except Exception as error:
    print(json.dumps({'status': 'NETWORK_ERROR', 'error_type': type(error).__name__, 'reason_type': type(getattr(error, 'reason', None)).__name__}))
    raise SystemExit(2)
