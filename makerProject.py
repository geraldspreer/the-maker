# -*- coding: cp1252 -*-

import os
import sys
import webbrowser
#from sets import Set
from xml.sax import parse
from xml.sax.handler import ContentHandler
from ftplib import FTP
import ftplib 
import time
import shutil
import re
import urllib
import urlparse
import cPickle
import string

import makerFileTemplates
import makerFileTypes
import makerServerlink
from makerUtilities import readFile, writeFile
from makerUtilities import copyFileTree
import makerUtilities
import makerImageImporter
import makerDeleteImage
import makerFtpBrowser
import makerAddNewLanguageCodedFile
import makerCheckInternetConnection
import makerProjectController


from makerConstants import Constants

def afterThisUpdateStatusInfo(func):
    def wrapped(*args, **kwds):
        self = args[0]
        func(*args, **kwds)
        # for now we have to do this check
        try:
            if self.projectController:
                self.projectController.updateStatusInformation()
        except Exception, e:
            print "makerProject"
            print "unable to process: afterThisUpdateInfo", str(e)
    
    return wrapped



def enforcePassword(func):
    def wrapped(*args, **kwds):
        self = args[0]
        if not self.checkIfProjectIsSetUp(verbose=True):
            return
        else:
            if self.loadPassword():
                func(*args, **kwds)
    return wrapped



class MakerProjectModel:
    """ The model for projects
        on instantiation you pass it a path to a project
    
    """
    def __init__(self, project, view, projectManager=None):
                
#        self.initialized = False
        
#        self.controller = controller
#        # instance of makerController
        
          #                                    model , view
        self.projectController = makerProjectController.MakerProjectController(self, view)
          
        self.projectManager = projectManager  
                                       
        self.setProjectPath(project)
        
        self.coreMessage("Working directory is: %s" % os.getcwd())
        
        self.systemSetup()
        
        self.pathParts = os.path.join(self.getProjectPath(), "parts/")
        
        self.setupProjectAndInitServerlink()
        
        self.setImageSyncNeeded(needed = False)
         
        self.clearPassAttempts()
        
        self.setCurrentFile(None)
        
        self.setRemotePassword() # defaults to None
        
        self.setContentEditMode(".content")
        
        self.markers = ["!projectName!", 
                        "!pageName!",
                        "!creationDate!",
                        "!todaysDate!"
                        ]
        
        self.initFtpQueue()
        
        self.supportedFiles = [".content",
                            ".css",
                            ".cgi",
                            ".js",
                            ".txt",
                            ".xml",
                            ".html",
                            ".php",
                            ".py",
                            ".dynamic",
                            ".mov",
                            ".pdf",
                            ".nav",
                            ".body",
                            ".foot",
                            ".head",
                            ".zip"]
                            
        self.supportedImages = [".png",
                                ".jpg",
                                ".jpeg",
                                ".tif",
                                ".tiff",
                                ".gif",
                                ".pnm",
                                ".pcx",
                                ".ico",
                                ".cur",
                                ".ani",
                                ".xpm",
                                ".PNG",
                                ".JPG",
                                ".JPEG",
                                ".TIF",
                                ".TIFF",
                                ".GIF",
                                ".PNM",
                                ".PCX",
                                ".ICO",
                                ".CUR",
                                ".ANI",
                                ".XPM"]
        
        
        self.loadFiles()
        
                
        #       self.initialized = True
        


    # ------------------------------------------------------------
    
    @afterThisUpdateStatusInfo
    def loadFiles(self):
        #self.projectController.treeViewReset()
        self.projectController.projectRootItem = self.projectManager.controller.findTreeItemByText(self.getProject())
        
        self.setItemGroups(self.mergeSupportedAndUnsupportedFileGroups())
        
        self.itemsInGroups = {}
        self.loadGroupItems() # this call populates the itemsInGroups List

        self.projectController.treeViewExpandItem(self.projectController.projectRootItem)
        self.projectController.selectTreeItem(self.projectController.projectRootItem)
      
        # mark queued files for the first time
        self.projectController.markAllQueuedFiles()
        
    
    def mergeSupportedAndUnsupportedFileGroups(self):
        
        allFileGroups = []
        
        for group in self.supportedFiles:
            allFileGroups.append(group)
        
        
        for group in self.getAllFileExtensionsFromParts():
            if allFileGroups.count(group) == 0:
                                
                allFileGroups.append(group)
        
        # remove groups we would like to ignore
        toIgnore = ['.head',
#                    '.foot',
#                    '.body',
#                    '.nav',
                    '.htm',
                    '.rss',
                    '.DS_Store']
                    
        
        
        for imageType in self.supportedImages:
            toIgnore.append(imageType)
            # also ignore the img when the .ext is uppercase
            toIgnore.append(imageType.upper())
    
        
        for item in toIgnore:
            try:
                allFileGroups.remove(item)
            
            except:
                sys.stdout.write("*")
        
        
        
        # remove _local and _content files
        for item in allFileGroups:
            if item.endswith("_local"):
                allFileGroups.remove(item)
            
        return allFileGroups
    
    # ------------------------------------------------------------

    def getAllFilesFromParts(self):
        """Returns a list of all the files in the parts folder."""
        return os.listdir(self.getPathParts())
        
    # ------------------------------------------------------------
    
    def getAllFileExtensionsFromParts(self):
        """ returns a list of all file extensions in parts"""      
        theExtensions = []
        for file in self.getAllFilesFromParts():
            theExt = os.path.splitext(file)[-1]
            if theExtensions.count(theExt) == 0: 
                theExtensions.append(theExt)
        
         
        return theExtensions
        
    # ------------------------------------------------------------
    
    def replaceStringInAllItems(self, old, new):            
        """
        Replaces old with new in all text based files that are in the parts
        folder.
        
        Note: there is no distinction between binary and text files
        only a try: block that fails (then it is likely to be a binary)
        if the anything goes wrong        
        """
        
        files = []
        #originalGroups = []
        itemGroups = self.getItemGroups()
        
        #for group in itemGroups:
        #    originalGroups.append(group)
                
        more = ['.nav','.body','.foot','.head']
        
        for items in more:
            itemGroups.append(items)
        
        for x in itemGroups:
            for y in self.getFilesByExtension(x):
                files.append(y + x)
            
        for z in files:
            f_ = readFile(self.getPathParts() + z)
            
            try:
                if old in f_:
                    self.addToFtpQueue(z)
                f__ = f_.replace(old , new)
                writeFile(self.getPathParts() + z , f__)            
            except:
                m  = "Cannot replace in file %s\n" % z
                m += 'Possible (likely) binary file...'
                print  m
            
        #self.setItemGroups(originalGroups)
        
    # ------------------------------------------------------------        
   
    def setProjectPath(self, aPath):
        self.pathProject = aPath
        
    def getProjectPath(self):
        return self.pathProject

    # ------------------------------------------------------------
        

        
    # ------------------------------------------------------------
        
    def getItemsByGroup(self, groupName):
        """Returns items of a special group. The index is the position 
        of the group in itemGroups.
        """
        return self.itemsInGroups[groupName]
        
    # ------------------------------------------------------------

    
    def loadGroupItems(self):
        
#        def rejectFile(groupName, theFile):
#            """ reject files not in the current language"""
#            
#            if groupName in ['.content', '.dynamic']:
#                if not theFile.endswith(self.getLanguage()):
#                    return True
#            return False
        
        
        self.coreMessage("loading group items...")

        self.itemsInGroups = {}
                        
        for groupName in self.getItemGroups():
            result = self.getFilesByExtension(groupName)
            
            self.itemsInGroups[groupName] = result
            
            parentItem = self.projectController.findTreeItemByText(groupName)
            if parentItem:
                for file in result:
                    # if rejectFile(groupName, file): continue
                    self.projectController.treeViewAppendItem(parentItem, file, type="File")
                    

    # ------------------------------------------------------------
    
    def getFilesByExtension(self, ext):
        """ext is in the .ext format eg. .jpg  or .content."""                
        theResult = []

        for thing in os.listdir(self.getPathParts()):
            (pfad, datei) = os.path.split(thing)
            (eins, zwei)  = os.path.splitext(datei)
            if zwei == ext:
                theResult.append(eins)
                
        return theResult
        
    # ------------------------------------------------------------
        
    def setItemGroups(self, groups):
        for item in groups:
            self.projectController.treeViewAppendItem(self.projectController.projectRootItem, item)
        
        self.itemGroups = groups
        
    def getItemGroups(self):
        return self.itemGroups
 

#    def getLanguage(self):
#        try:
#            return self.language
#            
#        except:
#            return "No Language"

#
#    @afterThisUpdateStatusInfo
#    def setLanguage(self, lang):
#        self.language = lang
#        
    # ------------------------------------------------------------
    @afterThisUpdateStatusInfo
    def setProject(self, proj):
        self.project = proj
       
    
    
    def getProject(self):
        
        return self.project
        
    # ------------------------------------------------------------

    def getPathParts(self):
        return self.pathParts

    # ------------------------------------------------------------
 
    def coreMessage(self, message):
        print 'makerCore: %s' % str(message)


    def closeProject(self):
        # call the cleanUp method
        
        self.cleanUp()
        
        if self.getFtpQueue():
            self.saveFtpQueue()



    def cleanUp(self):
        """
        some cleanup things
        """
        print "cleaning up"
        if os.path.isfile(os.path.join(self.getProjectPath(), "makerPrintOut.html")):
            print "deleting printOut file"
            os.remove(os.path.join(self.getProjectPath(), "makerPrintOut.html"))                   


    # ------------------------------------------------------------

    def importImage(self):
        
        makerImageImporter.MakerImageImporter(self, self.projectController.view)
        self.setImageSyncNeeded(needed = True)
        
    def deleteImage(self):
        
        delImg = makerDeleteImage.DeleteImg(self, self.projectController)
        delImg.deleteImage()
        
            
    def syncImages(self, verbose = True):
        """
        Sync local and remote image files
        
        """
        
        if not self.checkIfProjectIsSetUp(verbose = True):
            return
             
        self.serverLogin()
        if not self.server.status == "connected":
            return
                   
        imagesToUpload = []
        imagesToDownload = []
            
        
        remoteImages = self.getRemoteImageFiles()
                
        localImages = self.getImageFiles()
            
            
        for image in remoteImages:
            if localImages.count(image) == 0:
                imagesToDownload.append(image)
             
        for image in localImages:
            if remoteImages.count(image) == 0:
                imagesToUpload.append(image)
              
              
        if imagesToUpload == [] and imagesToDownload == []:
            self.serverLogout()
            if verbose == True:
                self.projectController.infoMessage("Nothing To Sync!")
            return
           
      
                
        if imagesToDownload != []:
            self.projectController.showProgress(len(imagesToDownload),"downloading:", title="synchronizing images...")
            count = 0
            for image in imagesToDownload:
                self.projectController.updateProgressMessage(count,"downloading:" + image)
                self.downloadFile(os.path.join(self.getRemoteGfxFolder(),image),
                                               os.path.join(self.getPathParts(),image),
                                               "binary")
                count += 1
             
                        
        if imagesToUpload != []:
            self.projectController.showProgress(len(imagesToUpload),"uploading:", title="synchronizing images...")
            count = 0
            for image in imagesToUpload:
                self.projectController.updateProgressMessage(count,"uploading:" + image)
                self.uploadFile(os.path.join(self.getPathParts(),image),
                                              self.getRemoteGfxFolder(),image,
                                              "binary")
                count += 1
            self.projectController.killProgressBar()
        
        
        self.serverLogout()
        self.projectController.killProgressBar()
        self.setImageSyncNeeded(needed = False)
    
    def setupProjectAndInitServerlink(self):
        
        self.projectSetup()
        self.coreMessage('Initializing link to ftp server')
        self.server = makerServerlink.Server(self)


    def saveProjectAsTemplate(self, event = None):
        
        def resetProjectSetup(pathToExported = None):
            string = """<?xml version="1.0" encoding="ISO-8859-1" ?>
            <project_setup>
            <version>1</version>
            <sprache>en</sprache>
            <encoding>utf-8</encoding>
            <add_language>de</add_language>
            <gfx_folder>gfx/</gfx_folder>
            <ftp_host>not set</ftp_host>
            <ftp_user>not set</ftp_user>
            <ftp_password>None</ftp_password>
            <ftp_root>.</ftp_root>
            <url>http://www.yourserver.com/</url>
            </project_setup>"""
            
            xPath = os.path.join(pathToExported, "setup", "project_setup.xml")
            
            writeFile(xPath, string)
        
        
        def deleteHiddenFiles(root = None):
            path = root
            maxDepth = 3
            folderDepth = -1
            for root,subFolders,files in os.walk(path):
                folderDepth += 1
                if folderDepth < maxDepth:  #limit folder depth for deletion to 3 (safety)
                    for root,subFolders, files in os.walk(path, topdown=False):#traverse filesystem from "path" in reverse
                        #delete files begining with "."
                        for file in files:
                            if file.startswith("."):
                                dPath = os.path.join(root,file)
                                #print dPath
                                self.projectController.updateProgressPulse("cleaning up: " + dPath)
                                os.remove(dPath)
                                #delete folders begining with "."
                        for dir in subFolders:
                            if dir.startswith("."):
                                dPath=os.path.join(root,dir)
                                self.projectController.updateProgressPulse("cleaning up: " + dPath)
                                shutil.rmtree(dPath, ignore_errors=True)
        
        
        
        m = "If you are exporting a template, make sure that you have "
        m += "a current screenshot included.\n"
        m += "Save this screenshot as 'preview.jpg' into your parts folder. "
        m += "Dimensions should be 320x240 pixels."
        
        
        self.projectController.infoMessage(m)
        
        tgt = self.projectController.dirDialog("Save Template To:")
        if not tgt: return
        
        fullTarget = os.path.join(tgt, self.getProject())
        
        if os.path.isdir(fullTarget):
            if self.projectController.askYesOrNo("'" + str(fullTarget) + 
                                                 "' already exists! Would you like to overwrite it?") != "Yes":
                return
            else:
                shutil.rmtree(fullTarget, ignore_errors=True)
        
        os.mkdir(fullTarget)
        
        src = self.getProjectPath()
        self.projectController.showProgress(limit=1, Message="Saving template...", title="Saving template...")
        copyFileTree(src, fullTarget, [], self.projectController.updateProgressPulse, ("storing: " + self.getProject()))
                     
        deleteHiddenFiles(root = fullTarget)
        resetProjectSetup(fullTarget)  
        self.projectController.killProgressBar()
        
        

    def systemSetup(self):
        """Sets up the CMS. Data is read from system.xml"""

        self.homeDir = os.path.dirname(sys.argv[0])

        if os.name == 'nt':
            self.coreMessage('nt found converting path')
            new = self.homeDir.replace('\\','/')
            self.homeDir = new
                
        self.pathSystem = os.path.join(self.homeDir, 'system')

        self.coreMessage('Setting up system')
      
        class XmlReader(ContentHandler):
            def __init__(XmlReader, scrwid=79, *args):
                ContentHandler.__init__(XmlReader, *args)

            def startElement(XmlReader, name, attrs):
                XmlReader.start_name = name
                if XmlReader.start_name=="System_Setup":
                    sys.stdout.write("setting up system...\n")

            def endElement(XmlReader, name):
                XmlReader.end_name = name
                if XmlReader.end_name=="System_Setup":
                    sys.stdout.write("\n done\n")
                
            def characters(XmlReader, chars):
                if XmlReader.start_name == "feedbackadress":
                    self.feedbackadress = chars   
                XmlReader.start_name = ""
                
        parse(self.getSystemSetupFilename(), XmlReader())
        
    # ------------------------------------------------------------
    @enforcePassword
    def serverLogin(self):
        """Login to FTP server."""        
        self.projectController.showProgress(2, "logging in...", "logging in...")
        self.projectController.updateProgressMessage(1, "logging in...")
        try:
            self.server.login()
            self.coreMessage("Logged in to server: OK...")
            self.projectController.killProgressBar()
            return True
        except:
            self.projectController.killProgressBar()
            self.projectController.errorMessage("Log in to server: FAILED...")
            return False
        
        
    def serverLogout(self):
        """Logout from the FTP server."""        
        self.projectController.showProgress(2, "logging out...", "logging out...")
        self.projectController.updateProgressMessage(1, "logging out...")
        try:
            self.server.logout()
            self.coreMessage("Logged out of server: OK...")
            self.projectController.killProgressBar()
            return True
        except:
            self.projectController.killProgressBar()
            self.projectController.errorMessage("Logging out of server: FAILED...")
            return False
        
    # ------------------------------------------------------------

    def checkIfRemoteDirIsDir(self, aDir):
        return self.server.isdir(aDir)

    # ------------------------------------------------------------

    def makeRemoteDir(self, aDir):
        return self.server.mkd(aDir)
            
    # ------------------------------------------------------------           
    
    
    def makeAll(self, event=None):
        """Rebuilds all web sites for the current language, and is queuing them.
        This method is not invoking any upload functions like in version < 0.91
        
        """
           
        def initForMakeAll(name, group):
                
            theClass = self.getFileClassForSupportedGroup(group)
            file = theClass(self, name, view=False)
            self.setCurrentFile(file)
        
        if self.getCurrentFile():
            nowFile = self.getCurrentFile()
        else:
            nowFile = None
        
        pagelist = self.getFilesByExtension(".content")
        #pagelist = []
        
#        # filter language
#        for i in list:
#            if i.endswith(nowFile.getLanguage()): 
#                pagelist.append(i)
#                
        
        self.projectController.showProgress(len(pagelist),"rebuilding websites")
        # the counter for the progress dialog
        step = xrange(len(pagelist))[0]     

        for i in pagelist:
            try:
                initForMakeAll(i,".content")
                x = self.getCurrentFile()
                x.makeWebSite()
                self.projectController.updateProgressMessage(step,"making page: "+ x.getName())
                step += 1
                
                
            except:
                print "Make all failed for :" , i
                
        self.projectController.killProgressBar()
        
        self.setCurrentFile(nowFile)
    

    def testFTPFromSetupFile(self):
        psfn = self.getProjectSetupFilename()
        theInformation = self.getProjectInformation(psfn)
        
        host = theInformation['ftp_host']
        user = theInformation['ftp_user']
        root = theInformation['ftp_root']
        
        print "testing connection from file...", host, user, root 
        
        if host == "not set" or user == "not set":
            return False
                
        passw = self.projectController.password("Please enter FTP password...")
        
        if self.testFtp(host, user, root, passw) != True:
            return False
        else:
            self.saveValidFTPHost(host, user, root)
            return True 
        

    def testFtp(self, host, user, root, passw):
        """
        Returns True if FTP settings are good, else an error string 
        about what is wrong. If the password is good it is stored
        and used for upcoming connections.
        """
  
        self.projectController.showProgress(4,"testing Hostname: " + host)
        testFtp = FTP()
        testFtp.set_debuglevel(2)
        try:
            print "action testFTP: testing hostname..."
            print "-----------------------------------"
            testFtp.connect(host)
            print testFtp.getwelcome()
        except Exception, e:
            self.projectController.killProgressBar()
            testFtp.close()
                        
            return "bad hostname!" 
            

        try:
            self.projectController.updateProgressMessage(3,"testing Username: " + user)
            print "action testFTP: testing username..."
            print "-----------------------------------"
            print testFtp.sendcmd("USER " +user )
        except ftplib.all_errors, e:
            testFtp.close()
            self.projectController.killProgressBar()
            
            return str("Error No:\n" +  e[0] + "\nbad username")
        
        try:
            self.projectController.updateProgressMessage(2,"testing Password" )
            print "action testFTP: testing password..."
            print "-----------------------------------"
            testFtp.sendcmd("PASS " +passw )
                     
        except ftplib.all_errors,e:
            
            self.projectController.killProgressBar()
            testFtp.close()
            self.setRemotePassword(None)
            # the fact that the server is accepting the username does not
            # mean that it is valid
            
            return str("Error No:\n" +  e[0] + "\nbad username or password")
        
        try:
            self.projectController.updateProgressMessage(1,"testing root" )
            testFtp.cwd(root)
                     
        except ftplib.all_errors,e:
            
            self.projectController.killProgressBar()
            testFtp.close()
            self.setRemotePassword(None)
                        
            return str("Error No:\n" +  e[0] + "\n bad path to project")
            
        self.projectController.killProgressBar()
        #self.projectController.infoMessage("All FTP settings are good.")
        testFtp.close()
        
        return True
        
    def addAllFilesToQueue(self):
        
        # build all content files
        self.makeAll()
        
        distributionData = self.readDistributionTable()
     
        listOfFiles = []
        
        for aDict in distributionData:
            listOfFiles.append(aDict["ftp_source"])
            
        
        for file in listOfFiles:
            # .htm files or in other words .content are already queued thru make all
            if not file.endswith(".htm"):
                try:
                    self.addToFtpQueue(file)
                except Exception, e:
                    self.projectController.errorMessage("Unable to add " + 
                                                                    file + 
                                                                    " to queue: \n" + 
                                                                    str(e) + "\n Skipping " + 
                                                                    file + "...")


    def uploadEverything(self, event=None):
              
        if not self.checkIfProjectIsSetUp(verbose=True):
            return

        self.addAllFilesToQueue()

        if not makerCheckInternetConnection.check():
            self.projectController.infoMessage("No internet connection!\nSorry, cannot send files to server...")   
        else:
            self.publishQueuedFiles()
            self.syncImages(verbose = False)


    def uploadFile(self, theFile, remoteFolder, theTarget, theFtpMode):
        """
        Uploads a single file and returns a boolean indicating outcome.
        You have to be logged in to do this.
        """
        
        try:
            
            self.server.upload(theFile, remoteFolder, theTarget, theFtpMode)
               
            return True
        except:
            
            return False
    
    
    def downloadFile(self, remoteFile, localFile, theFtpMode):
        """
        downloads a single file and returns file ?
        You have to be logged in to do this.
        """
        if self.server.download(remoteFile, localFile, theFtpMode):
            return True
        else:
            return False
            
    
    # ------------------------------------------------------------ 
 
    
    def renameRemoteFile(self, oldName, newName):
        try:
            self.server.rename(oldName, newName)
            return True
        except:
            return False
    # ------------------------------------------------------------ 
 
    def deleteRemoteFile(self, remoteFolder, theFile):
        """
        delete remote File
        you have to be logged in to do that
        returns True or False
        
        if one of the parameters is "undefined" which is the value in the
        distribution table for pages that exist only locally -
        this method returns True but does nothing
        """
        
        if remoteFolder=="undefined": return True
                
        res = self.server.delete(remoteFolder, theFile)
        if res != True:            
            return False
        else:
            return True
    # ------------------------------------------------------------             
            
    def getRemoteGfxFolder(self):
        
        return self.gfxFolder
            
    # ------------------------------------------------------------ 
        
    def getSystemPath(self):
        return self.pathSystem

    def getSystemSetupFilename(self):
        return os.path.join(self.getSystemPath(), 'system_setup.xml')

    
    def getProjectSetupFilename(self):
        return os.path.join(self.getProjectPath(), "setup/project_setup.xml")

    # ------------------------------------------------------------ 
    
    def initFtpQueue(self):
        """
        * check if there is an old queue
        * set the queue with old values or to []
        """
        self.ftpQueue = []
        
        currQueue = os.path.join(self.getPathParts(), "current.queue")
        if os.path.isfile(currQueue):
            bFile = open(currQueue,"rb")
            
            last = cPickle.load(bFile)
            lastQueue = cPickle.loads(last)
            bFile.close() 
            self.setFtpQueue(lastQueue)
            
            os.remove(currQueue)
        else:
            self.setFtpQueue([])
        self.coreMessage("FTP Queue: %s" % str(self.ftpQueue))
        
    # ------------------------------------------------------------             
        
    def setFtpQueue(self, files):
        """items is a list of maker files."""
        
        #for file in files:
        #    self.addToFtpQueue(file)
        
        self.ftpQueue = files
    
    # ------------------------------------------------------------     
    
    def isFileInQueue(self, theFile):
        """Returns a boolean."""
        
        if theFile in self.ftpQueue:
            return True
        else:
            return False
        
    # ------------------------------------------------------------     
    
    @afterThisUpdateStatusInfo
    def addToFtpQueue(self, theFile):
        # check if item is already in queue
        # TO DO: change to use "thing in list" syntax
        if self.ftpQueue.count(theFile) == 0:
            if os.path.isfile(os.path.join(self.getPathParts(), theFile)):
                self.ftpQueue.append(theFile)
                self.projectController.markQueuedFile(theFile)
            

    # ------------------------------------------------------------             

    @afterThisUpdateStatusInfo
    def deleteFromFtpQueue(self, theFile):
        self.ftpQueue.remove(theFile)
        
    # ------------------------------------------------------------     
    
    def getFtpQueue(self):
        """ returns the current FTP queue"""
        
        return self.ftpQueue

    # ------------------------------------------------------------     
    
    def renameItemInFtpQueue(self, oldName, newName):
        print self.ftpQueue
        if oldName in self.getFtpQueue():
            new = []
            for item in self.getFtpQueue():
                print "+"
                if item == oldName:
                    new.append(newName)
                else:
                    new.append(item)
        
            self.ftpQueue = new
            print self.ftpQueue
    
    # ------------------------------------------------------------     
    
    
    def clearFtpQueue(self):
        """Clears the queue with no warning."""
        self.ftpQueue = []

    # ------------------------------------------------------------     
    
    def saveFtpQueue(self):
        """Serializes the queue for the next session."""
        self.coreMessage("Saving FTP Queue for later...")
        currentQueue = self.getFtpQueue()
        bytes = cPickle.dumps(currentQueue, 2)
        
        bFile = open(os.path.join(self.getPathParts(),"current.queue"), "wb")
        cPickle.dump(bytes, bFile, 2)
        bFile.close()
        
     # ------------------------------------------------------------     
    
    @enforcePassword
    def publishQueuedFiles(self, event=None):
        """ also checks for image sync """
        if not self.checkIfProjectIsSetUp():
            self.projectController.errorMessage("You need to setup your project to do that...")
            return
            
        nowFile = self.getCurrentFile()
        
        publishedFiles = []
        
        self.projectController.showProgress(len(self.getFtpQueue()), 
                                            "uploading:", 
                                            title="uploading...")
        
        self.serverLogin()
        if not self.server.status == "connected":
            self.projectController.killProgressBar()
            return
        
        count = 0
        
        for aFile in self.getFtpQueue():
            split = os.path.splitext(aFile)
            self.justInitFile(split[0], split[1])
            
            fName = self.currentFile.getName()
            fExt = split[1]
            
            fileName = fName + fExt
                                    
            # mark file as published only when it is so
            
            
            # here you publish
            self.projectController.updateProgressMessage(count, fileName)
            self.currentFile.publish()
            count += 1
            
            
            publishedFiles.append(fileName)
            #if self.publishCurrentFile() == True:
            
            # remove the marker in the tree item
            self.projectController.markQueuedFile(fileName, mark=False)
            
            
            
                #reset = [self.currentFile.getName() + split[1]]
                #self.resetTreeItemIconForFiles(reset)
                        
                #self.GUI.DisablePublishButton()
        
        
        self.serverLogout()
    
        
        self.setCurrentFile(nowFile)
        
        # delete from Queue
        
        for file in publishedFiles:
            self.deleteFromFtpQueue(file)
        
        if self.imageSyncNeeded:
            self.syncImages(verbose = False)    
        self.projectController.killProgressBar()
        
        
    
    
    
      # ------------------------------------------------------------    
      # -- password stuff
      #-------------------------------------------------------------
        
        
    def getPassAttempts(self):
        """Returns the number of password attempts."""
        print "password attempt # ", self.passAttempts
        return self.passAttempts
       
    def incPassAttempts(self):
        """Increases by 1 the password attempts."""
        self.passAttempts += 1
    
    def clearPassAttempts(self):
        """Sets the number of pass attempts to zero."""
        self.passAttempts = 0
            
    # ------------------------------------------------------------    
            
    def maxPassAttemptsReached(self):
        return self.getPassAttempts() == Constants.MAX_PASS_ATTEMPTS
    
    # ------------------------------------------------------------    
    
    def dealWithMaxPassReached(self):
        m = 'Sorry, no more password attempts allowed. Exiting...'
        self.projectController.errorMessage(m)
        sys.exit()
    
        # ------------------------------------------------------------    
    
    def loadPassword(self):
                        
        def passwordOK(passw):
            """ password has been entered"""
            passw = passw.strip()
            if not passw: return False
            result = self.testFtp(self.ftpHost,
                                      self.ftpUser,
                                      self.ftpRoot,
                                      passw)
            return result
            
            
    
        if self.remotePasswordIsSet(): return True
            
        passw = self.projectController.password("Please enter FTP password...")
        
        if not passw:
            return False
        
        while passw is not None and passwordOK(passw) != True:
            self.handleBadPassword()                
    
            if self.maxPassAttemptsReached():
                self.dealWithMaxPassReached()
    
            passw = self.projectController.password("Please enter FTP password...")
    
        self.setRemotePassword(passw)
        self.clearPassAttempts()
        return passw != None
    
        # ------------------------------------------------------------    
        
    def handleBadPassword(self):
        self.incPassAttempts()
        left = Constants.MAX_PASS_ATTEMPTS - self.getPassAttempts()
        m  = 'Wrong password!'
        m += ' You have %d attempts left...' % left
        self.projectController.errorMessage(m)
    
        # ------------------------------------------------------------    
        #-------------------------------------------------------------
   
    
    
    
    def isFileBinary(self, file):
        """Returns a boolean. 
        PDF files are treated as binary by default."""
        
        if os.path.splitext(file)[-1].lower() == '.pdf':
            print 'PDF file found. Is considered binary.'
            return True
   
        #print "Checking file..."
           
        textCharacters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
        nullTrans = string.maketrans("", "")
        
        s = readFile(file)
        
        if "\0" in s:
            return True
        
        if not s:  # Empty files are considered text
            return False
    
        # Get the non-text characters (maps a character to itself then
        # use the 'remove' option to get rid of the text characters.)
        t = s.translate(nullTrans, textCharacters)
    
        # If more than 30% non-text characters, then
        # this is considered a binary file
        if len(t)/len(s) > 0.30: return True    
        return False
        
    #---------------------------------------------------------------------
     
    def setFtpHost(self, host):
        self.ftpHost = host
    
    def getFtpHost(self):
        return self.ftpHost
    
                        
    def setFtpUser(self, user):
        self.ftpUser = user
    
    
    def getFtpUser(self):
        return self.ftpUser
    
    
    def setFtpRoot(self,root):
        self.ftpRoot = root
    
    def getFtpRoot(self):
        return self.ftpRoot
    
    
    
    # ------------------------------------------------------------ 
   
    # ------------------------------------------------------------
    
    def checkIfProjectIsSetUp(self, verbose=False):
        """
        Determines weather FTP settings are useful
        
        returns True or False
        
        """
        
        # The project is NOT set up when:
        #
        # - there is no internet connection since we cannot test the settings
        # - there is no pickled file called validFTP
        # 
        #
        #
        
        connection = makerCheckInternetConnection.check()
        if not connection:
            if verbose:
                self.projectController.infoMessage("No Internet Connection !")
            return False
        
        
        if self.readValidFTPFile():
            # compare with setup data
            
            valid = self.readValidFTPFile()
                    
            psfn = self.getProjectSetupFilename()
            projectData = self.getProjectInformation(psfn)
            
            if projectData['ftp_host'] == valid[0] and projectData['ftp_user'] == valid[1]:
                return True
            
            
            
            else:
                m = "All right. It seems like you have manually changed your setup file.\n"
                m += "The current FTP settings have not been tested. Please use Project / Project Setup "
                m += "to run a test."
                self.projectController.errorMessage(m)
                return False
        
        
        
        
        
        else:
            if connection:
                if not self.testFTPFromSetupFile():
                    if verbose:
                        self.projectController.errorMessage("Please set up your FTP connection!")
                    return False
                else:
                    return True
            else:
                # no internet connection
                return False     
 
 
    def saveValidFTPHost(self, host, user, root):
        
        data = [host, user, root]
        bytes = cPickle.dumps(data, 2)
        
        bFile = open(os.path.join(self.getProjectPath(),"setup/valid.ftp"), "wb")
        cPickle.dump(bytes, bFile, 2)
        bFile.close()
    
    
    def readValidFTPFile(self):
               
        validFTPFile = os.path.join(self.getProjectPath(), "setup/valid.ftp")
        if os.path.isfile(validFTPFile):
            bFile = open(validFTPFile,"rb")
            
            last = cPickle.load(bFile)
            validConnection = cPickle.loads(last)
            bFile.close() 
            return validConnection

        else:
            return False


    def projectSetup(self):
        """
        This is the project setup function. It is reading all the settings
        from the projects setup.xml
        """
        class XmlReader(ContentHandler):                
            def __init__(XmlReader, scrwid=79, *args):
                
                ContentHandler.__init__(XmlReader, *args)
                
            def startElement(XmlReader, name, attrs):
                XmlReader.start_name = name
                if XmlReader.start_name=="project_setup":
                    sys.stdout.write("*")

            def endElement(XmlReader, name):
                XmlReader.end_name = name
                if XmlReader.end_name=="project_setup":
                    sys.stdout.write("\n done\n")
                
            def characters(XmlReader, chars):
                sys.stdout.write("*")
#                if XmlReader.start_name == "sprache":
#                    self.language = chars                    
                if XmlReader.start_name == "encoding":
                    self.encoding = chars
#                elif XmlReader.start_name == "add_language":
#                    self.add_language = chars
                elif XmlReader.start_name == "gfx_folder":
                    if not chars.endswith("/"):
                        self.gfxFolder = chars + "/"
                    else:
                        self.gfxFolder = chars
                elif XmlReader.start_name == "stylesheet":
                    self.stylesheet = chars
                elif XmlReader.start_name == "rss_feed":
                    self.rss_feed = chars
                elif XmlReader.start_name == "rss_page":
                    self.rss_page = chars
                elif XmlReader.start_name == "rss_language":
                    self.rss_language = chars
                elif XmlReader.start_name == "remote_rss_dir":
                    self.remote_rss_dir = chars
                elif XmlReader.start_name == "url":
                    self.url = chars
                elif XmlReader.start_name == "ftp_host":
                    self.setFtpHost(chars)
                elif XmlReader.start_name == "ftp_user":
                    self.setFtpUser(chars)
                elif XmlReader.start_name == "ftp_root":
                    self.setFtpRoot(chars)
                elif XmlReader.start_name == "startup_page":
                    self.page = chars
                       
                XmlReader.start_name = ""          

        # this is default for older projects < version 0.8 that did
        # not have the encoding node in the setup file
        self.encoding = 'latin-1'
        
        parse(self.getProjectSetupFilename(), XmlReader())
        some = os.path.split(self.getProjectPath())   
        self.setProject(some[1]) # use the projects dir name as project name
        
        return True

    # ------------------------------------------------------------     

#    def switchLanguage(self, lang):
#        
#        if lang == self.getLanguage():
#            return
#        
#        theList = self.filterFilesByLanguage(self.getFilesByExtension(".content"), 
#                                             self.getLanguage())
#        
#        # add dynamics        
#        for x in self.filterFilesByLanguage(self.getFilesByExtension(".dynamic"), 
#                                            self.getLanguage()):
#            theList.append(x)
#        
#        
#        for fName in theList:
#            item = self.projectController.findTreeItemByText(fName)
#            
#            # check if you have to delete from NoteBookPages
#            
#            # replace with None
#            
#            self.projectController.treeViewDeleteItem(item)
#        
#        
#        
#                           
#        self.setLanguage(lang)
#        
#        for type in [".content", ".dynamic"]:
#        
#            newFiles = self.filterFilesByLanguage(self.getFilesByExtension(type), self.getLanguage())
#             
#            for file in newFiles:
#                self.projectController.treeViewAppendItem(self.projectController.findTreeItemByText(type),
#                                                          file, type="File")
#                            
#        
#        self.projectController.reBindSelectEvent()
#        
#        #self.loadFiles()    
        
    # ------------------------------------------------------------     

#    def deleteMakerFile(self):
#        """Deletes local MakerFiles."""
#
#        self.coreMessage("Deleting: %s" % self.getCurrentFileName())
#        
#        try:
#            self.currentFile.delete()
#            return True
#        except:
#            return False
#        
    # ------------------------------------------------------------    
    
    def getPageLocationsBySource(self, theObject):
        """Returns a list of the pages locations on the server."""

        self.remotePageLocations = []
               
        class XmlReader(ContentHandler):        
            def __init__(XmlReader, scrwid=79, *args):
                ContentHandler.__init__(XmlReader, *args)
                
            def startElement(XmlReader, name, attrs):
                XmlReader.start_name = name
                        
                if XmlReader.start_name == "rule":
                    page   = theObject                            
                    object = attrs.get("ftp_source")

                    if object == page:
                        remoteDir = attrs.get("remote_dir")
                        if not remoteDir.endswith('/'):
                            remoteDir += '/'
                        
                        location = remoteDir + attrs.get("target") 
                        self.remotePageLocations.append(location)
                    
        parse(self.getDistributionTableFilename(), XmlReader())
              
        return self.remotePageLocations
    
    # ------------------------------------------------------------    
    
    def addToDistributionTable(self, ftpSource, remoteDir, ftpMode, target):
        """
        Adds information about a file to the distribution table.
        ftpSource : internal filename
        remoteDir :
        ftpMode   : lines or binary
        target    : filename on server
        """
        dictlist = self.readDistributionTable()
        new = {}
        new["ftp_source"] = ftpSource
        new["remote_dir"] = remoteDir
        new["ftp_mode"]   = ftpMode
        new["target"]     = target
        dictlist.append(new)

        self.writeDistributionTable(dictlist)
    
    # ------------------------------------------------------------    
    
    def deleteFromDistributionTable(self, filename):
        """Remove ALL rules for a file from the distribution table."""

        table = self.readDistributionTable()
        self.coreMessage('Current distribution table:\n%s' % str(table))

        pos = []
        # TO DO: convert to use "thing in table" syntax (more pythonic)
        for i in range(len(table)):
            if table[i]["ftp_source"] == filename:
                pos.append(i)
        
        x = pos[0]
        for i in range(len(pos)):
            x = pos[i]-i
            table.pop(x)
            
        self.writeDistributionTable(table)
    
    # ------------------------------------------------------------        
    
    # TO DO: convert to use DOM methods
    def writeDistributionTable(self, data):
        info  = self.getXmlHead()
        info += "<!-- file was created @: %s -->\n" % time.ctime()
        info += "<distribution>\n"
        
        for i in data:
            xl = i.keys()
            info += "<rule "
            for t in xl:
                info += t+'="'+i[t]+'" '
            info += "></rule>\n"
            
        info += "</distribution>"
        
        writeFile(self.getDistributionTableFilename(), info)
        
    # ------------------------------------------------------------        
    
    def getLocalFilesFromDistTable(self):
        
        sources = []
        data = self.readDistributionTable()
        for dict in data:
            sources.append(dict["ftp_source"])
        
        return sources
    
    
    def readDistributionTable(self):
        """
        Returns a list of dicts containing the distribution data.
        Reads from the current file.
        """
        self.distData = {}
        self.distList = []
        
        class XmlReader(ContentHandler):                
            def __init__(XmlReader, scrwid=79, *args):
                ContentHandler.__init__(XmlReader, *args)
                
            def startElement(XmlReader, name, attrs):
                if name == "rule":
                    self.distData["ftp_source"] = attrs.get("ftp_source")
                    self.distData["remote_dir"] = attrs.get("remote_dir")
                    self.distData["target"]     = attrs.get("target")
                    self.distData["ftp_mode"]   = attrs.get("ftp_mode")

            def endElement(XmlReader, name):                    
                if name == "rule":
                    self.distList.append(dict(self.distData))
                    self.distData.clear()
                
            def characters(XmlReader, chars):                    
                pass
                
        parse(self.getDistributionTableFilename(), XmlReader())
        
        return self.distList
    
    # ------------------------------------------------------------        
    
    def getDataForMakerMarker(self, theMarker):
        """Return the data that will replace a maker marker."""

        def getFileCreationDate(filename):
            f = open(filename,"r")       
            creationTime = os.fstat(f.fileno())
            f.close()
            return time.ctime(creationTime[-1])
        
        thePath = os.path.join(self.getPathParts(),
                               self.currentFile.getRealName())
        theDate  = getFileCreationDate(thePath)
        creationDate = "created: %s" % str(theDate)

        theData = {"!projectName!"  : str(self.getProject()).replace(".makerProject", ""),
                   "!pageName!"     : self.currentFile.getRealName(),
                   "!creationDate!" : creationDate,
                   "!todaysDate!"   : str(time.ctime()),
                    }
        try:
            return theData[theMarker]
        except:
            self.coreMessage("Marker %s not found !" % theMarker)
    
    # ------------------------------------------------------------
    
    def createNewDefaultFoldersFile(self):
            """
            this function is creating a new file called ./setup/defaultFolders.dat
            all types present at the moment of creation get the . value as default
            """
            typesToIgnore = [".dynamic",""]
            
            data = {}
            
            for type in self.getItemGroups():
                if type not in typesToIgnore:
                    data[type] = "."
            
            makerUtilities.writeDataToFile(data, os.path.join(self.getProjectPath(), 
                                                             "setup/defaultFolders.dat"))
            
      
    def readDefaultFoldersFile(self):
        """
        returns a dictionary
        {"filetype" : "defaultRemoteFolder"}
        """
        
        dataFile = self.getProjectPath() + "/" + "setup/defaultFolders.dat"
        if not os.path.isfile(dataFile):
            
            self.createNewDefaultFoldersFile()
            
        data = makerUtilities.readDataFromFile(dataFile)
        
        return data
    
    def writeDefaultFoldersFile(self, data):
        """
        """
        
        dataFile = self.getProjectPath() + "/" + "setup/defaultFolders.dat"
            
        data = makerUtilities.writeDataToFile(data, dataFile)
        
                     
    
    def getDefaultRemoteFolder(self, fileType):
        """
        returns a string
        
        the name of the default remote folder for fileType, 
        by reading the data from defaultFolders.xml
        if no entry is found in the data file the default value "."
        is returned
        """
                   
        default = "."
        dataFile = self.getProjectPath() + "/" + "setup/defaultFolders.dat"
        if not os.path.isfile(dataFile):
            
            self.createNewDefaultFoldersFile()
            
            return default      # the . dir is the default value
        
        data = makerUtilities.readDataFromFile(dataFile)
                
                        
        if fileType in data:
            remoteFolder = data[fileType]
        
        else:
            # add the new, unknown type to the data file
            data[fileType] = default
            makerUtilities.writeDataToFile(data, dataFile)
                        
            remoteFolder = default
        
        
        return remoteFolder
    
    # ------------------------------------------------------------

    def imageSyncNeeded(self):
        
        return self.imageSyncNeeded
        
    
    def setImageSyncNeeded(self, needed = False):
        self.imageSyncNeeded = needed




    def importFiles(self, event=None):
       	
        """Imports a MakerFile (handles all files, even binary)."""

        files = self.projectController._fileDialog()
        
        if not files:
            return
        
        filesToImport = []
        
        for item in files:
            print item.path()
            # these are NSUrls so we need to call path() 
            filesToImport.append(item.path())
        
        if filesToImport == []: return
        
        # just making sure that no images are imported this way
        
        for possibleImage in filesToImport:
            
            fileType = os.path.splitext(os.path.basename(possibleImage))[-1]
            
            if self.supportedImages.count(fileType.lower()) != 0:
                self.projectController.errorMessage("Please do NOT Import Images this way!\n" + 
                               "Use 'Import Image' instead!\n\n" + 
                               "Import canceled!")
                return
        
        
        # This might seem a little odd. Here is why it is dome this way.
        # In the file selector we need to enable all files because there is no
        # telling what the user might want to import.
        #
        # Images are not displayed in the treeView and are handled different from
        # all other files so we have to exclude them from being imported like 
        # any other file 
        
      
        # - - - 
        
        for file in filesToImport:
        
            try:
                
                fileName     = os.path.basename(file)
                filePath     = os.path.dirname(file)
                fileNameNoExt, fileType = os.path.splitext(fileName)
                
            except Exception, e:
                print str(e)
                return
    
            # just a flag for later
            isBinary = False
            flag   = 'r'        
            if self.isFileBinary(file):
                isBinary = True
                # we are only making this distinction on Xp or Vista
                # since the Mac and Linux handle binary data well 
                if os.name == 'nt': flag = 'rb'
                    
            content = readFile(file, binary=isBinary)
            
            theFile = os.path.split(file)[-1]
            
            # only display the rename message if the file already exists
            if os.path.isfile(os.path.join(self.getPathParts(),theFile)):
            
                m = "A file named '%s' already exists! " % theFile
                m += "Enter another name..."  
                
                name = self.projectController.inputWithValue(m, fileNameNoExt)
                
                # just in case someone hits OK 
                if name == fileNameNoExt:
                    name = None
            else:
                name = os.path.splitext(theFile)[0]
                    
            # ----
            if name is None or not name.strip():
                self.projectController.infoMessage("No File imported")
                return
    
            mode = 'lines'
            if isBinary: 
                mode = 'binary'
            print "adding maker file ", name, fileType, mode
            self.addMakerFile(name, fileType, content, mode)
            self.addToFtpQueue(name + fileType)
            
       

    def addLanguage(self, newLang=None, langName = None):
        
        
        # create header template
        
        contents = readFile(os.path.join(self.getProjectPath(),"templates", 
                                     self.getProjectLanguages()[0] + ".head"))
        writeFile(os.path.join(self.getProjectPath(),"templates", newLang + ".head"), contents)
        
        # ------
        
        fileTypesNeeded = ['.nav','.body','.foot']
        existingLangs = self.getProjectLanguages()
        
        for type in fileTypesNeeded:
            src = os.path.join(self.getPathParts(), existingLangs[0] + type)
            dst = os.path.join(self.getPathParts(), newLang + type)
            shutil.copyfile(src, dst)
            

            group = self.projectController.findTreeItemByText(type)
            if not group:
                group = self.projectController.treeViewAddFolder(type)
                    
            newItem = self.projectController.treeViewAppendItem(group, newLang, type=None)
            self.projectController.selectTreeItemAndLoad(newItem)
            
        m = "You have added the Language: '%s' to your project." % langName
        m += "\nThe following files have been created:\n"
        
        for type in fileTypesNeeded:
            
            m += "\t" + newLang + type + "\n"
            
        m += "Please translate them as needed."
        
        self.projectController.infoMessage(m)
        
        

    
    def removeLanguage(self, toRemove=None, langName = None):
        """ 
            toRemove is language code like de, en 
            langName is the written language name like 'German'
        """
        
        resp = self.projectController.askYesOrNo("This will remove all files of the language '" + langName 
                                           + "' and you will need to restart the application.\n Would you like to do that?" )
        
        if resp != "Yes":
            return
        
        
        # delete header template
        
        os.remove(os.path.join(self.getProjectPath(),"templates", toRemove + ".head"))
    
        # ------
        
        fileTypesNeeded = ['.nav','.body','.foot']
        
        for type in fileTypesNeeded:
            
           os.remove(os.path.join(self.getPathParts(), toRemove + type))
        

        types = [".content",".dynamic",".head"]
        
        for type in types:
            
            someFiles = self.getFilesByExtension(type)
            theList = self.filterFilesByLanguage(someFiles, toRemove)
            
            for item in theList:
                
                os.remove(os.path.join(self.getPathParts(), item + type))

        # exit
        self.projectManager.exitApplication()
    


    def addMakerFile(self, name=None, type=None, content=None, mode="lines"):    
        
        """
        Adds a file to the project parts/ directory.
         
        type = the file type, if type is .content a language marker 
        is added to the name. This will result in name_en.content but name.css
        this method also calls loadGroupItems to update the internal Lists
                
        mode is new since rev 112 
        either lines or binary - lines by default
                
        """
        
        depList = [".content", ".dynamic"]
        
        if not name:
        
            if type in depList:
                
                makerAddNewLanguageCodedFile.NewLangFile(self.projectController.view, self, type, content)
                return
                
            elif type == "other":
                
                m = "Enter a name for the new file: "
                name = self.projectController.input(m)
                
                # nothing was entered
                if not name: 
                    return
                else:
                
                    splitName = os.path.splitext(name)
                    
                    type = splitName[-1]
                    name = splitName[0]
                       
            else:
                
                m = "Enter a name for the new %s file: " % type
                name = self.projectController.input(m)
                
                       
                # nothing was entered
                if not name: return
                               
                                
        if not content:
            content = makerFileTemplates.getTemplate(type)
        
       
        def makerFileExists(thePath):
                    
            if os.path.isfile(thePath):
                message  = "%s is an existing file !\n" % thePath
                message += "Please try again."
                self.projectController.infoMessage(message)
                return True 
            return False
        
        def findLanguage(name):
            possibleLanguages = self.getProjectLanguages()
        
            for lang in possibleLanguages:
                if name.endswith("_" + lang):
                    return lang    
        
        
        addOn   = name + type
        newfile = self.getPathParts() + addOn
    
        exists = makerFileExists(newfile)
        if exists: 
            print "file exists !"
            return 
        
        
        # this is only for imported .content and dynamic files
        
        if type == ".content":
            
            lang = findLanguage(name)
        
            # TO DO: convert to use os.path.join()
            pathToHead = self.getPathParts()+"../templates/"+ lang +".head" 
            head = readFile(pathToHead)
                         
            pathToNewHead = self.getPathParts() + name +".head"
                                
            writeFile(pathToNewHead, head)
        
            # TO DO: convert to use os.path.join()
            nameInTable = name +  ".htm"
                                
            self.addToDistributionTable(nameInTable, 
                                        self.getDefaultRemoteFolder(type), 
                                        "lines", 
                                        nameInTable)
            
            newFile = self.getPathParts() + name + type
            writeFile(newFile, content)
        
                
        elif type==".dynamic":
        
            lang = getLanguage(name)
            
            # TO DO: convert to use os.path.join()
                                        
            newFile = self.getPathParts() + name +  type
            writeFile(newFile, content)
             
                                   
        isBinary = False
        if mode == "binary" and os.name == 'nt':
            isBinary = True
    
        writeFile(newfile, content, binary=isBinary)
    
                
        self.addToDistributionTable(addOn, 
                                    self.getDefaultRemoteFolder(type), 
                                    mode, 
                                    addOn)
            
        group = self.projectController.findTreeItemByText(type)
        if not group:
            group = self.projectController.treeViewAddFolder(type)
                    
        newItem = self.projectController.treeViewAppendItem(group, name, type=None)
        self.projectController.selectTreeItemAndLoad(newItem)


            
    # ------------------------------------------------------------   
    
    def help(self, topic):
        """Show http://www.makercms.org/tutorial/#topic in a browser."""
        webbrowser.open("http://www.makercms.org/tutorial/"+topic)
                
    # ------------------------------------------------------------

    def feedback(self):
        webbrowser.open("mailto:%s?subject=CMS Feedback" % self.feedbackadress)

    # ------------------------------------------------------------

    def viewInBrowser(self, url, uri):
        
        webbrowser.open(uri+url)
          
    # ------------------------------------------------------------

    # TO DO: convert to use DOM method
    def getXmlHead(self):    
        return  '<?xml version="1.0" encoding="ISO-8859-1" ?>'
                
    # ------------------------------------------------------------

    def setRemotePassword(self, password=None):
        """Store password used to access the FTP server. Default is None."""
        self.remotePassword = password
        
    def getRemotePassword(self):
        """Return the Password for the FTP server."""
        return self.remotePassword
        
    def remotePasswordIsSet(self):
        passw = self.getRemotePassword()
        return passw and passw.strip()

    # ------------------------------------------------------------
        
#    def preview(self, theContent):
#        self.currentFile.preview(theContent)
#        return True

    # ------------------------------------------------------------

    def distribute(self, theObject):
        """
        This method reads the file's information from the distribution table,
        and returns it as [remoteDir, target, ftpMode]
        """

        self.coreMessage("Looking up the distribution table...")

        locations = [] 

        class XmlReader(ContentHandler):
            def Upload(XmlReader):
                return    

            def __init__(XmlReader, scrwid=79, *args):
                ContentHandler.__init__(XmlReader, *args)
                
            def startElement(XmlReader, name, attrs):
                XmlReader.start_name = name
                        
                if XmlReader.start_name == "rule":
                    page = theObject
                            
                    object = attrs.get("ftp_source")
                    if  object == page:
                        ftpSource = self.getPathParts()+attrs.get("ftp_source")
                        remoteDir = attrs.get("remote_dir")
                        ftpMode   = attrs.get("ftp_mode")
                        target    = attrs.get("target") 

                        location = [remoteDir, target, ftpMode]
                        locations.append(location)

            def endElement(XmlReader, name):
                pass
                
            def characters(XmlReader, chars):
                pass
                
        parse(self.getDistributionTableFilename(), XmlReader())
        
        return locations

    # ------------------------------------------------------------
    
    def filterFilesByLanguage(self, listOfFiles, lang=None):
        """ filters a give list of files by language and returns the
            result
            language defaults to current language
            files is the filename without the extension
        """
        if not lang:
            lang = self.currentFile.getLanguage()
            
        result = []
        for aFile in listOfFiles:
            
            if aFile.endswith(lang): 
                result.append(aFile)
                
        return result
    
    
    
    def findContentFilesContainingThisDynamic(self, dynamic):
        """
        Returns a list of all .content files containing a reference
        to the given daynamic.
        """
                
        listOfFiles = []
        
        theList = self.getFilesByExtension(".content")
        for item in theList:
            pathToFile = os.path.join(self.getPathParts(), item + ".content")
            contentOfItem = readFile(pathToFile)
            
            if contentOfItem.find(dynamic.encode(self.encoding)) == -1:
                self.coreMessage("%s is not used in the file %s" % (dynamic,
                                                                    item))
            else:
                listOfFiles.append(item)

        return listOfFiles
    
    # ------------------------------------------------------------

    def getFileClassForSupportedGroup(self, group):
        """Returns the corresponding maker class given a group."""
             
        fileClasses = {".content" : makerFileTypes.MakerFileContent,     
                       ".css"     : makerFileTypes.MakerFileCss,     
                       ".cgi"     : makerFileTypes.MakerFileCgi,     
                       ".js"      : makerFileTypes.MakerFileJs,     
                       ".txt"     : makerFileTypes.MakerFileTxt,     
                       ".xml"     : makerFileTypes.MakerFileXml,     
                       ".php"     : makerFileTypes.MakerFilePhp,
                       ".py"     : makerFileTypes.MakerFilePython,       
                       ".html"    : makerFileTypes.MakerFileHtml,     
                       ".dynamic" : makerFileTypes.MakerFileDynamic,     
                       ".mov"     : makerFileTypes.MakerFileMov,     
                       ".zip"     : makerFileTypes.MakerFileZip,     
                       ".pdf"     : makerFileTypes.MakerFilePdf,
                       ".nav"     : makerFileTypes.MakerFileNav,
                       ".body"     : makerFileTypes.MakerFileBody,
                       ".foot"     : makerFileTypes.MakerFileFoot,
                       ".head"     : makerFileTypes.MakerFileHead,
                       ".head template" : makerFileTypes.MakerFileHeadTemplate
                       
                       }
        
        
        return fileClasses[group]

    # ------------------------------------------------------------
    
    def findOpenFileInstByName(self, fileName):
        for instance in self.projectManager.openFiles:
            instName = instance.getFileName()
            project = instance.core.getProject() 
                            # check if file is from another project
            if instName == fileName  and project == self.getProject():
                #print "returning ", instance.getFileName()
                return instance
        else:
            return None
    
    
    def justInitFile(self, name, group):
            """ for use when no interface interaction is needed"""
            print "just initalizing..."
            if group in self.supportedFiles:
                theClass = self.getFileClassForSupportedGroup(group)
                file = theClass(self, name, view=False)
            else:
                if self.isFileBinary(os.path.join(self.getPathParts(), name + group)):
                    file =  makerFileTypes.MakerFileUnsupportedBinaryFile(self, name + group, view = False)
                    
                else:
                    
                    file =  makerFileTypes.MakerFileUnsupportedTextFile(self, name + group, view = False)
                                
            self.setCurrentFile(file)
    
    
    @afterThisUpdateStatusInfo
    def loadFile(self, name, group):
        """Creates an new instance of a MakerFile"""    
        
        # check if group is supported if not use other classes
        
        existingInstance = self.findOpenFileInstByName(name + group)
        if existingInstance:
            #print "loading existing instance"
            self.setCurrentFile(existingInstance)
            # take control
            self.currentFile.fileController.bindActions()
            
        else:
        
            if group in self.supportedFiles:
                theClass = self.getFileClassForSupportedGroup(group)
                theFile = theClass(self, name)
                    
            else:
                if self.isFileBinary(os.path.join(self.getPathParts(), name + group)):
                    theFile =  makerFileTypes.MakerFileUnsupportedBinaryFile(self, name + group)
                    
                else:
                    
                    theFile =  makerFileTypes.MakerFileUnsupportedTextFile(self, name + group)
                                
                
            if theFile not in self.projectManager.openFiles:
                self.projectManager.openFiles.append(theFile)
            
            self.setCurrentFile(theFile)
                    
                # name in the line below is just the name eg.
                # index for index.htm cause .htm is determined in class
                
            self.currentFile.load()
           
            #return self.currentFile.load()
   
    # ------------------------------------------------------------

    @afterThisUpdateStatusInfo
    def setCurrentFile(self, aFile):
        """Set the ! instance of currentFile."""
        
        self.currentFile = aFile
            
    
    def getCurrentFile(self):
        """Get the ! instance of currentFile."""
        return self.currentFile    

    # ------------------------------------------------------------

    def switchContentEditMode(self):
        """Switching between .head and .content"""
        dict = {'.content': '.head'}
        mode = self.getContentEditMode()
        self.setContentEditMode(dict.get(mode, '.content'))
        
    def getContentEditMode(self):
        """Returns either .head or .content"""
        return self.contentEditMode
    
    def setContentEditMode(self, mode=".content"):
        """mode can be either .content (default) or .head"""
        self.contentEditMode = mode
               
    # ------------------------------------------------------------       
               
    def getCurrentFileType(self):
        return self.currentFile.type
    
    def getCurrentFileName(self):
        try:            
            return self.currentFile.name + self.currentFile.type
        except:
            return "No File loaded !"


    # ------------------------------------------------------------       
    
    def saveFile(self, theContent):
        self.coreMessage('saving...')
        self.currentFile.save(theContent)

    # ------------------------------------------------------------       

    def getProjectURL(self):
        return self.url

    # ------------------------------------------------------------       

    # TO DO: convert these 6 methods to use os.path.join()
    def getBodyFileName(self):        
        return self.getPathParts()+self.getLanguage()+'.body'

    def getFootFileName(self):
        return self.getPathParts()+self.getLanguage()+'.foot'

    def getNavigationFileName(self):        
        return self.getPathParts()+self.getLanguage()+'.nav'
    
    def getRSSFileName(self):
         return self.getPathParts()+self.rss_feed+'._content'
    
    def getRSSHeadFileName(self):
        return (self.getPathParts()+'rss.head')

    def getTemplateFileName(self):
        if not self.currentFile:
            return
        else:
            if not self.currentFile.getLanguage():
                return
            else:
                return os.path.splitext(self.getProjectPath()+"/"+ 
                                        "templates/"+ self.currentFile.getLanguage() + '.head')[0]

    def getProjectLanguages(self):
        """
        for each project language there is a file with the .nav extension
        eg. de.nav for German
        So here we extract existing languages by looking up all navigation 
        (.nav) files
        
        """
        list = self.getFilesByExtension(".nav")
        langList = []
        for item in list:
            langList.append(item)
        
        return langList



    # ------------------------------------------------------------           
    
    def restoreLocalFile(self):
        """If the file is not editable == binary this method does nothing."""

        self.coreMessage("Restoring original file")

        if self.currentFile.getEditable():
            pathToFile = self.getPathParts()+self.getCurrentFileName()+"_local"
            
            local = readFile(pathToFile)
            
            os.remove(pathToFile)
            
            writeFile(self.getPathParts()+self.getCurrentFileName(), local)
    
    # ------------------------------------------------------------       
    
    @enforcePassword
    def browseFtp(self):
        self.ftpBrowser = makerFtpBrowser.FTPBrowser(self.projectController.view)
        
        if not self.ftpBrowser.ftpBrowserAction_connect_(self.getFtpHost(), 
                                                         self.getFtpUser(),
                                                         self.getFtpRoot(),
                                                         self.getRemotePassword()):
            return None
        self.ftpBrowser.ftpBrowserAction_ls_()
        # return the pathname displayed when the ftpBrowser was shut
        pathName = self.ftpBrowser.ftpBrowserShow()
        
        return pathName 
    
    
    
    
    def backupLocalFile(self):        
        self.coreMessage("Backing up original file")

        bar = readFile(self.getPathParts()+self.getCurrentFileName())
        
        # save for restoration
        pathToFile = self.getPathParts()+self.getCurrentFileName()+"_local"
        writeFile(pathToFile, bar)
        
    # ------------------------------------------------------------       
    
    
    
    def updateAllImageReferences(self):
        """Updates all image references in the current file."""
        
        list = self.getImageFiles()

        for image in list:
            self.updateImageBase(image)
    

    
    def applyMakerMetaStamp(self):
        """
        puts a copyright stamp at the end of the <head> section
        """
        
        stamp = '  <meta name="generator" content="The Maker - Rapid Website Creation And Management" />'

        current = self.getCurrentFile()
        fileName = os.path.join(self.getPathParts(), current.getHead() + ".head")
        if current.getType() != ".content":
            return
        s = readFile(fileName)
        if not stamp in s:
            new = s.replace("</head>", stamp + "\n\n</head>")
            writeFile(fileName, new)
    
    
    
    def updateImageBase(self, theImage):
        """
        You must invoke self.backupLocalFile() before this method.
        
        Updates references to image files from local to the path on 
        the server one image at a time due to GUI interaction.

        After the file has been uploaded the self.restoreLocalFile()
        method has to be called.
        """

        theImage = theImage.encode(self.encoding)
        
        pathToFile = self.getPathParts() + self.getCurrentFileName()
        
        
        # replace images in single quotes
        urlJ = urlparse.urljoin(self.getProjectURL(), self.getRemoteGfxFolder())
        
                
        quoteList = [["'","'"],['"','"'],['url(',')']]
        
        for quotes in quoteList:        
            
            try:
                #self.coreMessage("Replacing single quoted imege: %s" % str(theImage))
                bar = readFile(pathToFile)
                this = quotes[0] + theImage + quotes[1]
                that = quotes[0] + urlJ + theImage + quotes[1]
                that = str(that).encode(self.encoding)
                newBar = bar.replace(this, that)
                writeFile(pathToFile, newBar)
            except Exception, e:
                print "replacing failed ", e
                
   
    # ------------------------------------------------------------        
        
    
    def getRemoteImageFiles(self):
        """returns a list of files in the remote image folder eg. gfx 
        you need to be logged in to do this
        """
        self.projectController.showProgress(1, "reading remote images...")
        imageList = []
        self.server.home()
        
        # does the folder exist ?
        
        remoteFolder = self.getRemoteGfxFolder()
        
        if not self.server.isdir(remoteFolder):
            self.server.mkd(remoteFolder)
            
        
        self.server.ftp.cwd(remoteFolder)
        list = self.server.ls()
        if list == []:
            return imageList
        
        for item in list:
            theFilesExt = os.path.splitext(item)[-1]
            if self.supportedImages.count(str(theFilesExt).lower()) > 0:
                imageList.append(item)
        self.projectController.killProgressBar()
        return imageList
    
    
    def getSupportedImageFormats(self):
        return self.supportedImages
    
    
    def getImageFiles(self):
        """Returns a list of all the existing images."""   
        extensions = self.supportedImages

        fullList = []
        
        for key in extensions:
            for eachCase in [key, key.upper()] :
                theList = self.getFilesByExtension(eachCase)
                for thing in theList:
                    fullList.append(thing + eachCase) 
        
        return fullList

    # ------------------------------------------------------------       

    # TO DO: convert to use os.path.join()
    def getDistributionTableFilename(self):
        return self.getProjectPath()+"/"+"setup/distribution"+".xml"

    # ------------------------------------------------------------       
    
    def getProjectInformation(self, theFile):
        info = {}

        class XmlReader(ContentHandler):                
            def __init__(XmlReader, scrwid=79, *args):
                ContentHandler.__init__(XmlReader, *args)
                
            def startElement(XmlReader, name, attrs):
                XmlReader.start_name = name
                if name != "project_setup":
                    info = {str(name): None}

            def endElement(XmlReader, name):
                pass
                
            def characters(XmlReader, chars):
                if XmlReader.start_name != "project_setup":
                    info[str(XmlReader.start_name)] = str(chars)
                            
                XmlReader.start_name=""  
                
        parse(theFile, XmlReader())
              
        del info['']
        return info

    # ------------------------------------------------------------        

    # TO DO: convert to use DOM methods
    def writeProjectSetupFile(self, information, filename):
        keylist = information.keys()

        output  = self.getXmlHead()
        output += '<project_setup>\n'

        for i in range(len(information)):            
            output += '<%s>' % str(keylist[i])
            output += information[keylist[i]]
            output += '</%s>\n' % str(keylist[i])

        output += '</project_setup>\n'

        writeFile(filename, output)
        
# ------------------------------------------------------------         
# ------------------------------------------------------------         
# ------------------------------------------------------------        
    
