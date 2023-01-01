# from fastkml import kml
from get_pictograms import open_input_file
from progress.bar import PixelBar


def get_objects_styles(soup):
    styles = set()
    bar = PixelBar(max=len(soup.Folder.find_all('Placemark')))
    for i in range(len(soup.Folder.find_all('Placemark'))):
        styles.add(soup.Folder.find_all('Placemark')[i].styleUrl.string)
        bar.next()
    bar.finish()
    return list(styles)


if __name__ == '__main__':
    base_dir, input_file, soup = open_input_file()
    styles = get_objects_styles(soup)
    print(styles)
