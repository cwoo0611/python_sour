from flask import Flask, render_template, request, redirect, jsonify
from db import get_connFunc

app = Flask(__name__);

@app.get("/")
def index():
    return render_template("index.html")

#전체직원 조회
@app.get("/acorn/jikwon")
def jikwon_list():
    sql = """
        select jikwonno,jikwonname,busername,jikwonjik,jikwonpay,
        year(jikwonibsail) as ibsayear
        from jikwon
        inner join buser on jikwon.busernum=buser.buserno
        order by jikwonno
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return jsonify({"ok":True, "data":rows})

#직원 한명 조회
@app.get("/acorn/jikwon/<int:no>")
def jikwon_one(no):
    sql = """
        select jikwonno,jikwonname,busername,jikwonjik,jikwonpay,
        year(jikwonibsail) as ibsayear
        from jikwon
        inner join buser on jikwon.busernum=buser.buserno
        where jikwonno=%s
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (no,))
            row = cur.fetchone()

    return jsonify({"ok":True, "data":row})

#부서 전체 조회
@app.get("/acorn/buser")
def Buser_list():
    sql = """
        select * from buser order by buserno
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return jsonify({"ok":True, "data":rows})

#특정 부서 조회
@app.get("/acorn/buser/<int:no>")
def Buser_one(no):
    sql = """
        select jikwonno,jikwonname,jikwonjik,jikwonpay,year(jikwonibsail) as ibsayear
        from jikwon
        where busernum=%s
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (no, ))
            row = cur.fetchall()

    return jsonify({"ok":True, "data":row})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);