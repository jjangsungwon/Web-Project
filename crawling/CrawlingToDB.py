from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
import requests
from bs4 import BeautifulSoup
import dbModule


def insert_notice(table_name, idx, title, data, link):
    db_class = dbModule.Database()

    sql = 'INSERT INTO %s VALUES(%d, "%s", "%s", "%s")' % (table_name, idx, title, data, link)
    db_class.execute(sql)
    db_class.commit()


def department_to_db():
    req = requests.get("http://computer.knu.ac.kr/06_sub/02_sub.html")
    soup = BeautifulSoup(req.text, 'html.parser')

    # 제목
    title = []
    for i in soup.select(
            '#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td:nth-child(2)'):
        # print(i.text)
        title.append(i.find("a")['title'])

    # 등록일
    date = []
    for i in soup.select(
            '#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td.bbs_date'):
        # print(i.text)
        date.append(i.text)

    # 링크
    link = []
    for i in soup.select(
            '#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td:nth-child(2)'):
        # print(i.find("a")['href'])
        temp = "http://computer.knu.ac.kr/06_sub/02_sub.html" + i.find("a")['href']
        link.append(temp)

    for i in range(len(title)):
        insert_notice("department", i + 1, title[i], date[i], link[i])


def knu_to_db():
    req = requests.get("http://knu.ac.kr/wbbs/wbbs/bbs/btin/list.action?bbs_cde=1&menu_idx=67")
    soup = BeautifulSoup(req.text, 'html.parser')
    # 제목
    title_1 = []
    for i in soup.select('div.board_list > table > tbody > tr > td.subject'):
        title_1.append(i.text.strip())  # 공백 제거
    # 등록일
    date_1 = []
    for i in soup.select('div.board_list > table > tbody > tr > td.date'):
        date_1.append(i.text.strip())
    # 링크
    link_1 = []
    for i in soup.select('div.board_list > table > tbody > tr > td.subject'):
        temp = "http://knu.ac.kr/wbbs/wbbs/bbs/btin/viewBtin.action?" + i.find("a")['href']
        link_1.append(temp)

    # (2) - 학사공지
    req = requests.get("http://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?menu_idx=42")
    soup = BeautifulSoup(req.text, 'html.parser')
    # 제목
    title_2 = []
    for i in soup.select('div.board_list > table > tbody > tr > td.subject'):
        title_2.append(i.text.strip())  # 공백 제거
    # 등록일
    date_2 = []
    for i in soup.select('div.board_list > table > tbody > tr > td.date'):
        date_2.append(i.text.strip())

    # 링크
    # 링크를 javascript:doRead('13997899', '000000', '812', 'row'); 형태로 줘서 앞에 숫자 2개를 이용하기 위해 별도의 과정을 추가함
    link_2 = []
    for i in soup.select('div.board_list > table > tbody > tr > td.subject'):
        val = i.find("a")['href']
        val = val[18:]
        val = val[:-2]
        val = val.split(' ')
        no1 = val[0][1:-2]
        no2 = val[1][1:-2]
        temp = "http://knu.ac.kr/wbbs/wbbs/bbs/btin/stdViewBtin.action?btin.doc_no=" + val[0][1:-2] + "&btin.appl_no=" + \
               val[1][
               1:-2] + "&btin.page=1&btin.search_type=&btin.search_text=&popupDeco=&btin.note_div=top&menu_idx=42"
        link_2.append(temp)

    for i in range(len(title_1)):
        insert_notice("knu_main", i + 1, title_1[i], date_1[i], link_1[i])

    for i in range(len(title_2)):
        insert_notice("knu_ud", i + 1, title_2[i], date_2[i], link_2[i])


def recruitment_to_db():
    req = requests.get("https://computer.knu.ac.kr/06_sub/03_sub.html")
    soup = BeautifulSoup(req.text, 'html.parser')

    # 제목
    title = []
    for i in soup.select(
            '#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td:nth-child(2)'):
        # print(i.text)
        title.append(i.find("a")['title'])
    # 등록일
    date = []
    for i in soup.select(
            '#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td.bbs_date'):
        # print(i.text)
        date.append(i.text)

    # 링크
    link = []
    for i in soup.select(
            '#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td:nth-child(2)'):
        # print(i.find("a")['href'])
        temp = "https://computer.knu.ac.kr/06_sub/03_sub.html" + i.find("a")['href']
        link.append(temp)

    # 출력 (결과 확인)
    for i in range(len(title)):
        insert_notice("Recruitment", i + 1, title[i], date[i], link[i])


department_to_db()
knu_to_db()
recruitment_to_db()
