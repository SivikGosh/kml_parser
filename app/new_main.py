import os
from datetime import datetime

from get_placemark_styles import get_placemark_styles
from souping_file import base_dir, soup
from styles import unique_styles
from legend import legend
import asyncio
import re
import requests


def get_line_width(soup, place_style):
    all_styles = soup.find_all('Style')
    for style in all_styles:
        if ('line' in place_style) and (place_style in style.attrs['id']):
            return style.find('width').text


def create_placemark_folder(soup, style):
    w = get_line_width(soup, style)
    if 'line' in style:
        file_name = f'{legend[style]}_width_{w}'
    else:
        file_name = legend[style]
    if not os.path.isdir(file_name):
        os.mkdir(file_name)
    os.chdir(file_name)
    return None


def get_photo_urls(soup, style):
    all_placemarks = soup.find_all('Placemark')
    photos = []
    for placemark in all_placemarks:
        placemark_style_url = placemark.find('styleUrl').text
        if f'#{style}' in placemark_style_url:
            if placemark.find('ExtendedData'):
                value = placemark.find('value').text
                url = re.search('https:(.)+fife', value).group(0)
                photos.append(url)
    return photos


async def download_photos(photos, style):
    if 'line' in style:
        w = get_line_width(soup, style)
        file_name = f'{legend[style]}_width_{w}'
    else:
        file_name = legend[style]

    if not os.path.isdir('photo'):
        os.mkdir('photo')

    os.chdir('photo')
    for photo in photos:
        print(photo)
        response = requests.get(photo)
        # потом можно удалить
        print(response.status_code)
        # # # # # # # # # # #
        with open(f'{file_name}.png', 'wb') as photo:
            photo.write(response.content)
            photo.close()

    return None


async def main(style):
    create_placemark_folder(soup, style)
    photos = get_photo_urls(soup, style)
    if len(photos) > 0:
        task1 = asyncio.create_task(download_photos(soup, style))
        await task1


if __name__ == '__main__':
    start_time = datetime.now()
    placemark_count = 0

    get_placemark_styles(soup)

    os.chdir(base_dir)
    folder_name = soup.find('name').text
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    os.chdir(folder_name)
    for style in unique_styles:
        asyncio.run(main(style))
        os.chdir('../')

    print('Время выполнения', datetime.now() - start_time)
