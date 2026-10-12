from flask import Flask, render_template,render_template_string,request
from flask import request, make_response, redirect, url_for
#redirect: 브라우저를 다른 url로 이동시키는(302) 라다이렉트 응답 생성
#url_for: 라우트 함수 이름으로 utl을 안전하게 생성
#render_template_string : 문자열로 작성한 jinja 템플릿을 렌더링해 HTML로 반환하는 함수

app = Flask(__name__);

#간단 HTML :text로 작성
HOME_HTML="""
    <h2>Flask Cookie test</h2>
    <form action="/set_cookie" method="post">
    쿠키값 : <input type="text" name="name" placeholder="예:hong">
    <button type="submit">쿠키 저장</button>
    </form>
    <p>
        <a href="/read_cookie">쿠키 읽기</a>
        <a href="/delete_cookie">쿠키 삭제</a>
    </p>
    


"""

@app.get("/")    #get방식으로만 받기 route get,post 둘다
def home():
    return render_template_string(HOME_HTML)  #HOME_HTML을 HTML형식으로 반환

@app.post("/set_cookie") #post방식으로만 받기
def set_cookie():
    #쿠기 저장
    irum = request.form.get("name", "anomymous")

    #클라이언트에 쿠키를 심으려면 응답 객체가 필요 
    #먼저 "read_cookie 페이지로 이동하라"는 redirect 객체를 만들고
    #그 응답에 따라 쿠키를 추가한 뒤 브라우저에 돌려 줌
    # resp = make_response(redirect("/read_cookie")) #보통 클라이언트에서 요청하지만 이건 서버에서 요청해서 read_cookie로 바로 들어가지게 해준다
    resp = make_response(redirect(url_for("read_cookie"))) #위와 동일한 결과가 나온다 직접 요청하지 않고 함수를 직접 요청한다 url_for("함수명")


    resp.set_cookie( #브라우저에 쿠키 저장
        key="name", #쿠키이름
        value=irum, #사용자가 전송한 값을 쿠키에 저장한다
        max_age=60*5, #유효시간 - 5분뒤 만료.일반적으로 1년
        httponly=True, #js에서 document.cookie로 접근 불가
        samesite="Lax" #CSRF 공격 방지용
        
        )

    return resp #쿠키가 포함된 응답을 브라우저로 반환
        # 브라우저는 쿠키를 저장하고,redirect 요청에 따라 read_cookue로 다시 요청함


@app.get("/read_cookie") #첫번쨰 resp
def read_cookie():            #두번쨰 resp
    #브라우저가 요청에 실어 보낸 모든 쿠키 중에서 내 서버가 만든 쿠키(name)를 꺼냄
    #만약 없으면 Noine을 반환(첫방문/만료/삭제된 경우)

    name = request.cookies.get("name")

    #읽은 쿠키 HTML로 출력
    return f"""
        <h3>쿠키 읽기</h3>
        <p>value 쿠키 값: {name}</p> 
        """

@app.get("/delete_cookie")
def delete_cookie():
    #쿠키 삭제후 홈(/)으로 이동하기 위해 redirect 응답을 만듦
    resp = make_response(redirect(url_for("home")))
    resp.delete_cookie("name")
    return resp



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);
