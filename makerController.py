
class SuperController:
    """
    A super class for all makerControllers 
    all controllers will inherit from this one
    
    It provides general purpose GUI interaction methods
    
    this class is also meant to serve as an abstraction layer
    """
    def __init__(self, model, view):
                  
        self.view = view
        self.model = model
        self.createAbstractNameForViewObjects()
        self.bindActions()
        
        # a list containing all tree items 
        self.treeItems = []
        
        self.treeFolders = []
                
        self.progressBars = []
        
        # important 'cause of the custom drawing code
        # this needs to be done in general so its in this super controller
        
        # just do this in the "right" controllers 
        if hasattr(self.view, 'tree'):
            self.view.tree.Bind(self.view.wx.EVT_TREE_ITEM_COLLAPSED, 
                           self.treeFixAfterProjectCollapsed)
        
        
    def treeFixAfterProjectCollapsed(self, event):
        """ refresh tree view """
        self.view.tree.Refresh()
        
        
    def bindActions(self):
        """ please override """
        pass
    
    
    def killProgressBar(self):
        try:

            bar = self.getLastProgressBar()
            self.deleteProgressBar(bar)
            bar.Destroy()
            #if self.keepGoing:
            # self.StopPulse()
        except Exception, e:
            print "unable to Kill Progress Bar", str(e)
    
    def deleteProgressBar(self,thisOne):
        """
! is deleting the instance from the stack
"""
        self.progressBars.remove(thisOne)
        
                               
    def addProgressBar(self, thisOne):
        """
ThisOne is an instance of a wxProgressbar
"""
        self.progressBars.append(thisOne)
    
    
    def getLastProgressBar(self):
        """
returns the instance of the progressbar that was last added to the stack
"""
        try:
            return self.progressBars[-1]
        except:
            return None
    
    def getAllProgressBars(self):
        return self.progressBars
    
    
    def showProgress(self, limit, Message="", title=None):
        #return
        if not title:
            # default for no title
            title = Message
            # if other bar is present
        
        progress = self.view.wx.ProgressDialog(title,
                              Message,
                              maximum = limit,
                              parent=self.view,
                              style = self.view.wx.PD_ESTIMATED_TIME)

        
        #self.progress.ShowModal()
        self.addProgressBar(progress)
        progress.SetInitialSize(self.view.wx.Size(400, 160))
        progress.Center()
        

    
#    def updateProgress(self, count):
#        #print self.Progress.max
#        #bar = self.getLastProgressBar()
#        #return
#        self.progress.Update(count)
# 
#    def updateProgressPulse(self, msg=None):
#        #return
#        #print self.Progress.max
#        
#        if msg:
#            self.progress.UpdatePulse(msg)
#        else:
#            self.progress.UpdatePulse()
#        
#
#    
#    def updateProgressMessage(self, count , message):
#        #return
#        self.progress.Update(count, message)

    def updateProgress(self, count):
        #print self.Progress.max
        bar = self.getLastProgressBar()
        bar.Update(count)
        

    def updateProgressPulse(self, msg=None):
        #print self.Progress.max
        bar = self.getLastProgressBar()
        if msg:
            bar.UpdatePulse(msg)
        else:
            bar.UpdatePulse()
        

    
    def updateProgressMessage(self, count , message):
        bar = self.getLastProgressBar()
        bar.Update(count,message)
    
 
    
    def fitRefreshAndCenter(self, widget):
        """
        is calling .Fit(), .Refresh() and .CenterOnScreen() for the widget
        """
        
        widget.Fit()
        widget.Refresh()
        widget.CenterOnScreen()
    
    
    
    
    def password(self, Message="Enter password:"):
        return self.view.Password(Message)
    
    
    def infoMessage(self, message):
        self.view.Message(str(message))
    
    def infoMessageNotModal(self, message):
        self.view.MessageNotModal(str(message))
    
    
    def warningMessage(self, error):
        self.view.Warning(str(error))
    
    
    def errorMessage(self, error):
        self.view.Error(str(error))
    
    def destroyView(self):
        """ overridden in some views """
        print "SuperController: Destroying Views"
        self.progress.Destroy()
        
        self.view.Destroy()    

    def askYesOrNo(self, question):
        return self.view.Ask_YesOrNo(question)
    
    def input(self, question="?", title="Question:"):
        return self.view.Input(question, title)
    
   
    def inputWithValue(self, question, value):
        
        return self.view.InputWithValue(question, value)
        
   
   
    
       
    def colorDialog(self):
        """ bring up a color picker dialog"""
        
        self.view.ColorDialog()
        color = self.view.color_data
        
        return color
   
   
    def importProjectDialog(self):
        project = self.view.SelectProject()
        if not project: 
            return None
        else:   
            return project
       
    def fileDialog(self, message = None):
        """
        returns a list(!) of pathnames or None when canceled
        
        """
        path = self.view.getFileFromUser(prompt = message)

        return path
        
    def imageDialog(self, path):
        """
        returns a pathname or None when canceled
        
        """
        return self.view.ImageDialogWithDir(path)
        
    
    
    def resetAllViews(self):
        """
        this will set all controls and views to their default state
        """
        # "resetting all views"
        
        # tools 
        
        self.view.toolBar.EnableTool(10, False) # Save
        self.view.toolBar.EnableTool(20, False) # Publish
        self.view.toolBar.EnableTool(30, False) # Preview
        self.view.toolBar.EnableTool(40, False) # Make All
        
#        # Buttons
#        
#        self.view.saveButton.Disable()
#        self.view.publishButton.Disable()
#        self.view.previewButton.Disable()
#        self.view.makeAllButton.Disable()
        
        # search
        
        # self.view.search.Disable()
                
        # FTP menu
        self.view.MenuItemEditDist.Enable(False)
        self.view.MenuItemPublish.Enable(False)
        self.view.MenuItemFullUpload.Enable(False)
        self.view.MenuItemBrowseFtp.Enable(False)
        
        # Project Menu
        
        
        #self.view.MenuItemLangSwitch.Enable(False) 
        self.view.MenuItemSetupFTP.Enable(False)
        
        # View Menu
                
        self.view.MenuItemWrapWord.Enable(False)
        self.view.MenuItemFontInc.Enable(False)
        self.view.MenuItemFontDec.Enable(False)
        self.view.MenuItemFontNormal.Enable(False)
        self.view.MenuItemEditorStyles.Enable(False)
                
        # Edit Menu
        
        self.view.MenuItemUndo.Enable(False)
        self.view.MenuItemRedo.Enable(False) 
        self.view.MenuItemCut.Enable(False)
        self.view.MenuItemCopy.Enable(False)
        self.view.MenuItemPaste.Enable(False)
        self.view.MenuItemReplace.Enable(False)
        self.view.MenuItemFind.Enable(False)
        self.view.MenuItemFindNext.Enable(False)
        
        
        # Tools Menu
                
        self.view.MenuItemEditHead.Enable(False)
        self.view.MenuItemLanguages.Enable(False)
        self.view.MenuItemSelectColor.Enable(False)
        self.view.MenuItemUnderline.Enable(False)
        self.view.MenuItemOblique.Enable(False)
        self.view.MenuItemBold.Enable(False)
        self.view.MenuItemLine_through.Enable(False)
        
        
        
        # Marker Sub Menu
        
#        self.view.MenuItemMarkerTodaysDate.Enable(False) 
#        self.view.MenuItemMarkerProjectName.Enable(False) 
#        self.view.MenuItemMarkerPageName.Enable(False) 
#        self.view.MenuItemMarkerCreationDate.Enable(False)
        
        # File Menu
                          
        self.view.MenuItemNewFiles.Enable(False) 
        self.view.MenuItemSaveFile.Enable(False)
        self.view.MenuItemDeleteFile.Enable(False) 
        self.view.MenuItemRenameFile.Enable(False)
        self.view.MenuItemSaveAsTemplate.Enable(False) 
        self.view.MenuItemAddToFTPQueue.Enable(False) 
        self.view.MenuItemCloseFile.Enable(False) 
        self.view.MenuItemPreview.Enable(False) 
        self.view.MenuItemImportFile.Enable(False)
        self.view.MenuItemImportProject.Enable(True)
        #self.view.MenuItemDeleteProject.Enable(False)
        self.view.MenuItemOpenProject.Enable(True)
        
        # you can always add new projects
        self.view.MenuItemAddProject.Enable(True) 
        
        self.view.MenuItemSaveProjectAsTemplate.Enable(False) 
        
        self.view.MenuItemPrint.Enable(False)
        
        # you can always quit
        self.view.MenuItemQuit.Enable(True)
        
        # Tree Contextual Menu
        
        self.view.treePopUpMenuItemDeleteFile.Enable(False) 
        self.view.treePopUpMenuItemRenameFile.Enable(False)
        self.view.treePopUpMenuItemCloseFile.Enable(False) 
        self.view.treePopUpMenuItemPreview.Enable(False) 
        self.view.treePopUpMenuItemPrint.Enable(False)
        self.view.treePopUpMenuItemCollapseOther.Enable(False)
        
        
        
        
        # Insert Menu
        
        self.view.MenuItemHTML.Enable(False)
        self.view.MenuItemCSS.Enable(False)
        self.view.MenuItemMarkers.Enable(False)
        self.view.MenuItemMarkdown.Enable(False)
        
        # Parts Menu
        
        #self.view.MenuItemEditNav.Enable(False)
        #self.view.MenuItemEditBody.Enable(False)
        #self.view.MenuItemEditFoot.Enable(False)
        self.view.MenuItemEditRssHead.Enable(False)
        
        # Images Menu
        
        self.view.MenuItemImportImage.Enable(False)
        self.view.MenuItemDeleteImage.Enable(False)
        self.view.MenuItemSyncImages.Enable(False)
        
        # Status Bar
        
        self.view.statusBar1.SetStatusText(number = 1, text='Project: ')
        self.view.statusBar1.SetStatusText(number = 2, text='Language: ')
        self.view.statusBar1.SetStatusText(number = 3, text='File: ')
        self.view.statusBar1.SetStatusText(number = 4, text="FTP Queue: ")
                
        
    
    def createAbstractNameForViewObjects(self):
        """
        This method is called from inside __init__
        
        Please override
        
        In controller classes inheriting from this super class, you will
        do things like: 
        
        self.tree = self.view.wxTreeCtrl1
        
        Creating an abstract name for view objects used by a corresponding
        model class
        
        """
    
    
    def singleChoice(self, choices, title="", message=""):
        
        return self.view.SingleChoiceDialog(choices, title, message)
    
    
    def dirDialog(self, message="Choose a directory:"):
        """
        returns a path or None when canceled
        """
        self.view.getDirFromUser(message)

        if self.view.dirDialog.ShowModal() == self.view.wx.ID_OK:
            path = self.view.dirDialog.GetPath()
            self.view.dirDialog.Destroy()
            
            # create bookmark
            
            dirURL = NSURL.fileURLWithPath_(path)
            myData = myData = NSData.alloc().initWithData_(dirURL.bookmarkDataWithOptions_includingResourceValuesForKeys_relativeToURL_error_(NSURLBookmarkCreationWithSecurityScope, None, None, None))
            print "NsData is", myData
            
            return path
        else:
            return None
        
    
# general purpose tree functions
    
    def treeViewExpandItem(self, item):
        try:
            self.view.tree.Expand(item)
        except Exception, e:
            print str(e)
    
    def treeViewCollapseItem(self, item):
        try:
            self.view.tree.Collapse(item)
        except Exception, e:
            print str(e)
          
    def treeViewGotoRoot(self):
        self.view.tree.EnsureVisible(self.view.treeGetRoot())
        
    
    def treeViewGetRoot(self):
        return self.view.tree.GetRootItem()
    
    
    def treeViewReset(self):
        if self.view.tree.GetCount() !=0:
            # print "resetting tree view"
            self.view.tree.DeleteAllItems()
            self.treeItems = []
        
    
    def treeViewDeleteItem(self, item):
        
        """ remove item from tree view as well as from self.treeItem"""
        
        
        self.view.tree.Delete(item)
        print "tree items:", self.treeItems
        self.treeItems.remove(item)
        
            
    def treeViewAppendItem(self, parent , itemText, type="Folder"):
        
        newItem = self.view.tree.AppendItem(parent, itemText)
        self.treeItems.append(newItem)
        
               
        # set the icons for when this item is either collapsed 
        # or expanded
        parts = [".content", ".dynamic", ".nav", ".body", ".foot", ".head"]
                
        if type == "Folder":
            
            self.treeFolders.append(itemText)
            
            
            if itemText in parts:
                self.view.tree.SetItemImage(newItem, 
                                            self.view.part, 
                                           self.view.wx.TreeItemIcon_Normal
                                           )
                self.view.tree.SetItemImage(newItem, 
                                           self.view.part, 
                                           self.view.wx.TreeItemIcon_Expanded)
            
            else:
                self.view.tree.SetItemImage(newItem, 
                                                self.view.fldridx, 
                                               self.view.wx.TreeItemIcon_Normal
                                               )
                self.view.tree.SetItemImage(newItem, 
                                               self.view.fldropenidx, 
                                               self.view.wx.TreeItemIcon_Expanded)
                    
        elif type == "Project":
            # add icon for projects
            self.view.tree.SetItemImage(newItem, 
                                            self.view.projidx, 
                                            self.view.wx.TreeItemIcon_Normal
                                           )
            self.view.tree.SetItemImage(newItem, 
                                           self.view.projidx, 
                                           self.view.wx.TreeItemIcon_Expanded)
            
            # make projects more distinct
            self.view.tree.SetItemBold(newItem, True)
            self.view.tree.SetItemTextColour(newItem, "#333333")
        
        
        else:
            self.view.tree.SetItemImage(newItem, self.view.fileidx, 
                                           self.view.wx.TreeItemIcon_Normal)
                
        return newItem
        
        # ---------
    
    
    
            
           
        
