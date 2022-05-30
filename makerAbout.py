import wx
import os
import os.path
import sys

from makerWidgets import MakerDialog

def create(parent):
    return MakerAbout(parent)

class MakerAbout(MakerDialog):

    def __init__(self, parent, versionNr):
        self.version = versionNr
        self.createDialog(parent)

    def createDialog(self, prnt):
        MakerDialog.__init__(self,
                {'name'       : '',
                    'parent'     : prnt, 
                    'pos'        : wx.Point(490, 398), 
                    'size'       : wx.Size(647, 318),
                    'style'      : wx.DEFAULT_DIALOG_STYLE, 
                    'title'      : 'About',
                    'clientSize' : wx.Size(639, 284),
                    'centerPos'  : wx.BOTH})

        self.OKbutton = self.add('button', {'label'   : 'OK',
            'name'    : 'okButton', 
            'parent'  : self, 
            'pos'     : None,
            'size'    : None, 
            'style'   : 0,
            'handler' : self.onOKButton})

        iName = os.path.join(os.path.dirname(sys.argv[0]), 'system/Splash.png')
        theBitMap = wx.Bitmap(iName, wx.BITMAP_TYPE_PNG)
        self.staticBitmap1 = wx.StaticBitmap(self,
                id=wx.NewId(),
                bitmap=theBitMap,
                pos=wx.Point(0, 0),
                size=wx.Size(641, 246), 
                style=0,
                name='staticBitmap1')

        self.staticText1 = self.add('staticText',
                {'label'  : 'Version number',
                    'name'   : 'staticText1',
                    'parent' : self,
                    'pos'    : wx.Point(10, 250),
                    'size'   : wx.Size(184, 13),
                    'style'  : 0})

        self.staticText1.SetLabel(u'Version: %s' % str(self.version))
        buttonSize = self.OKbutton.GetSizeTuple()
        winSize = self.GetSizeTuple()

        difference = winSize[0] - buttonSize[0]

        self.OKbutton.SetPosition(wx.Point(difference - 10, 245))

    def onOKButton(self, event):
        self.Close()
        event.Skip()
