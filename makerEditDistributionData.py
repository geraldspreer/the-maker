import makerController
import makerDistEditor
import os
from makerUtilities import readFile, writeFile
import makerDefaultRemoteFolderEditor
import urlparse

class Controller(makerController.SuperController):
    
    
    
    def drawDialog(self):
        
        data = self.model.project.readDistributionTable()
        
    
        self.dlg = makerDistEditor.DistributionTableEditor(self.view, data)
        self.saveOldData(data)
        
        self.itemsColors = {}
        self.markConflicts()
        
                
        self.dlg.Bind(self.view.wx.EVT_LIST_ITEM_SELECTED, self.checkAgain)
        self.dlg.Bind(self.view.wx.EVT_LIST_BEGIN_LABEL_EDIT, self.validateColumn)
        self.dlg.Bind(self.view.wx.EVT_LIST_END_LABEL_EDIT, self.endEdit)
        self.dlg.defaultFolderButton.Bind(self.view.wx.EVT_BUTTON, self.editDefaultRemoteFolders)
        
        self.dlg.ShowModal()
        #dlg.saved = True File was saved
        #dlg.saved = False File was not saved
    
        if self.dlg.saved:
            
            if not self.model.project.checkIfProjectIsSetUp():
                # save data
                self.model.project.writeDistributionTable(self.dlg.data)
                print "No cleanup necessary - project not set up"
                return
            
            self.model.project.serverLogin()
            if not self.model.project.server.status == "connected":
                self.dlg.Destroy()
            
            else:
                self.model.project.writeDistributionTable(self.dlg.data)
                self.model.compareDataForCleanup(self.dlg.oldDistData, self.dlg.data)
                # Task compare date sets for changes
                self.dlg.Destroy()
        else:
            self.dlg.Destroy()
    
    
    def editDefaultRemoteFolders(self, event):
        
        data = self.model.project.readDefaultFoldersFile()
        
        default = makerDefaultRemoteFolderEditor.DefRemFolderEditor(self.view, data)
        
                
        default.ShowModal()
        #dlg.saved = True File was saved
        #dlg.saved = False File was not saved

        if default.saved:
            
            self.model.project.writeDefaultFoldersFile(default.data)
            
            default.Destroy()
            
        else:
            default.Destroy()
           
    
    def endEdit(self, evt):
        # we bind it only after the edit has been made otherwise it will
        # seriously slow down the app
        #self.validateColumn(evt)
        self.dlg.Bind(self.view.wx.EVT_UPDATE_UI, self.checkAgain)
        # after markConflicts is finished this event is unbound
       
    
    
    
    def validateColumn(self, evt):
        print 'validating column'
        m = "You may only edit the 'Remote Dir' and the 'Remote File' column!"
        if evt.GetColumn() == 0:
            self.infoMessage(m)
            evt.Veto()
        elif evt.GetColumn() == 2:
            self.infoMessage(m)
            evt.Veto()
    
    
    
    def checkAgain(self, evt):
        
        self.resetItemBackgrounds()    
        self.markConflicts()
    
    
    def saveOldData(self, oldData):
        self.dlg.oldDistData = oldData 
        
    def readOldData(self):
        return self.dlg.oldDistData
        
        
   
    
    
    def markConflicts(self, event=None):
        markedItems = []
        for conflict in self.getFilesWithConflicts():
            item = self.dlg.listCtrl.FindItem(0, conflict)
            markedItems.append(item)
            self.itemsColors[item] = self.dlg.listCtrl.GetItemBackgroundColour(item)
            self.dlg.listCtrl.SetItemBackgroundColour(item, self.view.wx.RED)
            
        self.dlg.markedItems = markedItems
        
        # unbind until the next edit
        self.dlg.Unbind(self.view.wx.EVT_UPDATE_UI)
            
    
    def getFilesWithConflicts(self):
        conflicts = []
        for f in self.getListOfRemoteFolders():
            list = self.getConflictFilesForFolder(f)
            if list != []:
                for item in list:
                    conflicts.append(item)
                
        return conflicts
    
    
    def getListOfRemoteFolders(self):
        listOfFolders = []
        for dataSet in self.dlg.readData():
            if listOfFolders.count(dataSet['remote_dir'])==0:
                listOfFolders.append(dataSet['remote_dir'])
                
        return listOfFolders
    
    
    def getConflictFilesForFolder(self, folder):
        
        conflictFiles = []
        files = []
        
        for dataSet in self.dlg.readData():
            if dataSet['remote_dir']==folder:
                files.append(dataSet['target'])
            
            if files.count(dataSet['target']) > 1:
                for otherDataSet in self.dlg.readData():
                    
                    if otherDataSet["target"] == dataSet['target']:
                        
                        if not conflictFiles.count(otherDataSet['ftp_source']) >= 1:
                            conflictFiles.append(otherDataSet['ftp_source'])
                    
                #conflictFiles.append(dataSet['ftp_source'])
        
        return conflictFiles
    
    
    
    def resetItemBackgrounds(self):
        
        for item in self.dlg.markedItems:
            # due to some odd behavior in wx we have to set to white first
            # before we can use another esp. custom color
            self.dlg.listCtrl.SetItemBackgroundColour(item, self.view.wx.WHITE)
            self.dlg.listCtrl.SetItemBackgroundColour(item, self.itemsColors[item])
            # ----
        self.dlg.markedItems = []

   
        
        
    
class EditDistributionData:
    
    def __init__(self, mainView, project):
                
        self.projectController = project.projectController
        self.project = project
        
        self.controller = Controller(self, mainView)
        self.controller.drawDialog()
        
       
    
    def compareDataForCleanup(self, oldData, newData):
        
        toCleanup = []
                 
        for theOldDataSet in oldData:
            fileToCompare = theOldDataSet["ftp_source"]
            for newDataSet in newData:
                if newDataSet["ftp_source"]==fileToCompare:
                    if newDataSet["remote_dir"] == theOldDataSet["remote_dir"]:
                        pass
                    else:
                        # folder name has changed
                        toCleanup.append(((theOldDataSet["remote_dir"],
                                           theOldDataSet["target"]),
                                            (newDataSet["remote_dir"],
                                              newDataSet["target"]))) 
                    
                    if newDataSet["target"] == theOldDataSet["target"]:
                        pass
                    else:
                        # target name has changed
                        toCleanup.append(((theOldDataSet["remote_dir"],
                                           theOldDataSet["target"]),
                                            (newDataSet["remote_dir"],
                                              newDataSet["target"]))) 
                    
                
                
#        info = ""
#        for item in toCleanup:
#            info += str(item) + "\n"
#        
#        print "Files to cleanup: " , info
        
        self.cleanup(toCleanup)
     
    
    def cleanup(self, toCleanup):
        
        self.controller.showProgress(limit = 1, Message="Please wait...", title="Cleaning Up")
        runs = 1
        for x in toCleanup:
            target = x[1]
            source = x[0]
            if not source[0].endswith("/"):
                finalSourceFolder = source[0]+"/"
            else:
                finalSourceFolder = source[0]
            if not target[0].endswith("/"):
                finalTargetFolder = target[0]+"/"
            else:
                finalTargetFolder = target[0]
            
            self.controller.updateProgressPulse("Please wait...")
            if self.project.checkIfRemoteDirIsDir(finalTargetFolder):
                self.project.renameRemoteFile(urlparse.urljoin(finalSourceFolder, 
                                                               source[1]), 
                                                               urlparse.urljoin(finalTargetFolder, 
                                                                                target[1]))
            else:
                self.project.makeRemoteDir(finalTargetFolder)
                self.project.renameRemoteFile(urlparse.urljoin(finalSourceFolder, 
                                                               source[1]), 
                                                               urlparse.urljoin(finalTargetFolder, 
                                                                                target[1]))
            runs += 1
            
        self.controller.killProgressBar()
        self.project.serverLogout()
        
        
    
    
    
    
    
    
        
   
    
   
            
    
        
    
    
