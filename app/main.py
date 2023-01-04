import os

from fastkml import kml, styles
from get_pictograms import open_input_file
from progress.bar import PixelBar
import re
from datetime import datetime
from bs4 import CData


def get_unique_styles(folder):
    styles = set()
    all_placemarks = folder.find_all('Placemark')
    bar = PixelBar(max=len(all_placemarks))
    for placemark in all_placemarks:
        style_url = placemark.find('styleUrl').text
        styles.add(re.search('[A-Za-z-0-9]+', style_url).group(0))
        bar.next()
    bar.finish()
    return list(styles)


def get_style_objects(soup, placemark_style, dir, folder):
    style_list = []
    styles_amount = soup.find_all('Style')
    len_styles_amount = len(styles_amount)
    bar = PixelBar(max=len_styles_amount)
    for i in range(len_styles_amount):
        style_id = styles_amount[i]['id']
        if placemark_style in style_id:
            j = styles.Style(id=style_id)
            if styles_amount[i].find('IconStyle'):
                icon_url = styles_amount[i].find('href').text
                icon_name = re.search('[0-9-a-z_]+.png', icon_url).group(0)
                icon_style = styles.IconStyle(icon_href=f'app/{folder.find("name").text}/{icon_name}/')
                icon_style.scale = styles_amount[i].find('IconStyle').find('scale').text
                j.append_style(icon_style)
            if styles_amount[i].find('LabelStyle'):
                label_style = styles.LabelStyle(scale=styles_amount[i].find('LabelStyle').find('scale').text)
                j.append_style(label_style)
            if styles_amount[i].find('LineStyle'):
                line_style = styles.LineStyle()
                if styles_amount[i].find('LineStyle').find('color'):
                    line_style.color = styles_amount[i].find('LineStyle').find('color').text
                elif styles_amount[i].find('LineStyle').find('width'):
                    line_style.width = styles_amount[i].find('LineStyle').find('width').text
                j.append_style(line_style)
            if styles_amount[i].find('BalloonStyle'):
                balloon_style = styles.BalloonStyle()
                if styles_amount[i].find('BalloonStyle').find('text'):
                    c_data = CData(styles_amount[i].find('BalloonStyle').find('text').text)
                    balloon_style.text = c_data
                j.append_style(balloon_style)
            style_list.append(j)
        bar.next()
    bar.finish()
    return style_list


# def get_style_kids(soup):
#     outset = set()
#     style_maps = soup.find_all('Folder')
#     for style in style_maps:
#         pairs = style.find_all('Placemark')
#         for pair in pairs:
#             keys = pair.find_all('ExtendedData')
#             for key in keys:
#                 hrefs = key.find_all('Data')
#                 for href in hrefs:
#                     values = href.find_all('value')
#                     for value in values:
#                         kids = value.children
#                         for i in kids:
#                             outset.add(i.name)
#     print(outset)


if __name__ == '__main__':
    base_dir, input_file, soup = open_input_file()
    folder_list = soup.find_all('Folder')

    # get_style_kids(soup)

    start = datetime.now()
    os.chdir(base_dir)
    for folder in folder_list:
        bar = PixelBar(max=len(folder_list))
        if not os.path.isdir(folder.find('name').text):
            os.mkdir(folder.find("name").text)
        unique_styles_placemarks = get_unique_styles(folder)
        for style in unique_styles_placemarks:
            kml_file = kml.KML()
            stl = get_style_objects(soup, style, base_dir, folder)
            doc = kml.Document(
                name=style,
                description=folder.find('name').text,
                styles=[*stl]
            )
            kml_file.append(doc)
            print(kml_file.to_string(prettyprint=True))
        bar.next()
    bar.finish()
    print(datetime.now() - start)
