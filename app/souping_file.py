import os

from bs4 import BeautifulSoup

base_dir = os.path.dirname(__file__)


def get_soup_file(directory):
    """готовим суп, пригодится в различных файлах проекта"""
    os.chdir(directory)
    file = input('Введите название файла (без расширения):')
    with open(f'{file}.kml', encoding='utf-8') as f:
        souped_file = BeautifulSoup(f, 'xml')
    return souped_file


soup = get_soup_file(base_dir)

# # # скачивание иконок, вряд ли понадобится уже # # # # # # # # # # # # # # #

# import re
# import requests
# from progress.bar import PixelBar


# def get_urls(souped_file):
#     urls_list = set()
#     all_hrefs = souped_file.find_all('href')
#     for href in all_hrefs:
#         urls_list.add(href.text)
#     return list(urls_list)


# def download_icons(urls_list):
#     bar = PixelBar('Загрузка иконок', max=len(urls_list))
#     for url in urls_list:
#         img_url = requests.get(url)
#         img_name = re.search('[0-9-a-z_]+.png', url).group(0)
#         with open(img_name, 'wb') as img:
#             img.write(img_url.content)
#         bar.next()
#     bar.finish()


# if __name__ == '__main__':
#     urls = get_urls(soup)
#     os.chdir(base_dir)
#     if not os.path.isdir('pictograms'):
#         os.mkdir('pictograms')
#     os.chdir('pictograms')
#     download_icons(urls)
