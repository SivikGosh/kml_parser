import re

from get_pictograms import soup


# def get_placemark(soup):
#     placemark_set = set()
#     all_placemarks = soup.find_all('Placemark')
#     for placemark in all_placemarks:
#         placemark_set.add(placemark.find('styleUrl').text)
#     return list(placemark_set)
#
#
# placemarks = get_placemark(soup)
#
# icons = []
# lines = []
# for i in placemarks:
#     if re.search('^#line-', i) is not None:
#         lines.append(i)
#
# sort_icons = sorted(lines)
#
# for i in sort_icons:
#     print(i)
#
# print(get_placemark(soup))


icons ={
    'icon-1001.png': ['#icon-1001', '#icon-1001-labelson', '#icon-1001-labelson-nodesc', '#icon-1001-nodesc'],
    'icon-1002.png': ['#icon-1002', '#icon-1001-labelson', '#icon-1001-labelson-nodesc', '#icon-1001-nodesc'],
}

def get_key(d, value):
    for key, val in d.items():
        if value in val:
            return key


print(get_key(icons, '#icon-1001'))
