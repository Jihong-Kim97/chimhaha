from ast import Continue
import csv
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from utils import createDirectory, createFilename, rel2absTime
#열혈 접속자 기도를 해당월 마지막일 기준으로 스크래핑

year = 2022
month = 12
dirname = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}".format(year, month)
df_loyaluser = pd.read_csv('C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/소원의돌/{}{}_wish_loyaluser.csv'.format(year,month))
nicknames = df_loyaluser['nickname']
print(type(nicknames))

if month < 10:
    str_month = "0" + str(month)
else:
    str_month = str(month)

if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
    url = "https://chimhaha.net/check?date={}-{}-31".format(year, str_month)
elif month == 2:
    url = "https://chimhaha.net/check?date={}-{}-28".format(year, str_month)
else:
    rl = "https://chimhaha.net/check?date={}-{}-30".format(year, str_month)
res = requests.get(url)

res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")
items = soup.find_all("div", attrs={"class":"item"})
for item in items:
    number = item.find("div", attrs={"class":"number"}).get_text()[:-1]
    nickname = item.find("div", attrs={"class":"nickName"}).get_text().strip()
    wish = item.find("div", attrs={"class":"comment"}).get_text()
    point = item.find("div", attrs={"class":"point"}).get_text()[:-1]
    continuity = item.find("div", attrs={"class":"continue"}).get_text()[:-2]
    total = item.find("div", attrs={"class":"total"}).get_text()[1:-1]      
    
    if(df_loyaluser['nickname'].isin([nickname]).any()):
        df_loyaluser.loc[df_loyaluser['nickname'] == nickname, 'wish'] = wish
        print(nickname)
    # else:
    #     print(nickname)

print("finish!")
df_loyaluser.to_csv("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}/{}{}_소원의돌_loyaluser.csv".format(year,month,year,month), mode='w', index=False)