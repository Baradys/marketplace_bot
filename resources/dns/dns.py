import json
import os
import time

import fake_useragent
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

ua = UserAgent()
fake_ua = ua.random

headers = {
    'user-agent': fake_ua
}


def get_data_dns(search, user_id=None):
    items_result = []
    with webdriver.Chrome() as browser:
        for page in range(1, 6):
            url = f'https://www.dns-shop.ru/search/?q={search}&order=discount&stock=now&p={page}'
            browser.get(url=url)
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            items = soup.find_all(class_='catalog-product')
            for item in items:
                try:
                    item_name = item.findNext('a', class_='catalog-product__name').text
                except AttributeError:
                    item_name = None
                try:
                    item_price = item.findNext('div', class_='product-buy__price').text
                except AttributeError:
                    item_price = None
                try:
                    item_url = 'https://www.dns-shop.ru' + item.findNext('a', class_='catalog-product__name')['href']
                except AttributeError:
                    item_url = None
                try:
                    item_rating = item.findNext('a', class_='catalog-product__rating')['data-rating']
                except AttributeError:
                    item_rating = None
                try:
                    item_rating_count = item.findNext('a', class_='catalog-product__rating').text
                except AttributeError:
                    item_rating_count = None
                items_result.append({
                    'item_name': item_name,
                    'item_price': item_price,
                    'item_url': item_url,
                    'item_rating': item_rating,
                    'item_rating_count': item_rating_count
                })
    if not os.path.exists('data'):
        os.mkdir('data')
    with open(f'data/dns-{user_id}.json', 'w', encoding='utf-8') as file:
        json.dump(items_result, file, indent=4, ensure_ascii=False)


def main():
    get_data_dns(input('Поиск: '))


if __name__ == '__main__':
    main()
