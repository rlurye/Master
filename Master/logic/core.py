import csv

import time
from bs4 import BeautifulSoup
import requests

matter = ["Программная инженерия", "Информационные системы и технологии",
          "Прикладная математика и информатика"]

def disciplines(nap, mnap):
    nap.clear()
    mnap.clear()
    r = requests.get('http://eltech.ru/ru/abiturientam/priem-v-magistraturu/podavshie-zayavlenie/')
    c = r.content
    soup = BeautifulSoup(c, 'lxml')
    table = soup.find('table', attrs={"class": "table table-bordered"})
    for row in table.find_all('tr'):
        items = row.find_all('td')
        if items:
            bud = items[2].find('a', href=True)
            pay = items[3].find('a', href=True)
            hrefb = '-'
            hrefp = '-'
            if bud:
                hrefb = bud.get('href')
            if pay:
                hrefp = pay.get('href')
            if items[1].text in matter:
                mnap.append({'name': items[1].text,
                             'code': items[0].text,
                             'bud': hrefb,
                             'pay': hrefp})
            else:
                nap.append({'name': items[1].text,
                             'code': items[0].text,
                             'bud': hrefb,
                             'pay': hrefp})


# nap = []
# mnap = []
# disciplines(nap,mnap)
# for i in nap:
#     print(i)
# print()
# for i in mnap:
#     print(i)

def gen_table(entry, path):
    filename = entry['code']+path[-1]+"_"+time.strftime("%Y%m%d-%H%M%S")+".csv"
    if path[-1] == 'b':
        load_table(entry['bud'])
    else:
        load_table(entry['pay'])

    #r = requests.get('http://eltech.ru'+entry')
    #c = r.content
    with open('Master/static/tables/'+filename, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(matter)
    return filename


def load_table(link):
    r = requests.get('http://eltech.ru/'+link)
    c = r.content
    print(c)
    records = []
    soup = BeautifulSoup(c, 'lxml')
    table = soup.find('table', attrs={"id": "accepted-application"})
    tr0 = table.find_all('tr')[0]
    records.append([elem.text for elem in tr0.find_all('th')])

    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        records.append(elem.text for elem in tds)
    for i in records:
        print(i)