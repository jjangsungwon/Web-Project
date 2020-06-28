from flask import Flask, session, redirect, url_for, escape, request, render_template
import requests
from bs4 import BeautifulSoup
from crawling import dbModule

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

####### 학업 데이터 크롤링 코드 ##########
LOGIN_URL = 'https://abeek.knu.ac.kr/Keess/comm/support/login/login.action'
craw_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/list.action'
design_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/designPart.action'
must_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/essentPart.action'

##########################################
usr_id =''

# 각 페이지 라우팅 코드
@app.route('/')
def index():
    if 'user.usr_id' in session:
        return render_template(
            "index.html",
            usr_id = session['user.usr_id']
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

@app.route('/loginProcess', methods=['POST','GET'])
def loginProcess():
    if request.method == 'POST':
        result = request.form
        input_usr_id = result['inputID']
        input_usr_pw = result['inputPW']

        # 인풋받은 ID, PW의 유효성 검증
        params = dict()
        params['user.usr_id'] = input_usr_id  # abeek 아이디
        params['user.passwd'] = input_usr_pw  # 비밀번호

        with requests.Session() as s:
            login_req = s.post(LOGIN_URL, data=params)
            post_one = s.get(craw_url)
            soup = BeautifulSoup(post_one.text, 'html.parser')
            data = soup.find_all('tr')  # remove 4번하면 첫 번째 부터 나옴.
            if len(data) != 0:
                session['user.usr_id'] = input_usr_id  

                for i in range(4):
                    data.remove(data[0])
                grade_array = []
                for tmp in data:
                    grade_array.append(tmp.text.split())
                for i in range(len(grade_array)):
                    print(grade_array[i])    
        
    if 'user.usr_id' in session:
        return redirect('/')
    
    return render_template(
            "login.html",
            login_error = "error"
    )   

@app.route('/login')
def logins():
    return render_template("login.html")   

@app.route('/logout')
def logouts():
    session.pop('user.usr_id', None)
    return redirect('/')           

if __name__ == '__main__':
    app.run(debug=True)

