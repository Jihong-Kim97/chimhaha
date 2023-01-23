import csv
import requests
import re
from bs4 import BeautifulSoup
from utils import createDirectory, createFilename, rel2absTime
import datetime
#침착맨 나라 스크래핑

dirname = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/침착맨 나라"
createDirectory(dirname)
filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/침착맨 나라/침착맨.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
now = str(datetime.datetime.now())

writer = csv.writer(f)
row_title = ['title','nickname','view', 'like', 'date', 'comment', 'page url']
writer.writerow(row_title)
for page in range(1,500):
    url = "https://chimhaha.net/stream_free?page={}".format(page)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("a", attrs={"class":"item"})
    if len(items) == 0:
        break
    print("____________{}___________".format(page))

    for item in items:
        page_url = item["href"]
        page_url = "https://chimhaha.net{}".format(page_url)
        info = item.find("div", attrs={"class":"info"})
        title = item.find("span", attrs={"class":"title"}).find("span", attrs={"class":"text"}).get_text()
        if len(item.find_all("span", attrs={"class":"commentCount"}))>0:
            commentCount = item.find("span", attrs={"class":"commentCount"}).get_text()
        else:
            commentCount = 0
        date = rel2absTime(item.find("div", attrs={"class":"datetime"}).get_text(), now)       
        #category = info.find("div", attrs={"class":"category"}).get_text().strip()
        nickname = info.find("div", attrs={"class":"nickName"}).get_text().strip()
        view = info.find("div", attrs={"class":"viewCount"}).get_text().strip()
        if len(info.find_all("div", attrs={"class":"likeCount"})) > 0:
            like = info.find("div", attrs={"class":"likeCount"}).get_text().strip()
        else:
            like = 0

        data = [title, nickname, view, like, date, commentCount, page_url]
        writer.writerow(data)
    print("_________________________")