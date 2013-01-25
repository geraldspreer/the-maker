import urllib2


def check():
    """
    check internet connection 
    
    returns True or False
    """
    try:
        urllib2.urlopen("http://www.google.com", data=None)
        return True
    except Exception, e:
        return False