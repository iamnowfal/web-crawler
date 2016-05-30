import src.models.searchs.error as SearchError
import requests
from bs4 import BeautifulSoup
import uuid
import src.models.searchs.constants as SearchConstants
from src.common.database import Database

class Search:

    def __init__(self, title, tel, address, url, rates, search_term, place, active=False, username=None, _id=None):
        self.title = title
        self.address = address
        self.url = url
        self.tel = tel
        self.rates = rates
        self.search_term = search_term
        self.place = place
        self.active = active
        self.username = username
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            'title':self.title,
            'tel':self.tel,
            'address':self.address,
            'url':self.url,
            'rates':self.rates,
            'search_term':self.search_term,
            'place':self.place,
            'active':self.active,
            'username':self.username,
            '_id':self._id

        }

    def save_to_mongo(self):
        Database.update(SearchConstants.COLLECTION, {'title':self.title}, self.json())

    @classmethod
    def find_by_username(cls, username):
        return [cls(**elm) for elm in Database.find(SearchConstants.COLLECTION, {'username':username})]

    @classmethod
    def find_by_title(cls, title):
        return cls(**Database.find_one(SearchConstants.COLLECTION, {'title':title}))

    @classmethod
    def find_by_url(cls, url):
        return [cls(**elm) for elm in Database.find(SearchConstants.COLLECTION, {'url':url})]

    @classmethod
    def find_by_username_active(cls, username):
        return [cls(**elm) for elm in Database.find(SearchConstants.COLLECTION, {'username':username,'active':True})]

    @classmethod
    def find_by_search(cls, search_term, place):
        return [cls(**elm) for elm in Database.find(SearchConstants.COLLECTION, {'search_term':search_term,
                                                                                 'place':place})]

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    @staticmethod
    def search(search_terms, place):
        title_results = []
        url_results = []
        tels_results = []
        address_results = []
        rate_results = []
        page = 1

        if search_terms is None or place is None:
            raise SearchError.SearchTermsEmptyError("Search terms and search place cannot be empty")

        while page <= SearchConstants.MAX_PAGE:
            url = "http://www.truelocal.com.au/search/{}/{}/{}".format(search_terms, place, page)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            g_data = soup.find_all("div", {"class" : "search-result"})

            for item in g_data:
                titles=item.find_all("span", {"class":"name"})[0].text
                tels=item.find_all("a")[1].text
                urls=item.find_all("span", {"class":"name"})[0].find_all("a")
                address=item.find_all("span", {"class":"address secondary no-mobile"})[0].text
                rates=item.find_all("span", {"class":"ui-rating ui-rating-disabled ui-rating-star-small"})

                for rates in rates:
                    rate_results.append(rates.get('data-listing-rating'))

                for urls in urls:
                    url_results.append(urls.get('href'))
                tels_results.append(tels)
                title_results.append(titles)
                address_results.append(address)

            page += 1
        return (title_results, tels_results, url_results, address_results, rate_results)

