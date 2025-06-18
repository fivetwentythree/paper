from .exceptions import RequestException, Timeout, TooManyRedirects, SSLError

def get(*args, **kwargs):
    raise RuntimeError("Network access disabled")

def head(*args, **kwargs):
    raise RuntimeError("Network access disabled")
