import csv
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from creatDirectory import createDirectory

url = 'https://chimhaha.net/'
res = requests.get(url)

d = datetime.now()
time_name = "/"+ str(d.year) + str(d.month) +str(d.day) + str(d.hour) + str(d.minute)

res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")
nav = soup.find("div", attrs={"class":"navWrap"}).find("nav")
button_lis = nav.find("ul", attrs={"class":"active two"})
# print(button_lis[5])
# index_of_dominions = 5 #자치령 버튼 순서
dominions_lis = button_lis.find_all("li")
hrefs = {}
dominions = []

for dominions_li in dominions_lis:
    hrefs[dominions_li.find("a").get_text()] = dominions_li.find("a")["href"]
    dominions.append(dominions_li.find("a").get_text())

# print(hrefs)

for dominion in dominions:
    dirname = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/자치령"

    filenmae = "{}{}.csv".format(dirname, hrefs[dominion])
    f = open(filenmae, "w", encoding="utf-8-sig", newline="")

    writer = csv.writer(f)
    row_title = ['title','nickname', 'view', 'like', 'date', 'comment', 'image url', 'page url']
    writer.writerow(row_title)
    
    url = "https://chimhaha.net" + hrefs[dominion]

    for page in range(1,500):
        page_url = url + "?page={}".format(page)
        res = requests.get(page_url)

        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        boardLists = soup.find_all("section", attrs={"id":"boardList"})
        if(len(boardLists) == 0):
            print(str(page) + "page complete!")
            break
        notice = 0

        for boardList in boardLists:
            if len(boardList["class"]) > 0 :
                items = boardList.find_all("a", attrs={"class":"item"})
                notice = 1
            else:
                items = boardList.find_all("a", attrs={"class":"item"})
                notice = 0
            # items = boardList.find_all("a", attrs={"class":"item"})
            for item in items:
                title = item.find("div", attrs={"class":"info"}).find("span", attrs={"class":"text"}).get_text()
                nickname = item.find("div", attrs={"class":"nickName"}).get_text().strip()
                date = item.find("div", attrs={"class":"datetime"}).get_text()
                page_url = "https://chimhaha.net{}".format(item["href"])

                if len(item.find_all("div", attrs={"class":"viewCount"})) > 0:
                    view = item.find("div", attrs={"class":"viewCount"}).get_text().strip()
                else:
                    view = 0
                
                if len(item.find_all("div", attrs={"class":"likeCount"})):
                    like = item.find("div", attrs={"class":"likeCount"}).get_text().strip()
                else:
                    like = 0

                if len(item.find_all("span", attrs={"class":"commentCount"})):
                    comment = item.find("span", attrs={"class":"commentCount"}).get_text()
                else:
                    comment = 0

                if notice == 0 and len(item.find("div", attrs={"class":"image"}).find_all("img")) > 0:
                        image_url = item.find("div", attrs={"class":"image"}).img["style"][23:-3]
                else:
                    image_url = ""
                
                data = [title, nickname, view, like, date, comment, image_url, page_url]
                # print(data)
                writer.writerow(data)
        
    print("finish {}!".format(dominion))
