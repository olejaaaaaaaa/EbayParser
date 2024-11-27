from colorama import init, Fore
import pandas as pd
from os import listdir, curdir
from os.path import isfile, join
import requests
from bs4 import BeautifulSoup

init(autoreset=True)

def parse(files, url):

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    b = soup.find_all('span', class_="s-item__price")        # Цена
    c = soup.find_all('a', class_="s-item__link", href=True) # Ссылка
    d = soup.find_all('div', class_="s-item__title")         # Название

    price = []
    for i in b:
        count = 0
        sum = ""
        for j in str(i):

            if j == "<" and count == 3:
                break

            if count == 3:
                sum += j

            if j == ">":
                count += 1

        price.append(sum)

    links = []
    for i in c:
       links.append(i['href'])
    
    title = []
    for i in d:
        count = 0
        sum = ""
        for j in str(i):

            if j == "<" and count == 3:
                break

            if count == 3:
                sum += j

            if j == ">":
                count += 1

        title.append(sum)

    mpn = []
    number = []
    for i in range(0, len(price)):
        resp = requests.get(links[i])
        soup = BeautifulSoup(resp.text, "html.parser")
        res = soup.find_all("span", class_="ux-textspans")
        num = soup.find_all("span", class_="ux-textspans ux-textspans--BOLD")

        lol = False
        for i in num:
            for j in i:
                if str(j).isdigit():
                    number.append(str(j))
                    lol = True

        if not(lol):
            number.append(str(0))

        n = False
        l = len(mpn)
        for i in res:
            if "MPN" in i:
                n = True
                continue

            if n:
                for j in i:
                    mpn.append(str(j))
                    print(str(j))
                n = False

        if len(mpn) == l:
            mpn.append('Does Not Apply')        

    file = open("результат.xlsx", "w+")

    data = {
        'Заголовок':        title,
        'Ссылки':           links,
        'Артикль':          mpn,
        'Цена':             price,
        'Номер объявления': number
    }

    df = pd.DataFrame(data)
    df.to_excel('результат.xlsx', index=False)

print(Fore.BLUE + 'Программа для парсинга https://www.ebay.com')

files = [f for f in listdir(curdir) if isfile(join(curdir, f))]
res = []

for i in files:
    if ".xlsx" in i:
        print(Fore.BLUE + 'Обнаружен файл: ', Fore.GREEN + str(i))
        res.append(i)

print(Fore.BLUE + 'Проверяем сайт на доступность: ', end='')
resp = requests.get("https://ebay.com")

if resp.status_code == 200:
    print(Fore.GREEN + 'Сайт доступен')
    print(Fore.BLUE + 'Вставьте url: ', end='')
    x = str(input())
    print(Fore.BLUE + 'Начинаю парсить сайт...')
    parse(res, x)
else:
    print(Fore.RED + 'Сайт не доступен :( ')

print(Fore.BLUE + 'Программа закончила свое выполнение')
exit = str(input())

