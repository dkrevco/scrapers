import requests
import re
from bs4 import BeautifulSoup
import json
import csv
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
import urllib.parse



def scrape_sales(url: str, user_agent: str):

    if not os.path.exists('saved_sales/'):
        os.mkdir('saved_sales/')

    if not os.path.exists('saved_sales/src/'):
        os.mkdir('saved_sales/src/')

    if not os.path.exists('saved_sales/fixed/'):
        os.mkdir('saved_sales/fixed/')

    name = f'{str(url).split("/")[3]}_{str(url).split("/")[4]}'

    headers = {'User-Agent': user_agent}

    req = requests.get(url, headers=headers)

    with open(f'saved_sales/src/{name}.html', 'w', encoding='utf-8') as file:
        file.write(req.text)
        file.close()

    with open(f'saved_sales/src/{name}.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    src = soup.find('section', class_='ActionBlockstyles__ActionBlock-d8h34l-0 jSxWUc')

    links = []

    links_extraction = src.find_all('a')

    for link in links_extraction:
        href = link.get('href')
        links.append(href)

    not_none = filter(None.__ne__, links)

    with open('saved_sales/db.txt', 'a', encoding='utf-8') as file:
        for url in not_none:
            file.write(f'{url}\n')
        file.close()






if __name__ == '__main__':


    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

    with open('saved_sales/src.txt', 'r') as src:
        links = src.read().splitlines()
        src.close()

    for link in links:
        scrape_sales(link, user_agent)

