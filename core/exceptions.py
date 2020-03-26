class Exc(Exception):
    '''Base class for the errors in TRD_scraper'''
    pass


class ElementNotFoundException(Exc):
    def __str__(self):
        return '''Element specified cannot be found. check your xpath/class'''


class NetworkConnectionException(Exc):
    def __str__(self):
        return '''Problem with network occurred. Please check your network connection.'''


class StaleElementException(Exc):
    def __str__(self):
        return '''There is a problem interacting with the selected element. Please check webdriver actions.'''
