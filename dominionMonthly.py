import csv
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from creatDirectory import createDirectory

year = 2022
month = 12

nations = []
num_post = 0
num_comment = 0
num_view = 0
num_like = 0

filenmae = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DA/자치령/{}{}자치령.csv".format(year, month)
f = open(filenmae, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
row_title = ['dominion','post', 'view', 'mean view', 'like', 'mean like', 'comment', 'mean comment']
writer.writerow(row_title)

os.chdir('C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/자치령')
dominions = os.listdir()
#print(dominions)

for dominion in dominions:
    df_dominion = pd.read_csv('C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/자치령/{}'.format(dominion))
    # df_dominion['month'] = df_dominion['date'].str.split('.', n=1)
    # print(df_dominion.head())
    df_month = df_dominion.loc[df_dominion['date'].str.startswith(pat='{}'.format(month))]
    num_post = len(df_dominion.loc[df_dominion['date'].str.startswith(pat='{}'.format(month))])
    num_comment = df_month['comment'].sum()
    num_view = df_month['view'].sum()
    num_like = df_month['like'].sum()
    mean_comment = num_comment/num_post
    mean_view = num_view/num_post
    mean_like = num_like/num_post
    data = [dominion, num_post, num_view, mean_view, num_like, mean_like, num_comment, mean_comment]
    writer.writerow(data)
