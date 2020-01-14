class Exc(Exception):
    '''Base class for the errors in TRD_scraper'''
    pass


class ElementNotFoundException(Exc):
    def __str__(self):
        return '''Element specified cannot be found. check your xpath/class'''
