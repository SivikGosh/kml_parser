import os

from fastkml import kml, styles, data
from fastkml.geometry import Geometry
from get_pictograms import open_file
from progress.bar import PixelBar
import re
from datetime import datetime
from pygeoif import Point, LineString


def get_unique_styles(folder):
    styles = set()
    all_placemarks = folder.find_all('Placemark')
    for placemark in all_placemarks:
        style_url = placemark.find('styleUrl').text
        styles.add(re.search('[A-Za-z-0-9]+', style_url).group(0))
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
                line_style.color = style.find('LineStyle').find('color').text
                line_style.width = style.find('LineStyle').find('width').text
                style_obj.append_style(line_style)
            if style.find('BalloonStyle'):
                balloon_style = styles.BalloonStyle()
                balloon_style.text = (
                    style.find('BalloonStyle').find('text').text)
                style_obj.append_style(balloon_style)
            style_list.append(style_obj)
    return style_list


def get_style_map_objects(soup, placemark_style):
    style_map_list = []
    all_style_maps = soup.find_all('StyleMap')
    for style_map in all_style_maps:
        style_map_id = style_map['id']
        if placemark_style in style_map_id:
            style_map_object = styles.StyleMap()
            styl_map_url_n = style_map.find('key', text='normal').parent
            style_map_url_h = style_map.find('key', text='highlight').parent
            style_map_object.id = style_map_id
            style_map_object.normal = (
                styles.StyleUrl(url=styl_map_url_n.find('styleUrl').text))
            style_map_object.highlight = (
                styles.StyleUrl(url=style_map_url_h.find('styleUrl').text))
            style_map_list.append(style_map_object)
    return style_map_list


def get_coordinates(point):
    coordinates = [float(i) for i in point.split()[0].split(',')]
    return tuple(coordinates)


def get_line_string_coordinates(line_string):
    output_list = []
    line_string_list = line_string.strip().split('\n')
    for string in line_string_list:
        string = string.replace(' ', '').split(',')
        output_list.append(tuple(float(i) for i in string))
    return tuple(output_list)


def get_placemark_objects(folder, placemark_style):
    placemark_list = []
    all_placemarks = folder.find_all('Placemark')
    for placemark in all_placemarks:
        placemark_style_url = placemark.find('styleUrl').text
        if placemark_style in placemark_style_url:
            placemark_object = kml.Placemark(name=placemark.find('name').text)
            placemark_object.style_url = placemark_style_url
            if placemark.find('description'):
                placemark_object.description = (
                    placemark.find('description').text)
            if placemark.find('ExtendedData'):
                ext_data_kid = data.Data(name=placemark.find('Data')['name'])
                ext_data_kid.value = (
                    placemark.find('ExtendedData')
                    .find('Data').find('value').text)
                ext_data = data.ExtendedData(elements=[ext_data_kid])
                placemark_object.extended_data = ext_data
            if placemark.find('Point'):
                point = placemark.find('Point').find('coordinates').text
                coords = get_coordinates(point)
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


if __name__ == '__main__':
    base_dir, soup = open_file()
    folder_list = soup.find_all('Folder')
    bar = PixelBar('Обработано папок', max=len(folder_list))
    start = datetime.now()
    os.chdir(base_dir)
    for folder in folder_list:
        if not os.path.isdir(folder.find('name').text):
            os.mkdir(folder.find("name").text)
        os.chdir(folder.find("name").text)
        unique_styles_placemarks = get_unique_styles(folder)
        for style in unique_styles_placemarks:
            kml_file = kml.KML()
            style_objects = get_style_objects(soup, style, base_dir, folder)
            style_map_objects = get_style_map_objects(soup, style)
            doc = kml.Document(styles=[*style_objects, *style_map_objects])
            doc.name = style
            doc.description = folder.find('name').text
            placemarks = get_placemark_objects(folder, style)
            for placemark in placemarks:
                doc.append(placemark)
            kml_file.append(doc)
            print(kml_file.to_string(prettyprint=True))
            # kml_file_option = open(f'{style}.kml', 'wb')
            # kml_file_option.write(kml_file.to_string().encode())
            # kml_file_option.close()
        os.chdir(base_dir)
        bar.next()
    bar.finish()
    print(datetime.now() - start)
