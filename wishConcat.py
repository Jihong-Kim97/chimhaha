import pandas as pd
import csv
from utils import createDirectory, createFilename
from tqdm import tqdm

year = 2022
month = 12
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
        df_wish = pd.read_csv(filename)
        df_wish['date'] = "{}.{}.{}".format(year, month, day)
        df_all = pd.concat([df_all, df_wish])

    if month < 10:
        str_month = "0"+ str(month)
    else:
        str_month =str(month)
    df_all.to_csv("C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/소원의돌/{}/{}/{}{}_소원의돌.csv".format(year, month, year, str_month), mode='w',index=False)