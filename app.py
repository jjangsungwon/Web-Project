from flask import Flask, session, redirect, url_for, escape, request, render_template
import requests
from bs4 import BeautifulSoup
from crawling import dbModule


app = Flask(__name__)

usr_id =''

@app.route('/')
def index():
    if 'user.usr_id' in session:
        return render_template(
            "index.html",
            usr_id = 'user.usr_id'
        )
    else:    
        return render_template(
            "index.html",
            usr_id = "로그인이 필요합니다"
        )

# 학업 정보는 로그인 세션이 존재해야만 들어갈 수 있게 한다.


@app.route('/acainfo')
def acainfos():
    if 'user.usr_id' in session:
        return render_template("acainfo.html")

    else:
        return render_template("login.html")


@app.route('/mealmenu')
def mealmenus():
    return render_template("mealmenu.html")    


@app.route('/sitelink')
def sitelinks():
    return render_template("sitelink.html")        


@app.route('/notice', methods=['GET'])
def notices():
    db_class = dbModule.Database()

    sql = "Select Title, link from testdb.knu_main order by idx LIMIT 10;"
    row = db_class.executeAll(sql)

    sql2 = "Select Title, link from testdb.department order by idx LIMIT 10;"
    row2 = db_class.executeAll(sql2)

    return render_template(
        "notice.html",
        news_title=[[title['Title'], title['link']] for title in row],
        news_title2=[[title['Title'], title['link']] for title in row2]
        )       


@app.route('/schoolmap')
def schoolmaps():
    return render_template("schoolmap.html")           


@app.route('/login')
def logins():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)

