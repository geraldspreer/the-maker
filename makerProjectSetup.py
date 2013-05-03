import wx
from makerWidgets import MakerDialog
import makerFtpBrowser
import makerCheckInternetConnection

# Decorator
def checkFtpSettings(func):
    """Tests if FTP Host, FTP User and FTP Root are OK."""
    def wrapper(self, evt):
        if "not set" in [self.ftp_host.GetValue(),
                         self.ftp_user.GetValue(),
                         self.ftp_root.GetValue()]:            
            self.controller.errorMessage('"not set" is an illegal FTP value!')
            self.Close()
            evt.Skip()
            return
        
        root = self.ftp_root.GetValue()
        newroot = root
        if not root.startswith('/'):            
            newroot = '/' + root
            self.ftp_root.SetValue(newroot)

        if not newroot.endswith('/'):
            newroot += '/'
            self.ftp_root.SetValue(newroot)

        passw = self.controller.model.getRemotePassword()
        result =  self.controller.actionTestFtp(self.ftp_host.GetValue(),
                                                self.ftp_user.GetValue(),
                                                self.ftp_root.GetValue(),
                                                passw)

        
        if result: 
            return func(self, evt)
        
        self.controller.errorMessage(result)
        evt.Skip()
        return

    return wrapper

# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------

class ProjectSetup(MakerDialog):
    def __init__(self, parent, controller):
        """parent is the main GUI. controller refers to makerController."""        
        self.parent     = parent
        self.controller = controller
        self.projectModel = controller.model
        self.createDialog(parent)
        self.choices_sprache  = ['en', 'de']
        self.choices_add_lang = ['en', 'de', 'None']               
        self.saved = None
        self.keepGoodPassword(None)

    def createDialog(self, prnt):
	MakerDialog.__init__(self,
                             {'name'       : 'ProjectSetup',
                              'parent'     : prnt, 
                              'pos'        : wx.Point(439, 179), 
                              'size'       : wx.Size(394, 380),
                              'style'      : wx.DEFAULT_DIALOG_STYLE, 
                              'title'      : 'Setup FTP Connection...',
                              'clientSize' : wx.Size(394, 355),
                              'centerPos'  : wx.BOTH})

#        self.sprache = self.add('choice', 
#                                {'choices' : ['en', 'de'],
#                                 'name'    : 'sprache_choice',
#                                 'parent'  : self,
#                                 'pos'     : wx.Point(232, 32),
#                                 'size'    : wx.Size(130, 21),
#                                 'style'   : 0
#                                 })

#        self.add_language = self.add('choice', 
#                                     {'choices' : ['en', 'de', 'None'],
#                                      'name'    : 'add_lang_choice',
#                                      'parent'  : self,
#                                      'pos'     : wx.Point(232, 72),
#                                      'size'    : wx.Size(130, 21),
#                                      'style'   : 0
#                                      })

        self.ftp_host = self.add('textCtrl', 
                                 {'name'   : 'ftp_host_ctl',
                                  'parent' : self,
                                  'pos'    : wx.Point(136, 116),
                                  'size'   : wx.Size(232, 21),
                                  'style'  : 0,
                                  'value'  : 'www.myhost.com'
                                  })

        self.ftp_user = self.add('textCtrl', 
                                 {'name'   : 'ftp_user_ctl',
                                  'parent' : self,
                                  'pos'    : wx.Point(136, 156),
                                  'size'   : wx.Size(232, 21),
                                  'style'  : 0,
                                  'value'  : 'ftpuser'
                                  })
        
        self.browse_server = self.add('button', 
                                      {'label'   : 'Browse',
                                       'name'    : 'browse',
                                       'parent'  : self,
                                       'pos'     : wx.Point(280, 190),
                                       'size'    : wx.Size(80, 23),
                                       'style'   : 0,
                                       'handler' : self.onBrowseButton
                                       })
        
        self.ftp_root = self.add('textCtrl', 
                                 {'name'   : 'ftp_root_ctl',
                                  'parent' : self,
                                  'pos'    : wx.Point(136, 196),
                                  'size'   : wx.Size(132, 21),
                                  'style'  : 0,
                                  'value'  : '/path_to_my_project/'
                                  })

        #self.ftp_root.Enable(False)

        self.url = self.add('textCtrl', 
                            {'name'   : 'url_ctl',
                             'parent' : self,
                             'pos'    : wx.Point(136, 238),
                             'size'   : wx.Size(232, 21),
                             'style'  : 0,
                             'value'  : 'http://www.myurl.com'
                             })
        
        self.cancel = self.add('button',
                               {'label'   : 'Cancel',
                                'name'    : 'cancel',
                                'parent'  : self,
                                'pos'     : wx.Point(208, 308),
                                'size'    : wx.Size(75, 23),
                                'style'   : 0,
                                'handler' : self.onCancelButton
                                })

        self.Ok = self.add('button',
                           {'label'   : 'OK',
                            'name'    : 'ok',
                            'parent'  : self,
                            'pos'     : wx.Point(296, 308),
                            'size'    : wx.Size(75, 23),
                            'style'   : 0,
                            'handler' : self.onOkButton
                            })

#        self.staticLine1 = self.add('staticLine',
#                                    {'name'   : 'staticLine1',
#                                     'parent' : self, 
#                                     'pos'    : wx.Point(24, 128),
#                                     'size'   : wx.Size(336, 2), 
#                                     'style'  : 0})
        
        self.gfx_label = self.add('staticText',
                                  {'label'  : 'Name for remote graphics folder:',
                                   'name'   : 'gfx_label',
                                   'parent' : self, 
                                   'pos'    : wx.Point(24, 24),
                                   'size'   : wx.Size(230, 18), 
                                   'style'  : 0})
        
        self.gfxFolder = self.add('textCtrl',
                                  {'name'   : 'rem_gfx_folder',
                                   'parent' : self,
                                   'pos'    : wx.Point(136, 54),
                                   'size'   : wx.Size(232, 21),
                                   'style'  : 0,
                                   'value'  : ''
                                   })
        
        self.staticLine1 = self.add('staticLine',
                                    {'name'   : 'staticLine1',
                                     'parent' : self,
                                     'pos'    : wx.Point(24, 90),
                                     'size'   : wx.Size(336, 2),
                                     'style'  : 0})
    
        self.help = self.add('button',
                             {'label'   : 'Help',
                              'name'    : 'help',
                              'parent'  : self,
                              'pos'     : wx.Point(16, 308),
                              'size'    : wx.Size(75, 23),
                              'style'   : 0,
                              'handler' : self.onHelpButton
                              })

#        self.staticText1 = self.add('staticText',
#                                    {'label'  : 'Project language:',
#                                     'name'   : 'staticText1',
#                                     'parent' : self,
#                                     'pos'    : wx.Point(24, 40),
#                                     'size'   : wx.Size(122, 20),
#                                     'style'  : 0})

        self.staticText3 = self.add('staticText',
                                    {'label'  : 'FTP Host:',
                                     'name'   : 'staticText3',
                                     'parent' : self,
                                     'pos'    : wx.Point(24, 116),
                                     'size'   : wx.Size(99, 20),
                                     'style'  : 0})

        self.staticText4 = self.add('staticText',
                                    {'label'  : 'FTP User:',
                                     'name'   : 'staticText4',
                                     'parent' : self,
                                     'pos'    : wx.Point(24, 156),
                                     'size'   : wx.Size(106, 20),
                                     'style'  : 0})

        self.staticText6 = self.add('staticText',
                                    {'label'  : 'Path to Project:',
                                     'name'   : 'staticText6',
                                     'parent' : self,
                                     'pos'    : wx.Point(24, 196),
                                     'size'   : wx.Size(100, 20),
                                     'style'  : 0})

        self.staticText7 = self.add('staticText',
                                    {'label'  : 'Project url:',
                                     'name'   : 'staticText7',
                                     'parent' : self,
                                     'pos'    : wx.Point(24, 238),
                                     'size'   : wx.Size(100, 20),
                                     'style'  : 0})

#        self.staticText2 = self.add('staticText',
#                                    {'label'  : 'Additional language:',
#                                     'name'   : 'staticText2',
#                                     'parent' : self,
#                                     'pos'    : wx.Point(24, 80),
#                                     'size'   : wx.Size(165, 20),
#                                     'style'  : 0})

    # ------------------------------------------------------------

    def setValues(self, theInformation):
        """Information is a dictionary with the current Projects information"""
        #print "updating project setup information"
        
        #self.sprache.SetSelection(self.choices_sprache.index(theInformation['sprache']))
        #self.add_language.SetSelection(self.choices_add_lang.index(theInformation['add_language']))
        self.ftp_host.SetValue(theInformation['ftp_host'])
        self.ftp_user.SetValue(theInformation['ftp_user'])
        self.ftp_root.SetValue(theInformation['ftp_root'])
        self.gfxFolder.SetValue(theInformation['gfx_folder'])
        self.url.SetValue(theInformation['url'])
        self.theInformation = theInformation # save for later

    # ------------------------------------------------------------
    # BUTTON BOUND METHODS
    # ------------------------------------------------------------

    def doFTPCheck(self):
        if "not set" in [self.ftp_host.GetValue(),
                         self.ftp_user.GetValue(),
                         self.ftp_root.GetValue()]:            
            self.controller.errorMessage('"not set" is an illegal FTP value!')
                        
            return False
        
        root = self.ftp_root.GetValue()
        newroot = root
#        if not root.startswith('/'):            
#            newroot = '/' + root
#            self.ftp_root.SetValue(newroot)

        if not newroot.endswith('/'):
            if not newroot == ".":
                newroot += '/'
                self.ftp_root.SetValue(newroot)
        
        if self.getGoodPassword() != None:
            passw = self.getGoodPassword()
        else:
            passw = self.controller.password("Please enter FTP password...")
        
        if passw != None:
        
            result =  self.projectModel.testFtp(self.ftp_host.GetValue(),
                                                    self.ftp_user.GetValue(),
                                                    self.ftp_root.GetValue(),
                                                    passw)
        
            
            if result==True:
                # lets keep this one since it worked
                self.keepGoodPassword(passw)
                self.projectModel.setRemotePassword(passw)
                return True
            
            else:
                
                return result
        
        else:
            # if we return false the password dialog disappears and the check is 
            # cancelled
            return False
        
        



    
    
    def keepGoodPassword(self, passw):
        self.goodPassword = passw
        
    def getGoodPassword(self):
        return self.goodPassword
    
    #@checkFtpSettings
    #
    # Gerald : I did not use the decorator since it was better to have
    # doFTPCheck return True or an error message
    #
    
    def onOkButton(self, event):                
        
        if not makerCheckInternetConnection.check():
           
            self.controller.infoMessage("No Internet Connection! Unable to test settings!")
            self.saved = False
            self.Close()
            
            
        else:
            
            result = self.doFTPCheck()
            if result != True:
                if result != False:
                    self.controller.errorMessage(str(result))
                return
            
        #self.theInformation["sprache"]      = self.choices_sprache[self.sprache.GetSelection()]
        #self.theInformation["add_language"] = self.choices_add_lang[self.add_language.GetSelection()]
        
            self.theInformation["ftp_host"] = self.ftp_host.GetValue()
            self.theInformation["ftp_user"] = self.ftp_user.GetValue()
            self.theInformation["ftp_root"] = self.ftp_root.GetValue()
    
            value = self.gfxFolder.GetValue()
                        
            # make sure it is just a foldername
            
            if "/" in value:
                if value.count("/") == 1 and value.endswith("/"):
                    pass
                else:
                    self.controller.errorMessage("The image folder is just a NAME for a folder, not a path.")
                    return
            if value == "":
                self.controller.errorMessage('"Name for remote graphics folder:" cannot be empty!')
                return
            
            bad = [" ", "."]
            for x in bad:
                if x in value:
                    self.controller.errorMessage('Please do not use . or spaces in the "Name for remote graphics folder:" field!')
                    return
                           
            self.theInformation["gfx_folder"] = value
            
            self.gfxFolder.SetValue(value)
            
            self.theInformation["url"]= self.url.GetValue()
            if not self.url.GetValue().endswith('/'):
                self.theInformation["url"] = self.url.GetValue() + '/'
         
            self.saved = True
            self.Close()
            self.controller.model.setRemotePassword(self.getGoodPassword())
            event.Skip()

    # ------------------------------------------------------------

    
    def onBrowseButton(self, event):        
        
        if not makerCheckInternetConnection.check():
           
            self.controller.infoMessage("Unable to browse remote server! No internet connection! ")
            return
        
        
        passw = self.controller.password()
        if not passw:
            return
        
        self.ftpBrowser = makerFtpBrowser.FTPBrowser(self.parent)
        
        if not self.ftpBrowser.ftpBrowserAction_connect_(self.ftp_host.GetValue(),
                                                         self.ftp_user.GetValue(),
                                                         self.ftp_root.GetValue(),
                                                         passw):
            return None
        self.keepGoodPassword(passw)
        self.ftpBrowser.ftpBrowserAction_ls_()
        
        pathName = self.ftpBrowser.ftpBrowserShow()
        
        if pathName:
            self.ftp_root.SetValue(pathName) 
        event.Skip()

    # ------------------------------------------------------------

    def onCancelButton(self, event):
        self.saved = False
        self.Close()
        event.Skip()

    # ------------------------------------------------------------

    def onHelpButton(self, event):
        self.projectModel.help('#setup')
        event.Skip()
    
    # ------------------------------------------------------------
    
            

