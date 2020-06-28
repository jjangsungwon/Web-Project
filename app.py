from flask import Flask, session, redirect, url_for, escape, request, render_template
import requests
from bs4 import BeautifulSoup
from crawling import dbModule

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

grade = []
design_count, required_count = 0, 0
final_grade=[]

####### 학업 데이터 크롤링 코드 ##########
LOGIN_URL = 'https://abeek.knu.ac.kr/Keess/comm/support/login/login.action'
craw_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/list.action'
design_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/designPart.action'
must_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/essentPart.action'

# 설계과목
design = {'COMP205': 2, 'COMP217': 2, 'ELEC462': 2, 'COMP224': 2, 'COMP225': 2, 'COMP422': 2, 'ITEC401': 4,
          'ITEC402': 4}

# 필수과목
required = {'CLTR211': 3, 'CLTR213': 3, 'CLTR223': 3, 'COME301': 3, 'COMP204': 3, 'COMP205': 3, 'COME331': 3,
            'COMP217': 3, 'COMP411': 3, 'ELEC462': 3, 'COMP208': 3, 'COMP206': 3,
            'COMP312': 3, 'COMP319': 3, 'ITEC401': 4, 'ITEC402': 4}

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
    global grade
    global final_grade
    global design_count, required_count
    if 'user.usr_id' in session:
        return render_template(
            "acainfo.html",
            grade_array = grade,
            final_grade = final_grade,
            design_count = design_count,
            required_count = required_count
            )

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

    sql = "Select Title, link from testDB.knu_main order by idx LIMIT 10;"
    row = db_class.executeAll(sql)

    sql2 = "Select Title, link from testDB.department order by idx LIMIT 10;"
    row2 = db_class.executeAll(sql2)

    sql3 = "Select Title, link from testDB.knu_ud order by idx LIMIT 10;"
    row3 = db_class.executeAll(sql3)

    sql4 = "Select Title, link from testDB.Recruitment order by idx LIMIT 10;"
    row4 = db_class.executeAll(sql4)

    return render_template(
        "notice.html",
        knu_main=[[title['Title'], title['link']] for title in row],
        department=[[title['Title'], title['link']] for title in row2],
        knu_ud=[[title['Title'], title['link']] for title in row3],
        Recruitment=[[title['Title'], title['link']] for title in row4]
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

        global design_count, required_count

        with requests.Session() as s:
            login_req = s.post(LOGIN_URL, data=params)
            post_one = s.get(craw_url)
            soup = BeautifulSoup(post_one.text, 'html.parser')

            for i in soup.select('div.contents > div.contents_box > div.contents_body > div.info_table.mb_30 > table > tr > td'):
                final_grade.append(i.text)

            # 교과목번호
            num = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(1)'):
                num.append(i.text)
                # print(i.text)

            # 개설학과
            department = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(2)'):
                department.append(i.text)
                # print(i.text)
            # 교과목명
            lesson = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(3)'):
                lesson.append(i.text)
                # print(i.text)
            # 교과구분
            division = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(4)'):
                division.append(i.text)
                # print(i.text)
            # 학점
            credit = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(5)'):
                credit.append(i.text)
                # print(i.text)
            # 학기
            semester = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(6)'):
                semester.append(i.text)
                # print(i.text)
            # 평점
            g = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(7)'):
                g.append(i.text)
                # print(i.text)
            # 재이수
            check = []
            for i in soup.select('#tab_FU > table > tr > td:nth-child(8)'):
                check.append(i.text)
                # print(i.text)

            if len(grade) == 0:
                for i in range(len(num)):
                    grade.append((num[i], department[i], lesson[i], division[i], credit[i], semester[i], g[i], check[i]))
                    if num[i] in design.keys():
                        design_count += design[num[i]]
                    if num[i] in required.keys():
                        required_count += required[num[i]]
            print(design_count, required_count)
            print(final_grade)        

            if len(grade) != 0 and design_count != 0 and required_count != 0:
                session['user.usr_id'] = input_usr_id 

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

