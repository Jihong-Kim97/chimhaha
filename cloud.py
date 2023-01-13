from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

year = 2022
int_month = 12
text_month = ""

if int_month < 10:
    month = "0"+ str(int_month)
else:
    month =str(int_month)

for day in range(1,32):
    if day < 10:
        filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/소원의돌/{}{}0{}_소원의돌.csv".format(year, month, day)
    else:
        filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/소원의돌/{}{}{}_소원의돌.csv".format(year, month, day)
    wishes = pd.read_csv(filename)['내용']
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
    print("{}day finish!".format(day))




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
cloud.to_file("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/소원의돌/{}{}_소원의돌_cloud.jpg".format(year, month))
print("finish!".format(day))