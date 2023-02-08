import os

from bs4 import BeautifulSoup

base_dir = os.path.dirname(__file__)


def get_soup_file(directory):
    os.chdir(directory)
    file = input('Введите название файла (без расширения):')
    with open(f'{file}.kml', encoding='utf-8') as f:
        souped_file = BeautifulSoup(f, 'xml')
    return souped_file


soup = get_soup_file(base_dir)
