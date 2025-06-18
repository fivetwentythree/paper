class RequestException(Exception):
    pass
class Timeout(RequestException):
    pass
class TooManyRedirects(RequestException):
    pass
class SSLError(RequestException):
    pass
