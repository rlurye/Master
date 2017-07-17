#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

import itertools
import xlwt
import time
from bs4 import BeautifulSoup
import requests

matter = [u"Программная инженерия", u"Информационные системы и технологии",
          u"Прикладная математика и информатика"]

def disciplines(nap, mnap):
    nap[:] = []
    mnap[:] = []
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
#     print i
# print()
# for i in mnap:
#     print i


def gen_table(entry, path):
    filename = entry['code']+path[-1]+"_"+time.strftime("%Y%m%d-%H%M%S")+".xls"
    records = []
    if path[-1] == 'b':
        records = load_table(entry['bud'])
    else:
        records = load_table(entry['pay'])

    #r = requests.get('http://eltech.ru'+entry')
    #c = r.content

    work = xlwt.Workbook()
    sheet = work.add_sheet('Sheet1')
    for row_index, column in enumerate(records):
        for column_index, column_data in enumerate(column):
            cwidth = sheet.col(column_index).width
            if (len(column_data) * 367) > cwidth:
                sheet.col(column_index).width = (
                len(column_data) * 367)  # (Modify column width to match biggest data in that column)

            sheet.write(row_index, column_index, column_data)

    work.save('master/static/tables/' + filename)
    return filename

def load_table(link):
    r = requests.get('http://eltech.ru/'+link)
    c = r.content
    #print(c)
    records = []
    soup = BeautifulSoup(c, 'lxml')
    table = soup.find('table', attrs={"id": "accepted-application"})
    tr0 = table.find_all('tr')[0]
    records.append([elem.text for elem in tr0.find_all('th')])

    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        records.append([elem.text for elem in tds])
    for i in records:
        print i
    return records


def gen_table_all(mnap, nap):
    filename = "all"+"_"+time.strftime("%Y%m%d-%H%M%S")+".xls"
    records = []
    header = True
    for entry in itertools.chain(mnap, nap):
        if entry['bud'] != '-':
            records += load_table_all(entry['bud'], entry['name'], header)
            header = False
            #print(records)

    work = xlwt.Workbook()
    sheet = work.add_sheet('Sheet1')
    for row_index, column in enumerate(records):
        for column_index, column_data in enumerate(column):
            cwidth = sheet.col(column_index).width
            if (len(column_data) * 367) > cwidth:
                sheet.col(column_index).width = (
                len(column_data) * 367)  # (Modify column width to match biggest data in that column)

            sheet.write(row_index, column_index, column_data)

    work.save('master/static/tables/' + filename)
    return filename


def load_table_all(link, name, header):
    r = requests.get('http://eltech.ru/'+link)
    c = r.content
    #print(c)
    records = []
    soup = BeautifulSoup(c, 'lxml')
    table = soup.find('table', attrs={"id": "accepted-application"})
    if header:
        tr0 = table.find_all('tr')[0]
        records.append([elem.text for elem in tr0.find_all('th')[1:]])
        records[0].insert(1, "Направление подготовки")

    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        l = [elem.text for elem in tds[1:]]
        l.insert(1, name)
        records.append(l)
    #for i in records:
    #    print i
    return records