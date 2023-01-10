import csv
import requests
import re
from bs4 import BeautifulSoup

for page in range(1,10):
    url = "https://chimhaha.net/humor_try/likes/zilioner?page={}".format(page)

    filenmae = "{}년.csv".format(page)
    f = open(filenmae, "w", encoding="utf-8-sig", newline="")

    writer = csv.writer(f)

    res = requests.get(url+ str(1))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    data_rows = soup.find_all(["li", "div"], attrs={"class": ["event", "section section--highlight section--person-of-interest", "section section--highlight section--person-of-interest section--historical-photo-landscape"]})
    pages = soup.find("ul", attrs={"class" : "pag"}).find_all("li")
    end = int(pages[-2].get_text())
    for row in data_rows:
        date = row.find("a", attrs={"class":"date"}).get_text()
        if(row.name == "div"):
                    events = row.find("p").get_text()
        else:
               events = row.get_text()
        data=["{} ".format(year)+date, events[6:]]
        writer.writerow(data)
    

    for page in range(2,end+1):
        res = requests.get(url+ str(page))
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        data_rows = soup.find_all(["li", "div"], attrs={"class": ["event", "section section--highlight section--person-of-interest", "section section--highlight section--person-of-interest section--historical-photo-landscape"]})
        for row in data_rows:
            date = row.find("a", attrs={"class":"date"}).get_text()
            if(row.name == "div"):
                        events = row.find("p").get_text()
            else:
                events = row.get_text()            
            data=["{} ".format(year)+date, events[6:]]
            #print(data)
            writer.writerow(data)