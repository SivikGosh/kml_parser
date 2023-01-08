import os
import re

import requests
from input_datas import root_dir, soup_file
from progress.bar import PixelBar

base_dir = os.path.dirname(__file__)


def soup_file(dir):
    os.chdir(dir)
    file = input('Введите название файла (без расширения):')
    with open(f'{file}.kml', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    return soup


soup = soup_file(base_dir)


def get_urls(soup):
    urls = set()
    all_hrefs = soup.find_all('href')
    for href in all_hrefs:
        urls.add(href.text)
    return list(urls)


def download_icons(urls):
    bar = PixelBar('Загрузка иконок', max=len(urls))
    for url in urls:
        img_url = requests.get(url)
        img_name = re.search('[0-9-a-z_]+.png', url).group(0)
        with open(img_name, 'wb') as img:
            img.write(img_url.content)
        bar.next()
    bar.finish()


if __name__ == '__main__':
    urls = get_urls(soup)
    os.chdir(base_dir)
    if not os.path.isdir('pictograms'):
        os.mkdir('pictograms')
    os.chdir('pictograms')
    download_icons(urls)
