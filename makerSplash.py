import wx
import sys
import os.path


class MySplashScreen(wx.SplashScreen):
    """Create a splash screen widget."""

    def __init__(self):
        imageName = os.path.join(os.path.dirname(sys.argv[0]), "./system/Splash.png")
        aBitmap = wx.Image(name=imageName).ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 2000
        splashCallback = None

        wx.SplashScreen.__init__(
            self, aBitmap, splashStyle, splashDuration, splashCallback
        )

        self.Bind(wx.EVT_CLOSE, self.onExit)
        # wx.Yield()

    # ---------------------------------------------------------------------#

    def onExit(self, evt):
        self.Hide()
        evt.Skip()
