from flask import Flask, session, redirect, url_for, escape, request, render_template
import requests
from bs4 import BeautifulSoup
from crawling import dbModule
from crawling.Diet import culture, nuri, cheomseong

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

####### 학업 데이터 크롤링 코드 ##########
LOGIN_URL = 'https://abeek.knu.ac.kr/Keess/comm/support/login/login.action'
craw_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/list.action'
design_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/designPart.action'
must_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/essentPart.action'

# 설계과목
design = {'COMP205': [2, '기초창의공학설계'], 'COMP217': [2, '자바프로그래밍'], 'ELEC462': [2, '시스템프로그래밍'],
          'COMP224': [2, '소프트웨어설계'], 'COMP225': [2, '디지털설계및실험'], 'COMP422': [2, '소프트웨어공학'],
          'ITEC401': [4, '종합설계프로젝트1'], 'ITEC402': [4, '종합설계프로젝트2']}

# 필수과목
required = {'CLTR211': [3, '공학수학1'], 'CLTR213': [3, '물리학1'], 'CLTR223': [3, '물리학실험'], 'COME301': [3, '이산수학'],
            'COMP204': [3, '프로그래밍기초'], 'COMP205': [3, '대학글쓰기'], 'COME331': [3, '자료구조'], 'COMP217': [3, '자바프로그래밍'],
            'COMP411': [3, '컴퓨터구조'], 'ELEC462': [3, '시스템프로그래밍'], 'COMP208': [3, '물리학실험'],
            'COMP206': [3, '프로그래밍기초'], 'COMP312': [3, '운영체제'], 'COMP319': [3, '알고리즘1'],
            'ITEC401': [4, '종합설계프로젝트1'], 'ITEC402': [4, '종합설계프로젝트2']}

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
        return render_template(
            "acainfo.html",
            grade_array = session['grade'],
            final_grade = session['final_grade'],
            design_count = session['design_count'],
            required_count = session['required_count'],
            no_required = session['no_required'],
            no_design = session['no_design']
            )

    else:
        return render_template("login.html")


@app.route('/mealmenu')
def mealmenus():
    return render_template("mealmenu.html",
                           culture=culture,
                           nuri=nuri,
                           cheomseong=cheomseong
                           )


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

        final_grade = []
        grade = []
        required_count, design_count = 0, 0
        required_check, design_check = [], []  # 들은 필수 과목, 설계 과목 리스트
        no_design, no_required = [], []
        with requests.Session() as s:
            login_req = s.post(LOGIN_URL, data=params)
            post_one = s.get(craw_url)
            soup = BeautifulSoup(post_one.text, 'html.parser')

            for i in soup.select('div.contents > div.contents_box > div.contents_body > div.info_table.mb_30 > table > tr > td'):
                final_grade.append(i.text)

            #세션에 저장
            session['final_grade'] = final_grade

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
                        design_count += design[num[i]][0]
                        design_check.append(design[num[i]][1])
                    if num[i] in required.keys():
                        required_count += required[num[i]][0]
                        required_check.append(required[num[i]][1])
#            print(design_count, required_count)
#            print(final_grade)

            for key in design.keys():
                if design[key][1] not in design_check:
                    no_design.append(design[key][1])
            for key in required.keys():
                if required[key][1] not in required_check:
                    no_required.append(required[key][1])

 #           print(no_design)
 #           print(no_required)
            #세션에 저장
            session['design_count'] = design_count        
            session['required_count'] = required_count
            session['grade'] = grade
            session['no_required'] = no_required
            session['no_design'] = no_design              

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
    session.pop('required_count', None)
    session.pop('grade', None)
    session.pop('design_count', None)
    session.pop('final_grade', None)
    session.pop('no_required', None)
    session.pop('no_design', None)
    return redirect('/')           

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, ssl_context=('./cert/server.crt', './cert/server.key'))
