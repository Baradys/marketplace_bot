import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_mvideo(search):
    url = f'https://www.mvideo.ru/product-list-page?q={search}'
    with webdriver.Chrome() as browser:
        browser.get(url=url)
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'page-link')))
        pages = int(browser.find_element(By.CLASS_NAME, 'bottom-controls').find_elements(By.TAG_NAME, 'li')[-2].text)
        for page in range(1, pages + 1)[0:1]:
            url = f'https://www.mvideo.ru/product-list-page?q={search}&page={page}'
            browser.get(url=url)
            browser.set_window_size(700, 800)
            action = ActionChains(browser)
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'button--light')))
            action.move_to_element(browser.find_element(By.CLASS_NAME, 'button--light'))
            time.sleep(10)
            response = browser.page_source
            soup = BeautifulSoup(response, 'lxml')
            items = soup.find_all('div', class_='product-cards-layout__item')
            for item in items:
                main_price = item.findNext('span', class_='price__main-value').text
                print(main_price)


def main():
    get_mvideo('наушники')


if __name__ == '__main__':
    main()
