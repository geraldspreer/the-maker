#!/usr/bin/env python

import webbrowser as webView
import sys

print "Checking dependencies...\n"

try:
    import wx
    print "wxPython - OK  ","wxVersion:", wx.__version__
except:
    print "you need to have wxPython installed !"
    print "Download it at: http://www.wxpython.org/download.php"
    print "the maker does not run without it !"
    print "Leaving...."    
    sys.exit()

try:
    import markdown2
    print "Markdown2 - OK"
except:
    print "You need to have Markdown2 installed !"
    print "Download it at: http://code.google.com/p/python-markdown2/"
    print "The maker does not run without it !"
    print "Leaving...."    
    sys.exit()

import makerWxGUI
import makerSplash
import makerController
import makerProjectManager
import makerAbout
import makerCopyright
import makerErrorHandler
import makerBugReport
import makerVersion


def afterThisUpdateStatusInfo(func):
    def wrapped(*args, **kwds):
        self = args[0]
        func(*args, **kwds)
        # for now we have to do this check
        try:
            if self.projectController:
                self.projectController.updateStatusInformation()
        except Exception, e:
            print "makerApp"
            print "unable to process: afterThisUpdateInfo", str(e)
    
    return wrapped


class MakerAppController(makerController.SuperController):
         
    def bindActions(self):
        
        self.view.Bind(self.view.wx.EVT_MENU, self.model.viewLicense,  
                       self.view.MenuItemLicense)
            
        self.view.Bind(self.view.wx.EVT_MENU,self.showAboutDialog, 
                  id= self.view.wx.ID_ABOUT)
        
        self.view.Bind(self.view.wx.EVT_MENU, self.model.bugReport,  
                  self.view.MenuItemBugReport)
        
        self.view.Bind(self.view.wx.EVT_MENU, self.model.userFeedback,
                  self.view.MenuItemFeedback)
        
        self.view.Bind(self.view.wx.EVT_MENU, self.model.openProjectWebsite, 
                  self.view.MenuItemWebsite)
        
        self.view.Bind(self.view.wx.EVT_MENU, self.model.getHelp, 
                  self.view.MenuItemTutorial)
        
        self.view.Bind(self.view.wx.EVT_MENU, self.model.learnHTMLandCSS, 
                  self.view.MenuItemLearnHTMLandCSS
                  )
        
                
    def showView(self):
        
        # this is done in the project manager so we can access all
        # info that is needed... especially when saving
        self.model.pm.controller.loadAndSetInterfaceData()
        
        self.view.Show(True)
        self.view.SetTitle("The Maker for OS X - " + str(self.model.getVersion()))
        
        # this following works since model is a wxApp
        self.model.SetTopWindow(self.view)   
        
        
        
    def showAboutDialog(self, evt):
        dlg = makerAbout.MakerAbout(self.view, self.model.getVersion())
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy() 
    


class MakerApp(wx.App):

    def OnInit(self):
        self.showCopyRight()
        
        self.version  = makerVersion.appVersion
        self.author = ['Gerald Spreer', 'Brinick Simmons', 'Ian Barrow']

        self.mySplash = makerSplash.MySplashScreen()
               
        # Splash screen will show by itself
                    
        #wx.InitAllImageHandlers()
        self.mainView = makerWxGUI.create(None)
        
                
        self.appController = MakerAppController(self, self.mainView)
        self.appController.resetAllViews()
        
        # error Handler
        
        self.errorHandler = makerErrorHandler.ErrorHandler(self.mainView)
        sys.stderr = self.errorHandler
        
        # init projectManager
        
        self.pm = makerProjectManager.ProjectManager(self.mainView)
        
        # display GUI
        
        self.appController.showView()        
        
        return True
    
    
    def viewLicense(self, event):
        webView.open('http://www.makercms.org/license/index.htm')
        
    # ------------------------------------------------------------    
    
    def getVersion(self):
        return self.version

    # ------------------------------------------------------------    

    def getAuthors(self):
        return self.author


    def getHelp(self, event=None, topic="#all"):
        """Show http://www.makercms.org/tutorial/#topic in a browser."""
        webView.open("http://www.makercms.org/tutorial/" + topic)

    def bugReport(self, event):
        makerBugReport.report()
        
    def userFeedback(self, event):
        webView.open('http://sourceforge.net/tracker/?func=add&group_id=167680&atid=843919')

    def openProjectWebsite(self, event):
        webView.open('http://www.makercms.org')

    def learnHTMLandCSS(self, event):
        webView.open('http://www.makercms.org/resources/')

   
    def showCopyRight(self):
        print makerCopyright.getCopyright()
        

def main():
    
    application = MakerApp(0)
    application.MainLoop()
        
   
if __name__ == '__main__':
    main()
    
    

    
        

