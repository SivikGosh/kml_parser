from bs4 import BeautifulSoup

with open('test.kml', 'r') as file:
    soup = BeautifulSoup(file, 'xml')

styles = soup.find_all('Style')

print(styles[0])
