import os
import re

import requests
from bs4 import BeautifulSoup
from progress.bar import PixelBar


def open_input_file():
    base_dir = os.path.dirname(__file__)
    input_file_name = input('Введите название файла (без расширения):')
    with open(f'{base_dir}/{input_file_name}.kml', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')
    return base_dir, input_file_name, soup


def get_icon_urls(soup):
    urls = set()
    all_hrefs = soup.find_all('href')
    bar = PixelBar(max=len(all_hrefs))
    for href in all_hrefs:
        urls.add(href.text)
        bar.next()
    bar.finish()
    return list(urls)


def download_icons(urls):
    bar = PixelBar(max=len(urls))
    for url in urls:
        img = requests.get(url)
        img_name = re.search('[0-9-a-z_]+.png', url).group(0)
        img_option = open(img_name, 'wb')
        img_option.write(img.content)
        img_option.close()
        bar.next()
    bar.finish()


if __name__ == '__main__':
    base_dir, input_file, soup = open_input_file()
    urls = get_icon_urls(soup)
    os.chdir(base_dir)
    if not os.path.isdir('pictograms'):
        os.mkdir('pictograms')
    os.chdir(f'{base_dir}/pictograms')
    download_icons(urls)
