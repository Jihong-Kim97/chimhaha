import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def createFilename(page, year, int_month, day, type):
    filename = ""
    if int_month < 10:
        month = "0"+ str(int_month)
    else:
        month =str(int_month)

    if day < 10:
        filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/{}/{}/{}/{}{}0{}_{}.{}".format(page, year, int_month, year, month, day, page, type)
    else:
        filename = "C:/Users/KimJihong/Desktop/김지홍/개발/침하하/DB/{}/{}/{}/{}{}{}_{}.{}".format(page, year, int_month, year, month, day, page, type)

    return filename

def rel2absTime(rel_date, datetime):
    month = int(datetime[5:7])
    day = int(datetime[8:10])
    hour = int(datetime[11:13])
    minute = int(datetime[14:16])
    monthly_day = 0
    if month == 2:
        monthly_day = 28
    elif month in [1,3,5,7,8,10,12]:
        monthly_day = 31
    else:
        monthly_day = 30 

    abs_date = ""
    normal = False
    if rel_date[-2:] == "일전":
        day = int(day) - int(rel_date[:-2])
    elif rel_date[-2:] == "분전":
        minute = int(minute) - int(rel_date[:-2])
    elif rel_date[-3:] == "시간전":
        hour =  int(hour) - int(rel_date[:-3])
    elif rel_date[-2:] == "초전":
        normal = False
    else:
        normal = True

    print(month,day,hour,minute)
    if minute < 0:
        minute += 60
        hour -= 1
    
    if hour < 0:
        hour += 24
        day -= 1

    if day < 1:
        day += monthly_day
        month -= 1

    if month < 1:
        month += 12
    
    if not normal:
        abs_date = str(month) + "." + str(day)
    else:
        abs_date = rel_date
    
    return abs_date