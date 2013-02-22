import unittest
import os
import shutil
import wx
import sys
import makerVersion


class TemplateTest(unittest.TestCase):

    def setUp(self):
       
        self.user_home = "/Users/maker"
        self.templates = "Library/Application Support/TheMaker/makerProjects"
        self.projectPath = os.path.join(self.user_home, self.osx_correct)
        

    def test_WhiteTemplate(self):
       print "This is the template test"
       pass
    
        
    
              
if __name__=="__main__":
    unittest.main()
