import os
import sys
import wx
import shutil
import makerController

from makerWidgets import MakerDialog

class ImageGUI(MakerDialog):
    def __init__(self, parentView):
        self.createDialog(parentView)
        self.keepRatio.SetValue(True)
    def createDialog(self, prnt):
        MakerDialog.__init__(self,
                             {'name'       : '',
                              'parent'     : prnt,
                              'pos'        : wx.Point(259, 72),
                              'size'       : wx.Size(505, 590),
                              'style'      : wx.DEFAULT_DIALOG_STYLE,
                              'title'      : 'Image Tool',
                              'clientSize' : wx.Size(497, 556),
                              'centerPos'  : wx.BOTH})

        self.staticBitmap1 = self.add('staticBitmap',
                                      {'bitmap' : wx.NullBitmap,
                                       'name'   : 'staticBitmap1', 
                                       'parent' : self,
                                       'pos'    : wx.Point(16, 16),
                                       'size'   : wx.Size(400, 320), 
                                       'style'  : wx.BORDER_NONE})

        self.res_x = self.add('textCtrl',
                              {'name'   : 'res_x',
                               'parent' : self,
                               'pos'    : wx.Point(16, 475),
                               'size'   : wx.Size(56, 25),
                               'style'  : 0,
                               'value'  : '-'
                               })

        self.res_y = self.add('textCtrl',
                              {'name'   : 'res_y',
                               'parent' : self,
                               'pos'    : wx.Point(82, 475),
                               'size'   : wx.Size(48, 25),
                               'style'  : 0,
                               'value'  : '-'
                               })

        self.staticText1 = self.add('staticText',
                                    {'label'  : 'Width',
                                     'name'   : 'staticText1',
                                     'parent' : self,
                                     'pos'    : wx.Point(18, 445),
                                     'size'   : wx.Size(16, 25),
                                     'style'  : 0})        
        self.staticText2 = self.add('staticText',
                                    {'label'  : 'Height',
                                     'name'   : 'staticText2',
                                     'parent' : self,
                                     'pos'    : wx.Point(78, 445),
                                     'size'   : wx.Size(8, 25),
                                     'style'  : 0})        
        self.warning = self.add('staticText',
                                    {'label'  : '',
                                     'name'   : 'warning',
                                     'parent' : self,
                                     'pos'    : wx.Point(145, 445),
                                     'size'   : wx.Size(128, 25),
                                     'style'  : 0})   
        self.warning.SetForegroundColour(wx.RED)
        self.keepRatio = wx.CheckBox(self, 
                                     -1, 
                                     "Keep Proportions", 
                                     pos=wx.Point(16, 415),
                                     size=wx.Size(180, 25), 
                                     style=0)        
        self.buttonImport = self.add('buttonNoHandler', 
                                     {'label'   : 'Import',
                                      'name'    : 'buttonscale',
                                      'parent'  : self,
                                      'pos'     : wx.Point(380, 463),
                                      'size'    : wx.Size(80, 40),
                                      'style'   : 0})
        self.cancel_button = self.add('buttonNoHandler',
                                      {'label'   : 'Cancel',
                                       'name'    : 'cancel_button',
                                       'parent'  : self,
                                       'pos'     : wx.Point(290, 463),
                                       'size'    : wx.Size(80, 40),
                                       'style'   : 0})
        self.new_name = self.add('textCtrl',
                                 {'name'   : 'new_name',
                                  'parent' : self,
                                  'pos'    : wx.Point(145, 475),
                                  'size'   : wx.Size(135, 25),
                                  'style'  : 0,
                                  'value'  : 'newName'
                                  })

class Controller(makerController.SuperController):
    def bindActions(self):
        """
        Binds events to the textfields where the x / y value
        for scaling is entered. If a value is entered in each 
        of the fields the other one is automatically updated 
        with the new information.        
        """
        self.view.res_x.Bind(wx.EVT_SET_FOCUS,  self.bindX)
        self.view.res_y.Bind(wx.EVT_SET_FOCUS,  self.bindY)        
        self.view.res_x.Bind(wx.EVT_KILL_FOCUS, self.unbindX)
        self.view.res_y.Bind(wx.EVT_KILL_FOCUS, self.unbindY)
        self.view.cancel_button.Bind(wx.EVT_BUTTON, 
                       self.onCancelButton)
        self.view.buttonImport.Bind(wx.EVT_BUTTON, 
                       self.onImportButton)
        self.view.new_name.Bind(wx.EVT_TEXT, self.checkNewName)
        self.view.Show()
   
    def checkNewName(self, event):
        if self.model.doesImageFileExist(self.getImageName()):
            self.view.warning.SetLabel("Filename exists")
            self.view.buttonImport.Disable()
        else:
            if not self.view.buttonImport.IsEnabled():
                self.view.buttonImport.Enable()
            self.view.warning.SetLabel("")
   
    def checkNewFormat(self):
        if self.getImageFormat() not in self.model.projectModel.supportedImages:
            self.view.warning.SetLabel("Unsupported Format")
            self.view.buttonImport.Disable()
            return False
        else:
            if not self.view.buttonImport.IsEnabled():
                self.view.buttonImport.Enable()
            self.view.warning.SetLabel("")
            return True
   
    def calcX(self, y):
        ratio = self.model.getRatio()
        if ratio[1] == 'x':
            y = float(y) * ratio[0]
            y = int(y) 
        else:
            y = float(y) / ratio[0]
            y = int(y) 
        self.set_x(y)
    
    def calcY(self,x):
        ratio = self.model.getRatio()
        if ratio[1]=="x":
            x = float(x) / ratio[0]
            x = int(x) 
        else:
            x = float(x) * ratio[0]
            x = int(x) 
        self.set_y(x)
   
    def onEnteredY(self, event):
        if self.view.keepRatio.GetValue():            
            try:
                self.calcX(self.view.res_y.GetValue())
                self.view.warning.SetLabel("")
                if not self.view.buttonImport.IsEnabled():
                    self.view.buttonImport.Enable()
            except Exception, e:
                self.view.warning.SetLabel("invalid " + "Y" + " value")
                self.view.buttonImport.Disable()

    def onEnteredX(self, event):
        if self.view.keepRatio.GetValue():
            try:
                self.calcY(self.view.res_x.GetValue())
                self.view.warning.SetLabel("")
                if not self.view.buttonImport.IsEnabled():
                    self.view.buttonImport.Enable()
            except Exception, e:
                self.view.warning.SetLabel("invalid " + "X" + " value")
                self.view.buttonImport.Disable()

    def bindX(self, event):
        """
        Binds self.onEnteredX to res_x
        wx.EVT_TEXT
        """
        self.view.res_x.Bind(wx.EVT_TEXT, self.onEnteredX)
    
    def unbindX(self, event):
        """Unbinds the event."""
        self.view.res_x.Unbind(wx.EVT_TEXT)
    
    def bindY(self, event):
        """
        Binds self.onEnteredX to res_y
        wx.EVT_TEXT
        """
        self.view.res_y.Bind(wx.EVT_TEXT, self.onEnteredY)
        
    def unbindY(self, event):
        """Unbinds the event."""
        self.view.res_y.Unbind(wx.EVT_TEXT)

    def bindRatio(self):
       pass

    def Reset(self, event):
        self.controller.imageActionResetSize()
    
    def set_x(self, theValue):
        self.view.res_x.SetValue(str(theValue))
        
    def get_x(self):
        return self.view.res_x.GetValue()
    
    def set_y(self, theValue):
        self.view.res_y.SetValue(str(theValue))
    
    def get_y(self):
        return self.view.res_y.GetValue()

    def setImageName(self, name):
        self.view.new_name.SetValue(name)    

    def getImageName(self):
        return self.view.new_name.GetValue()
    
    def getImageFormat(self):
        """ getr the new image format out of the dialog"""
        s = self.view.new_name.GetValue()
        format = os.path.splitext(s)[-1]
        return format
        
    def setPreviewBitmap(self, image):
        x = image.GetWidth()
        y = image.GetHeight()
        self.view.staticBitmap1.SetBitmap(image)
        xPos = (self.view.GetSize()[0] - x) / 2 
        self.view.staticBitmap1.SetPosition(wx.Point(xPos, 16))
        self.view.Refresh()
                
    def onImportButton(self, event):
        if self.checkNewFormat():
            event.Skip()
            self.model.scaleImage(self.getImageName(), (int(self.get_x()), int(self.get_y())) )
        
    def onCancelButton(self, event):
        self.view.Close()
        event.Skip()

    def destroyView(self):
        self.view.Destroy()

    def disableScaling(self):
        """ quick fix for gifs """
        self.view.res_x.Enable(False)
        self.view.res_y.Enable(False)

class MakerImageImporter:
    def __init__(self, projectModel, mainView):
        imageView = ImageGUI(mainView)
        self.projectModel = projectModel
        self.existingImages = self.projectModel.getImageFiles()
        self.projectController = self.projectModel.projectController
        imageFile = self.projectController.fileDialog()
        if not imageFile: return
        imgExt = os.path.splitext(imageFile[0])[-1]
        if imgExt not in self.projectModel.supportedImages:
            self.projectController.errorMessage("This is not an image file...")
            return

        self.original = imageFile[0]
        self.setInputFile(imageFile[0])
        self.setOutputFile(None)
        self.imageController = Controller(self, imageView)
        self.imageController.setPreviewBitmap(self.getPreview())

    if imgExt.lower() == ".gif":
        self.imageController.disableScaling()

    def getOriginal(self):
        """Return path to original image."""
        return self.original
    
    def getOutputFile(self):
        return self.outputFile
    
    def setOutputFile(self, aFile):
        self.outputFile = aFile
    
    def getSupportedFormats(self):
        convert = {".png"  : wx.BITMAP_TYPE_PNG,
                   ".jpg"  : wx.BITMAP_TYPE_JPEG,
                   ".jpeg" : wx.BITMAP_TYPE_JPEG,
                   ".tif"  : wx.BITMAP_TYPE_TIF,
                   ".tiff" : wx.BITMAP_TYPE_TIF,
                   ".gif"  : wx.BITMAP_TYPE_GIF,
                   ".pnm"  : wx.BITMAP_TYPE_PNM,
                   ".pcx"  : wx.BITMAP_TYPE_PCX,
                   ".ico"  : wx.BITMAP_TYPE_ICO,
                   ".cur"  : wx.BITMAP_TYPE_CUR,
                   ".ani"  : wx.BITMAP_TYPE_ANI,
                   ".xpm"  : wx.BITMAP_TYPE_XPM}

        for key,val in convert.items():
            convert[key.upper()] = val

        return convert
    
    def getOriginalFormat(self):
        orgFile = self.getInputFile()
        return (os.path.splitext(orgFile))[-1]
        
    def getInputFile(self):
        return (os.path.split(self.inputFile))[-1]
    
    def setInputFile(self, aFile):
        self.inputFile = aFile
    
    def getPreview(self):
        """Returns a wx.Bitmap"""
        x = self.getSize()[0]
        y = self.getSize()[-1]

        self.imageController.set_x(x)
        self.imageController.set_y(y)
        self.imageController.setImageName(self.getInputFile())
        if x >= 400 or y >= 400: 
            ratio = self.getRatio()
            if ratio[-1]=="x":
                x = 400
                y = int(x / ratio[0])
            else:
                y = 400
                x = int(y / ratio[0])
        pic   = wx.Image(self.inputFile, wx.BITMAP_TYPE_ANY).Scale(x, y)
        return wx.BitmapFromImage(pic, -1)
    
    def getRatio(self):
        size = self.getSize()
        if size[0] > size[1]:
            # return ratio and bigger side
            return float(size[0]) / float(size[1]), "x" 
        else:
            return float(size[1]) / float(size[0]), "y"
    
    def getSize(self):
        """Returns the size of the original image (x,y)."""
        pic = wx.Image(self.inputFile, wx.BITMAP_TYPE_ANY)
        return pic.GetSize()
    
    def doesImageFileExist(self, Name):
        if Name in self.existingImages:
            return True
        else:
            return False
    
    def scaleImage(self, newName, resolution):
        """
        if the resolution has not changed then the image is
        NOT scaled and the original is stored in parts/
        resolution being (x,y)
        """
        self.setOutputFile(newName)
        input_file  = self.inputFile
        output_file = self.getOutputFile()
        if input_file != output_file:
            originalSize = self.getSize()
            if resolution == originalSize:
                format = (os.path.splitext(output_file))[-1]
                if format == self.getOriginalFormat():
                    # format and size are the same the image does not need to be
                    # converted
                    shutil.copyfile(self.inputFile , self.projectModel.getPathParts() + output_file)
                    self.imageController.destroyView()                  
                # format is not the same but the size is
                else:
                    # convert            
                    pic = wx.Image(self.inputFile, wx.BITMAP_TYPE_ANY)
                    supported = self.getSupportedFormats()
                    try:
                        path = self.projectModel.getPathParts() + output_file
                        pic.SaveFile(path, supported[format])
                        self.imageController.destroyView() 
                    except Exception, e:
                            m = "either %s image format is not supported or \n" % str(format)
                            m += str(e)
                            sys.stderr.write(m)

            # resolution is not the same
            else:                
                # the image will be scaled and eventually 
                # be converted into the right format                
                theImage = wx.Image(self.inputFile, wx.BITMAP_TYPE_ANY)
                pic = theImage.Scale(resolution[0], 
                                     resolution[1], 
                                     wx.IMAGE_QUALITY_HIGH) 
                path = self.projectModel.getPathParts() + output_file       
                format = (os.path.splitext(path))[-1]
                convert = self.getSupportedFormats()
                try:
                    pic.SaveFile(path,convert[format])
                    self.imageController.destroyView() 
                except Exception, e:
                    sys.stderr.write(str(e))
