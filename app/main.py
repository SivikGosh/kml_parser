import os

from fastkml import kml, styles
from get_pictograms import open_input_file
from progress.bar import PixelBar
import re
from datetime import datetime
from bs4 import CData, Tag


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


def create_icon_style_obj(folder, style, dir):
    folder_name = folder.find("name").text
    icon_url = style.find('href').text
    icon_name = re.search('[0-9-a-z_]+.png', icon_url).group(0)
    icon_style = styles.IconStyle()
    icon_style.icon_href = f'{dir}/{folder_name}/{icon_name}'
    icon_style.scale = style.find('IconStyle').find('scale').text
    if style.find('color'):
        icon_style.color = style.find('color').text
    if style.find('hotSpot'):
        attributes = style.find('hotSpot').attrs
        icon_style.hot_spot = attributes
    return icon_style


def get_style_objects(soup, placemark_style, dir, folder):
    style_list = []
    all_styles = soup.find_all('Style')
    bar = PixelBar(max=len(all_styles))
    for style in all_styles:
        style_id = style['id']
        if placemark_style in style_id:
            style_obj = styles.Style(id=style_id)
            if style.find('IconStyle'):
                icon_style = create_icon_style_obj(folder, style, dir)
                style_obj.append_style(icon_style)

            if style.find('LabelStyle'):
                label_style = styles.LabelStyle()
                label_style.scale = style.find('LabelStyle').find('scale').text
                style_obj.append_style(label_style)

            if style.find('LineStyle'):
                line_style = styles.LineStyle()
                if style.find('LineStyle').find('color'):
                    line_style.color = (
                        style.find('LineStyle').find('color').text)
                elif style.find('LineStyle').find('width'):
                    line_style.width = (
                        style.find('LineStyle').find('width').text)
                style_obj.append_style(line_style)

            if style.find('BalloonStyle'):
                balloon_style = styles.BalloonStyle()
                if style.find('BalloonStyle').find('text'):
                    # c_data = CData(style.find('BalloonStyle').find('text'))
                    # tag = Tag(c_data)
                    # balloon_style.text = tag.string()
                style_obj.append_style(balloon_style)

            style_list.append(style_obj)
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


# def amount_elements(soup):
#     placemarks = soup.find_all('Placemark')
#     count = 0
#     for placemark in placemarks:
#         extended_datas = placemark.find_all('ExtendedData')
#         for extended_data in extended_datas:
#             datas = extended_data.find_all('Data')
#             for data in datas:
#                 values = data.find_all('value')
#                 for value in values:
#                     print('value attr: ', value.attrs)
#                     count += 1
#     print(count)


if __name__ == '__main__':
    base_dir, input_file, soup = open_input_file()
    folder_list = soup.find_all('Folder')

    # # # amount_elements(soup)

    # # # # get_style_kids(soup)

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
