from urllib.parse import urlparse

def url_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    
    except AttributeError:
        return False
