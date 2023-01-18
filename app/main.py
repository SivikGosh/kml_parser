import os
import re
import shutil
from datetime import datetime
# import requests
# from time import sleep

from fastkml import data, kml, styles
from fastkml.geometry import Geometry
from souping_file import base_dir, soup
from legend import legend
from progress.bar import PixelBar
from pygeoif import LineString, Point


def get_placemark_styles(folder_object):
    """получаем список уникальных стилей объектов папки"""
    style_list = set()
    all_placemarks = folder_object.find_all('Placemark')
    for placemark_object in all_placemarks:
        style_url = placemark_object.find('styleUrl').text
        reg_line = 'line-[0-9A-F]{6}-[0-9]{4}'
        reg_icon = 'icon-[0-9]{3}-[0-9A-F]{6}|icon-[0-9]{4}'
        reg = f'({reg_line}|{reg_icon})'
        style_list.add(re.search(reg, style_url).group(0))
    return list(style_list)


def create_icon_style(folder, style, directory):
    """"""
    icon_id = style.attrs['id']
    icon_name = re.search(
        '(icon-[0-9]{3,4}-[0-9A-F]{6}|icon-[0-9]{3,4})', icon_id).group(0)
    icon_style = styles.IconStyle()
    icon_style.icon_href = f'{directory}/pictograms/{icon_name}.png'
    icon_style.scale = style.find('IconStyle').find('scale').text
    if style.find('color'):
        icon_style.color = style.find('color').text
    if style.find('hotSpot'):
        icon_style.hot_spot = style.find('hotSpot').attrs
    return icon_style


def create_label_style(style):
    """"""
    label_style = styles.LabelStyle()
    label_style.scale = style.find('LabelStyle').find('scale').text
    return label_style


def create_line_style(style):
    """"""
    line_style = styles.LineStyle()
    line_style.color = style.find('LineStyle').find('color').text
    line_style.width = style.find('LineStyle').find('width').text
    return line_style


def create_balloon_style(style):
    """"""
    balloon_style = styles.BalloonStyle()
    balloon_style.text = style.find('BalloonStyle').find('text').text
    return balloon_style


def add_styles(soup, placemark_style, directory, folder):
    """"""
    style_list = []
    all_styles = soup.find_all('Style')
    for style in all_styles:
        if placemark_style in style['id']:
            style_obj = styles.Style(id=style['id'])
            if style.find('IconStyle'):
                icon_style = create_icon_style(folder, style, directory)
                style_obj.append_style(icon_style)
            if style.find('LabelStyle'):
                label_style = create_label_style(style)
                style_obj.append_style(label_style)
            if style.find('LineStyle'):
                line_style = create_line_style(style)
                style_obj.append_style(line_style)
            if style.find('BalloonStyle'):
                balloon_style = create_balloon_style(style)
                style_obj.append_style(balloon_style)
            style_list.append(style_obj)
    return style_list


def add_style_maps(soup, placemark_style):
    """"""
    style_map_list = []
    all_style_maps = soup.find_all('StyleMap')
    for style_map in all_style_maps:
        if placemark_style in style_map['id']:
            style_map_object = styles.StyleMap()
            styl_map_url_n = style_map.find('key', text='normal').parent
            style_map_url_h = style_map.find('key', text='highlight').parent
            style_map_object.id = style_map['id']
            style_map_object.normal = (
                styles.StyleUrl(url=styl_map_url_n.find('styleUrl').text))
            style_map_object.highlight = (
                styles.StyleUrl(url=style_map_url_h.find('styleUrl').text))
            style_map_list.append(style_map_object)
    return style_map_list


def get_point_coordinates(point):
    """"""
    coordinates = [float(i) for i in point.split()[0].split(',')]
    return tuple(coordinates)


def get_line_string_coordinates(line_string):
    """"""
    output_list = []
    line_string_list = line_string.strip().split('\n')
    for string in line_string_list:
        string = string.replace(' ', '').split(',')
        output_list.append(tuple(float(i) for i in string))
    return tuple(output_list)


def add_placemarks(folder, placemark_style):
    """"""
    placemark_list = []
    all_placemarks = folder.find_all('Placemark')
    for placemark in all_placemarks:
        placemark_style_url = placemark.find('styleUrl').text
        if f'#{placemark_style}' in placemark_style_url:
            placemark_object = kml.Placemark(name=placemark.find('name').text)
            placemark_object.style_url = placemark_style_url
            if placemark.find('description'):
                placemark_object.description = (
                    placemark.find('description').text)
            if placemark.find('ExtendedData'):
                ext_data_kid = data.Data(name=placemark.find('Data')['name'])
                # try:
                #     ext_data_kid.value = (
                #         re.search(
                #             'https:(.)+fife',
                #             placemark.find('ExtendedData')
                #             .find('Data').find('value').text
                #         ).group(0)
                #     )
                #     photos.append(ext_data_kid.value)
                # except Exception:
                #     print('No photo')
                ext_data = data.ExtendedData(elements=[ext_data_kid])
                placemark_object.extended_data = ext_data
            if placemark.find('Point'):
                point = placemark.find('Point').find('coordinates').text
                coords = get_point_coordinates(point)
                point_object = Point(*coords)
                geometry_object = Geometry(geometry=point_object)
                placemark_object.geometry = geometry_object
            if placemark.find('LineString'):
                line_string = (
                    placemark.find('LineString').find('coordinates').text)
                line_coords = get_line_string_coordinates(line_string)
                line_object = LineString(coordinates=line_coords)
                geometry_line_object = Geometry(geometry=line_object)
                placemark_object.geometry = geometry_line_object
            placemark_list.append(placemark_object)
    return placemark_list


def get_line_width(soup, place_style):
    all_styles = soup.find_all('Style')
    for style in all_styles:
        if 'line' in style.attrs['id']:
            return style.find('width').text


if __name__ == '__main__':
    start_time = datetime.now()
    placemark_count = 0

    all_folders = soup.find_all('Folder')
    bar = PixelBar('Обработано папок', max=len(all_folders))

    os.chdir(base_dir)
    for folder in all_folders:
        folder_name = folder.find('name').text
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        placemark_styles = get_placemark_styles(folder)
        obj_bar = PixelBar('Обработано объектов', max=len(placemark_styles))

        os.chdir(folder_name)
        for style in placemark_styles:
            w = get_line_width(soup, style)
            if 'line' in style:
                file_name = f'{legend[style]}_width_{w}'
            else:
                file_name = legend[style]
            if not os.path.isdir(file_name):
                os.mkdir(file_name)

            os.chdir(file_name)
            kml_object = kml.KML()
            st_obj = add_styles(soup, style, base_dir, folder)
            st_map_obj = add_style_maps(soup, style)
            document = kml.Document(styles=[*st_obj, *st_map_obj])
            document.name = file_name
            document.description = folder.find('name').text
            placemarks = add_placemarks(folder, style)
            for placemark in placemarks:
                document.append(placemark)
                placemark_count += 1
            kml_object.append(document)

            kml_file = open(f'{file_name}.kml', 'wb')
            kml_file.write(kml_object.to_string(prettyprint=True).encode())
            kml_file.close()

            if 'icon' in style:
                shutil.copy(f'{base_dir}/pictograms/{style}.png',
                            f'{file_name}.png')
            os.chdir('../')
            obj_bar.next()
            # sleep(1)
        os.chdir(base_dir)
        obj_bar.finish()
        bar.next()
    bar.finish()
    print('Время выполнения', datetime.now() - start_time)
    assert placemark_count == len(soup.find_all('Placemark'))
