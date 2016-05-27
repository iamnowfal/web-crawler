import requests
from bs4 import BeautifulSoup
import uuid
import src.models.searchs.constants as SearchConstants

class Search:

    def __init__(self, search_terms, _id=None):
        self.search_terms = search_terms
        self._id = uuid.uuid4().hex if _id is None else _id

    def search_google(self):
        page = 1
        while page < SearchConstants.MAX_PAGE:
            start = page * 10
            url = 'https://www.google.com.au/search?q={}&start={}'.format(self.search_terms, start)
            source_code = requests.get(url)


    def search_bing(self):
        pass
