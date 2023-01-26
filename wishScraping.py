import csv
import requests
from bs4 import BeautifulSoup
from utils import createDirectory, createFilename, rel2absTime
from tqdm import tqdm
#소원의돌 스크래핑


year = 2023
month = 1


def wishScraping(year, month):
    board_name = "소원의돌"
    dirname = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}".format(year, month)
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        days = range(1, 32)
    elif month == 2:
        days = range(1,29)
    else:
        days = range(1,31)

    for day in tqdm(days, desc='{}월 소원의돌 수집중'.format(month)):
        #csv 파일 해더 입력
        filename = createFilename(board_name,year,month,day,"csv")
        createDirectory(dirname)
        f = open(filename, "w", encoding="utf-8-sig", newline="")
        writer = csv.writer(f)
        row_title = ['number', 'nickname', 'wish', 'point', 'continuity', 'total']
        writer.writerow(row_title)
        
        #url 주소 입력
        if day < 10:
            if month < 10:
                url = "https://chimhaha.net/check?date={}-0{}-0{}".format(year, month, day)
            else:
                url = "https://chimhaha.net/check?date={}-{}-0{}".format(year, month, day)
        else:
            if month < 10:
                url = "https://chimhaha.net/check?date={}-0{}-{}".format(year, month, day)
            else:
                url = "https://chimhaha.net/check?date={}-{}-{}".format(year, month, day)

        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        items = soup.find_all("div", attrs={"class":"item"})
        #하루에 빌어진 소원들 입력
        for item in tqdm(items, desc='{}월 {}일 소원의돌 수집중'.format(month,day)):
            number = item.find("div", attrs={"class":"number"}).get_text()[:-1]
            nickname = item.find("div", attrs={"class":"nickName"}).get_text()
            wish = item.find("div", attrs={"class":"comment"}).get_text()
            point = item.find("div", attrs={"class":"point"}).get_text()[:-1]
            continuity = item.find("div", attrs={"class":"continue"}).get_text()[:-2]
            total = item.find("div", attrs={"class":"total"}).get_text()[1:-1]      
            data = [number, nickname, wish, point, continuity, total]
            writer.writerow(data)