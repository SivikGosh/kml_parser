import re
import wsgiref.validate

import requests
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

# print(len(array_set))

# # # ширина стилей # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

all_style_obj = soup.find_all('Style')
widths = []
for i in all_style_obj:
    if 'line' in i['id']:
        widths.append(i.find('width').text)

# print(widths)

from selenium import webdriver
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10.0)
driver.maximize_window()
driver.get('https://doc-0k-as-mymaps.googleusercontent.com/untrusted/hostedimage/h1f3qom2nr9qorbo80tgc4uc6o/u1e0kg736t78n6vunjtd1mu3dk/1675695043750/FbB9bBXSolslE3bMVbGlJkDEGdDnLqk5/11787502090270993270/5AI-xGzzV5SUhrTOqR28ZjQMxyqXCPQQdZCL1_zsV1RTadpJvsA5dXt2NJ1xNO9hgKj5DtUofrRx_NdamS8KqLF3re3bDWeEH0HBIyhUhOm_go_G1hG7QwF0cfbb1XG2tBbFSemNKlb3-GE_nvMxSd3kso9FAosjsHJUMjYCjcmEwbpdoFnF9T8q-9JH0u4vxhScOsGo?session=0&fifehttps://doc-0k-as-mymaps.googleusercontent.com/untrusted/hostedimage/h1f3qom2nr9qorbo80tgc4uc6o/bjdeohkppb65ar16u955eaqn4c/1675695043750/FbB9bBXSolslE3bMVbGlJkDEGdDnLqk5/11787502090270993270/5AI-xGzxKLQ1ZmLLzYErrE6sCmOoQ8VNgnDfihWBolk9SOq7iZpEDwncHgiU_SHIN1pblqVlb-HN_8RInkTIhfdjZVo7Rx8QyxmvjfhNxlsLtBkvRWEdH1_gceyaPnhxqujEEd54cQmSvMALeefSausO3zOVab6cZ3iOZTz7vOVrVgZjrWHJFsaYrHS7qnO6g8B14Cbc?session=0&fifehttps://doc-0c-as-mymaps.googleusercontent.com/untrusted/hostedimage/h1f3qom2nr9qorbo80tgc4uc6o/bd9ctikm9ma1c502tkmtfa7b3o/1675695043750/FbB9bBXSolslE3bMVbGlJkDEGdDnLqk5/11787502090270993270/5AI-xGzy7aLP7YHGwR9b2ZpUe_9SgtaAnt4bkhv98wrfebS0QP8JfiBVg6CcYaPLhwJ6wYqiXSQXSEnhxjdyXSYwBYWSAloAW4LEay_7k3asN7BBuyFyWG5QPGyQ0_fye2VwEeg07_1V-tPeyFXzPspS8orh5GPS1ymBNE0XH3r4sEKxDPTUOTbCwH1Pk_fEwef0fy2Y?session=0&fifehttps://doc-0o-as-mymaps.googleusercontent.com/untrusted/hostedimage/h1f3qom2nr9qorbo80tgc4uc6o/s1a0gelq8qbbgltp8qpin1ctb4/1675695043750/FbB9bBXSolslE3bMVbGlJkDEGdDnLqk5/11787502090270993270/5AI-xGzy9VEYJJKHlCM9jlZIaePrhq06-q1qSNATN7z425N_-AAEfHHTXu08bfRTA2hqgQPoFR3LiKfZB_UxJh4FpM5RINFZ7e5NDGhQ5bVp9t7m_TN11ZrRl_5FOrNCkL-MXXTCQKIEY5DeMPxj9GWvssmY7RtZ1T9XO6iJmhQte0KOCuoErVe60faIFrLv7Zm2uTK1g?session=0&fife')
with open('image.png', 'wb') as image:
    i = driver.find_element(by=By.TAG_NAME, value='img')
    image.write(i.screenshot_as_png)
driver.quit()
