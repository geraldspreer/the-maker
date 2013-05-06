import os
import shutil
import webbrowser as web
import sys
from makerUtilities import writeDataToFile, readDataFromFile

TARGET_NAME = "MyMakerProjects"

class UpdateSandboxedProjects():

    
    def patchUISettings(self, projects):
        
        theFile = os.path.join(self.getApplicationSupportDir(), ".makerUISettings")
        interfaceData = readDataFromFile(theFile)
        
        interfaceData['linkedProjects'] = projects
        interfaceData['sessionFiles'] = []
        
        writeDataToFile(interfaceData, theFile)
    
    
    def getApplicationPath(self):
        """ get path where the maker executable resides """
        
        appPath = os.path.dirname(sys.argv[0])
        return appPath
    
    def getUserHomeDir(self):
        """ get the users gome dir """    
        try:
            theDir = os.environ['HOME']
        except:
            theDir = os.environ['HOMEPATH']
        
        return theDir
    
    def getApplicationSupportDir(self):
    
        try:
            theDir = os.environ['HOME']
        except:
            theDir = os.environ['HOMEPATH']
        
        supportDir = os.path.join(theDir, "Library/Application Support/TheMaker/")
        
        if not os.path.isdir(supportDir):
            os.mkdir(supportDir)
        
        return supportDir
    
    
    def getConversionTargetDir(self):
        
        return os.path.join(self.getUserHomeDir(), TARGET_NAME)
    
    
    def getSystemPath(self):
        """ get system path """
    
        systemPath = os.path.join(os.getcwd(), "system/")
    
        return systemPath
    
    def isProject(self, project):
        if os.path.isdir(os.path.join(project, "parts")):
            return True
        else:
            return False
    
    
    def exportOnManageProjectsClose(self, oldProject, targetDir):
        
        pass
        
    
    def update(self):
        
        sandBoxProjects = os.path.join(self.getApplicationSupportDir(), "makerProjects")
        converted = []
        # projects that need to be patched in the UI file
        toPatch = []
        errors = False
        
        if not os.path.isdir(sandBoxProjects):
            return
        
        targetDir = os.path.join(self.getUserHomeDir(), "MyMakerProjects")
        
        for item in os.listdir(sandBoxProjects):
            if not item.startswith(".") and self.isProject(os.path.join(sandBoxProjects, item)):
                
                src = os.path.join(sandBoxProjects, item)
                dst = os.path.join(targetDir ,item + ".makerProject") 
                
                if not os.path.isdir(dst):
                    # this is just a safety check. This case should never occur...
                    # 
                    shutil.copytree(src, dst)
                    converted.append(item + ".makerProject")
                    toPatch.append(dst)
                    
        
        for bundle in converted:
            try:
                if not bundle in os.listdir(targetDir):
                    errors = True
            except:
                errors = True
                
        if errors == True:
            web.open("http://www.makercms.org/conversion-info/")
            sys.exit(0)
        else:
            shutil.rmtree(sandBoxProjects, True)
            self.patchUISettings(toPatch)