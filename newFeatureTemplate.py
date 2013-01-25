import makerController


class Controller(makerController.SuperController):
    
    def drawDialog(self):
        
#        do someting like this:
#
#        self.dialog = makerNewFileDialog.xrcnewFile(self.view)
#        self.dialog.Cancel.Bind(self.view.wx.EVT_BUTTON, 
#                         self.close)
#
#        self.dialog.Add.Bind(self.view.wx.EVT_BUTTON, 
#                         self.add)
#    
#        self.dialog.SetTitle("add new " + self.model.type + " file..." )
        
    
        
        
    
class ClassName:
    
    def __init__(self, mainView, project):
                
        self.projectController = project.projectController
        self.project = project
        
        self.controller = Controller(self, mainView)
        self.controller.drawDialog()
        
        
    
    