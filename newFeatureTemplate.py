import makerController

class Controller(makerController.SuperController):
    def drawDialog(self):
    
class ClassName:
    def __init__(self, mainView, project):
        self.projectController = project.projectController
        self.project = project
        self.controller = Controller(self, mainView)
        self.controller.drawDialog()
