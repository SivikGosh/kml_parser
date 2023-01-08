import os
from bs4 import BeautifulSoup

root_dir = os.path.dirname(__file__)
file = input('Введите название файла (без расширения):')


def get_soup_file(dir, file):
    """преобразование входного файла"""
    os.chdir(dir)
    with open(f'{file}.kml', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    return soup


soup_file = get_soup_file(root_dir, file)
