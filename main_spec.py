#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import makerProjectManager
import spec_mockView
import wx
import sys



class TestApp(wx.App):
    
    def OnInit(self):

        self.mainView = self.create(None)
        return True
       

    def create(self, parent):
        return TestView(parent) 



        

class TestView(spec_mockView.wxPythonGUI):
    
    def Input(self, Question="?"):
    
        return self.inputReturnString
        
        
    def setInputReturnString(self, string):
        
        self.inputReturnString = string





class MakerTest(unittest.TestCase):

    def setUp(self):
       
        self.user_home = "/Users/maker"
        self.app = TestApp()
        self.pm = makerProjectManager.ProjectManager(self.app.mainView)

        
    def test_setCorrectProjectDir_OSX(self):
        
        osx_correct = "Library/Application Support/TheMaker/makerProjects"
        self.pm.setProjectDir()
        self.assertEqual(self.pm.projectDir, 
                         os.path.join(self.user_home, osx_correct),
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
        
        projects = len(self.pm.getProjects())
        
        print "There are ", projects
        
        #self.pm.addNewProject()
        
        

      
              
if __name__=="__main__":
    unittest.main()
