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
session = requests.session()

params = dict()
params['user.usr_id'] = 'ID'  # abeek 아이디
params['user.passwd'] = 'Pwd'  # 비밀번호
stu_nbr_code = '학번' #학번

with requests.Session() as session:
    login_req = session.post(LOGIN_URL, data=params)
    # 전체과목 성적
    post_one = session.get(craw_url)
    soup = BeautifulSoup(post_one.text, 'html.parser')

    data = soup.find_all('tr')  # remove 4번하면 첫 번째 부터 나옴.
    for i in range(4):
        data.remove(data[0])
    grade_array = []
    for tmp in data:
        grade_array.append(tmp.text.split())

    for i in range(len(grade_array)):
        print(grade_array[i])

    # 필수과목 성적조회
    post_two=session.post(must_url, data={'stu_nbr': stu_nbr_code, 'pgm_cde': 'CE02'})
    soup_es = BeautifulSoup(post_two.content, 'html.parser')
    es_data = soup_es.find_all('tr')
    es_data.remove(es_data[0])
    must_subject = []
    for tmp in es_data:
        must_subject.append(tmp.text.split())

    for i in range(len(must_subject)):
        print(must_subject[i])


    # 설계과목 성적조회
    post_three=session.post(design_url, data={'stu_nbr': stu_nbr_code, 'pgm_cde': 'CE02'})
    soup_de = BeautifulSoup(post_three.content, 'html.parser')
    de_data = soup_de.find_all('tr')
    de_data.remove(de_data[0])
    design_subject = []
    for tmp in de_data:
        design_subject.append(tmp.text.split())

    for i in range(len(design_subject)):
        print(design_subject[i])
