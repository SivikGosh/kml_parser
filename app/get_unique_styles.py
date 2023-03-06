import re
import os
from souping_file import base_dir, soup


def get_placemark_styles(soup):
    """список уникальных стилей объектов папки"""
    styles = set()
    all_placemarks = soup.find_all('Placemark')
    for placemark in all_placemarks:
        style_url = placemark.find('styleUrl').text
        reg_line = 'line-[0-9A-F]{6}-[0-9]{4}'
        reg_icon = 'icon-[0-9]{3}-[0-9A-F]{6}|icon-[0-9]{4}'
        reg = f'({reg_line}|{reg_icon})'
        styles.add(re.search(reg, style_url).group(0))
    return list(styles)


if __name__ == '__main__':
    styles = get_placemark_styles(soup)
    os.chdir(base_dir)
    with open('styles.py', 'a') as s:
        s.write(f'unique_styles = {str(styles)}')
