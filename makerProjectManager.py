import os
import sys
import shutil
import re

from makerConstants import Constants
from makerUtilities import readFile, writeFile
from makerUtilities import writeDataToFile, readDataFromFile
from makerUtilities import copyFileTree
from makerUtilities import verifyLatinChars

import makerController
import makerProject
import makerTemplateDialog
import makerProjectConverter
import makerManageLinkedProjects
import makerTemplateSelect
import makerTemplateViewBuilder


import wx.html2 as theView

class ProjectManagerController(makerController.SuperController):
    def __init__(self, model , view):
        #print "initializing:", self
        self.view = view
        self.model = model
        self.createAbstractNameForViewObjects()
        self.rootAndProjectTreeItems = []
        self.treeViewAddRoot()
        self.bindActions()
        self.treeItems = []
        self.progressBars = []
        # format {NoteBookSelection[int], <makerFileController class>}
        self.noteBookPages = {}
        
        # This is a flag used to control unit tests
        self.testing = False
        
        
    def bindActions(self):
        
        # this binding is overridden once a project is loaded
        # the binding for this event is then done in 
        # makerProjectController
        
        self.treeView.Bind(self.view.wx.EVT_TREE_SEL_CHANGED, 
                           self.loadProject)        
        
        self.view.Bind(self.view.wx.EVT_CLOSE, self.model.closeOpenProjects)
        
        self.view.Bind(self.view.wx.EVT_MENU, self.model.closeOpenProjects,  
                       self.view.MenuItemQuit)
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                       self.actionAddNewProject,  
                       self.view.MenuItemAddProject)
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                       self.model.importProject,  
                       self.view.MenuItemImportProject)

        self.view.Bind(self.view.wx.EVT_MENU, 
                       self.model.deleteProject,  
                       self.view.MenuItemDeleteProject)
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                       self.model.linkToProject,  
                       self.view.MenuItemLinkToProject)
    
        self.view.Bind(self.view.wx.EVT_MENU, 
                       self.model.manageLinkedProjects,  
                       self.view.MenuItemManageLinkedProjects)
        
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.actionTreeCollapseOtherProjects, 
                  self.view.treePopUpMenuItemCollapseOther
                  )
        
    
    def actionTreeCollapseOtherProjects(self, event):
        
        currentItem = self.treeView.GetSelection()
        
        self.treeView.CollapseAllChildren(self.treeView.GetRootItem())
        self.treeView.Expand(self.treeView.GetRootItem())
        
        currentProjName = self.model.getActiveProject().getProject()
        
        for item in self.rootAndProjectTreeItems:
            if self.treeView.GetItemText(item) == currentProjName:
                self.treeView.ExpandAllChildren(item)
                self.model.getActiveProject().projectController.selectTreeItem(currentItem)
                
    
    
    def destroyView(self):
        
        # save UI data and session info...
        
        interfaceData = {"Size" : self.view.GetSize(),
                          "Position" : self.view.GetPosition(),
                          "SplitterSashPosition" : self.view.splitter.GetSashPosition(),
                          "sessionFiles" : self.model.sessionFiles,
                          "linkedProjects" : self.model.linkedProjectPaths}
                        
        # due to Sandbox on OS X linked projects to get saved for next session
        #"linkedProjects" : self.model.linkedProjectPaths}
        
        # openFiles: [ [fileName,fileType, project, cursorPosition, isLastOpenFile],    ]
        self.saveInterfaceData(interfaceData)
                        
        # exit
        self.view.Destroy()
    
    def loadAndSetInterfaceData(self):
        
        def setDefaults():
            # set UI defaults
            self.view.SetClientSize(self.view.wx.Size(1200, 700))
            self.view.Center(self.view.wx.BOTH)
            
        
        theFile = os.path.join(self.model.getProjectDir(), "../.makerUISettings")
        if os.path.isfile(theFile):
            try:
                interfaceData = readDataFromFile(theFile)
                self.view.SetSize(interfaceData["Size"])
                self.view.SetPosition(interfaceData["Position"])
                self.view.splitter.SetSashPosition(interfaceData["SplitterSashPosition"])
                
                #linked projects
                
                
                try:
                    
                    # open all files that had been open in last session
                    for sessionFile in interfaceData["sessionFiles"]:
                        
                        print "SessionFile:", sessionFile[2]
                        self.autoLoadProject(sessionFile[2])
                        #self.model.load(sessionFile[2])
                        item = (self.model.getActiveProject()).projectController.findTreeItem(sessionFile[0], sessionFile[1])
                        (self.model.getActiveProject()).projectController.selectTreeItemAndLoad(item)
                        
                        # set scroll position
                        ed = ((self.model.getActiveProject()).getCurrentFile()).fileController.editor
                        ed.GotoPos(sessionFile[3])
#                        
                        
                    # make last open file current file
                    for sessionFile in interfaceData["sessionFiles"]:
                        if sessionFile[-1] == "True":
                            self.autoLoadProject(sessionFile[2])
                            item = (self.model.getActiveProject()).projectController.findTreeItem(sessionFile[0], sessionFile[1])
                            (self.model.getActiveProject()).projectController.selectTreeItemAndLoad(item)
                            # set scroll position
                            ed = ((self.model.getActiveProject()).getCurrentFile()).fileController.editor
                            ed.GotoPos(sessionFile[3])
                            
                        
                    self.view.Refresh()
                    return # otherwise defaults will be loaded
                
                except Exception, e:
                    print str(e)
                    
            
            except Exception, e:
                print str(e)
                
        setDefaults()
    
    
    def saveInterfaceData(self, data):
        writeDataToFile(data, os.path.join(self.model.getProjectDir(), "../.makerUISettings"))
    
           
    
    def autoLoadProject(self, projectName):
        """ load projectName automatically """
        
        #self.model.load(projectName)
        #return
        treeItem = self.findTreeItemByText(projectName)
        self.view.tree.SelectItem(treeItem)
        
           
    def loadProject(self, event):
        
        print "loading project"
        item = event.GetItem()
       
        if item:
            #itemParent = self.treeView.GetItemParent(item)
           
            if self.treeView.GetItemText(item) == self.treeView.GetItemText(self.treeViewGetRoot()):
                pass
                #print "root selected"
                    
            else:
                                            
                project = self.treeView.GetItemText(item)
                self.model.load(project)
                
        #self.view.wx.Yield()
        #event.Skip()
        
        
    def buildTemplateView(self):
        
        pass
        
        
    def actionAddNewProject(self, event):
        
        projName = self.input("Enter a project name...", title="Create new project...")

        if not projName: 
            return 

        if not verifyLatinChars(projName):
            self.errorMessage("Please use only Latin characters for project names...")
            if not self.testing:
                self.actionAddNewProject(None)
            else:
                return
        
        tgt = os.path.join(self.model.getProjectDir(), projName)
                
        if os.path.isdir(tgt):
            m  = "A project with the name '" + projName + "' already exists !"
            self.errorMessage(m)
            return
        
        else:    
            if not self.testing:
                self.showTemplateDialog(tgt, projName)        
            
        
    
    def showTemplateDialog(self, newProjectDir, newProjectName):
        """
        
        Displays the template selection dialog for a new project and calls
        model.addProject on selection
    
        """
        self.template = None
        
        selector = makerTemplateDialog.xrcDIALOG1(self.view)
        
        # customize 
        
        selector.wv = theView.WebView.New(selector)
        selector.selectedURL = None
        
        selector.Sizer.Replace(selector.WebView, selector.wv)
        selector.Sizer.Layout()
        selector.Refresh()
        
        
        def loadTemplates():
        
            selector.wv.LoadURL("file:///Users/maker/Desktop/test.html")
            selector.Bind(theView.EVT_WEB_VIEW_NAVIGATING, onWebViewNavigating, selector.wv)
        
        
        def onWebViewNavigating(evt):
            
            url = evt.GetURL()
            print "url is:", url 
            self.template = re.compile('--(.+)--', re.IGNORECASE).findall(url)
            
            if self.template == []:
                return
            
            template = self.template[0]
            src = os.path.join(self.model.getSystemPath(), 'templates', template)
            
            if not os.path.isdir(src):
                self.errorMessage("Template Error: Template does not exist...\n" + template)
                return
            
            selector.Destroy()
            
            self.showProgress(limit = 1, Message="Creating project...", title="Creating project...")
            
            self.model.addNewProject(src, newProjectDir, newProjectName)
                     
            self.addProjectIconToTree(newProjectName)
            self.killProgressBar()
            
            if not self.testing:
                self.model.activeProject.makeAll()


         
        def cancel(event):
            
            selector.Destroy()
            event.Skip()
        
          
        loadTemplates()
        selector.ShowWindowModal()
        
        
    
    def addProjectIconToTree(self, projectName):
        
        item = self.treeViewAppendItem(self.treeRoot, projectName, type="Project")
        self.rootAndProjectTreeItems.append(item)
        
        # only not if not running test suite
        if not self.testing:
            self.treeView.SelectItem(item, True)
    
    
    def createAbstractNameForViewObjects(self):
        
        self.treeView = self.view.tree
        
        
    def treeViewAddRoot(self, rootName="MAKER PROJECTS:"):
        self.treeRoot = self.treeView.AddRoot(rootName)
        
        self.rootAndProjectTreeItems.append(self.treeRoot)
        
        # style
        
        item = self.treeView.GetRootItem()
        self.treeView.SetItemBold(item, True)
        self.treeView.SetItemTextColour(item, "#555d6b")
            
#        self.treeView.SetItemImage(self.treeRoot, self.view.fldridx, 
#                                        self.view.wx.TreeItemIcon_Normal)
#        self.treeView.SetItemImage(self.treeRoot, self.view.fldropenidx, 
#                                        self.view.wx.TreeItemIcon_Expanded)



    def findTreeItemByText(self, text):
        
        for item in self.rootAndProjectTreeItems:
            result = self.view.tree.GetItemText(item) 
            #print len(self.rootAndProjectTreeItems), " tree items"
            if result == text:
                #print "! returning ", item
                return item

    def isEventTreeEvent(self, event):
        try:
            # if this fails event is not a tree event
            event.GetItem()
            return True
        except:
            return False
            



    def listProjectsInTree(self, projectList):
        
        for proj in projectList:
        
            item = self.treeViewAppendItem(self.treeRoot, proj, type="Project")
            self.rootAndProjectTreeItems.append(item)
            
        self.treeViewExpandItem(self.treeRoot)
        


class ProjectManager:
    
    def __init__(self, view):
        
        self.controller = ProjectManagerController(self, view)
        self.setProjectDir()
        
        self.linkedProjectPaths = []
        self.loadLinkedProjects()
        self.linkedProjects = {}
        self.controller.listProjectsInTree(self.getProjects())
        self.openProjects = []
        self.openFiles = []
       
    
    def getApplicationPath(self):
        """ get path where the maker executable resides """
        return os.path.dirname(sys.argv[0])
    
    
    def getSystemPath(self):
        """ get system path """
        return os.path.join(os.path.dirname(sys.argv[0]), "system/")

    # ------------------------------------------------------------    
    
    def getTemplates(self):
        """Return a list of the available project templates."""
        theList = os.listdir(os.path.join(self.getSystemPath(), 'templates'))
        templateList = []
        # filter out hidden files
        for item in theList:
            if not item.startswith('.'):
                templateList.append(item)
        
        return templateList
    
    
    def getTemplateDir(self):
        """ returns the directory containing the templates """
        return os.path.join(self.getSystemPath(), 'templates')
        
    
    def importProject(self, event=None):        
        """
        Imports a project and converts it to actual settings, 
        doing several checks at the same time. Returns a boolean 
        indicating outcome.
        """

        project = self.controller.importProjectDialog()
        if not project: return
        
        projectFolder = self.getProjectDir()

        # TO DO: Brinick is confused. Why do we bother calling the converter? 
        # It seems the only thing that marks a folder as a makerProject 
        # is the presence of a sub directory called 'parts'. 
        # And commenting out the line below does not seem to prevent me from
        # successfully importing a project. So what's its purpose?

        # Gerald: We used to have a dist table for each language among other 
        # odd things the newer project version avoids these
        
        # verify if project settings are up to date
        makerProjectConverter.Verify(project)

        if not os.path.isdir(os.path.join(project, 'parts')):
            self.controller.errorMessage('%s is not a maker project !' % project)
            return

        print '%s is a maker project' % project
        print 'importing: %s' % project
        print "Project: %s" % project
        print "ProjectFolder: %s" % projectFolder

        proj = os.path.basename(project)
        dest = os.path.join(projectFolder, proj)
        if os.path.isdir(dest):
            self.controller.errorMessage('A project named %s already exists!' % dest)
            return
        
        try:
            self.controller.showProgress(4," ")
            self.controller.updateProgressPulse("importing: " + proj)
            
            copyFileTree(project, os.path.join(projectFolder, proj), 
                                        self.controller.updateProgressPulse, 
                                        ("importing: " + proj))
            
              
            #m = "The project ' %s ' has been imported..." % proj
            
            self.controller.addProjectIconToTree(proj)
            self.controller.killProgressBar()
            
            return
        except Exception, e:
            self.controller.killProgressBar()
            m  = "Unable to import project: %s\n" % project
            m += "Detailed Information:\n\n" + str(e)
            
            self.controller.errorMessage(m)
            return
     
    
    
    
    def addNewProject(self, templatePath, newProjectDir, newProjectName):
        
        """ The actual project creation """
        copyFileTree(templatePath, newProjectDir, self.controller.updateProgressPulse, ("creating: " + newProjectName))
    
    
    
    def removeFromOpenFiles(self, name, group, project):
        """ remove a certain file from openFiles especially after the file has
            been closed
        """
        
        for theFile in self.openFiles:
            if theFile.getNameGroupAndProject() == [name, group, project]:
                self.openFiles.remove(theFile)
    
    
    def loadLinkedProjects(self):
    
        theFile = os.path.join(self.getProjectDir(), "../.makerUISettings")
        if os.path.isfile(theFile):
            try:
                interfaceData = readDataFromFile(theFile)
                for path in interfaceData['linkedProjects']:
                    if os.path.isdir(path):
                        self.linkedProjectPaths.append(path)
            except Exception, e:
                print "unable to load linked projects:" , str(e)
                
    

    def manageLinkedProjects(self, event=None):
        makerManageLinkedProjects.Manager(self.controller.view, self)
    
    
    def linkToProject(self, event=None):
        path = self.controller.dirDialog(message="Select a project to link to:")
        
        if not path:
            return
        
        if self.projectDir in path:
            self.controller.errorMessage("You cannot link to your makerProjects folder!")
            return
            
        # verify if project settings are up to date
        makerProjectConverter.Verify(path)

        if not os.path.isdir(os.path.join(path, 'parts')):
            self.controller.errorMessage('%s is not a maker project !' % path)
            return
    
        if path not in self.linkedProjectPaths:
            self.linkedProjectPaths.append(path)
            self.updateLinkedProjects()
            self.controller.addProjectIconToTree(os.path.basename(path))
        else:
            self.controller.infoMessage("There is already a link to this project...")
    
    def updateLinkedProjects(self):
        """ update list of linked projects """
        for path in self.linkedProjectPaths:
            self.linkedProjects[path] = os.path.basename(path) 
        
           
    def getProjects(self):
        """Returns a list with projects from the Constants.PROJECTBASE folder"""

        # only directories (not starting with '.') are to be retained
        
        
        projects = []
        
        self.updateLinkedProjects()
        
        for project in self.linkedProjects.itervalues():
            projects.append(project)
        
        for thing in os.listdir(self.getProjectDir()):
            fullThing = os.path.join(self.getProjectDir(), thing)
            if not thing.startswith('.') and os.path.isdir(fullThing):
                projects.append(thing)

        return projects
    
    def setProjectDirNonNT(self):
        

        try:
            theDir = os.environ['HOME']
        except:
            theDir = os.environ['HOMEPATH']
        
        if sys.platform == "darwin":       
            
            appDir = os.path.join(theDir, "Library/Application Support/TheMaker/")
        
        else:
        
            appDir = theDir

        if not os.path.isdir(appDir):
            os.mkdir(appDir)
        
        
        self.projectDir = os.path.join(appDir, Constants.PROJECTBASE)
        if not os.path.isdir(self.projectDir):
            self.createProjectDir()
    # ------------------------------------------------------------

    def setProjectDirNT(self, showOnlyWarnings = False):
        """
        from revision 387 
        we are moving the path file to the application directory due to problems on Vista
        
        """
        fPath = os.path.join(self.getApplicationPath(), 'makerPath')
        if os.path.isfile(fPath):

            path = readFile(fPath, asLines=True, lineRange=[0])

            if os.path.isdir(path) and path.endswith(Constants.PROJECTBASE):
                self.projectDir = path
            else:
                m  = "No maker projects OR invalid path to projects: "
                m += path
                self.controller.errorMessage(m)
                os.remove(fPath)
                self.setProjectDirNT(showOnlyWarnings = True)
        else:
            m  = "Please select a directory to store your projects!\n" 
            m += "You can also select an existing 'makerProjects' folder."
            
            if not showOnlyWarnings:
                self.controller.infoMessage(m)
                                
            p = self.controller.dirDialog()

            if p:
                self.projectDir = os.path.join(p, Constants.PROJECTBASE)
                if p.endswith(Constants.PROJECTBASE): self.projectDir = p
                    
                writeFile(fPath, self.projectDir)
                if not os.path.isdir(self.projectDir):
                    self.createProjectDir()
            else:                    
                m  = "You need to select a project folder "
                m += "to run the maker !\n"
                m += "Would you like to try again ?"
                if self.controller.askYesOrNo(m) == 'Yes':
                    self.setProjectDirNT(showOnlyWarnings= True)
                else:
                    sys.exit(0)
                    

    # ------------------------------------------------------------

    def setProjectDir(self):
        """
        Sets self.projectDir to $HOME/Constants.PROJECTBASE (Linux/Mac OS).
        On Windows it asks the user to specify a path on the first run 
        and then saves the path to path.
        """
        
        {'nt': self.setProjectDirNT}.get(os.name, self.setProjectDirNonNT)()

    # ------------------------------------------------------------
        
    def getProjectDir(self):
        """Returns the project folder."""        
        return self.projectDir

    # ------------------------------------------------------------
        
    def createProjectDir(self):
        """Creates the project folder."""
        os.mkdir(self.getProjectDir())
    

    def saveSessionFiles(self):
        
        # sessionFiles is an object used to store information about
        # the currently open files when the App is killed, this information
        # will be restored when the App is started again
        
        self.sessionFiles = []
        
        for theFile in self.openFiles:
            obj = []
            obj.append(theFile.getName())
            obj.append(theFile.getType())
            # save project that the file belongs to
            obj.append(theFile.getProject())
            # save current scroll position
            ed = theFile.fileController.editor
            obj.append(ed.GetCurrentPos())
            
            if theFile.getName() + theFile.getType() == (self.getActiveProject()).getCurrentFileName():
                obj.append("True")
            else:
                obj.append("False")
            
            self.sessionFiles.append(obj)
        
        
        
    
 
    def deleteProject(self, event=None):
        
        project = self.getActiveProject()
        if self.controller.askYesOrNo("Do you want to delete the project: '" + project.getProject() + "'?") == "Yes":
            
            values = []
            
            for value in self.controller.noteBookPages.itervalues():
                values.append(value)
            
            for aFile in values:

                if aFile.model.core.getProject() == project.getProject():
                    
                    aFile.model.closeFile(callController = True)

            for item in self.controller.rootAndProjectTreeItems:
                if self.controller.treeView.GetItemText(item) == project.getProject():
                    self.controller.treeView.Delete(item)


            shutil.rmtree(project.getProjectPath())
            self.openProjects.remove(project)
            
            if self.openProjects == []:
                self.controller.resetAllViews()
    
    
    def exitApplication(self):
        """ alias method """
        self.closeOpenProjects(None)
    
 
    def closeOpenProjects(self, event=None):
        """ called when the App is closed """
        
        self.saveSessionFiles()
        
        for theFile in self.openFiles:
        
            if not theFile.getSaved():
                if self.controller.askYesOrNo("Would you like to save: " + 
                                              theFile.core.getProject() + "/" +
                                              theFile.getFileName() +
                                               "?")=="Yes":
                    theFile.save()
                     
        for project in self.openProjects:
            project.closeProject()
        
        
        self.controller.destroyView()
    
    
    
    
    
    def setActiveProject(self, project):
        
        if project not in self.openProjects:
            self.openProjects.append(project)
                
        self.activeProject = project
        
        
    def getActiveProject(self):
        return self.activeProject
    
    def findOpenProjectInstByName(self, name):
        for instance in self.openProjects:
            result = instance.getProject() 
            if result == name:
                return instance
        else:
            return None
    
    
#    def switchProjectDueToNoteBookEvent(self, otherProject, event=None):
#        
#                
#        # if this method gets called from inside a current project
#        # an event gets passed on to the project we are switching to 
#        #
#        # please see makerProjectController.py / actionLoadFile for
#        # clarity
#        
#        print "switching from ", self.getActiveProject().getProject(), "to " , otherProject
#         
#        if self.getActiveProject() not in self.openProjects:
#            self.openProjects.append(self.getActiveProject())
#        
#        existingInstance = self.findOpenProjectInstByName(otherProject)
#        
#        if existingInstance:
#            #print "projectManager: loading existing instance", existingInstance.getProject()
#            self.setActiveProject(existingInstance)
#            # take control
#            #print "active project now: ", self.getActiveProject().getProject()
#            self.getActiveProject().projectController.bindActions()
#            
#            if event:
#                self.getActiveProject().projectController.actionLoadFile(event)
#                        
#        else:
#            # load new project
#            self.load(otherProject)
        
    
    def switchProject(self, otherProject, event=None):
        
        # if this method gets called from inside a current project
        # an event gets passed on to the project we are switching to 
        #
        # please see makerProjectController.py / actionLoadFile for
        # clarity
        
        if self.getActiveProject().getProject() == otherProject:
            return
        
        print "switching from ", self.getActiveProject().getProject(), "to " , otherProject
         
        if self.getActiveProject() not in self.openProjects:
            self.openProjects.append(self.getActiveProject())
        
        existingInstance = self.findOpenProjectInstByName(otherProject)
        
        if existingInstance:
            #print "projectManager: loading existing instance", existingInstance.getProject()
            self.setActiveProject(existingInstance)
            # take control
            #print "active project now: ", self.getActiveProject().getProject()
            self.getActiveProject().projectController.bindActions()
            if event:
                if self.controller.isEventTreeEvent(event):
                    
                    self.getActiveProject().projectController.actionLoadFile(event)
                else:
                    self.getActiveProject().projectController.noteBookPageChanged(event)
            
            
        else:
            # load new project
            self.load(otherProject)
        
        
    
    def load(self, projectName):
        """ initializes a new instance of makerProject.py """
        if projectName in self.linkedProjects.itervalues():
            for key in self.linkedProjects.iterkeys():
                if self.linkedProjects[key] == projectName:
                    path = key
                else:
                    pass
        
        else: 
        
            path = os.path.join(self.getProjectDir() , projectName)
        
        # ensuring backwards compatibility
        # just in case that project has been around before 0.6
        makerProjectConverter.Verify(path)
        
        self.setActiveProject(makerProject.MakerProjectModel(path, 
                                                             self.controller.view,
                                                             self)) 
    
    
    
    
    
  
    
    
    
    
