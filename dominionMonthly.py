import csv
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from creatDirectory import createDirectory
from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter

year = 2022
month = 12


num_post = 0
num_comment = 0
num_view = 0
num_like = 0
num_nations = 0

filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/자치령/{}{}자치령.csv".format(year, month)
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
row_title = ['dominion','post', 'view', 'mean view', 'like', 'mean like', 'comment', 'mean comment', 'nations']
writer.writerow(row_title)

os.chdir('C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/자치령')
dominions = os.listdir()
dominions.sort(key=os.path.getmtime)
#print(dominions)

for dominion in dominions:
    print("{} start!".format(dominion))
    nations = []
    text = ""
    df_dominion = pd.read_csv('C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/자치령/{}'.format(dominion))
    # df_dominion['month'] = df_dominion['date'].str.split('.', n=1)
    # print(df_dominion.head())
    df_month = df_dominion.loc[df_dominion['date'].str.startswith(pat='{}.'.format(month))]
    num_post = len(df_dominion.loc[df_dominion['date'].str.startswith(pat='{}.'.format(month))])
    num_comment = df_month['comment'].sum()
    num_view = df_month['view'].sum()
    num_like = df_month['like'].sum()
    mean_comment = num_comment/num_post
    mean_view = num_view/num_post
    mean_like = num_like/num_post
    
    for title in df_month["title"]:
        text = text + str(title)

    for nickname in df_month['nickname']:
        if not(nickname in nations):
            nations.append(nickname)

    print(len(df_month['page url']))
    for page_url in df_month['page url']:
        res = requests.get(page_url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        content = soup.find("div", attrs={"class":"item"}).find("div", attrs={"class":"content ck-content"}).get_text().strip()
        text = text + content

        
        comments = soup.find("div", attrs={"class":"comments"}).find_all("div", attrs={"class":"comment"})
        #print(page_url)
        if len(comments) > 0:
            for comment in comments:
                if len(comment.find_all("div", attrs={"class":"nickName"})):
                    nickname = comment.find("div", attrs={"class":"nickName"}).find("div", attrs={"class":"text"}).get_text().strip()
                    comment_content = comment.find("div", attrs={"class":"commentContent"}).get_text().strip
                    text = text + str(comment_content)
                    if not(nickname in nations):
                        nations.append(nickname)

    twitter = Twitter()

    num_nations = len(nations)
    data = [dominion[:-4], num_post, num_view, mean_view, num_like, mean_like, num_comment, mean_comment, num_nations]
    writer.writerow(data)

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
    cloud.to_file("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/자치령/{}{}".format(year, month) + dominion[:-4]+"_cloud.jpg")
    print("{} finish!".format(dominion))
    