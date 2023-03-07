from bs4 import BeautifulSoup


def cook_soup():
    file = input('Введите название файла (без расширения):')
    with open(f'{file}.kml', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    return soup
