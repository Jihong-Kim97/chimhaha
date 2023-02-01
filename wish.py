import csv
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter
import pandas as pd
import numpy as np
from utils import createDirectory, createFilename, rel2absTime
from tqdm import tqdm
import datetime
import os
import warnings

#소원의돌 스크래핑
def wishScraping(year, month):
    dirname = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}".format(year, month)

    now = str(datetime.datetime.now())
    now_month = int(now[5:7])
    now_day = int(now[8:10])

    start_day = 1
    for day in range(1,32):
        filename = createFilename("소원의돌",year,month,day,"csv")
        if not os.path.exists(filename):
            start_day = day - 1
            break

    if now_month > month:
        if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            days = range(start_day, 32)
        elif month == 2:
            days = range(start_day,29)
        else:
            days = range(start_day,31)
    else:
        days = range(start_day,now_day + 1)

    for day in tqdm(days, desc='{}월 소원의돌 수집중'.format(month)):
        #csv 파일 해더 입력
        filename = createFilename("소원의돌",year,month,day,"csv")
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

#소원의돌 일자별 데이터 월별로 병합
def wishConcat(year, month):
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        days = range(1, 32)
    elif month == 2:
        days = range(1,29)
    else:
        days = range(1,31)

    df_all = pd.DataFrame()

    for day in tqdm(days, desc='{}월 소원의돌 병합중'.format(month)):
        filename = createFilename("소원의돌",year,month,day,"csv")
        if not os.path.exists(filename):
            break
        df_wish = pd.read_csv(filename)
        df_wish['date'] = "{}.{}.{}".format(year, month, day)
        df_all = pd.concat([df_all, df_wish])

    if month < 10:
        str_month = "0"+ str(month)
    else:
        str_month =str(month)
    df_all.to_csv("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}/{}{}_소원의돌.csv".format(year, month, year, str_month), mode='w',index=False)

#열혈 접속자 기도를 해당월 마지막일 기준으로 스크래핑
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

#해당월 소원의 돌 워드클라우드 일자별, 월별로 생성
def wishCloud(year, month):
    warnings.filterwarnings('ignore')
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        days = range(1, 32)
    elif month == 2:
        days = range(1,29)
    else:
        days = range(1,31)
    text_month=''

    for day in tqdm(days, desc='{}월 소원의돌 wordcloud 생성중'.format(month)):
        filename = createFilename("소원의돌",year,month,day,"csv")
        if not os.path.exists(filename):
            break
        wishes = pd.read_csv(filename)['wish']
        text =""
        for wish in wishes:
            text = text + str(wish)
        
        text_month = text_month + text

        twitter = Twitter()

        # twitter함수를 통해 읽어들인 내용의 형태소를 분석한다.
        sentences_tag = []
        sentences_tag = twitter.pos(text) 

        noun_adj_list = []


        # tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
        for word, tag in sentences_tag:
            if tag in ['Noun' , 'Adjective']: 
                noun_adj_list.append(word)


        # 가장 많이 나온 단어부터 40개를 저장한다.
        counts = Counter(noun_adj_list)
        tags = counts.most_common(40) 


        # WordCloud를 생성한다.
        # 한글을 분석하기위해 font를 한글로 지정해주어야 된다. macOS는 .otf , window는 .ttf 파일의 위치를
        # 지정해준다. (ex. '/Font/GodoM.otf')
        wc = WordCloud(font_path='C:/Windows/Fonts/맑은 고딕/malgunbd.ttf',background_color="white", max_font_size=60)
        cloud = wc.generate_from_frequencies(dict(tags))


        # 생성된 WordCloud를 test.jpg로 보낸다.
        cloud.to_file(filename[:-4]+"_cloud.jpg")




    # 월단위 cloud 작성
    twitter = Twitter()

    # twitter함수를 통해 읽어들인 내용의 형태소를 분석한다.
    sentences_tag = []
    sentences_tag = twitter.pos(text_month) 

    noun_adj_list = []


    # tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
    for word, tag in sentences_tag:
        if tag in ['Noun' , 'Adjective']: 
            noun_adj_list.append(word)


    # 가장 많이 나온 단어부터 40개를 저장한다.
    counts = Counter(noun_adj_list)
    tags = counts.most_common(40) 
    wc = WordCloud(font_path='C:/Windows/Fonts/맑은 고딕/malgunbd.ttf',background_color="white", max_font_size=60)
    cloud = wc.generate_from_frequencies(dict(tags))
    cloud.to_file("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}/{}{}_소원의돌_cloud.jpg".format(year, month, year, month))
    print("finish!".format(day))