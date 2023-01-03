import os

from fastkml import kml, styles
from get_pictograms import open_input_file
from progress.bar import PixelBar
import re
from datetime import datetime


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


def get_style_objects(soup, placemark_style, dir):
    style_list = []
    styles_amount = soup.find_all('Style')
    len_styles_amount = len(styles_amount)
    bar = PixelBar(max=len_styles_amount)

    for i in range(len_styles_amount):
        style_id = styles_amount[i]['id']
        if placemark_style in style_id:
            j = styles.Style(id=style_id)
            if styles_amount[i].find('IconStyle'):
                icon_style = styles.IconStyle(icon_href='app/pictograms/503-wht-blank_maps.png')
                icon_style.scale = styles_amount[i].find('scale').text
                j.append_style(icon_style)
            style_list.append(j)
        bar.next()
    bar.finish()
    return style_list


if __name__ == '__main__':
    base_dir, input_file, soup = open_input_file()
    folder_list = soup.find_all('Folder')

    start = datetime.now()

    os.chdir(base_dir)
    for folder in folder_list:
        if not os.path.isdir(folder.find('name').text):
            os.mkdir(folder.find("name").text)
        unique_styles_placemarks = get_unique_styles(folder)
        for style in unique_styles_placemarks:
            kml_file = kml.KML()
            stl = get_style_objects(soup, style, base_dir)
            doc = kml.Document(
                name=style,
                description=folder.find('name').text,
                styles=[*stl]
            )
            kml_file.append(doc)
            print(kml_file.to_string(prettyprint=True))
