import csv
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from utils import createDirectory
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

filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/침착맨 나라/{}{}침착맨.csv".format(year, month)
# f = open(filename, "w", encoding="utf-8-sig", newline="")
# writer = csv.writer(f)
# row_title = ['title','nickname','view', 'like', 'date', 'comment', 'page url']
# writer.writerow(row_title)

print("{}월 start!".format(month))
nations = []
text = ""

df_chim = pd.read_csv('C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/침착맨 나라/침착맨.csv')
df_month = df_chim.loc[df_chim['date'].str.startswith(pat='{}.'.format(month))]

num_post = len(df_chim.loc[df_chim['date'].str.startswith(pat='{}.'.format(month))])
num_comment = df_month['comment'].sum()
num_view = df_month['view'].sum()
num_like = df_month['like'].sum()
mean_comment = num_comment/num_post
mean_view = num_view/num_post
mean_like = num_like/num_post

print(num_post, num_comment, mean_comment, num_view,  mean_view, num_like, mean_like)

for title in df_month["title"]:
    text = text + str(title)

for nickname in df_month['nickname']:
    if not(nickname in nations):
        nations.append(nickname)

for page_url in df_month['page url']:
    num_image = 0
    num_gif = 0 
    
    res = requests.get(page_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    content = soup.find("div", attrs={"class":"item"}).find("div", attrs={"class":"content ck-content"})
    text = text + content.get_text().strip()

    images = content.find_all("img")
    if(len(images) > 0):
        for image in images:
            if image["src"][-3:] == "jpg":
                num_image += 1
            elif image["src"][-3:] == "gif":
                num_gif += 1

    df_month.loc[df_month["page url"] == page_url,"img"] = num_image
    df_month.loc[df_month["page url"] == page_url,"gif"] = num_gif

    comments = soup.find("div", attrs={"class":"comments"}).find_all("div", attrs={"class":"comment"})
    if len(comments) > 0:
        for comment in comments:
            if len(comment.find_all("div", attrs={"class":"nickName"})):
                nickname = comment.find("div", attrs={"class":"nickName"}).find("div", attrs={"class":"text"}).get_text().strip()
                comment_content = comment.find("div", attrs={"class":"commentContent"}).get_text().strip
                text = text + str(comment_content)
                if not(nickname in nations):
                    nations.append(nickname)


df_month.to_csv(filename, mode='w', index=False)
twitter = Twitter()

num_nations = len(nations)
print(num_nations)

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
cloud.to_file("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/침착맨 나라/{}{}침착맨_cloud.jpg".format(year, month))
print("finish!")
