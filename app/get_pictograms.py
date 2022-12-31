import os
import re

import requests
from bs4 import BeautifulSoup
from progress.bar import ChargingBar

app_root_dir = os.path.dirname(__file__)
kml_file_name = input('Введите название файла (без расширения):')

with open(f'{app_root_dir}/{kml_file_name}.kml', encoding='utf-8') as kml_file:
    soup = BeautifulSoup(kml_file, 'xml')


def get_icon_urls(soup):
    """получение ссылок пиктограмм для их последующей загрузки"""
    urls = []
    bar = ChargingBar('Обработка', fill='█', max=len(soup.find_all('href')))
    for i in range(len(soup.find_all('href'))):
        urls.append(soup.find_all('href')[i].string)
        bar.next()
    bar.finish()
    return urls


def download_icons(url_list):
    """скачиваем пиктограммы в отдельную папку 'pictograms'"""
    os.chdir(app_root_dir)
    if not os.path.isdir('pictograms'):
        os.mkdir('pictograms')
    os.chdir(f'{app_root_dir}/pictograms')
    bar = ChargingBar('Загрузка', fill='█', max=len(soup.find_all('href')))
    for i in range(len(url_list)):
        icon = requests.get(url_list[i])
        icon_name = (
            re.search('[0-9-a-z_]+.png', url_list[i]).group(0)
        )
        icon_option = open(icon_name, 'wb')
        icon_option.write(icon.content)
        icon_option.close()
        bar.next()
    bar.finish()


if __name__ == '__main__':
    urls = get_icon_urls(soup)
    download_icons(urls)
