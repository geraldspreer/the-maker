import os
import sys
import shutil
import re

try:
    from Foundation import NSURL, NSData, NSURLBookmarkResolutionWithSecurityScope, NSURLBookmarkCreationWithSecurityScope 
    print "PyObjC - OK"
except:
    print "You need to have PyObjC installed !"
    print "Download it at: http://pythonhosted.org/pyobjc/"
    print "TheMaker does not run without it !"
    print "Leaving...."    
    sys.exit()

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
        self.noteBookPages = {}
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
        if not styleName: return

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
        return self.editorStyles
    
    def resetEditorStyle(self, event):
        """ reset editor style to default """
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
        for resource in self.model.securityScopedResources:
            try:
                resource.stopAccessingSecurityScopedResource()
            except Exception, e:
                print "Unable to stop using security scoped urls:", str(e)
        
        interfaceData = {"Size" : self.view.GetSize(),
                          "Position" : self.view.GetPosition(),
                          "SplitterSashPosition" : self.view.splitter.GetSashPosition(),
                          "sessionFiles" : self.model.sessionFiles,
                          "linkedProjects" : self.model.linkedProjectPaths,
                          "editorStyle" : self.getCurrentEditorStyle(),
                          "bookmarks": self.model.bookmarks}
        self.saveInterfaceData(interfaceData)
        self.view.Destroy()
    
    def loadAndSetInterfaceData(self):
        def setDefaults(interfaceData):
            if not interfaceData:
                self.view.SetClientSize(self.view.wx.Size(1200, 700))
                self.view.Center(self.view.wx.BOTH)
                self.setCurrentEditorStyle(self.defaultEditorStyle)
                return
            try:
                self.view.SetSize(interfaceData["Size"])
                self.view.SetPosition(interfaceData["Position"])
                self.view.splitter.SetSashPosition(interfaceData["SplitterSashPosition"])
            except:
                self.view.SetClientSize(self.view.wx.Size(1200, 700))
                self.view.Center(self.view.wx.BOTH)
            try:
                self.setCurrentEditorStyle(interfaceData["editorStyle"])
                self.toggleMenuItemByStyleName(interfaceData["editorStyle"])
            except:
                self.setCurrentEditorStyle(self.defaultEditorStyle)

        interfaceData = None
        theFile = os.path.join(self.model.getApplicationSupportDir(), ".makerUISettings")
        if os.path.isfile(theFile):
            try:
                interfaceData = readDataFromFile(theFile)
                self.view.SetSize(interfaceData["Size"])
                self.view.SetPosition(interfaceData["Position"])
                self.view.splitter.SetSashPosition(interfaceData["SplitterSashPosition"])
                try:
                    self.setCurrentEditorStyle(interfaceData["editorStyle"])
                    self.toggleMenuItemByStyleName(interfaceData["editorStyle"])
                except:
                    # no editor style on file
                    self.setCurrentEditorStyle(self.defaultEditorStyle)
                try:
                    # enable security-scoped-bookmarks for use in this session
                    for item in interfaceData["bookmarks"]:
                        nsdata = NSData.alloc().initWithBytes_length_(item, len(item))
                        url = NSURL.URLByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(nsdata, 
                                                                                                                NSURLBookmarkResolutionWithSecurityScope, 
                                                                                                                None, 
                                                                                                                None, 
                                                                                                                None) 
                        theURL = url[0]
                        #  save again to bookmarks but only if this project 
                        #  is still linked
                        if theURL.path() in self.model.linkedProjectPaths:
                            self.model.bookmarks.append(item)
                            theURL.startAccessingSecurityScopedResource()
                            self.model.securityScopedResources.append(theURL)
                except:
                    print "Unable to resolve security-scoped-bookmarks"
                try:
                    for sessionFile in interfaceData["sessionFiles"]:
                        self.autoLoadProject(sessionFile[2])
                        item = (self.model.getActiveProject()).projectController.findTreeItem(sessionFile[0], sessionFile[1])
                        (self.model.getActiveProject()).projectController.selectTreeItemAndLoad(item)
                        # set scroll position
                        ed = ((self.model.getActiveProject()).getCurrentFile()).fileController.editor
                        ed.GotoPos(sessionFile[3])
                        
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
                    return
                except Exception, e:
                    print str(e)
            except Exception, e:
                print str(e)
        setDefaults(interfaceData)
    
    def saveInterfaceData(self, data):
        writeDataToFile(data, os.path.join(self.model.getApplicationSupportDir(), ".makerUISettings"))
    
    def autoLoadProject(self, projectName):
        """ load projectName automatically """
        treeItem = self.findTreeItemByText(projectName)
        self.view.tree.SelectItem(treeItem)
           
    def loadProject(self, event):
        item = event.GetItem()
        if item:
            if self.treeView.GetItemText(item) != self.treeView.GetItemText(self.treeViewGetRoot()):
                project = self.treeView.GetItemText(item)
                self.model.load(project)
        
    def actionAddNewProject(self, event):
        projName = self.input("Project name...", title="Create new project:")

        if not projName: return

        if not verifyLatinChars(projName):
            self.errorMessage("Please use only Latin characters for project names...")
            if not self.testing:
                self.actionAddNewProject(None)
            else:
                return
        fromUser = self.dirDialog("Where would you like to keep your project?")

        if not fromUser: return

        projName += ".makerProject"
        tgt = os.path.join(fromUser, projName)
        print tgt
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
        self.selectedTemplate = makerTemplateViewBuilder.defaultTemplate()
        selector = makerTemplateDialog.xrcDIALOG1(self.view)
        selector.wv = theView.WebView.New(selector)
        selector.selectedURL = None
        selector.Sizer.Replace(selector.WebView, selector.wv)
        selector.Sizer.Layout()
        selector.Refresh()
        selector.Create.SetDefault()
        selector.Create.Enable(True)
        
        def loadTemplates(pathToView):
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
            if not self.selectedTemplate: return
            
            src = os.path.join(self.model.getSystemPath(), 'templates', self.selectedTemplate)
            if not os.path.isdir(src):
                self.errorMessage("Template Error: Template does not exist...\n" + self.selectedTemplate)
                return
            
            selector.Close() # Don't destroy here - only hide 
            self.showProgress(limit = 1, Message="Creating project...", title="Creating project...")
            self.model.addNewProject(src, newProjectDir, newProjectName)
            self.addProjectIconToTree(newProjectName)
            self.killProgressBar()
            
            if not self.testing: self.model.activeProject.makeAll()

            selector.Destroy()
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
        item = self.treeView.GetRootItem()
        self.treeView.SetItemBold(item, True)
        self.treeView.SetItemTextColour(item, "#555d6b")

    def findTreeItemByText(self, text):
        for item in self.rootAndProjectTreeItems:
            result = self.view.tree.GetItemText(item) 
            if result == text:
                return item

    def isEventTreeEvent(self, event):
        try:
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
        self.bookmarks = []
        self.securityScopedResources = [] 
        self.projectConvertRepoName = "MakerProjects"
        
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
    
    def getTemplates(self):
        """Return a list of the available project templates."""
        theList = os.listdir(os.path.join(self.getSystemPath(), 'templates'))
        templateList = []
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
            newPath = self.controller.dirDialog("Where would you like to save this project?")
            if newPath:
                projName = os.path.split(project)[-1]
                converted = os.path.join(newPath, projName + ".makerProject")
                shutil.copytree(project, converted)
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
            self.setSecurityScopedBookmark(newProjectDir)
    
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
    
    def setSecurityScopedBookmark(self, path):
        #=======================================================================
        #  Security Scoped Bookmark
        #=======================================================================
        try:
            dirURL = NSURL.alloc().initFileURLWithPath_(path)
            myData = dirURL.bookmarkDataWithOptions_includingResourceValuesForKeys_relativeToURL_error_(NSURLBookmarkCreationWithSecurityScope,
                                                                                                            None,
                                                                                                            None,
                                                                                                            None) 
            theBytes = myData[0].bytes().tobytes()
            self.bookmarks.append(theBytes)
        except Exception, e:
            print "Unable to create security-scoped-bookmarks"
            print str(e)
            print "------------------------------------------"
    
    def openThisProject(self, path, verbose = True):
        if not os.path.isdir(os.path.join(path, 'parts')):
            if verbose:
                self.controller.errorMessage('%s is not a TheMaker project !' % path)
            return
    
        if path not in self.linkedProjectPaths:
            self.linkedProjectPaths.append(path)
            self.updateLinkedProjects()
            # Because of Apple's Sandbox 
            self.setSecurityScopedBookmark(path)
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

    def setProjectDir(self):
        """
        Sets self.projectDir to $HOME/Constants.PROJECTBASE (Linux/Mac OS).
        On Windows it asks the user to specify a path on the first run 
        and then saves the path to path.
        """
        {'nt': self.setProjectDirNT}.get(os.name, self.setProjectDirNonNT)()

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
            obj.append(theFile.getProject())
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
 
    def exitApplicationForced(self):
        self.controller.view.Destroy()
 
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
            self.setActiveProject(existingInstance)
            self.getActiveProject().projectController.bindActions()
            if event:
                if self.controller.isEventTreeEvent(event):
                    self.getActiveProject().projectController.actionLoadFile(event)
                else:
                    self.getActiveProject().projectController.noteBookPageChanged(event)
        else:
            self.load(otherProject)
    
    def load(self, projectName):
        """ initializes a new instance of makerProject.py """
        if projectName in self.linkedProjects.itervalues():
            for key in self.linkedProjects.iterkeys():
                if self.linkedProjects[key] == projectName:
                    path = key
        self.setActiveProject(makerProject.MakerProjectModel(path, 
                                                             self.controller.view,
                                                             self)) 
