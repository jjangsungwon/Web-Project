"""
    ABEEK에서 들은 수업 모두를 불러온다.
    성적표에 있는 자료 모두를 파싱함.
    순서[강의코드, 개설대학, 과목명, 교과구분, 학점, 학기, 성적]
    단 공백이 있는 경우는 없어짐.
"""
import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'https://abeek.knu.ac.kr/Keess/comm/support/login/login.action'
craw_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/list.action'
design_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/designPart.action'
must_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/essentPart.action'

params = dict()
params['user.usr_id'] = 'ID'  # abeek 아이디
params['user.passwd'] = 'PW'  # 비밀번호
stu_nbr_code = '학번' #학번

with requests.Session() as session:
    login_req = session.post(LOGIN_URL, data=params)
    # 전체과목 성적
    post_one = session.get(craw_url)
    soup = BeautifulSoup(post_one.text, 'html.parser')

    grade = []
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

    for i in range(len(num)):
        grade.append((num[i], department[i], lesson[i], division[i], credit[i], semester[i], g[i], check[i]))
        print(grade[i])
