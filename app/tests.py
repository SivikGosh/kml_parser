# icons ={
#     'icon-1001.png': ['#icon-1001', '#icon-1001-labelson', '#icon-1001-labelson-nodesc', '#icon-1001-nodesc'],
#     'icon-1002.png': ['#icon-1002', '#icon-1001-labelson', '#icon-1001-labelson-nodesc', '#icon-1001-nodesc'],
# }
#
# def get_key(d, value):
#     for key, val in d.items():
#         if value in val:
#             return key
#
#
# print(get_key(icons, '#icon-1001'))

# with open('i_sort.txt', encoding='utf-8') as n:
#     name = n.read().split('\n')

# for i in name:
#     dictionary.setdefault(i, [])

# print(name)

from get_pictograms import soup

# print(soup.find('Style', id=f'line-000000-1000-highlight').find('width').text)
# array = []
# for i in styles:
#     try:
#         # print(i.find('value').text)
#         array.append(i.find('value').text)
#         print(i.find('name').text)
#     except Exception:
#         print('No value')

# for i in styles:
#     linestyles = i.find_all('LineStyle')
#     for j in linestyles:
#         print(j.find('width'))

# print(array)

# with open('id иконок (новое).txt', encoding='utf-8') as n:
#     name = n.read().split('\n')
#     print(len(name))
import re

all_styles = soup.find_all('Placemark')
array_set = set()

for i in all_styles:
    array_set.add(re.search('(line-[0-9A-F]{6}-[0-9]{4}|icon-[0-9]{3}-[0-9A-F]{6}|icon-[0-9]{4})', i.find('styleUrl').text).group())

# print(array_set)

sort_arrey = sorted(array_set)

for i in sort_arrey:
    if 'icon' in i:
        with open('icons.txt', 'a') as j:
            j.write("'")
            j.write(re.search('[-0-9A-Za-z]+', i).group())
            j.write("': '',")
            j.write('\n')
