# 정리 노트

pro4~pro8 학습 내용을 토대로 질문에 답하고, 답을 이 파일에 누적해서 적는다.

## 학습 요약 (pro4~pro8)

### pro4 — Jinja2 템플릿 (`fpro4`)
- `base.html`에 `{% block title %}`, `{% block content %}` 정의 → 자식은 `{% extends "base.html" %}`로 상속(공통 header/footer).
- 조건: `{% if score >= 90 %} ... {% elif %} ... {% else %} ... {% endif %}`
- 반복: `{% for user in users %}` ... `{{ loop.index }}`(1부터), `{{ users | length }}`
- 필터: `upper`, `capitalize`, `title`, `length`. 천단위 콤마는 기본 없음 → `@app.template_filter('format')`로 직접 등록, `format(value, ",")`.
- `render_template("x.html", 변수=값)`으로 데이터 전달, `{{ 변수 }}`로 출력.

### pro5 — GET / POST (`fpro5getpost`)
- GET: URL 뒤 query string(`?username=..&age=23`), 서버에서 `request.args.get("username")`. 값은 항상 문자열(`age + "살"`).
- GET 전송 방법: `<a href="/get_result?username=손오공&age=23">` 또는 `<form method="get">`.
- POST: `@app.route("/post_result", methods=['POST'])`, `request.form.get("username")`.
- POST 폼은 `type="button"` + JS `form.requestSubmit()`으로 submit 이벤트를 발생시켜 검증(이름 비어있음/이메일에 `@` 없음 → `alert` + `event.preventDefault()`).

### pro6 — 쿠키 기초 (`fpro6cookie`)
- `@app.get` / `@app.post`로 메서드 제한. `render_template_string`은 문자열 템플릿 렌더링.
- 쿠키 저장: `resp = make_response(redirect(url_for("read_cookie")))` → `resp.set_cookie(key, value, max_age=60*5, httponly=True, samesite="Lax")` → `return resp`.
- 읽기: `request.cookies.get("name")` (없으면 None). 삭제: `resp.delete_cookie("name")`.
- `redirect`: 302 이동, `url_for("함수명")`: 함수 이름으로 URL 생성.
- `httponly=True`: JS `document.cookie` 접근 차단, `samesite="Lax"`: CSRF 완화.

### pro7 — 쿠키로 로그인 + 방문 횟수 (`fpro7cookie`)
- `COOKIE_AGE = 60*60*24*7` (7일). `/login` GET(화면·방문수 증가) / POST(쿠키 `name`, `visits=0` 저장 후 redirect) / `/logout` POST(쿠키 2개 삭제).
- `visits = int(visits or "0") + 1` 후 `set_cookie("visits", str(visits), ...)`로 갱신.
- 템플릿에서 `{% if not name %}` 로그인 폼 / `{% else %}` 로그아웃 폼.

### pro8 — 세션 (`fpro8session`)
- 세션 = 서버 측 사용자 상태 유지(쿠키로 운영, 쿠키보다 안전). `session` 사용에는 `app.secret_key` 필수(위조 방지).
- 키 생성: `python -c "import secrets; print(secrets.token_hex(32))"`.
- 만료: `app.permanent_session_lifetime = timedelta(seconds=5)` + `session.permanent = True`.
- 저장 `session["f_os"] = 값`, 확인 `"f_os" in session`, 읽기 `session["f_os"]`.
- 흐름: `/setos?favorite_os=..` → 세션 저장 → `redirect(url_for("showos"))` → 결과 표시(만료 후 새로고침하면 사라짐).

---

## 질문 & 답변 기록

### Q. html에서 굵게 나오는 건?
- `<b>굵게</b>` 또는 `<strong>굵게(중요)</strong>` (strong은 "중요한 내용"이라는 의미까지 있음)
- 예(pro7 login.html): `<p><b>{{ msg }}</b></p>`
- 제목 태그 `<h2>`, `<h3>`도 기본적으로 굵게 표시됨
- CSS: `style="font-weight: bold;"` (pro4·pro8에서 `style="color: blue;"`처럼 인라인 스타일 사용)

### Q. 달력 만들어줘 (html 코드)
pro4~8 내용만 사용: Flask + Jinja2(상속·if·for·loop.index), `request.args`(pro5), `timedelta`(pro8).

**app.py**
```python
from flask import Flask, render_template, request
from datetime import date, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    today = date.today()
    year = int(request.args.get("year", today.year))    # get방식 값은 문자열이라 int로 변환
    month = int(request.args.get("month", today.month))

    # 이전/다음 달 링크에서 0월, 13월이 넘어오면 연도 보정
    if month < 1:
        month = 12
        year -= 1
    if month > 12:
        month = 1
        year += 1

    first = date(year, month, 1)
    start = (first.weekday() + 1) % 7   # 일요일=0 이 되도록 맞춤 (weekday: 월=0 ~ 일=6)

    if month == 12:
        next_first = date(year + 1, 1, 1)
    else:
        next_first = date(year, month + 1, 1)
    last = (next_first - timedelta(days=1)).day   # 다음 달 1일 - 1일 = 이번 달 마지막 날

    days = [""] * start + list(range(1, last + 1))   # 앞쪽 빈칸 + 날짜
    while len(days) % 7 != 0:
        days.append("")                              # 뒤쪽 빈칸
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]   # 7개씩 잘라 주(week) 목록 만들기

    return render_template("calendar.html", year=year, month=month, weeks=weeks, today=today)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**templates/base.html** (pro4와 같은 상속 구조)
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}기본 제목{% endblock %}</title>
</head>
<body>
    {% block content %}
        본문내용
    {% endblock %}
</body>
</html>
```

**templates/calendar.html**
```html
{% extends "base.html" %} <!--상속-->

{% block title %}달력{% endblock %}

{% block content %}
<h2>
    <a href="/?year={{year}}&month={{month-1}}">◀</a>
    {{year}}년 {{month}}월
    <a href="/?year={{year}}&month={{month+1}}">▶</a>
</h2>

<table border="1" style="border-collapse: collapse; text-align: center;">
    <tr>
        <th style="width:50px; color:red;">일</th>
        <th style="width:50px;">월</th>
        <th style="width:50px;">화</th>
        <th style="width:50px;">수</th>
        <th style="width:50px;">목</th>
        <th style="width:50px;">금</th>
        <th style="width:50px; color:blue;">토</th>
    </tr>
    {% for week in weeks %}
    <tr>
        {% for day in week %}
        <td style="height:40px;">
            {% if day == "" %}
                &nbsp;
            {% elif day == today.day and month == today.month and year == today.year %}
                <b style="background: yellow;">{{day}}</b>
            {% elif loop.index == 1 %}
                <span style="color: red;">{{day}}</span>
            {% elif loop.index == 7 %}
                <span style="color: blue;">{{day}}</span>
            {% else %}
                {{day}}
            {% endif %}
        </td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
{% endblock %}
```
- pro4: `{% extends %}` 상속, `{% for %}`, `{% if/elif/else %}`, `loop.index`(1이면 일요일 빨강, 7이면 토요일 파랑)
- pro5: `request.args.get()`으로 연·월 받기(문자열이라 `int()` 변환), `<a href="/?year=..&month=..">` get 링크로 ◀ ▶ 이동
- pro8: `datetime`/`timedelta`로 날짜 계산(다음 달 1일 - 1일 = 마지막 날)
- 실행: `python app.py` 후 `http://127.0.0.1:5000/`
