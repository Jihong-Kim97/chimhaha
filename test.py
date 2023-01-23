from utils import rel2absTime
import datetime

d = str(datetime.datetime.now())
d = "2023-01-05 16:50:43.895283"
r = rel2absTime("7일전", d)
print(d)
print(r)