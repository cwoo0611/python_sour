from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from db import get_connFunc

app = Flask(__name__);

@app.get("/")
def index():
    return render_template("index.html")

# 전체 자료 읽기
@app.get("/api/sangdata")
def list_sangdata():
    sql = "select code,sang,su,dan from sangdata order by code asc"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return jsonify({"ok":True, "datas":rows})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);