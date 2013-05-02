import os


class UpdateSandboxedProjects():

    
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
    
    
    def getSystemPath(self):
        """ get system path """
    
        systemPath = os.path.join(os.getcwd(), "system/")
    
        return systemPath
    
    
    def update(self):
        
        sandBoxProjects = os.path.join(self.getApplicationSupportDir(), "makerProjects")
        converted = []
        errors = False
        
        if not os.path.isdir(sandBoxProjects):
            return
        
        targetDir = os.path.joi(self.getUserHomeDir(), "MyMakerProjects")
        
        for item in os.listdir(sandBoxProjects):
            if not item.startswith("."):
                
                src = os.path.join(sandBoxProjects, item)
                dst = os.path.join(targetDir, self.projectConvertRepoName ,item + ".makerProject") 
                
                if not os.path.isdir(dst):
                    # this is just a safety check. This case should never occur...
                    # 
                    shutil.copytree(src, dst)
                    converted.append(item + ".makerProject")
                    
                    print "patch UISettings file here..."
                    print thisWillBreakHere
                    #if dst not in self.linkedProjectPaths:
                    #    self.openThisProject(dst, verbose = False)
                
        
        for bundle in converted:
            if not bundle in os.listdir(os.path.join(targetDir, self.projectConvertRepoName)):
                errors = True
                
        if errors == True:
            print thisWillBreakHere
            "before app exits, take users to info website..." 
            #self.controller.errorMessage("Fatal Installation Error!\nPlease report this to info@makercms.org.\nWe will help you out!\nShutting down...")
            sys.exit(0)
        else:
            shutil.rmtree(sandBoxProjects, True)