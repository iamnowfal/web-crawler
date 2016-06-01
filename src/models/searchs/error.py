class SearchError:
    def __init__(self,message):
        self.message = message

class SearchTermsEmptyError(SearchError):
    pass