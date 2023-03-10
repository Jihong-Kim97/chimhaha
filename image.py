import csv
import requests
import re
from bs4 import BeautifulSoup
from utils import rel2absTime
import datetime
#짤렉산드리아 스크래핑

filenmae = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/짤렉산드리아/짤렉산드리아.csv"
f = open(filenmae, "w", encoding="utf-8-sig", newline="")
now = str(datetime.datetime.now())

writer = csv.writer(f)
row_title = ['게시물 제목','게시자', '분류', '조회수', '좋아요 수', '업로드 날짜', '댓글 수', '이미지 url', '페이지 url']
writer.writerow(row_title)
for page in range(1,11):
    url = "https://chimhaha.net/humor_try/likes/zilioner?page={}".format(page)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("a", attrs={"class":"item"})
    print("____________{}___________".format(page))
    for item in items:
        page_url = item["href"]
        page_url = "https://chimhaha.net{}".format(page_url)
        image = item.find("div", attrs={"class":"image"}).img["style"][23:-3]
        title = item.find("div", attrs={"class":"info"}).span.get_text()
        commentCount = item.find("span", attrs={"class":"commentCount"}).get_text()
        date = rel2absTime(item.find("span", attrs={"class":"datetime"}).get_text(), now)   

        item_res = requests.get(page_url)
        item_res.raise_for_status()
        item_soup = BeautifulSoup(item_res.text, "lxml")
        info = item_soup.find("div", attrs={"class":"info"})
        category = info.find("div", attrs={"class":"category"}).get_text().strip()
        nickname = info.find("div", attrs={"class":"nickName"}).get_text().strip()
        view = info.find("div", attrs={"class":"viewCount"}).get_text().strip()
        like = info.find("div", attrs={"class":"likeCount"}).get_text().strip()

        data = [title, nickname, category, view, like, date, commentCount, image, page_url]
        writer.writerow(data)
    print("_________________________")