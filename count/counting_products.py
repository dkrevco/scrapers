import requests
from bs4 import BeautifulSoup
import os
import datetime



def count_products(url: str):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    req = requests.get(url, headers=headers).text

    soup = BeautifulSoup(req, 'lxml')
    src = soup.find_all('article', class_='CatalogItemstyles__CatalogItem-sc-8mov5i-0 ivEfYq')

    counter = len(src)
    name = f'{str(url).split("/")[3]}_{str(url).split("/")[4]}'

    print(f'processing {url}\n')
    return f'{name}: {url}: {counter}\n'

def main(url_list: str):

    with open(url_list, 'r') as src:
        links = src.read().splitlines()
        src.close()

    with open(f'result_product_scrape-{datetime.date.today()}.txt', 'a', encoding='utf-8') as file:
        for link in links:
            file.write(count_products(f'{link}'))
        file.close()


if __name__ == '__main__':

    urls = 'urls.txt'
    main(urls)