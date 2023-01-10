import csv
import requests
import re
from bs4 import BeautifulSoup

filenmae = "침하하.csv"
f = open(filenmae, "w", encoding="utf-8-sig", newline="")

writer = csv.writer(f)
for page in range(1,11):
    url = "https://chimhaha.net/humor_try/likes/zilioner?page={}".format(page)



    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("a", attrs={"class":"item"})
    print("____________{}___________".format(page))
    for item in items:
        image = item.find("div", attrs={"class":"image"}).img["style"][23:-3]
        title = item.find("div", attrs={"class":"info"}).span.get_text()
        commentCount = item.find("span", attrs={"class":"commentCount"}).get_text()
        print(image, title, commentCount)
        data = [image, title, commentCount]
        writer.writerow(data)
    print("_________________________")

    # data_rows = soup.find_all(["li", "div"], attrs={"class": ["event", "section section--highlight section--person-of-interest", "section section--highlight section--person-of-interest section--historical-photo-landscape"]})
    # pages = soup.find("ul", attrs={"class" : "pag"}).find_all("li")
    # end = int(pages[-2].get_text())
    # for row in data_rows:
    #     date = row.find("a", attrs={"class":"date"}).get_text()
    #     if(row.name == "div"):
    #                 events = row.find("p").get_text()
    #     else:
    #            events = row.get_text()
    #     data=["{} ".format(year)+date, events[6:]]
    #     writer.writerow(data)
    

    # for page in range(2,end+1):
    #     res = requests.get(url+ str(page))
    #     res.raise_for_status()
    #     soup = BeautifulSoup(res.text, "lxml")

    #     data_rows = soup.find_all(["li", "div"], attrs={"class": ["event", "section section--highlight section--person-of-interest", "section section--highlight section--person-of-interest section--historical-photo-landscape"]})
    #     for row in data_rows:
    #         date = row.find("a", attrs={"class":"date"}).get_text()
    #         if(row.name == "div"):
    #                     events = row.find("p").get_text()
    #         else:
    #             events = row.get_text()            
    #         data=["{} ".format(year)+date, events[6:]]
    #         #print(data)
    #         writer.writerow(data)