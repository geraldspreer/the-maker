import os
import sys
import wx
import shutil
import makerController
from makerUtilities import readFile, writeFile
from makerWidgets import MakerDialog


class RenameDialog(MakerDialog):

    # view class

    def __init__(self, parentView):

        self.createDialog(parentView)

    def createDialog(self, prnt):
        MakerDialog.__init__(
            self,
            {
                "name": "",
                "parent": prnt,
                "pos": wx.Point(259, 72),
                "size": wx.Size(400, 180),
                "style": wx.DEFAULT_DIALOG_STYLE,
                "title": "Rename File",
                "clientSize": wx.Size(400, 120),
                "centerPos": wx.BOTH,
            },
        )

        self.warning = self.add(
            "staticText",
            {
                "label": "",
                "name": "warning",
                "parent": self,
                "pos": wx.Point(20, 18),
                "size": wx.Size(128, 25),
                "style": 0,
            },
        )

        # make warning label RED
        self.warning.SetForegroundColour(wx.RED)

        self.Ok = self.add(
            "buttonNoHandler",
            {
                "label": "Rename",
                "name": "rename",
                "parent": self,
                "pos": wx.Point(300, 48),
                "size": wx.Size(80, 25),
                "style": 0,
            },
        )

        self.newName = self.add(
            "textCtrl",
            {
                "name": "new_name",
                "parent": self,
                "pos": wx.Point(20, 48),
                "size": wx.Size(250, 25),
                "style": 0,
                "value": "newName",
            },
        )

    # ------------------------------------------------------------


class Controller(makerController.SuperController):
    def bindActions(self):

        self.view.Ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.view.newName.Bind(wx.EVT_TEXT, self.checkNewName)

        self.view.Show()

    def checkNewName(self, event):
        if not self.view.Ok.IsEnabled():
            self.view.Ok.Enable()
            self.view.warning.SetLabel("")

    def setNewName(self, name):
        self.view.newName.SetValue(name)

    def getNewName(self):
        return self.view.newName.GetValue()

    def onOk(self, event):

        langTypes = [".content", ".dynamic"]

        if self.model.fileModel.getType() in langTypes:
            if not self.getNewName().endswith("_" + self.model.fileModel.getLanguage()):
                self.view.newName.AppendText("_" + self.model.fileModel.getLanguage())

        oldFilename = self.model.fileModel.getRealName()
        newName = self.getNewName()

        nName = os.path.join(
            self.model.fileModel.core.getPathParts(),
            newName + self.model.fileModel.getType(),
        )

        # fName = os.path.join(self.model.getFullName())

        if os.path.isfile(nName):
            self.view.warning.SetLabel("Filename exists")
            self.view.Ok.Disable()
            return

        else:

            self.model.rename()

            self.model.fileController.view.tree.SetItemText(
                self.model.fileController.getReferringTreeItem(), newName
            )

            newName = self.model.fileModel.getFileName()

            page = self.model.fileController.noteBook.GetSelection()
            pageText = self.model.fileController.noteBook.GetPageText(page)

            if not self.model.fileModel.getSaved():
                newName += "*"
            self.model.fileController.noteBook.SetPageText(
                self.model.fileController.noteBook.GetSelection(), newName
            )
            self.view.Destroy()

    def destroyView(self):
        self.view.DestroyChildren()
        self.view.Destroy()


class MakerFileRename:
    def __init__(self, fileModel, mainView):

        nameView = RenameDialog(mainView)
        self.fileModel = fileModel

        self.fileController = self.fileModel.fileController
        self.controller = Controller(self, nameView)
        self.controller.setNewName(self.fileModel.getName())

    def rename(self):

        oldFilename = self.fileModel.getFileName()
        oldRealName = self.fileModel.getRealName()
        newName = self.controller.getNewName()

        nName = os.path.join(
            self.fileModel.core.getPathParts(), newName + self.fileModel.getType()
        )

        fName = os.path.join(self.fileModel.core.getPathParts(), oldFilename)

        if self.fileModel.getType() == ".content":
            # print fName
            os.rename(fName, nName)
            os.rename(
                os.path.join(
                    self.fileModel.core.getPathParts(),
                    self.fileModel.getName() + ".head",
                ),
                os.path.join(self.fileModel.core.getPathParts(), newName + ".head"),
            )

            # remove old htm file
            fileName = self.fileModel.getFullName()

            if os.path.isfile(fileName):
                os.remove(fileName)

        elif self.fileModel.getType() == ".dynamic":
            # print fName
            os.rename(fName, nName)

        else:
            # print fName
            os.rename(fName, nName)

        self.fileModel.setName(newName)

        distContent = readFile(self.fileModel.core.getDistributionTableFilename())

        if self.fileModel.getType() == ".content":
            newDist = distContent.replace(oldRealName, newName + ".htm")

        else:

            newDist = distContent.replace(
                oldFilename, newName + self.fileModel.getType()
            )

        writeFile(self.fileModel.core.getDistributionTableFilename(), newDist)

        if self.fileModel.getType() == ".content":

            quotes = ["'", '"']

            for q in quotes:

                this = q + oldRealName + q
                that = q + newName + ".htm" + q
                self.fileModel.core.replaceStringInAllItems(this, that)

        else:
            quotes = ["'", '"']

            for q in quotes:

                this = q + oldFilename + q
                that = q + newName + self.fileModel.getType() + q
                # Brinick: why is this done twice?
                # Gerald once for single , once for double quotes
                self.fileModel.core.replaceStringInAllItems(this, that)

        # update in ftp queue
        self.fileModel.core.renameItemInFtpQueue(
            oldFilename, newName + self.fileModel.getType()
        )
