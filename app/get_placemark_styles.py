import re


def get_placemark_styles(soup):
    """получение списка уникальных стилей объектов"""
    styles = set()
    all_placemarks = soup.find_all('Placemark')
    for placemark in all_placemarks:
        style_url = placemark.find('styleUrl').text
        reg_line = 'line-[0-9A-F]{6}-[0-9]{4}'
        reg_icon = 'icon-[0-9]{3}-[0-9A-F]{6}|icon-[0-9]{4}'
        reg_ex = f'({reg_line}|{reg_icon})'
        styles.add(re.search(reg_ex, style_url).group(0))
    with open('styles.py', 'w') as s:
        s.write(f'unique_styles = {str(list(styles))}')
    return None
