import re

from souping_file import soup

# # # забираем список уникальных стилей объектов # # # # # # # # # # # # # # #

all_styles = soup.find_all('Placemark')
array_set = set()
for i in all_styles:
    reg = '(line-[0-9A-F]{6}-[0-9]{4}|icon-[0-9]{3}-[0-9A-F]{6}|icon-[0-9]{4})'
    style_url = i.find('styleUrl').text
    array_set.add(re.search(reg, style_url).group())

# # # создаём отсортированные словари и записываем в файлы # # # # # # # # # #

# sort_arrey = sorted(array_set)
# for i in sort_arrey:
#     if 'icon' in i:
#         with open('icons.txt', 'a') as j:
#             j.write("'")
#             j.write(re.search('[-0-9A-Za-z]+', i).group())
#             j.write("': '',")
#             j.write('\n')
#     if 'line' in i:
#         with open('line.txt', 'a') as j:
#             j.write("'")
#             j.write(re.search('[-0-9A-Za-z]+', i).group())
#             j.write("': '',")
#             j.write('\n')

print(len(array_set))

# # # ширина стилей # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

all_style_obj = soup.find_all('Style')
widths = []
for i in all_style_obj:
    if 'line' in i['id']:
        widths.append(i.find('width').text)

print(widths)