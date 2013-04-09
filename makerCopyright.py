from datetime import date

def getCopyright():
    
    copyright  = """-------------------------------------------------------------------------------
TheMaker - Content Management System
-------------------------------------------------------------------------------
Copyright (c) 2006 - """ + str(date.today().year) + """

Developers:
Gerald Spreer, Ian Barrow and Brinick Simmons

-------------------------------------------------------------------------------
The Maker is a Content Management System (CMS) for web sites.
Create, edit and preview web sites on your Mac then publish when ready via FTP. 
You stay creative, whilst TheMaker looks after your assets, links and page changes. 

We hope you enjoy using this application as much as we do.

The possibilities are endless.

-------------------------------------------------------------------------------

Visit http://www.makercms.org for more information.

"""
    return copyright
