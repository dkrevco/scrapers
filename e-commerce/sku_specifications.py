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



def scrape_dns(url):

    if not os.path.exists("data/dns-shop/"):
        os.mkdir("data/dns-shop/")

    if not os.path.exists("data/dns-shop/html/"):
        os.mkdir("data/dns-shop/html/")

    if not os.path.exists("data/dns-shop/csv/"):
        os.mkdir("data/dns-shop/csv/")

    if not os.path.exists("data/dns-shop/json/"):
        os.mkdir("data/dns-shop/json/")

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    brand_code = soup.find('div', class_='product-characteristics__spec product-characteristics__ovh').find('div', class_='product-characteristics__spec-value')
    name = brand_code.text.replace('[', '').replace(']', '').replace('/', '-')

    with open(f"data/dns-shop/html/{name}.html", "w", encoding="utf-8") as file:
        file.write(src)
        file.close()

    with open(f"data/dns-shop/html/{name}.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    product_info = []

    list_params = soup.find_all('div', class_="product-characteristics__spec")

    for item in list_params:
        item_name = item.find("div", class_="product-characteristics__spec-title").text.strip()
        item_value = item.find("div", class_="product-characteristics__spec-value").text.strip()

        product_info.append(
            {
                item_name: item_value
            }
        )

    with open(f"data/dns-shop/json/{name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
        file.close()



def scrape_re_store(url):

    if not os.path.exists("data/re-store/"):
        os.mkdir("data/re-store/")

    if not os.path.exists("data/re-store/html/"):
        os.mkdir("data/re-store/html/")

    if not os.path.exists("data/re-store/csv/"):
        os.mkdir("data/re-store/csv/")

    if not os.path.exists("data/re-store/json/"):
        os.mkdir("data/re-store/json/")

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'
    headers = {'User-Agent': user_agent}
    names = []


    req = requests.get(url, headers=headers)

    parsed = urllib.parse.urlsplit(url)

    name = parsed.path
    name = name.replace('/catalog/', "").replace('/', "")
    names.append(name)

    rep = [",", " ", "-", "'", "/"]
    for item in rep:
        if item in name:
            name = name.replace(item, "_")


    with open(f'data/re-store/html/{name}.html', "w", encoding="utf-8") as file:
        file.write(req.text)

    with open(f'data/names.txt', 'a', encoding='utf-8') as file:
        for element in names:
            file.write(element + "\n")
        file.close()

    with open(f"data/re-store/html/{name}.html", 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    list_params = soup.find_all('li', class_="list-param__item")

    product_info = []

    for item in list_params:
        item_name = item.find('div', class_='list-param__head').text.strip()
        item_value = item.find('div', class_='list-param__body')

        item_value = str(item_value).replace("<br/>", " ").replace("<div class=\"list-param__body\">", " ").replace("</div>", " ").strip()

        print(item_value)

        product_info.append(
            {
                item_name: item_value.strip()
            }
        )

    with open(f"data/re-store/json/{name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
        file.close()


def main(urls):

    for url in urls:
        if url.find('dns-shop.ru') > 0:
            scrape_dns(url)
        elif url.find('re-store.ru') > 0:
            scrape_re_store(url)



if __name__ == '__main__':

    with open('dns_products.txt') as file:
        dns_list = file.read().splitlines()

    with open('products.txt') as file:
        restore = file.read().splitlines()

    all_links = restore + dns_list

    main(all_links)

