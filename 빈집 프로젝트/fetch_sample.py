"""Run in the myproject Python environment. Secrets are never printed."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlencode, unquote
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parent

def main():
    secrets = {}
    for line in (ROOT / '.env.local').read_text(encoding='utf-8-sig').splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            name, value = line.split('=', 1)
            secrets[name.strip()] = value.strip().strip('\"\'')
    key = secrets.get('COMMERCIAL_API_KEY', '')
    if not key:
        print('COMMERCIAL_API_KEY is missing.')
        return 1
    params = dict(serviceKey=unquote(key), divId='signguCd', key='48330',
                  pageNo=1, numOfRows=5, type='json')
    endpoint = 'https://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong'
    try:
        with urlopen(endpoint + '?' + urlencode(params), timeout=30) as response:
            raw = response.read().decode('utf-8-sig')
    except HTTPError as error:
        print('HTTP status:', error.code)
        raw = error.read().decode('utf-8', errors='replace')
    except (URLError, TimeoutError):
        print('NETWORK_ERROR: Could not connect to the public API.')
        return 2
    for value in secrets.values():
        if value:
            raw = raw.replace(value, '[REDACTED]').replace(unquote(value), '[REDACTED]')
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print('API response:', re.sub(r'<[^>]+>', ' ', raw)[:1000])
        return 1
    output = ROOT / 'data' / 'commercial_yangsan_sample.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Python environment:', sys.prefix)
    print('Response header:', json.dumps(payload.get('header', {}), ensure_ascii=False))
    body = payload.get('body', {})
    items = body.get('items', [])
    if isinstance(items, dict):
        items = items.get('item', [])
    if isinstance(items, dict):
        items = [items]
    print('Sample count:', len(items))
    for item in items:
        print(json.dumps({k: item.get(k) for k in ['bizesNm', 'indsSclsNm', 'rdnmAdr', 'lon', 'lat']}, ensure_ascii=False))
    print('Saved:', output)
    return 0 if items else 1

if __name__ == '__main__':
    raise SystemExit(main())
