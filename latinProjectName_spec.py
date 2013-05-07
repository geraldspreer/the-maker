#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import makerProjectManager
import makerWxGUI
import wx
import sys
import makerVersion
from random import randint
import makerCopyright
import makerEditorWxView
from makerUtilities import readFile

class TestApp(wx.App):
    
    def OnInit(self):

        self.mainView = self.create(None)
        return True
       

    def create(self, parent):
        return TestView(parent) 


class ProjectManagerTestController(makerProjectManager.ProjectManagerController):


    def loadStyles(self):
        """ this creates self.editorStyles """
        
        self.editorStyles = {}
        
        path = os.path.join(os.getcwd(), "system/EditorStyles")
        for item in os.listdir(path):
            if item.endswith(".json"):
                _s = item.replace(".json", "")
                self.editorStyles[_s] = eval(readFile(os.path.join(path,item)))


    def loadEditorStylesAndCreateMenu(self):
        self.styleMenus = {}
        path = os.path.join(os.getcwd(), "system/EditorStyles")
        
        MenuItemDefaultStyle = self.view.subMenuEditorStyles.Append(help='Default Editor Style',
                                              id=-1, 
                                              kind=self.view.wx.ITEM_CHECK, 
                                              text = "Default Style")
        
        self.styleMenus[None] = MenuItemDefaultStyle.GetId()
        
        self.view.subMenuEditorStyles.AppendSeparator()
        
        self.view.Bind(self.view.wx.EVT_MENU, self.resetEditorStyle, MenuItemDefaultStyle)
        
        
        for item in os.listdir(path):
            if item.endswith(".json"):
                _s = item.replace(".json", "")
                
                x = self.view.subMenuEditorStyles.Append(help='Editor Style ' + _s,
                                              id=-1, 
                                              kind=self.view.wx.ITEM_CHECK, 
                                              text = _s)
                
                self.styleMenus[item] = x.GetId()
                
                self.view.Bind(self.view.wx.EVT_MENU_HIGHLIGHT, self.prevEditorStyle, x)
                self.view.Bind(self.view.wx.EVT_MENU, self.setEditorStyle, x)
                
        
        self.loadStyles()

    
    def dirDialog(self, message="Choose a directory:"):
        """
        returns a path or None when canceled
        """
        
        return "This would be the given dir"
        
            
    def showProgress(self, limit, Message, title):
       print Message
       
    def updateProgressPulse(self, foo):

       print "updating progress pulse"




class TestProjectManager(makerProjectManager.ProjectManager):

    def __init__(self, view):
        
        self.controller = ProjectManagerTestController(self, view)
        
        self.linkedProjectPaths = []
        self.loadLinkedProjects()
        self.linkedProjects = {}
        self.controller.listProjectsInTree(self.getProjects())
        self.openProjects = []
        self.openFiles = []
        self.projectConvertRepoName = "MakerProjects"
        
    def getSystemPath(self):
        """ get system path """
        return os.path.join(os.getcwd(), "system/")


class TestView(makerWxGUI.wxPythonGUI):

    def _init_ctrls(self, prnt):
        
        wx.Frame.__init__(self, id=-1, name='', parent=prnt,
              pos=wx.Point(0,0 ), size=wx.Size(1200, 700),
              style=wx.DEFAULT_FRAME_STYLE, title=u'the maker')
        
        self.base = "/Users/maker/Documents/workspace/TheMaker"
        
        try:            # - don't sweat it if it doesn't load
            self.SetIcon(wx.Icon(os.path.join(self.base, "system/tags.ico"), wx.BITMAP_TYPE_ICO))
        finally:
            pass
        
                    
        self._init_utils()
        
        
        self.SetMenuBar(self.mainMenuBar)
        self.SetStatusBarPane(0)


#the other splitter

        #self.splitter2 = MySplitter(self, -1,None)
                
#the top splitter        
        
        self.splitter = makerWxGUI.MySplitter(self, -1,None)
    
        

# and the stc is added to it

        # it is very importat to keep the NODRAG style
        #
        # if dragging is added at some point the 
        # makerProjectController.py method noteBookPageClosed has to be
        # changed where the noteBoolPages dict is updated
        #
        
#        self.noteBook = nb.FlatNotebook(self.splitter, -1, style= wx.lib.flatnotebook.FNB_NODRAG 
#                                        | wx.lib.flatnotebook.FNB_X_ON_TAB)

        self.noteBook = makerWxGUI.MyCustomNoteBook(self.splitter, -1, None, None)

        self.noteBook.SetPadding(wx.Size(20))
        
        # add a welcome message to the noteBook        
        
        self.styledTextCtrl1 = (makerEditorWxView.editorView(self, "default")).editor
        self.welcomeId = self.styledTextCtrl1.GetId()
        self.noteBook.AddPage(self.styledTextCtrl1, "Thank you for using The Maker.")
        self.styledTextCtrl1.SetText(self.BoilerPlate)



#switch off popup

        #self.styledTextCtrl1.Bind(wx.EVT_RIGHT_DOWN, self.OnSTCRightDown)

        

#add widgets to the first splitter

        self.listWindow = wx.Panel(self.splitter, -1, style = wx.NO_BORDER)
        #self.listWindow.SetBackgroundColour(wx.RED)

        self.listSizer = wx.BoxSizer(orient=wx.VERTICAL)


# the listbox is added to the splitter too
        self.tree = wx.TreeCtrl(self.listWindow, -1, 
                                style=wx.TR_HAS_BUTTONS
                                |wx.TR_LINES_AT_ROOT
                                |wx.TR_DEFAULT_STYLE)
        
        def drawAfterPaint(evt):
            
            Size = self.tree.GetClientSizeTuple()

            dc = wx.ClientDC(self.tree)
            dc.SetPen(self.treePen)
            dc.DrawLine(Size[0]-1, 0, 
                        Size[0]-1, Size[1])
           
           
        def onTreePaint(evt):
            
            wx.CallAfter(drawAfterPaint, evt)
            
            evt.Skip()
            
        self.treePen = wx.Pen('#666666', 1)
        self.tree.Bind(wx.EVT_PAINT, onTreePaint)
       
 
        image_size = (16,16)

        projectArt = wx.Image(os.path.join(self.base, 
                                 "./system/ToolBarIcons/114.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        folderArt = wx.Image(os.path.join(self.base, 
                                 "./system/ToolBarIcons/99.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        folderOpenArt = wx.Image(os.path.join(self.base, 
                                 "./system/ToolBarIcons/107.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        fileArt = wx.Image(os.path.join(self.base, 
                                 "./system/ToolBarIcons/93.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        fileChangeArt = wx.Image(os.path.join(self.base, 
                                 "./system/ToolBarIcons/118.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        partArt = wx.Image(os.path.join(self.base, 
                                 "./system/ToolBarIcons/24-16.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        il = wx.ImageList(image_size[0], image_size[1])
        self.projidx     = il.Add(projectArt)
        self.fldridx     = il.Add(folderArt)
        self.fldropenidx = il.Add(folderOpenArt)
        self.fileidx     = il.Add(fileArt)
        self.filechange  = il.Add(fileChangeArt)
        self.part = il.Add(partArt)
        
        #self.partArt(il, image_size)
        
        self.tree.SetImageList(il)
        self.il = il
   
        self.listSizer.Add(self.tree, 1, border=0, flag=wx.EXPAND)
            
        self.listWindow.SetAutoLayout(True)
        self.listWindow.SetSizer(self.listSizer)
        self.listSizer.Fit(self.listWindow)

        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SplitVertically(self.listWindow, self.noteBook, 180)    

        self.toolBar = self.CreateToolBar( style =  wx.TB_HORIZONTAL
            | wx.NO_BORDER
            #| wx.TB_FLAT
            | wx.TB_TEXT
            )


        
        self.search = wx.SearchCtrl(self.toolBar, id= -1,  pos=(750,-1), size=(180,25), style=wx.TE_PROCESS_ENTER)
        
        #extract the searchCtrl's textCtrl 
        self.searchStatus = wx.StaticText(self.toolBar, -1, size=wx.DefaultSize, pos=wx.DefaultPosition, style=0)             
        self.searchStatus.SetLabel("                         ")
        
        saveArt = wx.Bitmap(os.path.join(self.base, 
                                 "./system/ToolBarIcons/23.png"))
        
        publishArt = wx.Bitmap(os.path.join(self.base, 
                                 "./system/ToolBarIcons/53.png"))
        previewArt = wx.Bitmap(os.path.join(self.base, 
                                 "./system/ToolBarIcons/25.png"))
        makeAllArt = wx.Bitmap(os.path.join(self.base, 
                                 "./system/ToolBarIcons/24.png"))
        
        
        self.toolBar.AddSeparator()

        self.toolBar.AddLabelTool(10, "Save", saveArt)
        self.toolBar.AddLabelTool(20, "Publish", publishArt)
        self.toolBar.AddLabelTool(30, "Preview", previewArt)
        self.toolBar.AddLabelTool(40, "Make All", makeAllArt)
        
        self.toolBar.AddStretchableSpace()

        self.toolBar.AddControl(self.searchStatus)
        self.toolBar.AddControl(self.search)
        
        self.toolBar.Realize()
        

        
        self.statusBar1 = wx.StatusBar(id=-1,
              name='statusBar1', parent=self, style=wx.ST_SIZEGRIP)
        
        #self.statusBar1.SetConstraints(LayoutAnchors(self.statusBar1, True,
        #      True, False, False))
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

 
        
        self.styledTextCtrl1.Bind(wx.EVT_PAINT, self.OnStyledTextCtrl1Paint)
        self.styledTextCtrl1.Bind(wx.EVT_ERASE_BACKGROUND,
              self.OnStyledTextCtrl1EraseBackground)

    def Ask_YesOrNo(self, question):
        return self.choiceReturnString
    
    
    def Input(self, Question="?", title = None):
    
        print "Input string was:", self.inputReturnString
        return self.inputReturnString
    
    def partArt(self, il, image_size):
        """ don't need no custom art in this mock class """
        pass

    def Error(self, Message):
        
        self._lastErrorMessage = Message

    
    def setInputReturnString(self, string):

        self.inputReturnString = string


    def setChoiceReturnString(self, string):

        self.choiceReturnString = string



class MakerTest(unittest.TestCase):
    
    
    def setUp(self):
       
        self.user_home = "/Users/maker"
        self.osx_correct = "Library/Application Support/TheMaker/makerProjects"
        self.projectPath = os.path.join(self.user_home, self.osx_correct)
        self.app = TestApp()
        self.pm = TestProjectManager(self.app.mainView)
        self.pm.controller.testing = True
       


    def test_mockViewErrorMessage(self):
        
        m = "This is an error..."
        self.pm.controller.errorMessage(m)
        self.assertEqual(self.pm.controller.view._lastErrorMessage, m)
    

      
    def test_invalidCharsShouldNotCreateProject(self):
        
        existingProjects = len(self.pm.getProjects())
        self.app.mainView.setInputReturnString(u"лывора")
        
        self.pm.controller.actionAddNewProject(event = None)
        
        self.assertEqual(len(self.pm.getProjects()), existingProjects) 
        self.assertEqual(self.app.mainView._lastErrorMessage, "Please use only Latin characters for project names...") 
        
        self.app.mainView.inputReturnString = None
        self.app.mainView._lastErrorMessage = None
    
        

    def test_validCharsShouldNotGiveError(self):

        self.app.mainView.inputReturnString = None
        self.app.mainView._lastErrorMessage = None
            
        testProjectName = u"Test_Project"
        
        self.app.mainView.setInputReturnString(testProjectName)
        
        self.pm.controller.actionAddNewProject(event = None)
        
        self.assertEqual(self.app.mainView._lastErrorMessage, None)
        

        
              
if __name__=="__main__":
    unittest.main()
