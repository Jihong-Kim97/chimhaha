from ast import Continue
import csv
import requests
import re
from bs4 import BeautifulSoup
import creatDirectory
from creatDirectory import createDirectory, createFilename

year = 2022
month = 12
dirname = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}".format(year, month)

for day in range(1,32):
    filename = createFilename("소원의돌",year,month,day,"csv")
    createDirectory(dirname)
    f = open(filename, "w", encoding="utf-8-sig", newline="")

    writer = csv.writer(f)
    row_title = ['number', 'nickname', 'wish', 'point', 'continuity', 'total']
    writer.writerow(row_title)
    if day < 10:
        url = "https://chimhaha.net/check?date={}-{}-0{}".format(year, month, day)
    else:
        url = "https://chimhaha.net/check?date={}-{}-{}".format(year, month, day)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("div", attrs={"class":"item"})
    print("____________{}___________".format(day))
    for item in items:
        number = item.find("div", attrs={"class":"number"}).get_text()[:-1]
        nickname = item.find("div", attrs={"class":"nickName"}).get_text()
        wish = item.find("div", attrs={"class":"comment"}).get_text()
        point = item.find("div", attrs={"class":"point"}).get_text()[:-1]
        continuity = item.find("div", attrs={"class":"continue"}).get_text()[:-2]
        total = item.find("div", attrs={"class":"total"}).get_text()[1:-1]      
        data = [number, nickname, wish, point, continuity, total]
        writer.writerow(data)
    print("_________________________")