from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
import requests
from bs4 import BeautifulSoup
import dbModule


def insert(table_name, idx, title, data, link):
    db_class = dbModule.Database()

    sql = 'INSERT INTO %s VALUES(%d, "%s", "%s", "%s")' % (table_name, idx, title, data, link)
    db_class.execute(sql)
    db_class.commit()


# 페이지 text 모두 가져오기
req = requests.get("http://computer.knu.ac.kr/06_sub/02_sub.html")
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
    temp = "http://computer.knu.ac.kr/06_sub/02_sub.html" + i.find("a")['href']
    link.append(temp)

# 출력 (결과 확인)
for i in range(len(title)):
    print("Title", title[i])
    print("Date", date[i])
    print("Link", link[i])
    print("*" * 100)
    insert("department", i + 1, title[i], date[i], link[i])

print("done")



