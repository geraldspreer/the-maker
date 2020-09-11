import makerController
import makerManageLinkedProjDialog
import shutil
import os.path


class Controller(makerController.SuperController):
    def drawDialog(self):

        self.conversionInfoShown = False
        self.forceRestart = None

        self.dialog = makerManageLinkedProjDialog.xrcManageLinked(self.view)

        self.dialog.Cancel.Bind(self.view.wx.EVT_BUTTON, self.cancel)
        #
        self.dialog.Unlink.Bind(self.view.wx.EVT_BUTTON, self.unlink)

        self.dialog.Bind(self.view.wx.EVT_CLOSE, self.close)

        for item in self.model.getManagedProjectsList():

            self.dialog.theList.Append(item)

        self.pathList = []
        try:
            # there might be no projects
            self.dialog.theList.SetSelection(0)

        except:
            pass

        self.dialog.Show()

    def cancel(self, event):
        # close without doing stuff
        print "cancel button"
        self.close(None)

    def unlink(self, event):

        path = self.dialog.theList.GetStringSelection()

        if path != "":

            if "Containers/com.barnhouse.maker" in path:
                self.forceRestart = True
                m = "This project has been created with a previous version of TheMaker.\n\n"
                m += "If you would like to use this project in the future, you will need to store it "
                m += "in a different location. \n\n"
                m += "Please click OK to choose a folder for your project...\n"
                if self.conversionInfoShown == False:
                    self.warningMessage(m)

                target = self.dirDialog("Where would you like to store your project?")

                if target:
                    fullTarget = os.path.join(target, os.path.split(path)[-1])

                    if not os.path.isdir(fullTarget):
                        shutil.move(path, target)
                    else:
                        self.errorMessage(
                            fullTarget + " already exists. Please try again..."
                        )
                        self.conversionInfoShown = True
                        return
            self.dialog.theList.Delete(self.dialog.theList.GetSelection())
            self.pathList.append(path)

    def close(self, event=None):
        m1 = "TheMaker needs to restart for the changes to take effect."

        if self.forceRestart:
            self.infoMessage(m1)
            self.model.unlink(self.pathList)

        elif self.pathList != []:
            if self.askYesOrNo(m1 + " Would you like to do that?") == "Yes":
                self.model.unlink(self.pathList)

        self.dialog.Destroy()


class Manager:
    def __init__(self, mainView, projectManager):

        self.projectManager = projectManager

        self.controller = Controller(self, mainView)
        self.controller.drawDialog()

    def unlink(self, pathsToUnlink):

        for path in pathsToUnlink:
            self.projectManager.linkedProjectPaths.remove(path)

        self.controller.view.application.restart = True

        if self.controller.forceRestart == True:

            self.projectManager.exitApplicationForced()
        else:
            self.projectManager.closeOpenProjects()

    def getManagedProjectsList(self):
        return self.projectManager.linkedProjectPaths
