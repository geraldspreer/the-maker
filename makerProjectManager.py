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
import makerManageLinkedProjects
import makerTemplateViewBuilder
import makerThread
import webbrowser as web

import wx.html2 as theView

class ProjectManagerController(makerController.SuperController):
    def __init__(self, model , view):
        
        self.view = view
        self.model = model
        self.createAbstractNameForViewObjects()
        self.rootAndProjectTreeItems = []
        self.treeViewAddRoot()
        self.bindActions()
        self.treeItems = []
        self.progressBars = []
        self.defaultEditorStyle = "Github"
        self.loadEditorStylesAndCreateMenu()
        
        # format {NoteBookSelection[int], <makerFileController class>}
        self.noteBookPages = {}
        
        # This is a flag used to control unit tests
        self.testing = False
    
    
    def loadStyles(self):
        """ this creates self.editorStyles """
        
        self.editorStyles = {}
        
        path = os.path.join(self.model.getApplicationPath(), "system/EditorStyles")
        for item in os.listdir(path):
            if item.endswith(".json"):
                _s = item.replace(".json", "")
                self.editorStyles[_s] = eval(readFile(os.path.join(path,item)))
    
        
    
        
    def loadEditorStylesAndCreateMenu(self):
        self.styleMenus = {}
        path = os.path.join(self.model.getApplicationPath(), "system/EditorStyles")
        
        MenuItemDefaultStyle = self.view.subMenuEditorStyles.Append(help='Default Editor Style',
                                              id=-1, 
                                              kind=self.view.wx.ITEM_CHECK, 
                                              text = "Default Style")
        
        self.styleMenus[None] = MenuItemDefaultStyle.GetId()
        
        self.view.subMenuEditorStyles.AppendSeparator()
        
        self.view.Bind(self.view.wx.EVT_MENU, self.resetEditorStyle, MenuItemDefaultStyle)
        
        
        for item in os.listdir(path):
            if item.endswith(".json"):
                _s = item.replace(".json", "")
                
                x = self.view.subMenuEditorStyles.Append(help='Editor Style ' + _s,
                                              id=-1, 
                                              kind=self.view.wx.ITEM_CHECK, 
                                              text = _s)
                
                self.styleMenus[item] = x.GetId()
                
                self.view.Bind(self.view.wx.EVT_MENU_HIGHLIGHT, self.prevEditorStyle, x)
                self.view.Bind(self.view.wx.EVT_MENU, self.setEditorStyle, x)
                
        
        self.loadStyles()
    
    
    
    def toggleMenuItemByStyleName(self, styleName = None):
        
        if not styleName:
            return

        for key, value in self.styleMenus.iteritems():
                
            if key == styleName + ".json":
                
                self.view.subMenuEditorStyles.FindItemById(value).Check(True) 
            else:
                self.view.subMenuEditorStyles.FindItemById(value).Check(False) 
    

    def toggleEditorStyleItems(self, itemId):
        
        for key, value in self.styleMenus.iteritems():
                
            if value == itemId:
                
                self.view.subMenuEditorStyles.FindItemById(value).Check(True) 
            else:
                self.view.subMenuEditorStyles.FindItemById(value).Check(False) 
    
    
    def setCurrentEditorStyle(self, style = None):
        
        if not style:
            self.currentEditorStyle = self.defaultEditorStyle
        else:
            self.currentEditorStyle = style
            
        # apply style to all open files
        for theFile in self.model.openFiles:
            
            edWrapper = theFile.fileController.editorWrapper
            edWrapper.applyCodeStyle(self.getCurrentEditorStyleData())
            
            
    
    def getCurrentEditorStyle(self):
        
        return self.currentEditorStyle 
    
    
    def getCurrentEditorStyleData(self):
        return self.editorStyles[self.getCurrentEditorStyle()]
    
    def getEditorStyleData(self, styleName = None):
        if not styleName:
            style = self.defaultEditorStyle
        else:
            return self.editorStyles[styleName]
    
    def getEditorStyles(self):
        """ returns the dict """
    
        return self.editorStyles
    
    
    def resetEditorStyle(self, event):
        """ reset editor style to default """
        print "now we are here..."
        editorWrapper = self.model.getActiveProject().getCurrentFile().fileController.editorWrapper
        editorWrapper.applyCodeStyle(self.getEditorStyleData(self.defaultEditorStyle))
        
        self.setCurrentEditorStyle(self.defaultEditorStyle)
        
        self.toggleEditorStyleItems(event.GetId())
    
    
    def setEditorStyle(self, event):
        
        for key, value in self.styleMenus.iteritems():
            
            if value == event.GetId():
                
                self.setCurrentEditorStyle(key.replace(".json",""))
        
        self.toggleEditorStyleItems(event.GetId())
    
    
    
    def prevEditorStyle(self, event):
        for key, value in self.styleMenus.iteritems():
            
            if value == event.GetMenuId():
                
                self.model.getActiveProject().getCurrentFile().fileController.editorWrapper.applyCodeStyle(self.editorStyles[key.replace(".json","")])
        
    
    
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
                       self.model.importClassicProject,  
                       self.view.MenuItemImportProject)
        
#
#        self.view.Bind(self.view.wx.EVT_MENU, 
#                       self.model.deleteProject,  
#                       self.view.MenuItemDeleteProject)
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                       self.model.openProject,  
                       self.view.MenuItemOpenProject)
    
        self.view.Bind(self.view.wx.EVT_MENU, 
                       self.model.manageLinkedProjects,  
                       self.view.MenuItemManageProjects)
        
        
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
                          "linkedProjects" : self.model.linkedProjectPaths,
                          "editorStyle" : self.getCurrentEditorStyle()}
                        
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
            self.setCurrentEditorStyle(self.defaultEditorStyle)
        
        theFile = os.path.join(self.model.getApplicationSupportDir(), ".makerUISettings")
        if os.path.isfile(theFile):
            try:
                interfaceData = readDataFromFile(theFile)
                self.view.SetSize(interfaceData["Size"])
                self.view.SetPosition(interfaceData["Position"])
                self.view.splitter.SetSashPosition(interfaceData["SplitterSashPosition"])
                self.setCurrentEditorStyle(interfaceData["editorStyle"])
                self.toggleMenuItemByStyleName(interfaceData["editorStyle"])
                
                #linked projects
                
                
                try:
                    
                    # open all files that had been open in last session
                    for sessionFile in interfaceData["sessionFiles"]:
                        
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
        
        writeDataToFile(data, os.path.join(self.model.getApplicationSupportDir(), ".makerUISettings"))
    
           
    
    def autoLoadProject(self, projectName):
        """ load projectName automatically """
        
        #self.model.load(projectName)
        #return
        treeItem = self.findTreeItemByText(projectName)
        self.view.tree.SelectItem(treeItem)
        
           
    def loadProject(self, event):
        
        item = event.GetItem()
       
        if item:
            #itemParent = self.treeView.GetItemParent(item)
           
            if self.treeView.GetItemText(item) == self.treeView.GetItemText(self.treeViewGetRoot()):
                pass
                #print "root selected"
                    
            else:
                                            
                project = self.treeView.GetItemText(item)
                self.model.load(project)
                


        
    def actionAddNewProject(self, event):
        
        projName = self.input("Project name...", title="Create new project:")

        if not projName: 
            return 

        if not verifyLatinChars(projName):
            self.errorMessage("Please use only Latin characters for project names...")
            if not self.testing:
                self.actionAddNewProject(None)
            else:
                return
        # use get dir then put together...
        fromUser = self.dirDialog("Where would you like to keep your project?")
        if not fromUser:
            return
        
        # set correct name
        projName += ".makerProject"
        
        tgt = os.path.join(fromUser, projName)
                
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
        
        viewPath = makerTemplateViewBuilder.buildView(self.model.getSystemPath(), self.model.getApplicationSupportDir())
        
        self.template = None
        self.selectedTemplate = None
        
        selector = makerTemplateDialog.xrcDIALOG1(self.view)
        
        # customize 
        
        selector.wv = theView.WebView.New(selector)
        selector.selectedURL = None
        
        selector.Sizer.Replace(selector.WebView, selector.wv)
        selector.Sizer.Layout()
        selector.Refresh()
    
        selector.Create.SetDefault()
        selector.Create.Enable(False)
        
        def loadTemplates(pathToView):
        
            # turn into proper URL and load
            selector.wv.LoadURL("file://" + pathToView.replace(" ", "%20"))
            
            selector.Bind(theView.EVT_WEB_VIEW_NAVIGATING, onWebViewNavigating, selector.wv)
            selector.Bind(self.view.wx.EVT_BUTTON, onCreateButton, selector.Create)
        
    
        def onWebViewNavigating(evt):
            
            url = evt.GetURL()
            if not url.endswith("--"):
                web.open(url)
                evt.Veto()
            else:
                onWebViewNavigated(evt)
            
            
        def onWebViewNavigated(evt):
            
            url = evt.GetURL()
            self.template = re.compile('--(.+)--', re.IGNORECASE).findall(url)
            
            if self.template == []:
                return
            
            self.selectedTemplate = self.template[0]
            
            selector.Create.Enable(True)

        def onCreateButton(event):
            event.Skip()
            if not self.selectedTemplate:
                return
            
            src = os.path.join(self.model.getSystemPath(), 'templates', self.selectedTemplate)
            
            if not os.path.isdir(src):
                self.errorMessage("Template Error: Template does not exist...\n" + self.selectedTemplate)
                return
            
            selector.Close() # Don't destroy here - only hide 
            
            self.showProgress(limit = 1, Message="Creating project...", title="Creating project...")
            
            self.model.addNewProject(src, newProjectDir, newProjectName)
                     
            self.addProjectIconToTree(newProjectName)
            self.killProgressBar()
            
            if not self.testing:
                self.model.activeProject.makeAll()

            selector.Destroy() # Destroy dialog
        
        
        loadTemplates(viewPath)
        selector.ShowWindowModal()
        
        
    
    def addProjectIconToTree(self, projectName):
        
        item = self.treeViewAppendItem(self.treeRoot, projectName, type="Project")
        self.rootAndProjectTreeItems.append(item)
        
        # only do this if not running test suite
        if not self.testing:
            self.treeView.SelectItem(item, True)
            self.actionTreeCollapseOtherProjects(None)
            self.treeView.EnsureVisible(item)
    
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
        
        self.linkedProjectPaths = []
        self.loadLinkedProjects()
        self.linkedProjects = {}
        self.controller.listProjectsInTree(self.getProjects())
        self.openProjects = []
        self.openFiles = []
        self.projectConvertRepoName = "MakerProjects"
        
        makerThread.newThread(self.checkForSandboxedProjects)
        
        self.loadArgumentPassedProject()
       
    
    def checkForSandboxedProjects(self):
        
        updateInfo = ""
        
        updateInfo += "Please read carefully:\n"
        updateInfo += "We have improved the way TheMaker handles projects.\n"
        updateInfo += "Now you can have projects as external files wherever you like.\n"
        updateInfo += "But you need to choose where you would like to store your existing"
        updateInfo += " projects.\n\n "
        updateInfo += "Click OK to choose...\n "
        
        def getTargetDir(verbose = False):
            target = None
            if verbose:
                self.controller.infoMessage(updateInfo)
            
            target = self.controller.dirDialog("Where would you like to store your existing projects?")
            
            return target
        
        
        sandBoxProjects = os.path.join(self.getApplicationSupportDir(), "makerProjects")
        converted = []
        errors = False
        
        if not os.path.isdir(sandBoxProjects):
            
            return
        
        self.controller.view.Center()
        self.controller.view.Show()
        
        targetDir = getTargetDir(False)
        
        if not targetDir:
            targetDir = getTargetDir(verbose = True)
            if not targetDir:
                return

        
        for item in os.listdir(sandBoxProjects):
            if not item.startswith("."):
                
                src = os.path.join(sandBoxProjects, item)
                dst = os.path.join(targetDir, self.projectConvertRepoName ,item + ".makerProject") 
                
                if not os.path.isdir(dst):
                    # this is just a safety check. This case should never occur...
                    # 
                    shutil.copytree(src, dst)
                    converted.append(item + ".makerProject")
                    
                    if dst not in self.linkedProjectPaths:
                        self.openThisProject(dst, verbose = False)
                
        
        for bundle in converted:
            if not bundle in os.listdir(os.path.join(targetDir, self.projectConvertRepoName)):
                errors = True
                
        if errors == True:
            self.controller.errorMessage("Fatal Installation Error!\nPlease report this to info@makercms.org.\nWe will help you out!\nShutting down...")
            sys.exit(0)
        else:
            shutil.rmtree(sandBoxProjects, True)
            
    
    def getApplicationPath(self):
        """ get path where the maker executable resides """
        
        return os.path.dirname(sys.argv[0])
    
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
        
        return os.path.join(theDir, "Library/Application Support/TheMaker/")
    
    
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
        
    
    def importClassicProject(self, event=None):        
        """
        Imports a project and converts it to actual settings, 
        doing several checks at the same time. Returns a boolean 
        indicating outcome.
        """


        project = self.controller.importProjectDialog()
        if not project: return

        #=======================================================================
        # verify
        #=======================================================================
        if not os.path.isdir(os.path.join(project, 'parts')):
            self.controller.errorMessage('%s is not a TheMaker project!' % project)
            return

        if not project.endswith(".makerProject"):
            converted = project + ".makerProject"
            os.rename(project, converted)
            
        self.openThisProject(converted, verbose = False)        
    
    
    def addNewProject(self, templatePath, newProjectDir, newProjectName):
        
        """ 
            The actual project creation 
            The info.json file is ignored
        
        """
        copyFileTree(templatePath, newProjectDir,["info.json"], self.controller.updateProgressPulse, ("creating: " + newProjectName))
        if newProjectDir not in self.linkedProjectPaths:
            self.linkedProjectPaths.append(newProjectDir)
            self.updateLinkedProjects()
            
    
    def removeFromOpenFiles(self, name, group, project):
        """ remove a certain file from openFiles especially after the file has
            been closed
        """
        
        for theFile in self.openFiles:
            if theFile.getNameGroupAndProject() == [name, group, project]:
                self.openFiles.remove(theFile)
    
    
    def loadLinkedProjects(self):
    
        theFile = os.path.join(self.getApplicationSupportDir(), ".makerUISettings")
        if os.path.isfile(theFile):
            try:
                interfaceData = readDataFromFile(theFile)
                for path in interfaceData['linkedProjects']:
                    if os.path.isdir(path):
                        self.linkedProjectPaths.append(path)
            except Exception, e:
                print "unable to load linked projects:" , str(e)
                
    
    def loadArgumentPassedProject(self):
        """ load project that has been clicked on outside the app"""
        try:
            path = sys.argv[1]
        except:
            return
        
        if os.path.isdir(path) and path.endswith(".makerProject"):
            self.openThisProject(path, verbose = False)
           
    
    def manageLinkedProjects(self, event=None):
        makerManageLinkedProjects.Manager(self.controller.view, self)
    
    
    def openProject(self, event=None):
        bundle = self.controller.fileDialog(message = "Open A Project...")
        
        
        if not bundle:
            return
        
        path = bundle[0]
        
        self.openThisProject(path)
        
    def openThisProject(self, path, verbose = True):
        
        if not os.path.isdir(os.path.join(path, 'parts')):
            if verbose:
                self.controller.errorMessage('%s is not a TheMaker project !' % path)
            return
    
        if path not in self.linkedProjectPaths:
            self.linkedProjectPaths.append(path)
            self.updateLinkedProjects()
            self.controller.addProjectIconToTree(os.path.basename(path))
        else:
            if verbose:
                self.controller.infoMessage("This project is already open...")
    
    
    
    
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
        
#        for thing in os.listdir(self.getProjectDir()):
#            fullThing = os.path.join(self.getProjectDir(), thing)
#            if not thing.startswith('.') and os.path.isdir(fullThing):
#                projects.append(thing)

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
        
#    def getProjectDir(self):
#        """Returns the project folder."""        
#        return self.projectDir

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
            pass
            #path = os.path.join(self.getProjectDir() , projectName)
        
        self.setActiveProject(makerProject.MakerProjectModel(path, 
                                                             self.controller.view,
                                                             self)) 
    
    
    
    
    
  
    
    
    
    
