import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from utils import createDirectory, createFilename, rel2absTime
from tqdm import tqdm
#열혈 접속자 기도를 해당월 마지막일 기준으로 스크래핑

year = 2023
month = 1

def wishLoyal(year, month):
    if month < 10:
        str_month = "0"+ str(month)
    else:
        str_month =str(month)
    df_wish = pd.read_csv("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}/{}{}_소원의돌.csv".format(year, month, year, str_month))
    nicknames = df_wish['nickname'].unique()
    # 연속 기도, 누적 기도 수 입력
    for nickname in tqdm(nicknames, desc='유저 정보 생성 중'):
        df_single_user = df_wish[df_wish['nickname'] == nickname].sort_values(by='date')
        dates = df_single_user['date'].unique()
        for date in dates:
            day = int(date.split('.')[2])
            if date == dates[0]:
                continuity = 1
                total = 1
            else:
                total += 1
            if "{}.{}.{}".format(year, month, day-1) in dates:
                continuity += 1
            else:
                continuity = 1
            df_wish.loc[(df_wish['nickname'] == nickname) & (df_wish['date'] == date), 'continuity'] = continuity
            df_wish.loc[(df_wish['nickname'] == nickname) & (df_wish['date'] == date), 'total'] = total
    # 유저 정보 생성
    df_user = pd.DataFrame()
    df_user['nickname'] = nicknames
    for nickname in tqdm(nicknames, '연속/누적 기도 계산 중'):
        df_user.loc[df_user['nickname'] == nickname, 'total'] = np.max(df_wish[df_wish['nickname'] == nickname]['total'])
        df_user.loc[df_user['nickname'] == nickname, 'continuity'] = np.max(df_wish[df_wish['nickname'] == nickname]['continuity'])
    dirname = 'C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/소원의돌/{}/{}'.format(year, month)
    createDirectory(dirname)
    df_user.to_csv("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/소원의돌/{}/{}/{}{}_소원의돌_user.csv".format(year,month,year,month), mode='w', index=False)

    #열혈 유저 정보 생성
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        full_month = 31
    elif month == 2:
        full_month = 28
    else:
        full_month = 30
    df_loyal_users = df_user[df_user['total'] == full_month]
    nicknames = df_loyal_users['nickname']
    for nickname in nicknames:
        df_loyal_users.loc[df_loyal_users['nickname'] == nickname, 'order'] = np.mean(df_wish[df_wish['nickname'] == nickname]['number'])
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
    for item in tqdm(items, '열혈 유저 정보 수집 중'):
        number = item.find("div", attrs={"class":"number"}).get_text()[:-1]
        nickname = item.find("div", attrs={"class":"nickName"}).get_text().strip()
        wish = item.find("div", attrs={"class":"comment"}).get_text()
        point = item.find("div", attrs={"class":"point"}).get_text()[:-1]
        continuity = item.find("div", attrs={"class":"continue"}).get_text()[:-2]
        total = item.find("div", attrs={"class":"total"}).get_text()[1:-1]      
        
        if(df_loyal_users['nickname'].isin([nickname]).any()):
            df_loyal_users.loc[df_loyal_users['nickname'] == nickname, 'wish'] = wish

    df_loyal_users.to_csv("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/소원의돌/{}/{}/{}{}_소원의돌_loyaluser.csv".format(year,month,year,month), mode='w', index=False)