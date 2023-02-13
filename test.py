from utils import rel2absTime
import datetime
import csv
import datetime

now = str(datetime.datetime.now())
now_year = now[0:4]
now_month = int(now[5:7])
now_day = int(now[8:10])
print(now_year)