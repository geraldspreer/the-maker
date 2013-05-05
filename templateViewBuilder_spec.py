import unittest
import os
import webbrowser as web
import sys
import makerTemplateViewBuilder
from makerUtilities import readFile

class TemplateTest(unittest.TestCase):

    def setUp(self):
       
        self.sysPath = "system/"
        self.viewPath = "/Users/maker/Library/Application Support/TheMaker/"
        
    
    def test_templateView(self):
        
        makerTemplateViewBuilder.buildView(self.sysPath, self.viewPath)
        self.assertTrue(os.path.isfile(os.path.join(self.viewPath, "yourTemplates.html")), "Template file has been created")

        contents = readFile(os.path.join(self.viewPath, "yourTemplates.html"))
        
        self.assertTrue(contents.find(os.path.join(self.sysPath,"jquery.min.js")) != -1, "Correct jquery reference found in view...")
        
    
         
        
    def test_paths(self):
        
        self.assertTrue(os.path.isdir(self.sysPath), "System Path is correct...")
        self.assertTrue(os.path.isfile(os.path.join(self.sysPath, "Splash.png")), "View Path is correct...")

    
              
if __name__=="__main__":
    unittest.main()
