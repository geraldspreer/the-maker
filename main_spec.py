#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import makerProjectManager
import spec_mockView
import wx
import sys
import makerVersion
from random import randint

class TestApp(wx.App):
    
    def OnInit(self):

        self.mainView = self.create(None)
        return True
       

    def create(self, parent):
        return TestView(parent) 


class ProjectManagerTestController(makerProjectManager.ProjectManagerController):

   def showTemplateDialog(self):
       """ return the Simple template for testing"""
       print "Returning Template 'Simple'"
       return "Simple"

   def showProgress(self, limit, Message, title):
       print Message
       
   def updateProgressPulse(self, foo):

       print "updating progress pulse"




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
        
    def getSystemPath(self):
        """ get system path """
        return os.path.join(os.getcwd(), "system/")


class TestView(spec_mockView.wxPythonGUI):
    
    def Ask_YesOrNo(self, question):
        return self.choiceReturnString
    
    
    def Input(self, Question="?"):
    
        print "Input string was:", self.inputReturnString
        return self.inputReturnString
    

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
    
        

    def test_validCharsShouldCreateProject_IfNotExising(self):
    
        testProjectName = u"Test_Project"
        existingProjects = len(self.pm.getProjects())
        self.app.mainView.setInputReturnString(testProjectName)
        testPath = os.path.join(self.projectPath, testProjectName)

        if os.path.isdir(testPath):
            shutil.rmtree(testPath)
        
        self.pm.addNewProject()
        
        self.assertEqual(len(self.pm.getProjects()), existingProjects + 1) 
        
        self.assertTrue(os.path.isdir(os.path.join(testPath, "parts")))
        self.assertTrue(os.path.isdir(os.path.join(testPath, "templates")))
        self.assertTrue(os.path.isdir(os.path.join(testPath, "setup")))
        
        # Test for not creating project if it exists
        self.pm.addNewProject()
        self.assertEqual(self.app.mainView._lastErrorMessage, "A project with the name '" + testProjectName + "' already exists !")

        
        self.app.mainView.inputReturnString = None
        print "Removing test project..."
        
        shutil.rmtree(testPath)
    
    
    
    
    def test_deleteProject(self):
    
        return 
        testProjectName = u"To_Delete_Project"
        existingProjects = len(self.pm.getProjects())
        self.app.mainView.setInputReturnString(testProjectName)
        testPath = os.path.join(self.projectPath, testProjectName)
        
        if os.path.isdir(testPath):
            shutil.rmtree(testPath)
        
        self.pm.addNewProject()
        
        #self.assertEqual(len(self.pm.getProjects()), existingProjects + 1) 
        
        self.assertTrue(os.path.isdir(os.path.join(testPath, "parts")))
        self.assertTrue(os.path.isdir(os.path.join(testPath, "templates")))
        self.assertTrue(os.path.isdir(os.path.join(testPath, "setup")))
        
        
        self.pm.load(testProjectName)
        
        print "PROJECT IS:", self.pm.getActiveProject().getProject()
        
        self.app.mainView.choiceReturnString = "Yes"
        
        self.pm.deleteProject()
        
        self.assertTrue(testProjectName not in self.pm.getProjects())

        self.app.mainView.choiceReturnString = None
        
        
    
    
        
              
if __name__=="__main__":
    unittest.main()
