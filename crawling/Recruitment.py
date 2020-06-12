"""
    경북대학교 컴퓨터학부 홈페이지 취업정보 크롤링(https://computer.knu.ac.kr/06_sub/03_sub.html)
    첫 페이지에 등록된 제목, 등록일, 링크 정보를 가져온다
"""

import requests
from bs4 import BeautifulSoup

# 페이지 text 모두 가져오기
req = requests.get("https://computer.knu.ac.kr/06_sub/03_sub.html")
soup = BeautifulSoup(req.text, 'html.parser')

# 제목
title = []
for i in soup.select('#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td:nth-child(2)'):
    # print(i.text)
    title.append(i.find("a")['title'])
# 등록일
date = []
for i in soup.select('#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td.bbs_date'):
    # print(i.text)
    date.append(i.text)

# 링크
link = []
for i in soup.select('#content > article > article.sub-content.area > div:nth-child(9) > table > tbody > tr > td:nth-child(2)'):
    # print(i.find("a")['href'])
    temp = "https://computer.knu.ac.kr/06_sub/03_sub.html" + i.find("a")['href']
    link.append(temp)

# 출력 (결과 확인)
for i in range(len(title)):
    print("Title", title[i])
    print("Date", date[i])
    print("Link", link[i])
    print("*" * 100)