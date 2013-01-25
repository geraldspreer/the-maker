import makerController
import makerReplaceDialog
import os
import makerFileTemplates
from makerUtilities import readFile, writeFile

class Controller(makerController.SuperController):
    
    def drawDialog(self):
        
        self.dialog = makerReplaceDialog.xrcFindReplace(self.view)
        self.dialog.Cancel.Bind(self.view.wx.EVT_BUTTON, 
                         self.close)
        
        self.dialog.OK.Bind(self.view.wx.EVT_BUTTON, 
                         self.doReplaceCurrent)
    
        self.dialog.findInCurrent.Bind(self.view.wx.EVT_RADIOBUTTON, 
                         self.findInCurrent)
        
        self.dialog.findInProject.Bind(self.view.wx.EVT_RADIOBUTTON, 
                         self.replaceInProject)
    
        
        self.dialog.Find.Bind(self.view.wx.EVT_TEXT, 
                         self.showOccurences)
    
        self.dialog.Find.Bind(self.view.wx.EVT_TEXT_ENTER, 
                         self.showOccurences)
        
        self.dialog.findInProject.Enable(True)
        
        self.dialog.findInOpen.Enable(False)
        
        self.dialog.SetTitle("Find / Replace..." )
        
        self.rawText = self.editor.GetText()
        
        # set selected text in Find field
        self.dialog.Find.SetValue(self.editor.GetSelectedText())
        
    def showOccurences(self, evt):
        """ update status label """
        s = self.dialog.Find.GetValue()
    
        if s != "":
            occ = self.rawText.count(s)
            
            if occ > 0:
                self.dialog.Status.SetLabel(str(occ) + " found")
            elif occ == 0: 
                self.dialog.Status.SetLabel("Not found")
        else: 
            self.dialog.Status.SetLabel("")
   
    def showDialog(self):
        self.dialog.Show()

    def setEditor(self, editor):
        
        self.editor = editor

    def close(self, event):
        self.dialog.Close()

    def findInCurrent(self, evt):
        """ just updating bindings """
        self.dialog.OK.Unbind(self.view.wx.EVT_BUTTON)
        self.dialog.OK.Bind(self.view.wx.EVT_BUTTON, 
                         self.doReplaceCurrent)

        self.dialog.Replace.Unbind(self.view.wx.EVT_SET_FOCUS)

        
        self.dialog.Find.Bind(self.view.wx.EVT_TEXT_ENTER, 
                         self.showOccurences)

        self.dialog.Find.Bind(self.view.wx.EVT_TEXT, 
                         self.showOccurences)

        self.showOccurences(None)
    
    
    def replaceInProjectFinal(self, evt):
        
        old = self.dialog.Find.GetValue() 
        new = self.dialog.Replace.GetValue()
        
        # replace in current open file
        self.replaceCurrent(True)
        # call model and replace in whole project
        self.model.replaceInProject(old,new)
        self.dialog.Destroy()
    
    
    def showOccurencesInProject(self, evt):
        
        project = self.model.project
        
        pathToProject = project.getPathParts()
        string = self.dialog.Find.GetValue()
        if string:
            count = 0
            for file in os.listdir(pathToProject):
                try:
                    count += (readFile(os.path.join(pathToProject, file))).count(string)
                except:
                    pass
            if count > 0:
                self.dialog.Status.SetLabel(str(count) + " Found")
            else:
                self.dialog.Status.SetLabel("Not Found")
                
    def findInFocus(self, evt):
        self.dialog.Status.SetLabel("")
        
        
    def replaceInProject(self, evt):
        """ just updates bindings """
        self.dialog.Find.Bind(self.view.wx.EVT_SET_FOCUS, 
                         self.findInFocus)
        
        self.dialog.Replace.Bind(self.view.wx.EVT_SET_FOCUS, 
                         self.showOccurencesInProject)

        self.dialog.Find.Unbind(self.view.wx.EVT_TEXT)
        self.dialog.Find.Unbind(self.view.wx.EVT_TEXT_ENTER)
        
        self.dialog.OK.Unbind(self.view.wx.EVT_BUTTON)
        self.dialog.OK.Bind(self.view.wx.EVT_BUTTON, 
                         self.replaceInProjectFinal)

    
    def doReplaceCurrent(self, event):
        """ calls replaceCurrent catches event """
        self.replaceCurrent(doProject = False)
        
    
    def replaceCurrent(self, doProject = False):
        """ if do project is True, this 
            method will replace in all open files 
            belonging to this project
               
         """
        findText = self.dialog.Find.GetValue()
        replaceText = self.dialog.Replace.GetValue()
                
        if findText:
            if doProject:
                # replace in open files belonging to project
                for file in self.model.project.projectManager.openFiles:
                    if file.getProject() == self.model.project.getProject():
                        ed = file.fileController.editor
                        pageText = ed.GetText()
                        if replaceText:
                            ed.SetText(pageText.replace(findText, replaceText))
            else:
                # replace just in the open file
                pageText = self.editor.GetText()
                if replaceText:
                    self.editor.SetText(pageText.replace(findText, replaceText))
            
        self.dialog.Destroy()
            
        
        
        
    
class Replace:
    
    def __init__(self, mainView, editor, project):
        
        self.controller = Controller(self, mainView)
        self.controller.setEditor(editor)
        self.controller.drawDialog()
        self.controller.showDialog()
        self.project = project
    
    
    def replaceInProject(self, old, new):
        """ replace in project method"""
        self.project.replaceStringInAllItems(old, new)
        
    
    