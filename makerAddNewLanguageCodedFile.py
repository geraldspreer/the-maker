import makerController
import makerNewFileDialog
import os
import makerFileTemplates
from makerUtilities import readFile, writeFile


class Controller(makerController.SuperController):
    def drawDialog(self):
        self.dialog = makerNewFileDialog.xrcnewFile(self.view)
        self.dialog.Cancel.Bind(self.view.wx.EVT_BUTTON, self.close)
        self.dialog.Add.Bind(self.view.wx.EVT_BUTTON, self.add)
        self.dialog.SetTitle("add new " + self.model.type + " file..." )

    def updateLanguageList(self, itemList):
        self.dialog.langChoice.Clear()
        self.dialog.langChoice.AppendItems(itemList)
        self.dialog.langChoice.Select(0)
        self.dialog.langChoice.Update()

    def showDialog(self):
        self.dialog.Show()

    def close(self, event):
        self.dialog.Close()

    def add(self, event):
        name = self.dialog.textField.GetValue()
        lang = self.dialog.langChoice.GetStringSelection()

        if not name.endswith("_"):
            name += "_"
            self.dialog.textField.SetValue(name)
        if self.model.makerFileExists(name + lang + self.model.type):
            return
        else:
            self.model.createFile(name , lang)
            self.dialog.Destroy()

class NewLangFile:
    def __init__(self, mainView, project, type, content):
        self.content = content
        self.type = type
        self.projectController = project.projectController
        self.project = project

        self.controller = Controller(self, mainView)
        self.controller.drawDialog()
        self.controller.updateLanguageList(project.getProjectLanguages())
        self.controller.showDialog()

    def makerFileExists(self, thePath):
        if os.path.isfile(os.path.join(self.project.getPathParts(), thePath)):
            message  = "%s is an existing file !\n" % thePath
            self.projectController.infoMessage(message)
            return True
        return False

    def createFile(self, name, lang):
        if not name.endswith("_"):
            name += "_"
        if not self.content:
            content = makerFileTemplates.getTemplate(self.type)
        if self.type == ".content":
            # TO DO: convert to use os.path.join()
            pathToHead = self.project.getPathParts()+"../templates/"+ lang +".head" 
            head = readFile(pathToHead)
            pathToNewHead = self.project.getPathParts() + name + lang +".head"
            writeFile(pathToNewHead, head)
            # TO DO: convert to use os.path.join()
            nameInTable = name + lang + ".htm"

            self.project.addToDistributionTable(nameInTable, 
                                        self.project.getDefaultRemoteFolder(self.type), 
                                        "lines", 
                                        nameInTable)
            newFile = self.project.getPathParts() + name + lang + self.type
            writeFile(newFile, content)
        elif self.type == ".dynamic":
            # TO DO: convert to use os.path.join()
            newFile = self.project.getPathParts() + name + lang + self.type
            writeFile(newFile, content)

        group = self.projectController.findTreeItemByText(self.type)
        if not group:
            group = self.projectController.treeViewAddFolder(self.type)
        newItem = self.projectController.treeViewAppendItem(group, name + lang, type=None)
        self.projectController.selectTreeItemAndLoad(newItem)
