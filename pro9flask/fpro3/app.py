# Flask app의 Entry FloatingPointError
# 라우팅, 서버 실행 담당

# jinja2:flask에서 html을 동적으로 랜더링 할떄 사용하는 템플릿 엔젠.
# 웹 서버에서 html 문을 완성한후 클라이언트 전송.
# html 안에 파이썬 변수를 넣고, 반복/조건문 등을 사용할 수있게 해주는 도구

# render_template : html 템플릿 파일(jinja2 템플릿)을 읽어 필요한 값을
# 채운후 완성 된 html을 응답으로 반환해 주는 함수
from flask import Flask,render_template

app = Flask(__name__);

@app.route("/")
def home():
    return render_template("home.html");

@app.route("/hello")
def hello():
    name = "길동이";
    addr = "서초구 서초2동 123";
    return render_template("hello.html", name=name, juso=addr);

@app.route("/world")
def world_image():
    return render_template("my.html");


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);