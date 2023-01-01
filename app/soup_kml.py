class SoupKML:
    def __init__(self, soup):
        self.soup = soup

    def get_all_tags(self, tagname):
        return self.soup.find_all(tagname)
