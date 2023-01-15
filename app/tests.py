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

style = soup.find('Style')
print(style.attrs['id'])

# with open('id иконок.txt', encoding='utf-8') as n:
#     name = n.read().split('\n')
#     print(len(name))
