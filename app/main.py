import os

from fastkml import kml, styles
from get_pictograms import open_input_file
from progress.bar import PixelBar
import re


def get_unique_styles(folder):
    styles = set()
    bar = PixelBar(max=len(folder.find_all('Placemark')))
    for i in range(len(folder.find_all('Placemark'))):
        styles.add(
            re.search(
                '[A-Za-z-0-9]+',
                folder.find_all('Placemark')[i].find('styleUrl').text).group(0)
        )
        bar.next()
    bar.finish()
    return list(styles)


def get_style_objects(soup, placemark_style):
    style_list = []
    for i in range(len(soup.find_all(id=re.findall('[a-z-]+', placemark_style)))):
        j = styles.Style(id=soup.find_all(id=re.findall('[a-z-]+', placemark_style))[i]['id'])
        style_list.append(j)
    return style_list


if __name__ == '__main__':
    base_dir, input_file, soup = open_input_file()
    folder_list = soup.find_all('Folder')

    os.chdir(base_dir)
    for folder in folder_list:
        if not os.path.isdir(folder.find('name').text):
            os.mkdir(folder.find("name").text)
        unique_styles_placemarks = get_unique_styles(folder)
        for style in unique_styles_placemarks:
            kml_file = kml.KML()
            stl = get_style_objects(soup, style)
            doc = kml.Document(
                name=style,
                description=folder.find('name').text,
                styles=[*stl]
            )
            kml_file.append(doc)
            print(kml_file.to_string(prettyprint=True))
