from flask import Flask, session, redirect, url_for, escape, request, render_template
######(추후 삭제) 
import requests
from bs4 import BeautifulSoup
######(추후 삭제) 

app = Flask(__name__)

####### 크롤링 데이터 출력 테스트 (추후 삭제) ########


# (1) - 전체 공지사항

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

for i in range(len(title_1)):
    print("Title", title_1[i])
    print("Date", date_1[i])
    print("Link", link_1[i])

##########################################
usr_id =''

@app.route('/')
def index():
    if 'user.usr_id' in session:
        return render_template(
            "index.html",
            usr_id = 'user.usr_id'
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

@app.route('/notice')
def notices():
    return render_template(
        "notice.html",
        news_title=[ title_1[i] for i in range(len(title_1))]
        )       

@app.route('/schoolmap')
def schoolmaps():
    return render_template("schoolmap.html")           

@app.route('/login')
def logins():
    return render_template("login.html")     



if __name__ == '__main__':
    app.run(debug=True)
