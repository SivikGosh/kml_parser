import os
import re

import requests
from input_datas import root_dir, soup_file
from progress.bar import PixelBar


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
    os.chdir(root_dir)
    urls = get_urls(soup_file)
    if not os.path.isdir('pictograms'):
        os.mkdir('pictograms')
    os.chdir(f'{root_dir}/pictograms')
    download_icons(urls)
