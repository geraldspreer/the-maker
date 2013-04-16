import makerController
import makerManageLinkedProjDialog

class Controller(makerController.SuperController):
    
    def drawDialog(self):
        
        self.dialog = makerManageLinkedProjDialog.xrcManageLinked(self.view)
        
        self.dialog.Cancel.Bind(self.view.wx.EVT_BUTTON, 
                         self.cancel)
#
        self.dialog.Unlink.Bind(self.view.wx.EVT_BUTTON, 
                         self.unlink)

        
        self.dialog.Bind(self.view.wx.EVT_CLOSE, 
                         self.close)

        for item in self.model.getManagedProjectsList():
            
            self.dialog.theList.Append(item)
     
        self.pathList = []
        try:
            # there might be no projects
            self.dialog.theList.SetSelection(0)
            
        except:
            pass
        
        self.dialog.Show()
    
    
    def cancel(self, event):
        # close without doing stuff
        print "cancel button"
        self.close(None)
	
        

    def unlink(self, event):
        path = self.dialog.theList.GetStringSelection()
        if path != "":
            self.dialog.theList.Delete(self.dialog.theList.GetSelection())
            self.pathList.append(path)
    
    
    def close(self, event=None):
        if self.pathList != []:
            if self.askYesOrNo("TheMaker needs to restart for the changes to take effect. Would you like to do that?") == "Yes":
                self.model.unlink(self.pathList)
        
	self.dialog.Destroy()
    
class Manager:
    
    def __init__(self, mainView, projectManager):
                
        self.projectManager = projectManager
        
        self.controller = Controller(self, mainView)
        self.controller.drawDialog()
        
        
    def unlink(self, pathsToUnlink):
        
        for path in pathsToUnlink:
            self.projectManager.linkedProjectPaths.remove(path)
        
        self.projectManager.closeOpenProjects()
        self.controller.view.application.restart = True
        
    
    def getManagedProjectsList(self):
        return self.projectManager.linkedProjectPaths
    
