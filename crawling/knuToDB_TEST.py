"""
    경북대학교 홈페이지 전체 공지사항, 학사 공지 크롤링 (제목(title), 등록일(date), 주소(link))
    - 전체 공지사항(http://knu.ac.kr/wbbs/wbbs/bbs/btin/list.action?bbs_cde=1&menu_idx=67)
    - 학사공지(http://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?menu_idx=42)
"""

# 1 -> 전체 공지사항
# 2 -> 학사공지


import requests
from bs4 import BeautifulSoup
import dbModule


def insert(table_name, idx, title, data, link):
    db_class = dbModule.Database()

    sql = 'INSERT INTO %s VALUES(%d, "%s", "%s", "%s")' % (table_name, idx, title, data, link)
    db_class.execute(sql)
    db_class.commit()


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
    temp = "http://knu.ac.kr/wbbs/wbbs/bbs/btin/stdViewBtin.action?btin.doc_no=" + val[0][1:-2] + "&btin.appl_no=" + val[1][1:-2] + "&btin.page=1&btin.search_type=&btin.search_text=&popupDeco=&btin.note_div=top&menu_idx=42"
    link_2.append(temp)


# 출력
print("*" * 30, "전체 공지사항", "*" * 30)
for i in range(len(title_1)):
    print("Title", title_1[i])
    print("Date", date_1[i])
    print("Link", link_1[i])
    insert("knu_main", i + 1, title_1[i], date_1[i], link_1[i])

print('\n', "*" * 30, "학사공지", "*" * 30)
for i in range(len(title_2)):
    print("Title", title_2[i])
    print("Date", date_2[i])
    print("Link", link_2[i])
    insert("knu_ud", i + 1, title_2[i], date_2[i], link_2[i])
