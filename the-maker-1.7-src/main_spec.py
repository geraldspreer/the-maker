#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import makerProjectManager
import spec_mockView
import wx
import sys
import makerVersion

class TestApp(wx.App):
    
    def OnInit(self):

        self.mainView = self.create(None)
        return True
       

    def create(self, parent):
        return TestView(parent) 


class ProjectManagerTestController(makerProjectManager.ProjectManagerController):

   def showTemplateDialog(self):
       """ return the Simple template for testing"""
       
       return "Simple"



class TestProjectManager(makerProjectManager.ProjectManager):

    def __init__(self, view):
        
        self.controller = ProjectManagerTestController(self, view)
        self.setProjectDir()
        
        self.linkedProjectPaths = []
        self.loadLinkedProjects()
        self.linkedProjects = {}
        self.controller.listProjectsInTree(self.getProjects())
        self.openProjects = []
        self.openFiles = []
        

class TestView(spec_mockView.wxPythonGUI):
    
    def Input(self, Question="?"):
    
        return self.inputReturnString
    

    def Error(self, Message):
        
        self._lastErrorMessage = Message

    
    def setInputReturnString(self, string):

        self.inputReturnString = string

    

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
    
    
    def test_setCorrectProjectDir_OSX(self):
        
        self.pm.setProjectDir()
        self.assertEqual(self.pm.projectDir, 
                         os.path.join(self.user_home, self.osx_correct),
                         "Project dir is set correct...")
        
    
    def test_setCorrectProjectDir_Linux(self):
        
        linux_correct = os.path.join(self.user_home, "makerProjects")

        # Pretending to be Linux...
        realOS = sys.platform
        sys.platform = "linux2"      

        self.pm.setProjectDir()
        self.assertEqual(self.pm.projectDir, 
                         os.path.normpath(linux_correct), 
                         "Project path on linux is set correct...")
        
        # restore
        sys.platform = realOS
        
      
      
    def test_invalidCharsShouldNotCreateProject(self):
        
        existingProjects = len(self.pm.getProjects())
        self.app.mainView.setInputReturnString(u"лывора")
        
        self.pm.addNewProject()
        
        self.assertEqual(len(self.pm.getProjects()), existingProjects) 
        
        self.assertEqual(self.app.mainView._lastErrorMessage, "Please use only Latin characters for project names...") 
        
        self.app.mainView.inputReturnString = None
        self.app.mainView._lastErrorMessage = None
    
        

    def test_validCharsShouldCreateProject(self):
        return 
    
        testProjectName = u"__Test__"
        existingProjects = len(self.pm.getProjects())
        self.app.mainView.setInputReturnString(testProjectName)
        
        
        self.pm.addNewProject()
        
        self.assertEqual(len(self.pm.getProjects()), existingProjects + 1) 
        
        self.app.mainView.inputReturnString = None
        
        # make this a run shell script thing cause sudo needed
        #os.remove(os.path.join(self.projectPath, testProjectName))
        
     
    
    def test_deleteProject(self):
        
        pass

        
      
              
if __name__=="__main__":
    unittest.main()
