import wx
import wx.stc

# ================================================================
# ===== Widgets r us
# ================================================================

def toolBar(dict):
    return wx.ToolBar(
        id=wx.NewId(),
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def choice(dict):
    return wx.Choice(
        choices=dict["choices"],
        id=wx.NewId(),
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def button(dict):
    theID = wx.NewId()
    theButton = wx.Button(
        id=theID,
        label=dict["label"],
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

    theButton.Bind(wx.EVT_BUTTON, dict["handler"], id=theID)

    return theButton

def buttonNoHandler(dict):
    theID = wx.NewId()
    return wx.Button(
        id=theID,
        label=dict["label"],
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def listBox(dict):
    theID = wx.NewId()
    listBox = wx.ListBox(
        choices=dict["choices"],
        id=theID,
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )
    listBox.Bind(wx.EVT_LISTBOX_DCLICK, dict["handler"], id=theID)
    return listBox

def staticLine(dict):
    return wx.StaticLine(
        id=wx.NewId(),
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def staticText(dict):
    return wx.StaticText(
        id=wx.NewId(),
        label=dict["label"],
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def staticBitmap(dict):
    return wx.StaticBitmap(
        bitmap=dict["bitmap"],
        id=wx.NewId(),
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def window(dict):
    return wx.Window(
        id=wx.NewId(),
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def panel(dict):
    return wx.Panel(
        id=wx.NewId(),
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

def textCtrl(dict):
    return wx.TextCtrl(
        id=wx.NewId(),
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
        value=dict["value"],
    )

def styledTextCtrl(dict):
    idValue = -1
    if dict["hasID"]:
        idValue = wx.NewId()

    sCtrl = wx.stc.StyledTextCtrl(
        id=idValue,
        name=dict["name"],
        parent=dict["parent"],
        pos=dict["pos"],
        size=dict["size"],
        style=dict["style"],
    )

    for evt, evtHandler in dict["handlers"].items():
        sCtrl.Bind(evt, evtHandler)

    return sCtrl

# ================================================================
# ================================================================
# ================================================================


def widgetFactory():
    # All known widgets
    return {
        "button": button,
        "buttonNoHandler": buttonNoHandler,
        "toolbar": toolBar,
        "window": window,
        "listbox": listBox,
        "panel": panel,
        "choice": choice,
        "textCtrl": textCtrl,
        "staticLine": staticLine,
        "staticText": staticText,
        "staticBitmap": staticBitmap,
        "styledTextCtrl": styledTextCtrl,
    }


# Decorator
def checkWidgetExists(func):
    def wrapper(self, widgetName, widgetDict):
        try:
            return func(self, widgetName, widgetDict)
        except Exception, e:
            print e
            print "Widget %s does not exist!" % widgetName
            print "Known widgets: %s" % str(widgetFactory().keys())
            return None

    return wrapper


# ================================================================
# ================================================================
# ================================================================


class MakerDialog(wx.Dialog):
    """Base class that serves as a useful method holder for child dialogs."""

    def __init__(self, dict):
        wx.Dialog.__init__(
            self,
            id=wx.NewId(),
            name=dict["name"],
            parent=dict["parent"],
            pos=dict["pos"],
            size=dict["size"],
            style=dict["style"],
            title=dict["title"],
        )
        self.SetClientSize(dict["clientSize"])
        self.Center(dict["centerPos"])

    @checkWidgetExists
    def add(self, widgetName, widgetDict):
        return widgetFactory()[widgetName](widgetDict)
