import wx
from makerWidgets import MakerDialog
import makerFtpTools
import os

class FTPBrowser(MakerDialog):
    def __init__(self, parent):
        print 'initializing ftp Browser...'
        
        self.saved = False
        
        
        self.parent = parent
        self.createDialog(self.parent)
        self.pathname = None

    # ------------------------------------------------------------

    def createDialog(self, prnt):
	MakerDialog.__init__(self,
                             {'name'       : 'ftpBrowser',
                              'parent'     : prnt, 
                              'pos'        : wx.Point(441, 187), 
                              'size'       : wx.Size(387, 501),
                              'style'      : wx.DEFAULT_DIALOG_STYLE, 
                              'title'      : 'FTP Browser',
                              'clientSize' : wx.Size(387, 501),
                              'centerPos'  : wx.BOTH})


        # ----- LIST BOX -----
        self.listBox = self.add('listbox', {'choices' : [],
                                            'name'    : 'listBox',
                                            'parent'  : self,
                                            'pos'     : wx.Point(0, 53),
                                            'size'    : wx.Size(385, 352),
                                            'style'   : 0,
                                            'handler' : self.ftpBrowserAction_select_})

	# ----- WINDOW 1 -----
        self.win1 = self.add('window', {'name'   : 'win1',
                                        'parent' : self,
                                        'pos'    : wx.Point(0, 0),
                                        'size'   : wx.Size(387, 50),
                                        'style'  : 0
                                        })
        
	# ----- WINDOW 2 -----
        self.win2 = self.add('window', {'name'   : 'win2',
                                        'parent' : self,
                                        'pos'    : wx.Point(0, 405),
                                        'size'   : wx.Size(387, 50),
                                        'style'  : 0
                                        })

	# ----- OK BUTTON -----
        self.OKbutton = self.add('button', {'label'   : 'OK',
                                            'name'    : 'OK', 
                                            'parent'  : self.win2, 
                                            'pos'     : wx.Point(290, 60),
                                            'size'    : wx.Size(75, 25), 
                                            'style'   : 0,
                                            'handler' : self.ftpBrowserAction_Ok_})
        
	# ----- CANCEL BUTTON -----
        self.cancelButton = self.add('button', {'label'   : 'Cancel',
                                                'name'    : 'cancel', 
                                                'parent'  : self.win2, 
                                                'pos'     : wx.Point(200, 60),
                                                'size'    : wx.Size(80, 25), 
                                                'style'   : 0,
                                                'handler' : self.ftpBrowserAction_cancel_})


	# ----- NEW FOLDER BUTTON -----
        self.newFolderButton = self.add('button', {'label'   : 'New Folder',
                                                   'name'    : 'newfolder', 
                                                   'parent'  : self.win1, 
                                                   'pos'     : wx.Point(280, 16),
                                                   'size'    : wx.Size(90, 25), 
                                                   'style'   : 0,
                                                   'handler' : self.ftpBrowserAction_newFolder_})

	# ----- DELETE BUTTON -----
        self.deleteButton = self.add('button', {'label'   : 'Delete',
                                                'name'    : 'delete', 
                                                'parent'  : self.win1, 
                                                'pos'     : wx.Point(200, 16),
                                                'size'    : wx.Size(75, 25), 
                                                'style'   : 0,
                                                'handler' : self.ftpBrowserAction_delete_})

	# ----- HELP BUTTON -----
        self.helpButton = self.add('button', {'label'   : 'Help',
                                              'name'    : 'help', 
                                              'parent'  : self.win2, 
                                              'pos'     : wx.Point(8, 60),
                                              'size'    : wx.Size(75, 25), 
                                              'style'   : 0,
                                              'handler' : self.onHelpButton})

	# ----- UP BUTTON -----
        self.upButton = self.add('button', {'label'   : 'Up',
                                            'name'    : 'up', 
                                            'parent'  : self.win1, 
                                            'pos'     : wx.Point(8, 16),
                                            'size'    : wx.Size(75, 25), 
                                            'style'   : 0,
                                            'handler' : self.ftpBrowserAction_up_})

        self.createSizers()

    # ------------------------------------------------------------    

    def createSizers(self):
        self.boxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.boxSizer.AddWindow(self.win1, 0, border=0, flag=wx.FIXED_MINSIZE)
        self.boxSizer.AddWindow(self.listBox, 0, border=0, flag=wx.GROW)
        self.boxSizer.AddWindow(self.win2, 1, border=0, flag=wx.FIXED_MINSIZE)

        self.SetSizer(self.boxSizer)
    
    # ------------------------------------------------------------    

    def fillList(self, theList):
        items = self.listBox.GetCount()
        for i in range(items):
            self.listBox.Delete(0)
            
        for i in range(len(theList)):
            self.listBox.Append(theList[i])
            self.list = theList # save the list for later use
            # make sure the first item in the list is visible
            self.listBox.EnsureVisible(0)

    # ------------------------------------------------------------

    


    # ------------------------------------------------------------         
    
    def onHelpButton(self, event):
        m  = 'You can browse your server here as well as create/delete folders.'
        m += "It is also possible to delete files..."
        self.parent.Message(m)   

    
    def ftpBrowserAction_ls_(self):
        """Fills the ftpbrowser's listbox."""
        self.parent.busy()
        self.list = self.ftp_tools.ls()
        
        if self.ftp_tools.pwd()==self.start:
            try:
                self.list.remove('..')
            except:
                print 'seems like really root'
        
        self.fillList(self.list)
        self.parent.relax()
    # ------------------------------------------------------------     
    
    def ftpBrowserAction_Ok_(self, event):
    
        if self.listBox.GetSelection() == -1:
            # 'no selection - taking current'
            string = self.ftp_tools.pwd()
        else:
            # 'there is a selection...'
            if self.ftp_tools.isdir(self.list[self.listBox.GetSelection()]):
                # let's see if this works 
                string = self.ftp_tools.pwd() +"/"+ self.list[self.listBox.GetSelection()]
            else:
                
                string = self.ftp_tools.pwd()    
                
        
            
        self.pathname = string     
        self.saved = True
        self.Close()
        
    # ------------------------------------------------------------     
    
    def ftpBrowserAction_delete_(self, event):

        if self.listBox.GetSelection() == -1:
            self.parent.Error('Please select an item')
            return
            
        theDir = self.list[self.listBox.GetSelection()]
        if self.ftp_tools.isfile(self.ftp_tools.pwd(), theDir):
            
            answer = self.parent.Ask('Do you really want to delete %s?' % theDir)
            if answer == 'Ok':
                
                res = self.ftp_tools.deleteFile(self.ftp_tools.pwd() + "/" + theDir)
                if res != True:
                    self.parent.Error("Unable to delete file:\n" + str(res))
                    
                
            
        else:
            answer = self.parent.Ask('Do you really want to delete %s ?' % theDir)
            if answer == 'Ok':
                
                result = self.ftp_tools.rmd(theDir)
                if result != True:
                    self.parent.Error("Unable to delete folder:\n" + result)
            
        self.ftpBrowserAction_ls_()

    # ------------------------------------------------------------     
        
    def ftpBrowserAction_newFolder_(self, event):
        result = self.parent.Input('Please enter a name for the new folder:')
        if result=="Null":
            return

        try:
            self.ftp_tools.mkd(result)
            self.ftpBrowserAction_ls_()
        except Exception, e:
            self.parent.Error("unable to create new folder!")

    # ------------------------------------------------------------     

    def ftpBrowserAction_select_(self, event):
        item = self.listBox.GetSelection()
        
        target = self.list[item]
        
        try:
            self.ftp_tools.cd(target)
        except:
            print "this is not a dir"
            return
            
        items = self.listBox.GetCount()
        print items
        for i in range(items):
            self.listBox.Delete(0)
        
        self.ftpBrowserAction_ls_()

    # ------------------------------------------------------------     
        
    def ftpBrowserAction_up_(self, event):

# Since the textfield in the browser is disabled 
# the check for root does not make sense anymore
                
#        if self.ftp_tools.pwd() == self.start:
#            self.parent.Error('this is the project\'s "root" - you cannot go up')
#            return
#        
        try:
            self.ftp_tools.cd('..')
        except Exception, e:
            self.parent.Error('You cannot go up! ' + str(e))
        
        self.ftpBrowserAction_ls_()
    
    # ------------------------------------------------------------     
    
    def ftpBrowserAction_cancel_(self, event):
        self.saved = False
        self.ftp_tools.logout()
        self.Close()  

    # ------------------------------------------------------------     
    
    def ftpBrowserAction_connect_(self, host, user, root, password):
        """
        before calling this method you have to use
        actionLoadPassword
        
        returns True or False
        """
        self.parent.busy()
        try:
            
            self.ftp_tools = makerFtpTools.Browser(host, root, user, password)
        except Exception, e:
            if "550" in str(e):
                self.parent.Error("Unable to connect! Root folder '" + root + "' does not exist!\n Using the servers default folder instead...") 
            try:
                self.ftp_tools = makerFtpTools.Browser(host, ".", user, password)
                                        
            except Exception, e:
                self.parent.Error('unable to connect ! Check your settings...' + str(e))
                #self.model.setRemotePassword(None)
                #raise Exception
                self.Destroy()
                self.parent.relax()    
                return False
            
        try:
            self.start = self.ftp_tools.pwd()
        except:
            self.parent.Message("unable to read root")
        
        # check for root
        if self.ftp_tools.pwd() == self.start:
            try:
                self.list.remove('..')
            except:
                print 'seems to be really root !'
        self.parent.relax()
        return True
        
    # ------------------------------------------------------------  
    
    def ftpBrowserShow(self):
        # this works
        try:
            self.ShowModal()
        finally:
            
            if self.saved:
                path = self.pathname
                self.Destroy()
                return path
            else:
                self.Destroy()
                return None
    
 
