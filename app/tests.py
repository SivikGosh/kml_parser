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

styles = soup.find_all('Placemark')
# array = []
# for i in styles:
#     try:
#         # print(i.find('value').text)
#         array.append(i.find('value').text)
#         print(i.find('name').text)
#     except Exception:
#         print('No value')

for i in styles:
    print(i.find('LineString'))

# print(array)

# with open('id иконок (новое).txt', encoding='utf-8') as n:
#     name = n.read().split('\n')
#     print(len(name))
