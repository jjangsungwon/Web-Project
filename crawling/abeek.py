import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'https://abeek.knu.ac.kr/Keess/comm/support/login/login.action'
craw_url = 'http://abeek.knu.ac.kr/Keess/kees/web/stue/stueStuRecEnq/list.action'

params = dict()
params['user.usr_id'] = 'ID'  # abeek 아이디
params['user.passwd'] = 'PW'  # 비밀번호
stu_nbr_code = '학번'  # 학번

# 설계과목
design = {'COMP205': 2, 'COMP217': 2, 'ELEC462': 2, 'COMP224': 2, 'COMP225': 2, 'COMP422': 2, 'ITEC401': 4,
          'ITEC402': 4}

# 필수과목
required = {'CLTR211': 3, 'CLTR213': 3, 'CLTR223': 3, 'COME301': 3, 'COMP204': 3, 'COMP205': 3, 'COME331': 3,
            'COMP217': 3, 'COMP411': 3, 'ELEC462': 3, 'COMP206': 3, 'COMP208': 3,
            'COMP312': 3, 'COMP319': 3, 'ITEC401': 4, 'ITEC402': 4}

design_count, required_count = 0, 0
with requests.Session() as session:
    login_req = session.post(LOGIN_URL, data=params)

    # 전체과목 성적
    post_one = session.get(craw_url)
    soup = BeautifulSoup(post_one.text, 'html.parser')

    final_grade = []
    for i in soup.select(
            'div.contents > div.contents_box > div.contents_body > div.info_table.mb_30 > table > tr > td'):
        final_grade.append(i.text)

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
        if num[i] in design.keys():
            design_count += design[num[i]]
        if num[i] in required.keys():
            required_count += required[num[i]]

    print(design_count, required_count)
    # 설계과목
