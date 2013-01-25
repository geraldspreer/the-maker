import wx
from makerWidgets import MakerDialog


class ImportOrNew(MakerDialog): 
    def __init__(self, parent):
        self.createDialog(parent)
        self.choice = None
                   
    def createDialog(self, prnt):
        MakerDialog.__init__(self,
                             {'name'       : '',
                              'parent'     : prnt, 
                              'pos'        : wx.Point(392, 323), 
                              'size'       : wx.Size(391, 63),
                              'style'      : wx.DEFAULT_DIALOG_STYLE, 
                              'title'      : 'Import or create a project',
                              'clientSize' : wx.Size(391, 63),
                              'centerPos'  : wx.BOTH})

	# ----- NEW PROJECT BUTTON -----
        self.newProjButton = self.add('button', {'label'   : 'Create New Project',
                                                 'name'    : 'newProject', 
                                                 'parent'  : self, 
                                                 'pos'     : wx.Point(202, 17),
                                                 'size'    : wx.Size(176, 30), 
                                                 'style'   : 0,
                                                 'handler' : self.onNewProject})

	# ----- IMPORT PROJECT BUTTON -----
        self.newProjButton = self.add('button', {'label'   : 'Import Project',
                                                 'name'    : 'importProject', 
                                                 'parent'  : self, 
                                                 'pos'     : wx.Point(10, 17),
                                                 'size'    : wx.Size(184, 30), 
                                                 'style'   : 0,
                                                 'handler' : self.onImportProject})
    

    def onNewProject(self, event):        
        self.choice = 'new'
        self.Close()

    def onImportProject(self, event):
        self.choice = 'import'
        self.Close()
