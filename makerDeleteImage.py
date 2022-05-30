import os
import sys

class DeleteImg:
    def __init__(self, projectModel, controller):
        self.projectModel = projectModel
        self.controller = controller

    def deleteImage(self):
        file = self.controller.imageDialog(self.projectModel.getPathParts())
        if not file:
            return

        fileparts = os.path.split(file)
        ext = os.path.splitext(fileparts[1])[-1]
        if ext not in self.projectModel.getSupportedImageFormats():
            self.controller.infoMessage("This is NOT an image file!")
            return

        if self.projectModel.checkIfProjectIsSetUp():
            try:
                self.projectModel.serverLogin()
                gfxFolder = self.projectModel.getRemoteGfxFolder()
                result = self.projectModel.deleteRemoteFile(gfxFolder, fileparts[1])
                if result == True:
                    self.projectModel.serverLogout()
                else:
                    m = "Unable to delete remote file!\n"
                    m += "Image not on server?"
                    self.controller.errorMessage(m)
            except Exception, e:
                self.controller.errorMessage("cannot delete image..." + str(e))

            try:
                os.remove(file)
                self.controller.infoMessage("image deleted...")
            except Exception, e:
                self.controller.errorMessage("Cannot delete local image..." + str(e))

        else:
            os.remove(file)
            self.controller.infoMessage("image deleted...")
