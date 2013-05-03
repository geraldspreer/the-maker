#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
from makerUpdateSandboxedProjects import UpdateSandboxedProjects as theUpdater
import makerUpdateSandboxedProjects
import sys
from makerUtilities import writeDataToFile, readDataFromFile


class MakerTest(unittest.TestCase):
    
    def tearMeDown(self):
        
        pass
        
    def setMeUp(self):
       
        self.user_home = "/Users/maker/"
        
        testProjects = os.path.join(os.getcwd(),"_Testing_")
        self.tool = theUpdater()
        
        self.templateDir = os.path.join(self.tool.getSystemPath(), "templates")
        

    def test_noValidFTPFileInTemplate(self):
        
        self.setMeUp()
        
        for item in os.listdir(self.templateDir):
            daFile = os.path.join(self.templateDir, item, "setup/valid.ftp" )
            self.assertFalse(os.path.isfile(daFile), "valid.ftp file does not exist. Template->" + item)
        
        self.tearMeDown()
    
     


 


              
if __name__=="__main__":
    unittest.main()
