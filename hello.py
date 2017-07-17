from bs4 import BeautifulSoup
import requests

respond = requests.get("http://www.eltech.ru/ru/abiturientam/priem-v-magistraturu/podavshie-zayavlenie")
soup = BeautifulSoup(respond.text)
l = soup.find_all('table')
t = l[0].find_all('tr')
time = ""
for i in t:
    cols = i.find_all('td')
    print([c.text for c in cols])