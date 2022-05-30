import urllib2

def check():
    """
    Check internet connection
    """
    try:
        urllib2.urlopen("https://www.google.com", data=None)
        return True
    except Exception, e:
        return False
