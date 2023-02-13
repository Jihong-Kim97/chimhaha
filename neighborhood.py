import csv
import requests
from bs4 import BeautifulSoup
from utils import createDirectory, rel2absTime
import datetime
import pandas as pd
import numpy as np
#우리동네추천 스크래핑

board = "우리동네추천"
dirname = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/{}".format(board)
createDirectory(dirname)
filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/{}/{}.csv".format(board, board)
f = open(filename, "w", encoding="utf-8-sig", newline="")
now = str(datetime.datetime.now())
seoul_gu = ['은평', '강서', '양천', '구로', '금천', '동작', '영등포', '관악', '서초', '강남', '송파', '강동', '광진', '성동', '용산', '마포', '서대문', '종로', '성북', '중구', '동대문', '중랑', '노원', '도봉', '강북']

df_geo = pd.read_csv("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/우리동네추천/geo.csv", encoding='cp949')
df_city = df_geo['Korean']
titles = []

writer = csv.writer(f)
row_title = ['title','nickname','view', 'like', 'date', 'comment', 'page url', 'city_kor', 'city_eng']
writer.writerow(row_title)
for page in range(1,500):
    url = "https://chimhaha.net/mycity?page={}".format(page)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("a", attrs={"class":"item"})
    if len(items) == 1:
        break
    print("____________{}___________".format(page))

    for item in items:
        page_url = item["href"]
        page_url = "https://chimhaha.net{}".format(page_url)
        info = item.find("div", attrs={"class":"info"})
        date = rel2absTime(item.find("div", attrs={"class":"datetime"}).get_text(), now)       
        nickname = info.find("div", attrs={"class":"nickName"}).get_text().strip()
        if nickname == "침착맨":
            continue
        view = info.find("div", attrs={"class":"viewCount"}).get_text().strip()
        title = item.find("span", attrs={"class":"title"}).find("span", attrs={"class":"text"}).get_text()
        city_kor = ""
        city_eng = ""
        index = -1
        for gu in seoul_gu:
            if gu in title:
                print(gu)
                city_kor = "서울"
                city_eng = "Seoul"
        for city in df_city:
            if city in title:
                if index < title.index(city):
                    index = title.index(city)
                    city_kor = city
                    city_eng = df_geo.loc[df_geo['Korean'] == city]['Name'].values[0]

        
        if len(item.find_all("span", attrs={"class":"commentCount"}))>0:
            commentCount = item.find("span", attrs={"class":"commentCount"}).get_text()
        else:
            commentCount = 0
        if len(info.find_all("div", attrs={"class":"likeCount"})) > 0:
            like = info.find("div", attrs={"class":"likeCount"}).get_text().strip()
        else:
            like = 0

        data = [title, nickname, view, like, date, commentCount, page_url, city_kor, city_eng]
        if not title in titles:
            writer.writerow(data)
        titles.append(title)
    print("_________________________")