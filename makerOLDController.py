#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import traceback
import shutil
import time
from ftplib import FTP
import ftplib 
import string
import urllib
import urlparse
import re
import wx
import threading


#import makerAbout
import makerCore
import makerEditor
import makerDistEditor
import makerDefaultRemoteFolderEditor
import makerProjectSetup
import makerFtpBrowser
import makerFtpTools
import ImageGUI
import makerImage
import makerProjectBrowser
import makerImportOrNew
import makerProjectConverter
import makerTemplateDialog
import makerCSSTools

from makerUtilities import readFile, writeFile
import makerUtilities 
from makerConstants import Constants

#-----------------

# decorator


def ensureCurrentFileSaved(func):
    def wrapped(*args, **kwds):
        self = args[0]
        if not self.isCurrentFileSaved(): self.saveCurrentFile()
        func(*args, **kwds)
    return wrapped



    


class aLotOfLameCode:    
    def __init__(self, GUI):
        #print 'initialising: makerController'
        self.initialized = False
        self.GUI = GUI
        #print GUI
        self.GUI.ClearEditor()

        # use this call to have error messages displayed in the Logtext field
        self.GUI.SetStderrToLogtext()
                
        self.setProjectDir()
        
        self.setLastUsedItem(None)                
        #print "checking dirs"
        self.checkDirs()
        
        self.loadProject()
        
        currentProj = self.getCurrentProject()
        
        if not currentProj:
            #print "oh oh...no project to load, exiting..."
            sys.exit(0)
  
        theProject = os.path.join(self.getProjectDir(), currentProj)
        self.core = makerCore.CmsCore(os.path.abspath(theProject), self)
        
#              
#        self.clearPassAttempts() # the counter for login attempts
#        
#        
        self.initAutoComplete()
#        
#        

        
        self.initialized = True
        
    # ------------------------------------------------------------  
 
    def runThreaded(self, function, arg):
        class MyThread(threading.Thread):
            def run ( self ):
                
                function(arg)
                
        MyThread().start()
        
         
    # ------------------------------------------------------------        
    
    def enableSetupRelated(self, enable):
        """
        False =  off
        True  =  on
        """
        self.GUI.MenuItemSyncImages.Enable(enable)
        self.GUI.MenuItemFullUpload.Enable(enable)
        self.GUI.MenuItemBrowseFtp.Enable(enable)
    
    
    def enablePrintMenu(self, enable):
        """
        False =  off
        True  =  on
        
        """
        return
           
        try:
            if self.core.currentFile.getPrintable():
                self.GUI.MenuItemPrint.Enable(enable)
            else:
                self.GUI.Error("not printable")
        except:
            self.GUI.MenuItemPrint.Enable(False)
            #print "no current file"
        
    
    
    def enableEditMenus(self, enable):
        """
        False =  off
        True  =  on
        
        """
        for item in self.GUI.insert.GetMenuItems():
            item.Enable(enable)
            
        
        self.GUI.MenuItemCut.Enable(enable)
        self.GUI.MenuItemCopy.Enable(enable)
        self.GUI.MenuItemPaste.Enable(enable)
        
        self.GUI.MenuItemCutSubmenu.Enable(enable)
        self.GUI.MenuItemCopySubmenu.Enable(enable)
        self.GUI.MenuItemPasteSubmenu.Enable(enable)
        
        self.GUI.underline.Enable(enable)
        self.GUI.oblique.Enable(enable)
        self.GUI.bold.Enable(enable)
        self.GUI.line_through.Enable(enable)
        
        
        self.GUI.MenuItemFind.Enable(enable)
        self.GUI.MenuItemFindNext.Enable(enable)
        
            
    # ------------------------------------------------------------        
    
    def enableEditor(self, enable):
        self.GUI.styledTextCtrl1.Enable(enable)
    
    def enableFileOps(self, enable):
        """
        Turning file related buttons and menus on or off
        
        False =  off
        True  =  on
        """
        
        # Menu Items
        self.GUI.MenuItemSaveFile.Enable(enable)
        self.GUI.MenuItemDeleteFile.Enable(enable)
        self.GUI.MenuItemPreview.Enable(enable)
        self.GUI.MenuItemUploadFile.Enable(enable)
        
                
        if enable:
            self.GUI.saveButton.Enable()   
            self.GUI.preview.Enable()
            self.GUI.publishButton.Enable()
        else:
            self.GUI.saveButton.Disable()   
            self.GUI.preview.Disable()
            self.GUI.publishButton.Disable()
        
        
            
    # ------------------------------------------------------------        
     
    def checkDirs(self):
        if not os.path.isdir(self.getProjectDir()):
            self.createProjectDir()
            
    # ------------------------------------------------------------

#    def loadProject(self):
#        """Returns a project or None."""
#
#        # -------------------------------------
#        # Maker projects exist already
#        # -------------------------------------
#        if self.thereExistProjects():
#            self.loadExistingProject()
#            return
#
#        # -------------------------------------
#        # No maker projects exist already
#        # -------------------------------------
#        #print "No known projects: create or import one?"
#        actionToTake = self.actionCreateOrImportProjects()
#
#        while not actionToTake:
#            m  = "Really quit?\n"
#            m += "Project create or import is necessary to use the maker."
#            answer = self.GUI.Ask(m)
#            if answer != "Cancel": 
#                self.setCurrentProject(None)
#                return
#            actionToTake = self.actionCreateOrImportProjects()
#
#        actions = {'new'    : self.createNewProjectProcedure,
#                   'import' : self.importOldProjectProcedure}
#        actions[actionToTake]()

    # ------------------------------------------------------------
        
    def thereExistProjects(self):
        return len(self.getProjects()) > 0

    # ------------------------------------------------------------

    def loadExistingProject(self):
        proj = self.getLastProject()
        if not proj:
            proj = self.actionShowProjectBrowser(self.getProjects())

        self.setCurrentProject(proj)

    # ------------------------------------------------------------

    def createNewProjectProcedure(self):
        self.setCurrentProject(self.actionNewProject())
        
    # ------------------------------------------------------------
        
    def importOldProjectProcedure(self):
        self.setCurrentProject(self.actionImportProject())

    # ------------------------------------------------------------
    
#    def checkForProjectDir(self):
#        """
#        Checks if the Constants.PROJECTBASE folder 
#        exists in the user home folder.
#        """
#        return os.path.isdir(self.getProjectDir())

    # ------------------------------------------------------------
#   
#    def writeProjectHistory(self):
#        """
#        Writes the last project to a file of name defined 
#        in Constants.LASTPROJECT.
#        """
#        fPath = os.path.join(self.getProjectDir(), Constants.LASTPROJECT)
#        writeFile(fPath, self.getCurrentProject())
#        
#    # ------------------------------------------------------------
   
#    def getLastProject(self):
#        """
#        Reads the lastProject.txt file and returns its contents (the last 
#        project) or an empty string if no file, no contents or if the
#        last known project is not in the list of known projects as returned by
#        getProjects().
#        """
#        
#        fPath = os.path.join(self.getProjectDir(), Constants.LASTPROJECT)
#        if os.path.isfile(fPath):
#            last = readFile(fPath, asLines=True, lineRange=[0])
#            last = last.strip()
#        else:
#            return ''
#
#        if not last or not last in self.getProjects(): return ''
#
#        return last
#    
#    # ------------------------------------------------------------
#
#
#    
#        
#    def actionCreateOrImportProjects(self):
#        """Choice dialog: import or create new project."""
#
#        dlg = makerImportOrNew.ImportOrNew(self.GUI)
#        choice = None
#        try:
#            dlg.ShowModal()
#            choice = dlg.choice
#        finally:
#            dlg.Destroy() 
#            return choice
#
#    
#    
#    
    
#    
#    
#    @ensureCurrentFileSaved
#    def actionImportFile(self):
##        """Imports a MakerFile (handles all files, even binary)."""
#
#        filesToImport = self.fileDialog()
#        
#        if not filesToImport: return
#      
#        # just making sure that no images are imported this way
#        
#        for possibleImage in filesToImport:
#            
#            fileType = os.path.splitext(os.path.basename(possibleImage))[-1]
#            
#            if self.core.supportedImages.count(fileType.lower()) != 0:
#                self.view.ErrorMessage("Please do NOT Import Images this way!\n" + 
#                               "Use 'Import Image' instead!\n\n" + 
#                               "Import canceled!")
#                return
#        
#        # This might seem a little odd. Here is why it is dome this way.
#        # In the file selector we need to enable all files because there is no
#        # telling what the user might want to import.
#        #
#        # Images are not displayed in the treeView and are handled different from
#        # all other files so we have to exclude them from being imported like 
#        # any other file 
#        
#      
#        # - - - 
#        
#        for file in filesToImport:
#        
#            try:
#                
#                fileName     = os.path.basename(file)
#                filePath     = os.path.dirname(file)
#                fileNameNoExt, fileType = os.path.splitext(fileName)
#                
#            except Exception, e:
#                print str(e)
#                return
#    
#            # just a flag for later
#            isBinary = False
#            flag   = 'r'        
#            if self.isFileBinary(file):
#                isBinary = True
#                # we are only making this distinction on Xp or Vista
#                # since the Mac and Linux handle binary data well 
#                if os.name == 'nt': flag = 'rb'
#                    
#            content = readFile(file, binary=isBinary)
#            
#            theFile = os.path.split(file)[-1]
#            
#            # only display the rename message if the file already exists
#            if os.path.isfile(os.path.join(self.core.getPathParts(),theFile)):
#            
#                m = "A file named '%s' already exists! " % theFile
#                m += "Enter another name..."  
#                
#                name = self.GUI.InputWithValue(m, fileNameNoExt)
#                
#                # just in case someone hits OK 
#                if name == fileNameNoExt:
#                    name = None
#            else:
#                name = os.path.splitext(theFile)[0]
#                    
#            # ----
#            if name is None or not name.strip():
#                self.GUI.Message("No File imported")
#                return
#    
#            mode = 'lines'
#            if isBinary: mode = 'binary'
#            result = self.core.addMakerFile(name, fileType, content, mode)
#            self.core.addToFtpQueue(name + fileType)
#            print result
#            
#        
#        # end of for loop
#            
#        # if we import a file that belongs to a non existing group
#        # we have to set the groups first
#        self.core.setItemGroups(self.core.mergeSupportedAndUnsupportedFileGroups())
#                
#        self.core.loadGroupItems()     # update data in core
#        self.actionFillTree()
#        
#        
#                
#        # show the last imported file
#        self.autoSelect(self.getTreeItemForFilename(name + fileType))
#        
#        # when a binary file is imported we have to enable the 
#        # Publish button since this button is toggled by edits 
#        # but binary files cannot be edited
#        
#        if mode == "binary":
#            self.GUI.EnablePublishButton()
#    
#    
#    
#    
#    
#    
#    
    
    
    # ------------------------------------------------------------    
    
    
    # ------------------------------------------------------------
        
    def actionImportProject(self):
        """
        Imports a project and converts it to actual settings, 
        doing several checks at the same time. Returns a boolean 
        indicating outcome.
        """

        project = self.GUI.SelectProject()
        if not project: return None
        
        projectFolder = self.getProjectDir()

        # TO DO: Brinick is confused. Why do we bother calling the converter? 
        # It seems the only thing that marks a folder as a makerProject 
        # is the presence of a sub directory called 'parts'. 
        # And commenting out the line below does not seem to prevent me from
        # successfully importing a project. So what's its purpose?

        # Gerald: We used to have a dist table for each language among other 
        # odd things the newer project version avoids these
        
        converter = makerProjectConverter.Converter(project)

        if not os.path.isdir(os.path.join(project, 'parts')):
            self.GUI.Error('%s is not a maker project !' % project)
            return None

        print '%s is a maker project' % project
        print 'importing: %s' % project
        print "Project: %s" % project
        print "ProjectFolder: %s" % projectFolder

        proj = os.path.basename(project)

        try:
            self.GUI.ShowProgress(4," ")
            self.GUI.PulseProgress("importing: " + proj)
            
            makerUtilities.copyFileTree(project, os.path.join(projectFolder, proj), 
                                        self.GUI.PulseProgress, ("importing: " + proj))
            
              
            m = "The project ' %s ' has been imported..." % proj
            
            self.GUI.KillProgress()
            self.GUI.Message(m)
            return proj
        except Exception, e:
            self.GUI.KillProgress()
            m  = "Unable to import project: %s\n" % project
            m += "Detailed Information:\n\n" + str(e)
            
            self.GUI.Error(m)
            return None
     
    
        
    # ------------------------------------------------------------
       
    def getSystemPath(self):
        """ get system path """
        return os.path.join(os.path.dirname(sys.argv[0]), "system/")


        
    # ------------------------------------------------------------
    
    def addNewProject(self):
        """Wraps around actionNewProject."""

        if not self.isCurrentFileSaved(): self.saveCurrentFile()
        projName = self.actionNewProject()
        if projName != None:
        
            self.switchToProject(projName)
            # since we are loading a new project we have to build some files
            self.actionBuildAll()
            

   # ------------------------------------------------------------
    
    def actionNewProject(self):
        template = self.showTemplateDialog()        
        if not template: return None

        projName = self.GUI.Input("Enter a project name...")

        if projName == 'Null': return None

        print "creating folders and files for ", projName
        
        src = os.path.join(self.getSystemPath(), 'templates', template)
        tgt = os.path.join(self.getProjectDir(), projName)
                
        if os.path.isdir(tgt):
            m  = "A project with the name '" + projName + "' already exists ! "
            m += "Try again... "
            self.GUI.Error(m)
            self.addNewProject()
        else:    
        
            shutil.copytree(src, tgt)
            return projName
    
    # TO DO: Brinick removes this call. What's the point of it? For the user
    # it's very annoying to have to choose the project we just created.
    # The maker should (and now does) just open it up in the GUI.

    # self.ActionSwitchProject()

#    
#    @ensureCurrentFileSaved
#    def actionSwitchLanguage(self, theLanguage):
#        self.selectNothing()
#        self.core.switchLanguage(theLanguage)
#        
#        self.actionFillTree()
            
    # ------------------------------------------------------------       
    
    def actionShowPopupTool(self, event):
        """event is the GUI event that is sent back to the GUI."""              
        self.GUI.ShowPopupTool(self.core.currentFile.getType(), event)
        print event
          
    # ------------------------------------------------------------             

    def actionInsertImage(self):
        """Insert html tags in GUI Editor."""
        
        image = self.GUI.ImageDialogWithDir(self.core.getPathParts())
        if not image: return

        # only use the image filename - not the full path
        image = os.path.split(image)
        
        if self.core.getPathParts().endswith("/"):
            origPath = self.core.getPathParts()
        else:
            origPath = self.core.getPathParts() + "/"
        
        
        if image[0] + "/" != origPath:
            m  = "Please do not change the directory in the image dialog! \n"
            m += "If you do not find the image you need, you will have to\n"
            m += " import it first."
            self.GUI.Error(m)
            return
        
        image = image[1]
                    
        theTag = '<img src="'+image+'" align="left" alt="'+image+'"/>'
        self.GUI.InsertHtmlTags([theTag])
    
    # ------------------------------------------------------------ 

    @checkIfToolIsRight('.content')
    def actionPopupTool(self, event, toolType):
        toolTypes = {
            'a'    : ['<a href="'+'">','</a>'],
            'p'    : ["<p>", "</p>"],
            'br'   : ['<br />'],
            'hr'   : ['<hr />'],
            'h1'   : ["<h1>","</h1>"],
            'h2'   : ["<h2>","</h2>"],
            'h3'   : ["<h3>","</h3>"],
            'h4'   : ["<h4>","</h4>"],
            'h5'   : ["<h5>","</h5>"],
            'h6'   : ["<h6>","</h6>"],
            'span' : ['<span class="">','</span>'],
            'div'  : ['<div id="">','</div>'],
            }
        
        self.GUI.InsertHtmlTags(toolTypes[toolType])

    # ------------------------------------------------------------ 
#
#    @checkIfToolIsRight('.content')
##    def actionFormatText(self, event, format):
##        """Inset html tags in GUI Editor."""
##        formats = {
##            'bold'    : ['<span style="font-weight:bold;">', '</span>'],
##            'oblique' : ['<span style="font-style:oblique;">', '</span>']
##            }
##        
##        defaultTags = ['<span style="text-decoration:'+format+'">','</span>']
##        tags = formats.get(format, defaultTags)
##        self.GUI.InsertHtmlTags(tags)            
##        
#    # ------------------------------------------------------------ 
#        
#    @checkIfToolIsRight('.css')
#    def actionCssToolStyle(self, event):
#        """Inset html tags in GUI Editor."""
#        self.actionInsertText("_replace_me_ {color:#000;background-color:#ffff;border:1px solid #333;}")    
#            
#    # ------------------------------------------------------------ 
##
##    @checkIfToolIsRight('.css')         
##    def actionCssToolColor(self, event):
##        """Inset html tags in GUI Editor."""
##
##        self.GUI.ColorDialog()
##        color = self.GUI.color_data 
##        self.actionInsertText("rgb" + str(color))                       

    # ------------------------------------------------------------ 

#    def imageActionCalcX(self,y):
#        ratio = self.makerImage.getRatio()
#        
#        #ratio = (ratio, bigger side of image)
#        
#        if ratio[1]== 'x':
#        
#            print ratio[0], y
#            y = float(y) * ratio[0]
#            
#            y = int(y) 
#        else:
#            print ratio[0], y
#            y = float(y) / ratio[0]
#            
#            y = int(y) 
#        
#        self.ImageGUI.set_x(y)
#        
#    # ------------------------------------------------------------     
#    
#    def imageActionCalcY(self,x):
#        ratio = self.makerImage.getRatio()
#        
#        if ratio[1]=="x":
#        
#            print ratio[0], x
#            x = float(x) / ratio[0]
#            
#            x = int(x) 
#        else:
#            print ratio[0], x
#            x = float(x) * ratio[0]
#            
#            x = int(x) 
#        
#        self.ImageGUI.set_y(x)
    
    # ------------------------------------------------------------ 
    
   
    
 
    # ------------------------------------------------------------     
             
#    def actionDeleteImage(self):
#        m = "Do not change the directory in the following dialog!"
#        self.GUI.Message(m)
#
#        file = self.GUI.ImageDialogWithDir(self.core.getPathParts())
#        if not file: return
#        
#        fileparts = os.path.split(file)
#        
#        if self.checkIfProjectIsSetUp():
#            if not self.actionLoadPassword():
#                self.GUI.Message("cancelled...")
#                return
#
#            try:                
#                self.core.serverLogin()
#                gfxFolder = self.core.getRemoteGfxFolder()
#                result = self.core.deleteRemoteFile(gfxFolder, fileparts[1])
#                if result:
#                    self.core.serverLogout()
#                    os.remove(file)
#                    self.GUI.Message("image deleted")
#                else:
#                    m  = 'Unable to delete remote file!\n'
#                    m += 'Image not on server?'
#                    self.GUI.Error(m)
#            except:
#                self.GUI.Error("cannot delete image...")
#        
#        else:
#            os.remove(file)
#            self.GUI.Message("image deleted")
#            
    # ------------------------------------------------------------         
#    
#    def actionStoreFileInParts(self, fileName, newName):
#        """Stores the file in the parts directory."""
#        shutil.copyfile(fileName, self.core.getPathParts() + newName)
#            
    # ------------------------------------------------------------     
        
  
#    
#    def actionEditDefaultRemoteFolders(self):
#                        
#        data = self.core.readDefaultFoldersFile()
#        
#        dlg = makerDefaultRemoteFolderEditor.DefRemFolderEditor(self.GUI, data)
#        
#                
#        dlg.ShowModal()
#        #dlg.saved = True File was saved
#        #dlg.saved = False File was not saved
#
#        if dlg.saved:
#            
#            self.core.writeDefaultFoldersFile(dlg.data)
#            
#            dlg.Destroy()
#        else:
#            dlg.Destroy()
#    
#        
    
   
    
    def fullUpload(self):
        """
        is uploading all files and images to the server after the 
        project has been set up for the first time
        
        """
#        if not self.checkIfProjectIsSetUp():
#            self.GUI.Message("First you need to setup your project.")
#            return
#        
#        self.isCurrentFileSaved()
#        
#        self.actionBuildAll()
#        
#        
#        
#        itemGroups = self.core.getItemGroups()
#        try:
#            itemGroups.remove(".dynamic")
#            itemGroups.remove(".other files")
#        except Exception, e:
#            print str(e)
#           
#        theList = {}
#        
#        for item in itemGroups:
#            theList[item] =self.core.getFilesByExtension(item)
#        
#        if not self.ftpLogin():
#            return
#        
#        runs = 0
#        for i in theList.keys():
#            if runs != 0:
#                try:
#                    self.GUI.KillProgress()
#                except:
#                    print "nothing to kill"
#
#            runs += 1
#            
#            pagelist = theList[i]
#            
#                        
#            if not pagelist:
#                pass
#                # skip if there are no files in group
#            else:
#                self.GUI.ShowProgress(len(pagelist),"uploading all files...")
#                count = 0
#                for theFile in pagelist:
#                    self.core.loadFile(theFile,i)
#                    
#                    self.GUI.UpdateProgressMessage(count,str(theFile))
#                    count += 1
#                    target_list = self.core.currentFile.getFTPInformation()
#                
#                    if target_list==[]:
#                        sys.stderr.write("no targets found for "+theFile+i+" !")
#                        # just keep going
#                        
#                        #self.selectNothing()
#                        #return
#                    else:
#                       # remote_dir, target, ftp_mode
#                        self.core.backupLocalFile()                 
#                        self.actionUpdateImageBase()
#                        # for content files the images are updated in updateFileBase
#                        
#                    if self.core.currentFile.getType()==".content":
#                        self.core.currentFile.makeWebSite()
#                        self.core.currentFile.updateFileBase()
#                    else:
#                        print "seems like ", theFile, "its not an html (.content) File"
#                    
#                    
#                                            
#                        
#                    for target in target_list: # do this for all targets
#                            
#                        dir=target[0]
#                            
#                        if not self.core.checkIfRemoteDirIsDir(dir):
#                            if self.GUI.Ask("the remote directory: "+dir+" does not exist! \nDo you want to create it?" )=="Ok":
#                                result = self.core.makeRemoteDir(dir)
#                                print "remote dir created:",result
#                            else:
#                                self.GUI.Error("upload cancelled")
#                                self.GUI.KillProgress()
#                                self.core.restoreLocalFile()
#                                if self.getLastUsedItem() != None:
#                                    self.autoSelect(self.getLastUsedItem())
#                                else:
#                                    self.selectNothing()       
#                                return 
#                        else:
#                            print "the remote dir ",dir," does exist..."
#                            
#                     
#                        self.GUI.UpdateProgressMessage(count,"storing: " + 
#                                                           self.core.currentFile.getRealName() )
#                        
#                        self.core.uploadFile(self.core.getPathParts() + 
#                                                 self.core.currentFile.getRealName(),
#                                                 str(target[0]),
#                                                 str(target[1]),
#                                                 str(target[2]))
#                        
#                        self.core.restoreLocalFile()        
#                        
#                                #
#                                # if it is a content file upload the rss feed too
#                                #
#                                
#                        if self.core.currentFile.getType()==".content":
#                            try:
#                                self.GUI.UpdateProgressMessage(count,"storing RSS")
#                                self.core.uploadFile(self.core.getPathParts()+self.core.currentFile.getRSSName(),str(target[0]),self.core.currentFile.getRSSName(),str(target[2]))
#                                self.GUI.UpdateProgressMessage(count,"done...")
#                            except:
#                                print "First upload failed for file: ", self.core.currentFile.getRealName()
#                            
#        
#        #  here we upload the gfx
#        
#        gfx = self.core.getImageFiles()
#        
#        self.GUI.ShowProgress(len(gfx),"uploading gfx")
#        count = 0
#        for image in gfx:
#            self.GUI.UpdateProgressMessage(count,image)
#            count += 1
#            fileparts = os.path.split(image)
#            
#            self.actionUploadFile(self.core.getRemoteGfxFolder(),os.path.join(self.core.getPathParts(),image),fileparts[1],"binary")
#
#        self.GUI.KillProgress()
#        
#        if self.getLastUsedItem() != None:
#            self.autoSelect(self.getLastUsedItem())
#        else:
#            self.selectNothing()            
#        try:            
#            self.ftpLogout()
#                        
#            #self.selectNothing()
#            self.GUI.Message("All items have been sent to the server !")
#            self.resetAllTreeIcons()
#            
#        except Exception, e:
#            print str(e) 

           
#    def actionTmpSetupFtp(self, host, user, root):
#        """
#        Temporarily set the ftp server with different settings.        
#        Used to test settings in the makerProjectSetup dialog.
#        """        
#        self.core.setFtpHost(host)
#        self.core.setFtpUser(user)
#        self.core.setFtpRoot(root)        
#        # Here you need to check the ftp settings...
#
#    # ------------------------------------------------------------     
#        
#    def actionResetFtp(self):
#        """
#        Re-sets the FTP settings in the core by executing
#        the projectSetup() method. Settings will be read 
#        from file in this case.
#        """
#        self.core.projectSetup()
#        
    # ------------------------------------------------------------         

#    def actionTestFtp(self, host, user, root, passw):
#        """
#        Returns True if FTP settings are good, else an error string 
#        about what is wrong. If the password is good it is stored
#        and used for upcoming connections.
#        """
#        
#        
#        self.GUI.look_busy()
#        self.GUI.ShowProgress(3,"testing Hostname: " + host)
#        testFtp = FTP()
#        testFtp.set_debuglevel(2)
#        try:
#            print "action testFTP: testing hostname..."
#            print "-----------------------------------"
#            testFtp.connect(host)
#            print testFtp.getwelcome()
#        except:
#            self.GUI.KillProgress()
#            testFtp.close()
#            self.GUI.relax()
#            
#            return "bad hostname"
#            
#
#        try:
#            self.GUI.UpdateProgressMessage(2,"testing Username: " + user)
#            print "action testFTP: testing username..."
#            print "-----------------------------------"
#            print testFtp.sendcmd("USER " +user )
#        except ftplib.all_errors, e:
#            testFtp.close()
#            self.GUI.KillProgress()
#            self.GUI.relax()
#            return str("Error No:\n" +  e[0] + "\nbad username")
#        
#        try:
#            self.GUI.UpdateProgressMessage(3,"testing Password" )
#            print "action testFTP: testing password..."
#            print "-----------------------------------"
#            testFtp.sendcmd("PASS " +passw )
#                     
#        except ftplib.all_errors,e:
#            
#            self.GUI.KillProgress()
#            testFtp.close()
#            self.core.setRemotePassword(None)
#            # the fact that the server is accepting the username does not
#            # mean that it is valid
#            self.GUI.relax()
#            return str("Error No:\n" +  e[0] + "\nbad username or password")
#            
#        print "All ftp settings are good..."
#        self.GUI.KillProgress()
#        testFtp.close()
#        self.GUI.relax()
#        return True
#        
    # ------------------------------------------------------------         
#    
#    #@enforcePassword
#    def actionBrowseServer(self):
#        """Opens the ftpBrowser and returns the path that was selected."""
#        
#        # this is a quick fix since at this time rev 238 enforcePassword is not 
#        # working with functions that return a value
#        
#        if not self.actionLoadPassword():
#            return
#
#        # ---------- fix end
#        
#        self.ftpBrowser = makerFtpBrowser.FTPBrowser(self)
#        # if we cannot connect we go one step back
#        if not self.ftpBrowserAction_connect_():
#            return None
#        self.ftpBrowserAction_ls_()
#        # return the pathname displayed when the ftpBrowser was shut
#        pathName = self.ftpBrowserShow()
#        print "will return ", pathName
#        return pathName 
#  
#    # ------------------------------------------------------------         
#    
#    def ftpBrowserAction_ls_(self):
#        """Fills the ftpbrowser's listbox."""
#        self.GUI.look_busy()
#        self.list = self.ftp_tools.ls()
#        
#        if self.ftp_tools.pwd()==self.start:
#            try:
#                self.list.remove('..')
#            except:
#                print 'seems like really root'
#        
#        self.ftpBrowser.fillList(self.list)
#        self.GUI.relax()
#    # ------------------------------------------------------------     
#    
#    def ftpBrowserAction_Ok_(self):
#    
#        if self.ftpBrowser.listBox.GetSelection() == -1:
#            # 'no selection - taking current'
#            string = self.ftp_tools.pwd()
#        else:
#            # 'there is a selection...'
#            if self.ftp_tools.isdir(self.ftpBrowser.list[self.ftpBrowser.listBox.GetSelection()]):
#
#                # This is an odd piece of code. os.path.join works 
#                # well on linux and the mac on XP it returns backslashes 
#                # thats why we use the very straigtforward
#                # code below
#
#                # TO DO: use join, but then do a replace of os.separator to
#                # replace XP backslashes
#
#               #string = os.path.join(self.ftp_tools.pwd(), self.ftpBrowser.list[self.ftpBrowser.listBox.GetSelection()])
#               string = self.ftp_tools.pwd() + "/" + self.ftpBrowser.list[self.ftpBrowser.listBox.GetSelection()]
#                
#            else:
#                self.GUI.Error('This is not a directory')
#                #self.relax()    
#                return
#        
#            
#        self.ftpBrowser.pathname = string     
#        self.ftpBrowser.saved = True
#        self.ftpBrowser.Close()
#        
#    # ------------------------------------------------------------     
#    
#    def ftpBrowserAction_delete_(self):
#
#        if self.ftpBrowser.listBox.GetSelection() == -1:
#            self.GUI.Error('Please select an item')
#            return
#            
#        theDir = self.list[self.ftpBrowser.listBox.GetSelection()]
#        answer = self.GUI.Ask('Do you really want to delete %s?' % theDir)
#        if answer == 'Ok':
#            self.ftp_tools.rmd(dir)
#            print 'deleted'
#        else:
#            print "cancelled"
#        
#        self.ftpBrowserAction_ls_()
#
#    # ------------------------------------------------------------     
#        
#    def ftpBrowserAction_newFolder_(self):
#        result = self.GUI.Input('Please enter a name for the new folder:')
#        if result=="Null":
#            return
#
#        try:
#            self.ftp_tools.mkd(result)
#            self.ftpBrowserAction_ls_()
#        except:
#            self.GUI.Error("unable to create new folder")
#
#    # ------------------------------------------------------------     
#
#    def ftpBrowserAction_select_(self):
#        item = self.ftpBrowser.listBox.GetSelection()
#        
#        target = self.list[item]
#        
#        try:
#            self.ftp_tools.cd(target)
#        except:
#            print "this is not a dir"
#            return
#            
#        items = self.ftpBrowser.listBox.GetCount()
#        print items
#        for i in range(items):
#            self.ftpBrowser.listBox.Delete(0)
#        
#        self.ftpBrowserAction_ls_()
#
#    # ------------------------------------------------------------     
#        
#    def ftpBrowserAction_up_(self):
#        if self.ftp_tools.pwd() == self.start:
#            self.GUI.Error('this is the project\'s "root" - you cannot go up')
#            return
#        
#        try:
#            self.ftp_tools.cd('..')
#        except:
#            self.GUI.Error('I cannot go up')
#        
#        self.ftpBrowserAction_ls_()
#    
#    # ------------------------------------------------------------     
#    
#    def ftpBrowserAction_cancel_(self):
#        self.ftpBrowser.saved = False
#        self.ftp_tools.logout()
#        self.ftpBrowser.Close()  
#
#    # ------------------------------------------------------------     
#
#    def ftpBrowserAction_connect_(self):
#        """
#        before calling this method you have to use
#        actionLoadPassword
#        
#        returns True or False
#        """
#        try:
#            print '--- FTP info ---'
#            print "connecting to server"
#            print 'Host: %s' % self.core.ftpHost
#            print 'Root: %s' % self.core.ftpRoot
#            print 'User: %s' % self.core.ftpUser
#            print 'Pass: %s' % self.core.getRemotePassword()
#            self.ftp_tools = makerFtpTools.Browser(self.core.ftpHost,
#                                                   self.core.ftpRoot,
#                                                   self.core.ftpUser,
#                                                   self.core.getRemotePassword())    
#        except:
#            self.GUI.Error('unable to connect ! Check your settings...')
#            print "DEBUG: unable to connect",self.core.ftpHost,self.core.ftpRoot,self.core.ftpUser,self.core.getRemotePassword()
#            self.core.setRemotePassword(None)
#            self.ftpBrowser.Destroy()    
#            return False
#        
#        try:
#            self.start = self.ftp_tools.pwd()
#        except:
#            self.GUI.Message("unable to read root")
#        
#        # check for root
#        if self.ftp_tools.pwd() == self.start:
#            try:
#                self.list.remove('..')
#            except:
#                print 'seems to be really root !'
#        return True
#        
#    # ------------------------------------------------------------  
#    
#    def ftpBrowserShow(self):
#        # this works
#        try:
#            self.ftpBrowser.ShowModal()
#        finally:
#            
#            if self.ftpBrowser.saved:
#                path = self.ftpBrowser.pathname
#                self.ftpBrowser.Destroy()
#                return path
#            else:
#                self.ftpBrowser.Destroy()
#                return None
#    
# 
#   
#    # ------------------------------------------------------------     
#
#    def actionDeleteCurrentFile(self):
#        """Deletes the current file."""
#        
#        if not self.isCurrentFileSaved(): self.saveCurrentFile()
#
#        fPath = self.core.getCurrentFileName()
#        m = "Do you really want to delete the file: %s" % fPath
#        Answer = self.GUI.Ask(m)
#
#        if Answer =="Ok":            
#            self.GUI.ShowProgress(5,"deleting File")
#            if self.checkIfProjectIsSetUp():
#
#                # the remote file needs to be removed first
#                try:
#                    print "removing remote pages..."
#                       
#                    if not self.actionLoadPassword():
#                        self.GUI.KillProgress()
#                        self.GUI.Message("cancelled...\n\nYou need to enter the password to delete the file!")
#                        return
#                    
#                    info = self.core.currentFile.getFTPInformation()
#                #self.GUI.Message(str(info))
#                
#                    
#                    self.GUI.UpdateProgressMessage(1,"login")
#                    self.core.serverLogin()
#                            
#                    self.GUI.UpdateProgressMessage(2,"deleting")
#                    for i in info: # delete File from all locations
#                        result = self.core.deleteRemoteFile(i[0],i[1])
#                        if not result:
#                            self.GUI.Error("unable to delete remote File:"+str(i))
#                        else:
#                            print "deleted...",i
#                            self.GUI.UpdateProgressMessage(3,"logout")
#                            self.core.serverLogout()
#                except:
#                     print "unable to delete remote file"
#                
#            fName = self.core.currentFile.getFileName()
#            if self.core.isFileInQueue(fName):
#                self.core.deleteFromFtpQueue(fName)
#            self.GUI.UpdateProgressMessage(4,"deleting local files")
#            result = self.core.deleteMakerFile()
#            print result
#            if result:
#                self.GUI.KillProgress()
#                self.GUI.Message("File has been deleted...")
#                                
#                self.selectNothing()
#                self.core.loadGroupItems()
#                self.actionFillTree()
#            else:
#                self.GUI.Error("unable to delete File")
#            
    # ------------------------------------------------------------
#            
#    def updateStatusInformation(self):
#              
#        self.GUI.statusBar1.SetStatusText(number=1, text='Project: ' + self.core.project)
#        self.GUI.statusBar1.SetStatusText(number=2, text='Language: '+ self.core.language)
#        self.GUI.statusBar1.SetStatusText(number=3, text='File: ' + self.core.getCurrentFileName())
#        self.markQueuedFilesAsModified()
                
    # ------------------------------------------------------------   
   
    def getSelectedItem(self):
        self.GUI.tree.GetSelection()

    # ------------------------------------------------------------
   
    def selectNothing(self):
        """
        is unbinding the text change event in the editor
        is clearing the editor
        is setting core.currentFile to None
        is refeshing the status bar
        """
        self.GUI.UnbindModifiedToEditor()
        self.GUI.styledTextCtrl1.ClearAll() # Clear the editor
        #self.GUI.styledTextCtrl1.SetText("nothing") 
        
        self.core.setCurrentFile(None)
        
        
    # ------------------------------------------------------------

    def setOriginalName(self, theName):
        self.originalItemName = theName
        
    def getOriginalItemName(self):
        return self.originalItemName
        
    # ------------------------------------------------------------
        
    def actionEditTreeItemLabel(self):
        """
        event has to be passed to this method
        edit item labels in the tree
        
        for renaming items
        
        if the file is a .content or .dynamic file
        the makerGUI method BindVerifyer() is called
        
        """
        # if there is no current selection
        
        if self.core.currentFile :
            item = self.GUI.tree.GetSelection()
        
            if item:
                self.GUI.tree.EditLabel(item)

    # ------------------------------------------------------------
            
    def actionOnEditTreeItem(self, event):
        """
        verify if item can be edited
        
        the root item and the group names cannot be changed
        """
        print "Action On Edit", event
        
        
        self.setOriginalName(event.GetLabel())
        
        
        item = event.GetItem()
        if item == self.GUI.tree.GetRootItem():
            self.GUI.Error("You cannot rename this one...")
            
            event.Veto()
            
        else:
            parent = self.GUI.tree.GetItemParent(item)
            if self.GUI.tree.GetItemText(parent)=="items:":
                self.GUI.Error("You cannot rename this one...")
                
                event.Veto()
        
    # ------------------------------------------------------------

    def actionTreeEditFinish(self, event):
        """
        Called after renaming of a tree label.
        the currentFile.rename(newName) method is called
        
        and the Verifyer is Unbound in the GUI
        """
        # TO DO: renaming w/o correct ending _sometimes_ results in the 
        # same error message popping up twice! Why?!
        newName = event.GetLabel()
        if self.core.currentFile.getType() in [".content", ".dynamic"]:
            if not newName.endswith("_"+self.core.getLanguage()):
                m = 'This file must end with _%s' % self.core.getLanguage()
                self.GUI.Error(m)
                event.Veto()
                return

        if newName == self.getOriginalItemName():
            event.Veto()
            
            
        else:
            if not self.core.currentFile.rename(newName):
                theName = newName + self.core.currentFile.getType()
                m = "%s already exists!" % theName
                self.GUI.Error(m)
                event.Veto()
            else:
                pass
                

    
    
#    def actionEditDistributionTable(self):
#        
#        def saveOldData(oldData):
#            dlg.oldDistData = oldData 
#        
#        def readOldData():
#            return dlg.oldDistData
#        
#        
#        data = self.core.readDistributionTable()
#        
#        dlg = makerDistEditor.DistributionTableEditor(self.GUI, data)
#        saveOldData(data)
#        
#      
#        
#        def getListOfRemoteFolders():
#            listOfFolders = []
#            for dataSet in dlg.readData():
#                if listOfFolders.count(dataSet['remote_dir'])==0:
#                    listOfFolders.append(dataSet['remote_dir'])
#                
#            return listOfFolders
#            
#        def getConflictFilesForFolder(folder):
#            
#            conflictFiles = []
#            files = []
#            
#            for dataSet in dlg.readData():
#                if dataSet['remote_dir']==folder:
#                    files.append(dataSet['target'])
#                
#                if files.count(dataSet['target']) > 1:
#                    for otherDataSet in dlg.readData():
#                        
#                        if otherDataSet["target"] == dataSet['target']:
#                            
#                            if not conflictFiles.count(otherDataSet['ftp_source']) >= 1:
#                                conflictFiles.append(otherDataSet['ftp_source'])
#                        
#                    #conflictFiles.append(dataSet['ftp_source'])
#            
#            return conflictFiles
#        
#        def compareDataForCleanup(oldData, newData):
#            
#            toCleanup = []
#                     
#            for theOldDataSet in oldData:
#                fileToCompare = theOldDataSet["ftp_source"]
#                for newDataSet in newData:
#                    if newDataSet["ftp_source"]==fileToCompare:
#                        if newDataSet["remote_dir"]==theOldDataSet["remote_dir"]:
#                            print "remote_dir : the same"
#                        else:
#                            # folder name has changed
#                            toCleanup.append(((theOldDataSet["remote_dir"], 
#                                               theOldDataSet["target"]),
#                                                (newDataSet["remote_dir"],
#                                                  newDataSet["target"]))) 
#                        
#                        if newDataSet["target"]==theOldDataSet["target"]:
#                            print "target : the same"
#                        else:
#                            # target name has changed
#                            toCleanup.append(((theOldDataSet["remote_dir"], 
#                                               theOldDataSet["target"]),
#                                                (newDataSet["remote_dir"],
#                                                  newDataSet["target"]))) 
#                        
#                    
#                    
#            
#            
#            
#            cleanup(toCleanup)
#         
#        
#        def cleanup(toCleanup):
#            if not self.checkIfProjectIsSetUp():
#                print "No cleanup necessary - project not set up"
#                return
#            self.ftpLogin()
#            self.GUI.ShowProgress(len(toCleanup),"cleanup:")
#            runs = 1
#            for x in toCleanup:
#                target = x[1]
#                source = x[0]
#                if not source[0].endswith("/"):
#                    finalSourceFolder = source[0]+"/"
#                else:
#                    finalSourceFolder = source[0]
#                if not target[0].endswith("/"):
#                    finalTargetFolder = target[0]+"/"
#                else:
#                    finalTargetFolder = target[0]
#                
#                self.GUI.UpdateProgressMessage(runs, "cleanup:")
#                if self.core.checkIfRemoteDirIsDir(finalTargetFolder):
#                    self.core.renameRemoteFile(urlparse.urljoin(finalSourceFolder, source[1]),urlparse.urljoin(finalTargetFolder, target[1]))
#                else:
#                    self.core.makeRemoteDir(finalTargetFolder)
#                    self.core.renameRemoteFile(urlparse.urljoin(finalSourceFolder, source[1]),urlparse.urljoin(finalTargetFolder, target[1]))
#                runs += 1
#                
#            self.GUI.KillProgress()
#            self.ftpLogout()
#            
#            
#        
#        
#        
#        def getFilesWithConflicts():
#            conflicts = []
#            for f in getListOfRemoteFolders():
#                list = getConflictFilesForFolder(f)
#                if list != []:
#                    for item in list:
#                        conflicts.append(item)
#                    
#            return conflicts
#        
#        def markConflicts():
#            markedItems = []
#            for conflict in getFilesWithConflicts():
#                item = dlg.listCtrl.FindItem(0,conflict)
#                markedItems.append(item)
#                itemsColors[item] = dlg.listCtrl.GetItemBackgroundColour(item)
#                dlg.listCtrl.SetItemBackgroundColour(item,wx.RED)
#                
#            dlg.markedItems = markedItems
#            
#            # unbind until the next edit
#            dlg.Unbind(wx.EVT_UPDATE_UI)
#                
#        
#        def resetItemBackgrounds():
#            
#            for item in dlg.markedItems:
#                # due to some odd behavior in wx we have to set to white first
#                # before we can use another esp. custom color
#                dlg.listCtrl.SetItemBackgroundColour(item, wx.WHITE)
#                dlg.listCtrl.SetItemBackgroundColour(item, itemsColors[item])
#                # ----
#            dlg.markedItems = []
#   
#            
#        def checkAgain(evt):
#            
#            resetItemBackgrounds()    
#            markConflicts()
#        
#        def endEdit(evt):
#            # we bind it only after the edit has been made otherwise it will
#            # seriously slow down the app
#             
#            dlg.Bind(wx.EVT_UPDATE_UI, checkAgain)
#            # after markConflicts is finished this event is unbound
#           
#        def validateColumn(evt):
#            m = "You may only edit the 'Remote Dir' and the 'Remote File' column!"
#            if evt.GetColumn() == 0:
#                self.GUI.Message(m)
#                evt.Veto()
#            elif evt.GetColumn() == 2:
#                self.GUI.Message(m)
#                evt.Veto()
#                
#        itemsColors = {}
#        markConflicts()
#        
#                
#        dlg.Bind(wx.EVT_LIST_ITEM_SELECTED, checkAgain)
#        dlg.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,validateColumn)
#        dlg.Bind(wx.EVT_LIST_END_LABEL_EDIT, endEdit)
#        
#        dlg.ShowModal()
#        #dlg.saved = True File was saved
#        #dlg.saved = False File was not saved
#
#        if dlg.saved:
#            self.core.writeDistributionTable(dlg.data)
#            compareDataForCleanup(dlg.oldDistData,dlg.data)
#            # Task compare date sets for changes
#            
#            dlg.Destroy()
#        else:
#            dlg.Destroy()
#    
#        
#    
#    # ------------------------------------------------------------    
# 
#  
#    # ------------------------------------------------------------    
#   
#            
#    # ------------------------------------------------------------
#            
   
