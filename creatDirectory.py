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