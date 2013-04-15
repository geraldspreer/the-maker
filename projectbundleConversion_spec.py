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

class TestApp(wx.App):
    
    def OnInit(self):

        self.mainView = self.create(None)
        return True
       

    def create(self, parent):
        return TestView(parent) 


class ProjectManagerTestController(makerProjectManager.ProjectManagerController):

    def importProjectDialog(self):
        project = self.view.getDirFromUser()
        if not project: 
            return None
        else:
            print "import Dialog returning:", project   
            return project

    def showProgress(self, limit, Message, title):
        print Message
       
    def updateProgressPulse(self, foo):

        print "updating progress pulse"
       
    def infoMessage(self, message):
        self.view.Message(message)
        print "Info Message:", message 
       
    def errorMessage(self, message):
       self.view.Error(str(message))
       print "Error Message:", message 
       
    def dirDialog(self, message):
        
        return self.view.getDirFromUser(message)
       

class TestProjectManager(makerProjectManager.ProjectManager):

    def __init__(self, view):
        
        self.controller = ProjectManagerTestController(self, view)
        
        self.linkedProjectPaths = []
        self.loadLinkedProjects()
        self.linkedProjects = {}
        self.controller.listProjectsInTree(self.getProjects())
        self.openProjects = []
        self.openFiles = []
        self.projectConvertRepoName = "Test-YourMakerProjects"
        self.loadArgumentPassedProject()
        
        # call converter manually for testing
        #self.checkForSandboxedProjects()
        
    def getSystemPath(self):
        """ get system path """
        return os.path.join(os.getcwd(), "system/")
    
    def getApplicationSupportDir(self):
    
        try:
            theDir = os.environ['HOME']
        except:
            theDir = os.environ['HOMEPATH']
        
        return os.path.join(theDir, "Library/Application Support/TheMaker-TESTING/")
   


class TestView(makerWxGUI.wxPythonGUI):
    
    def Show(self):
        pass
    
    def Ask_YesOrNo(self, question):
        return self.choiceReturnString
    
    def Message(self, message):
        self._lastInfoMessage = message
    
    def Input(self, Question="?", title = None):
    
        print "Input string was:", self.inputReturnString
        return self.inputReturnString
    
    def partArt(self, il, image_size):
        """ don't need no custom art in this mock class """
        pass
    
    def getDirFromUser(self, dialogMessage = None):

        return self.userSelectedDir 
    
    
    def Error(self, Message):
        
        self._lastErrorMessage = Message

    
    def setInputReturnString(self, string):

        self.inputReturnString = string

    def setChoiceReturnString(self, string):

        self.choiceReturnString = string

    def setUserSelectedDir(self, string):

        self.userSelectedDir = string


    def initError(self):

        self._lastErrorMessage = ""
        

class MakerTest(unittest.TestCase):
    
    def tearMeDown(self):
        
        shutil.rmtree(self.convertedProjectsPath, True)
        self.app.Destroy()
    
    def setMeUp(self):
       
        self.user_home = "/Users/maker/"
         
        self.app = TestApp()
        self.pm = TestProjectManager(self.app.mainView)
        self.pm.controller.testing = True
        
        self.projectPath = os.path.join(self.pm.getApplicationSupportDir(), "makerProjects")
        self.sandBox = self.projectPath
        
        self.convertedProjectsPath = os.path.join(self.user_home, self.pm.projectConvertRepoName)


    def test_todo(self):
        pass
    
    # controller should not create central project dir !!!

    def test_ifNoProjectsInSandboxDoNothing(self):
        pass
    

    def test_ifProjectExistsInNewRepoAppendNumber(self):
        pass
    


    def test_importAndConvertClassicProject(self):
        
        self.setMeUp()
        
        
        testProjectBefore = os.path.join(self.user_home,
                                         "/Users/maker/testing-makerProjects/testProject")
        
        if os.path.isdir(testProjectBefore):
            shutil.rmtree(testProjectBefore, ignore_errors = True)
        
        
        if not os.path.isdir(testProjectBefore):
            os.mkdir(testProjectBefore)
            os.mkdir(os.path.join(testProjectBefore, "parts"))
        
        
        
        testProjectAfter = os.path.join(self.user_home,
                                        "/Users/maker/testing-makerProjects/testProject.makerProject")
        notAProject = os.path.join(self.user_home,
                                   "/Users/maker/testing-makerProjects/")
        targetDir = os.path.join(self.user_home,
                                 "/Users/maker/Desktop/")
        
        
        if os.path.isdir(testProjectAfter):
            os.rename(testProjectAfter, testProjectBefore)
        
        #=======================================================================
        # not a project given but wrong dir
        #=======================================================================
        
        self.app.mainView.initError()
        self.app.mainView.setUserSelectedDir(notAProject)
        
        self.pm.importClassicProject(event = None)
        self.assertTrue("not a TheMaker" in self.app.mainView._lastErrorMessage, "If wrong dir given - Error and return")
        
        #=======================================================================
        # correct classic project given
        #=======================================================================
        
        self.app.mainView.setUserSelectedDir(testProjectBefore)
        
        self.pm.importClassicProject(event = None)
        
        self.assertTrue(os.path.isdir(testProjectAfter), "Project has been renamed correctly...")
        
        self.assertTrue(testProjectAfter in self.pm.linkedProjectPaths, "Project has been linked correctly...")
        
        # cleaning up
        
        if os.path.isdir(testProjectAfter):
            os.rename(testProjectAfter, testProjectBefore)
        
        self.tearMeDown()



    def test_ifProjectsInSandboxMoveToSelectedAndConvert_withCorrectChoice(self):
        
        self.setMeUp()
        
        # create Test Sandbox
        if not os.path.isdir(self.sandBox):
            os.mkdir(self.sandBox)
        
        
        print "creating dummy projects"
        dummy = ["Test_One","Test_Two","Test Three"," Test Four"]
        for item in dummy:
            if not os.path.isdir(os.path.join(self.sandBox, item)):
                os.mkdir(os.path.join(self.sandBox, item))
                os.mkdir(os.path.join(self.sandBox, item, "parts"))
                
        
        projectsInSandbox = [] 
        projectsInNewRepo = []
        
        def getProjectsInSandbox():
            projects = []
            for item in os.listdir(self.sandBox):
                if not item.startswith("."):
                    projects.append(item)
            
            return projects
        
        def getProjectsInCreatedRepo():
            projects = []
            for item in os.listdir(self.convertedProjectsPath):
                if not item.startswith("."):
                    projects.append(item)
                    print "In new repo:", item
            
            return projects
        
        projectsInSandbox = getProjectsInSandbox()
        
        self.app.mainView.setUserSelectedDir(self.user_home)
        self.pm.checkForSandboxedProjects()
        
        self.assertTrue(os.path.isdir(self.convertedProjectsPath), "new Repo should have been created...")
        
        self.assertEqual(len(projectsInSandbox), 
                         len(getProjectsInCreatedRepo()), "All projects should have been moved...")
        
        self.assertEqual(len(projectsInSandbox), 
                         len(getProjectsInCreatedRepo()), 
                         "Projects from Sandbox should be converted")
        
        
        for item in getProjectsInCreatedRepo():
            self.assertTrue(item.endswith(".makerProject"), "projects in new repo should be bundles")
            itemPath = os.path.join(self.convertedProjectsPath,item)
            
            self.assertTrue(itemPath in self.pm.linkedProjectPaths, 
                            "Project has been linked correctly...")
        
        self.assertFalse(os.path.isdir(self.sandBox), "Sandbox project repo deleted...")
        
        self.tearMeDown()


        #===============================================================================
        # No choice 
        #===============================================================================


    def test_ifProjectsInSandboxMoveToSelectedAndConvert_withNoChoice(self):
        
        self.setMeUp()
        
        # create Test Sandbox
        if not os.path.isdir(self.sandBox):
            os.mkdir(self.sandBox)
        
        
        print "creating dummy projects"
        dummy = ["Test_One","Test_Two","Test Three"," Test Four"]
        for item in dummy:
            if not os.path.isdir(os.path.join(self.sandBox, item)):
                os.mkdir(os.path.join(self.sandBox, item))
                os.mkdir(os.path.join(self.sandBox, item, "parts"))
                
        
        projectsInSandbox = [] 
        projectsInNewRepo = []
        
        def getProjectsInSandbox():
            projects = []
            for item in os.listdir(self.sandBox):
                if not item.startswith("."):
                    projects.append(item)
            
            return projects
        
        def getProjectsInCreatedRepo():
            projects = []
            for item in os.listdir(self.convertedProjectsPath):
                if not item.startswith("."):
                    projects.append(item)
            
            return projects
        
        projectsInSandbox = getProjectsInSandbox()
        
        self.app.mainView.setUserSelectedDir(None)
        self.pm.checkForSandboxedProjects()
        
        self.assertFalse(os.path.isdir(self.convertedProjectsPath), "new Repo should NOT have been created...")
        
        self.assertTrue("" in self.app.mainView._lastInfoMessage, "Correct info message afer cancel is displayed...")
        
        self.assertTrue(os.path.isdir(self.sandBox), "Sandbox project repo still exists...")
        
        self.tearMeDown()

              
if __name__=="__main__":
    unittest.main()
