import os
import sys
import makerProjectSetup
import makerController
import makerEditDistributionData
import makerThread
from makerProjectLanguages import possibleLanguages

class MakerProjectController(makerController.SuperController):
    
    def bindActions(self):
        self.view.Bind(self.view.wx.EVT_TOOL, self.model.makeAll, id=40)
        self.view.Bind(self.view.wx.EVT_TOOL_RCLICKED, self.model.makeAll, id=40)
        self.view.Bind(self.view.wx.EVT_MENU,
                  self.actionProjectSetup,
                  self.view.MenuItemSetupFTP
                  )
        self.view.Bind(self.view.wx.EVT_MENU,
                  self.model.publishQueuedFiles,
                  self.view.MenuItemPublish
                  )
        self.view.Bind(self.view.wx.EVT_TOOL, self.model.publishQueuedFiles, id=20)
        self.view.Bind(self.view.wx.EVT_TOOL_RCLICKED, self.model.publishQueuedFiles, id=20)
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.actionLoadPart, 
                  self.view.MenuItemEditRssHead
                  )
        # new files
        self.view.Bind(self.view.wx.EVT_MENU,
                  self.findActionForEvent, 
                  self.view.MenuItemNewHtmlFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemNewXmlFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU,
                  self.findActionForEvent, 
                  self.view.MenuItemNewDynamicFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU,
                  self.findActionForEvent, 
                  self.view.MenuItemNewOtherFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemNewContentFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemNewCssFile)

        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemNewCgiFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemNewJsFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemNewTxtFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemNewPhpFile
                  )
        # file import 
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemImportFile
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemAddToFTPQueue
                  )
        # Unbind since control of tree items is handed to this class
        self.treeView.Unbind(self.view.wx.EVT_TREE_SEL_CHANGED)
        self.treeView.Bind(self.view.wx.EVT_TREE_SEL_CHANGED, 
                           self.actionLoadFile)
        self.treeView.Bind(self.view.wx.EVT_RIGHT_DOWN, 
                           self.actionShowTreePopUp)
        # font zoom
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemFontInc
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemFontDec
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemFontNormal
                  )
        # images
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemImportImage
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemDeleteImage
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemSyncImages
                  )
        # FTP
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemBrowseFtp
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent, 
                  self.view.MenuItemEditDist
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.model.uploadEverything, 
                  self.view.MenuItemFullUpload
                  )
        self.view.Bind(self.view.wx.EVT_MENU,
        self.actionEditCurrentFileHead,
        self.view.MenuItemEditHead)
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.model.saveProjectAsTemplate, 
                  self.view.MenuItemSaveProjectAsTemplate
                  )
        # add language to project
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.actionAddLanguageToProject, 
                  self.view.MenuItemAddLanguage
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.actionRemoveLanguageFromProject, 
                  self.view.MenuItemRemoveLanguage
                  )
        # tree popup menu
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.actionTreeExpandAll, 
                  self.view.treePopUpMenuItemExpandAll
                  )
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.actionTreeCollapseAll, 
                  self.view.treePopUpMenuItemCollapseAll
                  )

    def actionTreeExpandAll(self, event):
        self.treeView.ExpandAll()
    
    def actionTreeCollapseAll(self, event):
        self.treeView.CollapseAllChildren(self.treeView.GetRootItem())
        self.treeView.Expand(self.treeView.GetRootItem())
    
    def createAbstractNameForViewObjects(self):
        self.treeView = self.view.tree
        self.treeFolders = []
        self.noteBook = self.view.noteBook
        self.saveMenu = self.view.MenuItemSaveFile
        self.previewMenu = self.view.MenuItemPreview
        self.deleteMenu = self.view.MenuItemDeleteFile
        self.publishMenu = self.view.MenuItemPublish
        self.search = self.view.search
        # ----
        # trying to fiddle with a tree item that has been deleted causes bad 
        # crashes. Pointers will still be available but the object is dead
        # So this is a list containing those Zombie Items
        self.deletedTreeItems = []

    def treeViewAddFolder(self, folder):
        pRoot = self.findProjectRootItem()
        if folder not in self.treeFolders:
            return self.treeViewAppendItem(pRoot, folder)
        else:
            # folder exists
            return self.findTreeItemByText(folder)
      
    def findActionForEvent(self, event):
        theActions = {
            self.view.MenuItemNewHtmlFile.GetId() : (self.model.addMakerFile, [None, ".html"]),
            self.view.MenuItemNewXmlFile.GetId() : (self.model.addMakerFile, [None, ".xml"]),
            self.view.MenuItemNewDynamicFile.GetId() : (self.model.addMakerFile, [None, ".dynamic"]),
            self.view.MenuItemNewOtherFile.GetId() : (self.model.addMakerFile, [None, "other"]),
            self.view.MenuItemNewContentFile.GetId() : (self.model.addMakerFile, [None, ".content"]),
            self.view.MenuItemNewCssFile.GetId() : (self.model.addMakerFile, [None, ".css"]),
            self.view.MenuItemNewCgiFile.GetId() : (self.model.addMakerFile, [None, ".cgi"]),
            self.view.MenuItemNewJsFile.GetId() : (self.model.addMakerFile, [None, ".js"]),
            self.view.MenuItemNewTxtFile.GetId() : (self.model.addMakerFile, [None, ".txt"]),
            self.view.MenuItemNewPhpFile.GetId() : (self.model.addMakerFile, [None, ".php"]),
            self.view.MenuItemImportFile.GetId() : (self.model.importFiles,),
            self.view.MenuItemFontInc.GetId() : (self.editorZoom, 1),
            self.view.MenuItemFontDec.GetId() : (self.editorZoom, -1),
            self.view.MenuItemFontNormal.GetId() : (self.editorFontReset,),
            self.view.MenuItemImportImage.GetId() : (self.model.importImage,),
            self.view.MenuItemDeleteImage.GetId() : (self.model.deleteImage,),
            self.view.MenuItemSyncImages.GetId() : (self.model.syncImages,),
            self.view.MenuItemBrowseFtp.GetId() : (self.model.browseFtp,),
            self.view.MenuItemEditDist.GetId() : (self.editDistributionTable,),
            self.view.MenuItemAddToFTPQueue.GetId() : (self.addFileToFTPQueue,),
            }
        action = theActions[event.GetId()]
        try:
            # one arg
            action[0](action[-1])
        except Exception, e:
            try:
                # more than one argument
                action[0](*action[1])
            except Exception, e:
                print "after second try:", str(e)
                # no argument
                action[0]()
   
    def editorZoom(self, step):
        curZoom = self.model.currentFile.fileController.editor.GetZoom()
        newZoom = int(curZoom) + step
        try:
            self.model.currentFile.fileController.editor.SetZoom(newZoom)
        except:
            self.errorMessage("You cannot change Font size any further...")
    
    def editDistributionTable(self, event=None):
        makerEditDistributionData.EditDistributionData(self.view, self.model)
    
    def editorFontReset(self, event):
        zoom = self.model.currentFile.fileController.getDefaultZoom()
        self.model.currentFile.fileController.editor.SetZoom(zoom)
   
    def addFileToFTPQueue(self):
        """
        for adding binary file manually
        """
        self.model.addToFtpQueue(self.model.currentFile.getRealName())
        self.updateStatusInformation()
   
    def actionEditCurrentFileHead(self, event):
        g = self.treeViewAddFolder(".head")
        if not g:
            return
        item = self.treeViewAppendItem(g, self.model.currentFile.getHead(), type="item")
        self.treeView.SelectItem(item, True)    
   
    def actionEditHeadTemplate(self, event):
        if not self.model.getTemplateFileName():
            return
                
        self.infoMessage("Very soon now")
   
    def actionLoadPart(self, event):
        """ load a part like .nav .body or .foot into the editor """
                  
        if event.GetId() == self.view.MenuItemEditRssHead.GetId():
            g = self.treeViewAddFolder(".head")
            item = self.treeViewAppendItem(g, "rss", type="item")
            self.treeView.SelectItem(item, True)     
  
    def actionShowTreePopUp(self, event):
        """ show tree popup tool """
        pt = event.GetPosition();
        item, flags = self.treeView.HitTest(pt)
        if item:
            self.selectTreeItemAndLoad(item)
        self.treeView.PopupMenu(self.view.treePopUp, event.GetPosition())
  
    def actionProjectSetup(self, event):
        if self.model.checkIfProjectIsSetUp():
            firstSetup = False
        else:
            firstSetup = True
        psfn = self.model.getProjectSetupFilename()
        projectData = self.model.getProjectInformation(psfn)
        dlg = makerProjectSetup.ProjectSetup(self.view, self) 
        dlg.setValues(projectData)
        dlg.ShowModal()
        if dlg.saved:
            self.model.writeProjectSetupFile(dlg.theInformation, self.model.getProjectSetupFilename())
            info = dlg.theInformation
            self.model.saveValidFTPHost(info["ftp_host"], info["ftp_user"], info["ftp_root"])
            self.model.setupProjectAndInitServerlink()
            if firstSetup:
                self.model.setImageSyncNeeded(needed = True)
                m = "Congratulations! All FTP settings are good...\n"
                m+= "Would you like to upload your files?"
                if self.askYesOrNo(m) == "Yes":
                    self.model.uploadEverything(event = None)
        dlg.Destroy()

    def findProjectRootItem(self):
        root = self.treeViewGetRoot()
        item = self.view.tree.GetSelection()
        while self.treeView.GetItemParent(item) != root:
            item = self.treeView.GetItemParent(item)
        return item
    
    def findProjectByTreeItem(self, item):
        """ returns the name of the project the treeItem belongs to 
            or None if root is selected
        """
        #    root = "makerProjects"  -
        #                            - project x
        #                            - project y
        #
        #     it the parent of an item is root 
        #    then that item is "root" of a project
        root = self.treeViewGetRoot()
        item = item
        if item == root:
            return None
        while self.treeView.GetItemParent(item) != root:
            item = self.treeView.GetItemParent(item)
        return self.treeView.GetItemText(item)
    def actionAddLanguageToProject(self, event):
        choices = []
        for language in possibleLanguages.iterkeys():
            choices.append(language)
        choices.sort(cmp=None, key=None, reverse=False)
        theChoice = self.singleChoice(choices, message="Add language to project...")
        if theChoice:
            langCode = possibleLanguages[theChoice]
            if not langCode in self.model.getProjectLanguages():
                self.model.addLanguage(langCode, theChoice)
            else:
                self.errorMessage("The language '%s' already exists in this project." % theChoice)
        else:
            return
    
    def actionRemoveLanguageFromProject(self, event):
        inProject = self.model.getProjectLanguages()
        if len(inProject) == 1:
            self.errorMessage("This cannot be done.\nYou do need at least ONE language in your project.")
            return
        langNames = []
        for item in inProject:
            for name, code in possibleLanguages.iteritems():
                if code == item:
                    langNames.append(name)
        langNames.sort(cmp=None, key=None, reverse=False)
        theChoice = self.singleChoice(langNames, message="Remove language from project...")
        if theChoice:
            langCode = possibleLanguages[theChoice]
            self.model.removeLanguage(langCode, theChoice)
        else:
            return
    
    def actionLoadFile(self, event):
        item = event.GetItem()
        if item:
            itemParent = self.treeView.GetItemParent(item)
            if self.view.tree.GetItemText(item) in self.treeFolders:
                print "a group was selected..."
            elif item == self.treeViewGetRoot():
                return      
            elif itemParent == self.treeViewGetRoot():
                self.model.projectManager.switchProject(self.treeView.GetItemText(item))
            else:
                theFile = self.treeView.GetItemText(item)
                if self.model.getProject() != self.findProjectByTreeItem(item):
                    # switch to the project the file belongs to and pass the event
                    # that called this method here to the other project
                    self.model.projectManager.switchProject(self.findProjectByTreeItem(item), event)
                    # we let dead end here since after this call another projectController will take over    
                else:           
                    openFileList = []
                    for data in self.model.projectManager.controller.noteBookPages.itervalues():
                        openFileList.append(data.model.getName())
                                    
                    if theFile in openFileList:
                        for key in self.model.projectManager.controller.noteBookPages.iterkeys():
                            if (self.model.projectManager.controller.noteBookPages[key]).model.getName() == theFile:
                                if (self.model.projectManager.controller.noteBookPages[key]).getReferringTreeItem() == self.view.tree.GetSelection():
                                    self.noteBook.SetSelection(key)
                                    self.noteBook._pages.OnSetFocus(None)
                    fileType = self.treeView.GetItemText(itemParent)
                    self.model.loadFile(theFile, fileType)
                    self.noteBook._pages.OnSetFocus(None)

    def selectTreeItemAndLoad(self, item):
        """  select a tree item    
             this call will cause the file to load
        """
        self.treeView.SelectItem(item, True)
        
    def selectTreeItem(self, item):
        """ just select item - don't load """
        #     the selection event is unbound here because since it
        #     is bound to the actionLoadFile this method here would 
        #     trigger a file to be loaded but its purpose is to
        #     make sure that the current file is selected in the tree
        self.treeView.Unbind(self.view.wx.EVT_TREE_SEL_CHANGED)
        self.treeView.SelectItem(item, True)
        #     bind selection event again
        self.treeView.Bind(self.view.wx.EVT_TREE_SEL_CHANGED, 
                           self.actionLoadFile)
     
    def findTreeItem(self, text, parentText):
        """ this only refers to tree items that belong to the 
            "model" project. Not to the whole tree
        """
        for item in self.treeItems:
            result = self.view.tree.GetItemText(item) 
            if result == text and self.view.tree.GetItemText(self.view.tree.GetItemParent(item)) == parentText:
                return item
    
    def findTreeItemByText(self, text):
        for item in self.treeItems:
            result = self.view.tree.GetItemText(item) 
            if result == text:
                return item
        return None
    
    def markAllQueuedFiles(self):
        """ mark all tree items that are queued for FTP """
        for theFile in self.model.getFtpQueue():
            if os.path.isfile(os.path.join(self.model.getPathParts(), theFile)):
                try:
                    self.markQueuedFile(theFile, mark=True)
                except:
                    print "unable to mark file..."
            else:
                m = "There is a non-existing file called: '" + theFile
                m += "'\n in the FTP Queue!\n"
                m += "The queue entry will be removed..."
                self.infoMessage(m)
                self.model.deleteFromFtpQueue(theFile)
    
    def markQueuedFile(self, fileName, mark=True):
        """ mark a tree item as queued or as not in queue """
        nameAndParent = os.path.splitext(fileName)
        item = self.findTreeItem(nameAndParent[0], nameAndParent[-1])
        if mark:
            self.view.tree.SetItemImage(item, 
                                        self.view.filechange, 
                                        self.view.wx.TreeItemIcon_Normal)
        else:
            self.view.tree.SetItemImage(item, 
                                    self.view.fileidx, 
                                    self.view.wx.TreeItemIcon_Normal)
      
    def noteBookPageChanged(self, event):
        self.noteBook._pages.OnSetFocus(None)
        data = (self.model.projectManager.controller.noteBookPages[event.GetSelection()])
        item = data.getReferringTreeItem()
        if item not in self.deletedTreeItems:
            self.selectTreeItem(item)
        theFile = data.model.getName()
        group = data.model.getType()
        project = data.model.getProject()
        if self.model.getProject() != project:
            # switch to the project the file belongs to and pass the event
            # that called this method here to the other project
            self.model.projectManager.switchProject(project, event)
        else:
            self.model.loadFile(theFile, group)    
        
    def noteBookPageClosed(self, event):
        data = (self.model.projectManager.controller.noteBookPages[event.GetSelection()])
        theFile = data.model.getName()
        group = data.model.getType()
        project = data.model.getProject()

        del self.model.projectManager.controller.noteBookPages[event.GetSelection()]
        self.model.projectManager.removeFromOpenFiles(theFile, group, project)

        # update noteBookPages -----------------------
        # --------------------------------------------
        # this only works if noteBook tabs cannot be dragged
        #
        # What is happening here ?
        #
        # self.model.projectManager.noteBookPages has the following format
        # {Page [page_idx], treeItem[itemID]} 
        # Once a page is closed all the remaining page_idx's are remixed in the  
        # noteBook Control 
        # So the values in the noteBookPages dict have to be updated with the new
        # values
        # Since the internal order in the noteBook Control is always 
        # 0,1,2,3,....
        # We just have to update the keys in the noteBookPages dict
        #
        #

        count = 0
        beSorted = {}
        for key in self.model.projectManager.controller.noteBookPages:
            beSorted[count] = self.model.projectManager.controller.noteBookPages[key]
            count += 1
        self.model.projectManager.controller.noteBookPages = beSorted
        if self.view.noteBook.GetPageCount() == 0:
            # no more open pages
            # clear selection in tree view
            self.view.tree.UnselectAll()
            self.model.setCurrentFile(None)
            self.reBindSelectEvent()
        else:
            newSelection = self.view.noteBook.GetSelection()
            event.SetSelection(newSelection)
            self.noteBookPageChanged(event)
   
    def treeViewDeleteItem(self, item):
        """ remove item from tree view as well as from self.treeItem"""
        self.treeView.Unbind(self.view.wx.EVT_TREE_SEL_CHANGED)
        self.deletedTreeItems.append(item)
        self.view.tree.Delete(item)
        self.treeItems.remove(item)
        
    def reBindSelectEvent(self):
        self.view.wx.Yield()
        self.treeView.Bind(self.view.wx.EVT_TREE_SEL_CHANGED, 
                           self.actionLoadFile)
    
    def deleteChildrenFromTreeViewItem(self, treeViewItem):
        self.treeView.DeleteChildren(treeViewItem)
    
    def updateStatusInformation(self):
        self.view.statusBar1.SetStatusText(number=1,
                                           text='Project: ' 
                                           + self.model.project
                                           )
        try:
            self.view.statusBar1.SetStatusText(number=2, 
                                           text='Language: ' 
                                           + str((self.model.getCurrentFile()).getLanguage())
                                           )
        except Exception, e:
            print "Exception was:", e
        self.view.statusBar1.SetStatusText(number=3,
                                           text='File: '
                                           + self.model.getCurrentFileName()
                                           )
        try:
            self.view.statusBar1.SetStatusText(number=4,
                                           text="FTP Queue: " + str(len(self.model.getFtpQueue())) 
                                           + " Files"
                                           )
        except Exception, e:
            pass
        self.view.toolBar.EnableTool(40, True) # Make All Tool
        self.view.treePopUpMenuItemCollapseOther.Enable(True)
        if self.model.currentFile:
            if self.model.currentFile.fileController:   # only update interface when UI interaction is needed
                self.view.SetTitle("The Maker - " + self.model.getProject() + 
                                   " - " + self.model.currentFile.getFileName())
                self.view.MenuItemWrapWord.Enable(True)
                if self.model.currentFile.fileController.editor.GetWrapMode() == self.view.wx.stc.STC_WRAP_WORD:
                    self.view.MenuItemWrapWord.Check(True)
                else:
                    self.view.MenuItemWrapWord.Check(False)
                self.view.treePopUpMenuItemDeleteFile.Enable(True) 
                self.view.treePopUpMenuItemRenameFile.Enable(True)
                self.view.treePopUpMenuItemCloseFile.Enable(True) 
                self.view.treePopUpMenuItemPreview.Enable(True) 
                self.view.treePopUpMenuItemPrint.Enable(True)
                self.search.Enable()
                self.view.MenuItemReplace.Enable(True)
                self.view.MenuItemFind.Enable(True)
                self.view.MenuItemFindNext.Enable(True)
                self.view.MenuItemCut.Enable(True)
                self.view.MenuItemCopy.Enable(True)
                self.view.MenuItemPaste.Enable(True)
                if self.model.currentFile.getEditable():
                    self.view.MenuItemUndo.Enable(True)
                    self.view.MenuItemRedo.Enable(True)
                else:
                    self.view.MenuItemUndo.Enable(False)
                    self.view.MenuItemRedo.Enable(False)
                if self.model.currentFile.getType() == ".head":
                    self.view.toolBar.EnableTool(30, False)
                    self.previewMenu.Enable(False)
                    self.deleteMenu.Enable(False)
                    self.view.MenuItemRenameFile.Enable(False)
                elif self.model.currentFile.getType() == ".py":
                    self.previewMenu.SetText("Run Python Script")
                    self.view.toolBar.EnableTool(30, True)
                    self.previewMenu.Enable(True)
                elif self.model.currentFile.getType() != ".py":
                    self.previewMenu.SetText("Preview File\tF5")
                    self.view.toolBar.EnableTool(30, True)
                    self.previewMenu.Enable(True)
                    self.deleteMenu.Enable(True)
                    self.view.MenuItemRenameFile.Enable(True)
                else:
                    self.view.toolBar.EnableTool(30, True)
                    self.previewMenu.Enable(True)
                    self.deleteMenu.Enable(True)
                    self.view.MenuItemRenameFile.Enable(True)
                self.view.MenuItemCloseFile.Enable(True)
                self.view.MenuItemEditorStyles.Enable(True)
                if self.model.currentFile.saved:
                    self.view.toolBar.EnableTool(10, False)
                    self.saveMenu.Enable(False)
                else:
                    self.view.toolBar.EnableTool(10, True)
                    self.saveMenu.Enable(True)
                if self.model.currentFile.getType() == ".content":
                    self.view.MenuItemEditHead.Enable(True)
                else:
                    self.view.MenuItemEditHead.Enable(False)
                markdownTypes = [".content",".head",".body",".nav",".foot",".dynamic"]
                if self.model.currentFile.getEditable():
                    if self.model.currentFile.getType() in markdownTypes:
                        self.view.MenuItemMarkdown.Enable(True)
                    else:
                        self.view.MenuItemMarkdown.Enable(False)
                    self.view.MenuItemComment.Enable(True)
                    self.view.MenuItemHTML.Enable(True)
                    self.view.MenuItemCSS.Enable(True)
                    self.view.MenuItemMarkers.Enable(True)
                else:
                    self.view.MenuItemMarkdown.Enable(False)
                    self.view.MenuItemComment.Enable(False)
                    self.view.MenuItemHTML.Enable(False)
                    self.view.MenuItemCSS.Enable(False)
                    self.view.MenuItemMarkers.Enable(False)
                # print
                if self.model.currentFile.getEditable(): 
                    self.view.MenuItemPrint.Enable(True)
                else:
                    self.view.MenuItemPrint.Enable(False)
                self.view.MenuItemFontInc.Enable(True)
                self.view.MenuItemFontDec.Enable(True)
                self.view.MenuItemFontNormal.Enable(True)
                if not self.model.currentFile.getEditable(): 
                    fName = self.model.currentFile.getRealName()
                    if not self.model.isFileInQueue(fName):
                        self.view.MenuItemAddToFTPQueue.Enable(True)
                    else:
                        self.view.MenuItemAddToFTPQueue.Enable(False)
        else:
            self.view.treePopUpMenuItemDeleteFile.Enable(False) 
            self.view.treePopUpMenuItemRenameFile.Enable(False)
            self.view.treePopUpMenuItemCloseFile.Enable(False) 
            self.view.treePopUpMenuItemPreview.Enable(False) 
            self.view.treePopUpMenuItemPrint.Enable(False)
            self.view.toolBar.EnableTool(10, False)
            self.view.toolBar.EnableTool(30, False)
            self.previewMenu.Enable(False)
            self.deleteMenu.Enable(False)
            self.view.MenuItemCloseFile.Enable(False)
            self.view.MenuItemRenameFile.Enable(False)
            self.search.Disable()
            self.view.MenuItemFind.Enable(False)
            self.view.MenuItemFindNext.Enable(False)
            self.view.MenuItemCut.Enable(False)
            self.view.MenuItemCopy.Enable(False)
            self.view.MenuItemPaste.Enable(False)
            self.view.MenuItemUndo.Enable(False)
            self.view.MenuItemRedo.Enable(False)
            # Insert menus
            self.view.MenuItemHTML.Enable(False)
            self.view.MenuItemCSS.Enable(False)
            self.view.MenuItemMarkers.Enable(False)
            # View menu
            self.view.MenuItemWrapWord.Enable(False)
            self.view.MenuItemEditorStyles.Enable(False)
            # print 
            self.view.MenuItemPrint.Enable(False)
            self.view.MenuItemFontInc.Enable(False)
            self.view.MenuItemFontDec.Enable(False)
            self.view.MenuItemFontNormal.Enable(False)
            # tools menu
            # items get enabled by the FileController
            self.view.MenuItemEditHead.Enable(False)
            self.view.MenuItemLine_through.Enable(False)
            self.view.MenuItemUnderline.Enable(False)
            self.view.MenuItemBold.Enable(False)
            self.view.MenuItemOblique.Enable(False)
            self.view.MenuItemSelectColor.Enable(False)
            self.view.MenuItemAddToFTPQueue.Enable(False)

        # languages 
        self.view.MenuItemLanguages.Enable(True)
        if len(self.model.getProjectLanguages()) == 1:
            self.view.MenuItemRemoveLanguage.Enable(False)
        else:
            self.view.MenuItemRemoveLanguage.Enable(True)
        # images
        self.view.MenuItemImportImage.Enable(True)
        self.view.MenuItemDeleteImage.Enable(True)
        self.view.MenuItemSyncImages.Enable(True)
        # Edit dist table
        self.view.MenuItemEditDist.Enable(True)
        # publish
        self.view.MenuItemFullUpload.Enable(True)
        self.view.MenuItemSaveProjectAsTemplate.Enable(True)
        if not self.model.getFtpQueue():
            self.publishMenu.SetText("Publish\tCtrl+u")
            self.view.toolBar.EnableTool(20, False)
            self.publishMenu.Enable(False)
        else:
            self.view.toolBar.EnableTool(20, True)
            self.publishMenu.Enable(True)
            self.publishMenu.SetText("Publish [" + str(len(self.model.getFtpQueue())) + " Files in Queue]\tCtrl+u")
            self.view.statusBar1.SetStatusText(number=4,
                                           text="FTP Queue: " + str(len(self.model.getFtpQueue())) 
                                           + " Files "
                                           )
        self.view.MenuItemSetupFTP.Enable(True)
        self.view.MenuItemBrowseFtp.Enable(True)
        # File import 
        self.view.MenuItemImportFile.Enable(True)
        self.view.MenuItemEditRssHead.Enable(True)
        self.view.MenuItemNewFiles.Enable(True) 
