import wx
import os
from makerWidgets import MakerDialog


class ProjectBrowser(MakerDialog):

    def __init__(self, parent):        
        self.createDialog(parent)
        self.selectedProject = None
 
    def createDialog(self, prnt):
	MakerDialog.__init__(self,
                             {'name'       : '',
                              'parent'     : prnt, 
                              'pos'        : wx.Point(497, 197), 
                              'size'       : wx.Size(309, 459),
                              'style'      : wx.DEFAULT_DIALOG_STYLE, 
                              'title'      : 'Select a Project',
                              'clientSize' : wx.Size(301, 425),
                              'centerPos'  : wx.BOTH})

        # ----- LISTBOX -----
        self.listBox1 = self.add('listbox', {'choices' : [],
                                             'name'    : 'listBox1',
                                             'parent'  : self,
                                             'pos'     : wx.Point(0, 13),
                                             'size'    : wx.Size(301, 328),
                                             'style'   : wx.VSCROLL,
                                             'handler' : self.onListBoxClick})
        
        # ----- PANEL -----
        self.panel1 = self.add('panel', {'name'   : 'panel1',
                                         'parent' : self,
                                         'pos'    : wx.Point(0, 341),
                                         'size'   : wx.Size(301, 80),
                                         'style'  : wx.TAB_TRAVERSAL
                                         })

	# ----- OK BUTTON -----
        self.OKbutton = self.add('button', {'label'   : 'OK',
                                            'name'    : 'ok', 
                                            'parent'  : self.panel1, 
                                            'pos'     : wx.Point(208, 24),
                                            'size'    : wx.Size(75, 23), 
                                            'style'   : 0,
                                            'handler' : self.onOKButton})

	# ----- CANCEL BUTTON -----
        self.cancelButton = self.add('button', {'label'   : 'Cancel',
                                                'name'    : 'cancel', 
                                                'parent'  : self.panel1, 
                                                'pos'     : wx.Point(120, 24),
                                                'size'    : wx.Size(75, 23), 
                                                'style'   : 0,
                                                'handler' : self.onCancelButton})

        self.createSizers()

    # ------------------------------------------------------------

    def createSizers(self):
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self.boxSizer1.Add(self.listBox1, 0, border=0, flag=wx.EXPAND | wx.GROW)
        self.boxSizer1.Add(self.panel1, 0, border=0, flag=wx.FIXED_MINSIZE)
        self.SetSizer(self.boxSizer1)

    # ------------------------------------------------------------
    
    def fillProjectList(self, theList):
        for thing in theList:
            self.listBox1.Append(thing)

    # ------------------------------------------------------------

    def onOKButton(self,event):
        self.selectedProject = self.listBox1.GetStringSelection()
        self.Close()
        event.Skip()

    # ------------------------------------------------------------

    def onCancelButton(self, event):
        self.Close()
        event.Skip()

    # ------------------------------------------------------------

    def onListBoxClick(self, event):
        self.selectedProject = self.listBox1.GetStringSelection()
        self.Close()
        event.Skip()
