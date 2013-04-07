from datetime import date

def getCopyright():
    
    copyright  = """-------------------------------------------------------------------------------
the maker - Content Management System
-------------------------------------------------------------------------------
Copyright (c) 2006 - """ + str(date.today().year) + """, the makerProject

Developers:
Gerald Spreer, Ian Barrow and Brinick Simmons

-------------------------------------------------------------------------------
The maker is a CMS for websites. You use it on your Mac and after you 
made your changes you publish to your webhosting service via FTP. 

We hope you enjoy using this application as much as we do.

The possibilities are endless.

-------------------------------------------------------------------------------

Visit http://www.makercms.org for more information.

"""
    return copyright
