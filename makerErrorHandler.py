import makerController
import makerErrorReport
import makerBugReport


class Controller(makerController.SuperController):
    def drawDialog(self):
        self.dialog = makerErrorReport.xrcErrorDialog(self.view)
        self.dialog.Cancel.Bind(self.view.wx.EVT_BUTTON, self.close)
        self.dialog.Report.Bind(self.view.wx.EVT_BUTTON, self.report)

    def write(self, text):
        if not self.dialog:
            self.drawDialog()
        print text
        self.dialog.ErrorText.AppendText(text)
        self.dialog.Show()

    def close(self, event):
        self.dialog.Close()

    def report(self, event):
        makerBugReport.report()

class ErrorHandler:
    def __init__(self, mainView):

        self.controller = Controller(self, mainView)
        self.controller.drawDialog()

    def write(self, text):
        self.controller.write(text)
