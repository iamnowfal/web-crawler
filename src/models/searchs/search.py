import src.models.searchs.error as SearchError
import requests
from bs4 import BeautifulSoup
import uuid
import src.models.searchs.constants as SearchConstants

class Search:

    def __init__(self, title, price, ship_price, url, _id=None):
        self.title = title
        self.price = price
        self.ship_price = ship_price
        self.url = url
        self._id = uuid.uuid4().hex if _id is None else _id


    @staticmethod
    def search(search_terms, place):
        title_results = []
        url_results = []
        tels_results = []
        address_results = []
        rate_results = []
        page = 0

        if search_terms is None or place is None:
            raise SearchError.SearchTermsEmptyError("Search terms and search place cannot be empty")

        while page < SearchConstants.MAX_PAGE:
            url = "http://www.truelocal.com.au/search/{}/{}".format(search_terms, place)
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

