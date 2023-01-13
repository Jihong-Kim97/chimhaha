from ast import Continue
import csv
import requests
import re
from bs4 import BeautifulSoup

year = 2022
int_month = 12

if int_month < 10:
    month = "0"+ str(int_month)
else:
    month =str(int_month)

for day in range(1,32):
    if day < 10:
        filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/소원의돌/{}{}0{}_소원의돌.csv".format(year, month, day)
    else:
        filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/소원의돌/{}{}{}_소원의돌.csv".format(year, month, day)
    f = open(filename, "w", encoding="utf-8-sig", newline="")

    writer = csv.writer(f)
    row_title = ['등수', '게시자', '내용', '점수', '연속', '총 기도일 수']
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
        number = item.find("div", attrs={"class":"number"}).get_text()
        nickname = item.find("div", attrs={"class":"nickName"}).get_text()
        wish = item.find("div", attrs={"class":"comment"}).get_text()
        point = item.find("div", attrs={"class":"point"}).get_text()
        continuity = item.find("div", attrs={"class":"continue"}).get_text() 
        total = item.find("div", attrs={"class":"total"}).get_text()        
        data = [number, nickname, wish, point, continuity, total]
        writer.writerow(data)
    print("_________________________")