import os

from fastkml import kml
from get_pictograms import open_input_file
from progress.bar import PixelBar


def get_objects_styles(soup):
    styles = set()
    bar = PixelBar(max=len(soup.Folder.find_all('Placemark')))
    for i in range(len(soup.Folder.find_all('Placemark'))):
        styles.add(soup.Folder.find_all('Placemark')[i].styleUrl.string)
        bar.next()
    bar.finish()
    return list(styles)


def get_folders(base_dir, soup):
    folders = []
    bar = PixelBar(max=len(soup.find_all('Folder')))
    for i in range(len(soup.find_all('Folder'))):
        folders.append(soup.find_all('Folder')[i].find('name').string)
        if not os.path.isdir(folders[i]):
            os.mkdir(f'{base_dir}/{folders[i]}')
        bar.next()
    bar.finish()
    return folders


def create_kml_files(folders, styles):
    pass


if __name__ == '__main__':
    base_dir, input_file, soup = open_input_file()
    styles = get_objects_styles(soup)
    folders = get_folders(base_dir, soup)
