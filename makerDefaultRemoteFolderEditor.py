import sys
import wx
import  wx.lib.mixins.listctrl  as  listmix
import wx.lib.colourdb

from makerWidgets import MakerDialog

class DefRemFolderEditor(MakerDialog):

    def __init__(self, parent, theData):        
        self.createDialog(parent)        
        self.data  = theData
        self.populate(theData)
        self.saved = None

    # ------------------------------------------------------------    

    def createDialog(self, prnt):
	MakerDialog.__init__(self,
                             {'name'       : 'Edit',
                              'parent'     : prnt, 
                              'pos'        : wx.Point(437, 249), 
                              'size'       : wx.Size(400, 520),
                              'style'      : wx.DEFAULT_DIALOG_STYLE, 
                              'title'      : 'default remote folders',
                              'clientSize' : wx.Size(400, 520),
                              'centerPos'  : wx.BOTH})

        # please don't use any sorting styles like wx.LC_SORT_ASCENDING
        # because of zebra table hack
        styleValue = wx.LC_REPORT | wx.BORDER_NONE 
        self.listCtrl = DistListCtrl(self, -1, style=styleValue)
        self.parent = prnt

	# ----- TOOLBAR -----
        self.toolBar = self.add('toolbar', {'name'   : 'toolBar',
                                            'parent' : self, 
                                            'pos'    : wx.Point(0, 0), 
                                            'size'   : wx.Size(400, 28),
                                            'style'  : wx.TB_HORIZONTAL | wx.NO_BORDER})
        
	# ----- WINDOW -----
        self.window = self.add('window', {'name'   : 'window',
                                          'parent' : self,
                                          'pos'    : wx.Point(0, 545),
                                          'size'   : wx.Size(400, 80),
                                          'style'  : wx.FULL_REPAINT_ON_RESIZE})
        
	# ----- SAVE SYSTEM SETUP BUTTON -----
        self.saveButton = self.add('button', {'label'   : 'OK',
                                              'name'    : 'saveSystemSetup', 
                                              'parent'  : self.window, 
                                              'pos'     : None,
                                              'size'    : None, 
                                              'style'   : 0,
                                              'handler' : self.onSaveButton})

	# ----- CANCEL SYSTEM SETUP BUTTON -----
        self.cancelButton = self.add('button', {'label'   : 'Cancel',
                                                'name'    : 'cancelSystemSetup', 
                                                'parent'  : self.window, 
                                                'pos'     : None,
                                                'size'    : None, 
                                                'style'   : 0,
                                                'handler' : self.onCancelButton})


    
        self.createSizers()
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,self.validateColumn)

    # ------------------------------------------------------------    

    def validateColumn(self, evt):
        """
        make sure only the default folder column is editable
        """
        if evt.GetColumn() == 0:
            evt.Veto()
            
                    
    def createSizers(self):
        
        self.window.SetAutoLayout(True)
               
        boxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        boxSizer.AddWindow(self.toolBar, 0, border=0, flag=wx.EXPAND)
        boxSizer.AddWindow(self.listCtrl, 1, border=0, flag=wx.EXPAND | wx.FIXED_MINSIZE)
        boxSizer.AddWindow(self.window, 0, border=0, flag= wx.EXPAND | wx.FIXED_MINSIZE)
               
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
                      
        self.buttonSizer.AddStretchSpacer(1)
        self.buttonSizer.Add(self.cancelButton, 0, wx.ALIGN_CENTER | wx.EAST, 20)
        self.buttonSizer.Add(self.saveButton, 0, wx.ALIGN_CENTER | wx.EAST, 20)
                
        self.window.SetSizer(self.buttonSizer)
                
        self.SetSizer(boxSizer)
        self.window.Layout()
        

    # ------------------------------------------------------------    
        
    def onCancelButton(self, event):
        self.saved = False
        self.Close()
        event.Skip()
        
   
        
        
    # ------------------------------------------------------------    
    
    def onSaveButton(self, event):
#        # HACK trigger another select event so the data is checked before we go on
#        
#        if self.listCtrl.GetFocusedItem() != -1:
#            self.listCtrl.Select(self.listCtrl.GetFocusedItem(), False)
#            self.listCtrl.Select(self.listCtrl.GetFocusedItem(), True)
#        # HACK END
#        
#        def getCorrectMessage():
#            if len(self.markedItems) > 1:
#                m = "There are " +  str(len(self.markedItems)) 
#                m += " conflicts in the table! "  
#                m += " Would you like to resolve them ?"
#                
#            elif len(self.markedItems) == 1:
#                m = "There is " +  str(len(self.markedItems)) 
#                m += " conflict in the table! " 
#                m += " Would you like to resolve it ?"
#            
#            return m
#        
#        if len(self.markedItems) != 0:
#            answer = self.parent.Ask_YesOrNo(getCorrectMessage())
#        
#        
#            if answer == "Yes":
#                if self.listCtrl.GetFocusedItem() != -1:
#                    self.listCtrl.Select(self.listCtrl.GetFocusedItem(),False )
#                    return
#                else:
#                    return

        self.data = self.readData()                
        self.saved = True
        self.Close()   
        event.Skip()

    # ------------------------------------------------------------    
        
    def readData(self):
        columns = self.listCtrl.GetColumnCount()
        items = self.listCtrl.GetItemCount()
        dict = {}
        
        for item in range(items):
            type = self.listCtrl.GetItem(item , 0)
            folder = self.listCtrl.GetItem(item , 1)
            dict[str(type.GetText())] = str(folder.GetText())
            
        return dict
        
    # ------------------------------------------------------------            
    # tool for zebra tables
    def swap(self):
        if self.value == 1:
            self.value = 0
            return 0
        else:
            self.value = 1
            return self.value
        
        
    
    def populate(self, theData , ):
        # for normal, simple columns, you can add them like this:
        self.listCtrl.InsertColumn(0, "Filetype")
        self.listCtrl.InsertColumn(1, "Default Folder")
        #self.listCtrl.InsertColumn(2, "FTP Mode")
        #self.listCtrl.InsertColumn(3, "Remote File", wx.LIST_FORMAT_RIGHT)
        #print theData
        #print "---------------------------"
        self.value = 0
        for key in theData.iterkeys():
            
            fileType = key
            defaultFolder  = theData[key]
            #print key, theData[key]
            index = self.listCtrl.InsertStringItem(sys.maxint, fileType)
            self.listCtrl.SetStringItem(index, 0, fileType)
            self.listCtrl.SetStringItem(index , 1, defaultFolder)
            # Zebra Tables
            #
            # make any other line blue
            #
            # I know this is not very elegant but I thought since wxPython
            # might support zebra tables natively at some point we could just 
            # remove those lines instead of going through the trouble of overriding
            # all relevant "insert" methods in wx.ListCtrl
            if self.value == 1:
                self.listCtrl.SetItemBackgroundColour(index, wx.Colour(240, 246 ,254))
            self.swap()
            #----------------------
                
        self.listCtrl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.listCtrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        
# ------------------------------------------------------------            
# ------------------------------------------------------------            
# ------------------------------------------------------------            

class DistListCtrl(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.TextEditMixin):

     
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)
        # A list of items with conflicts
        self.markedItems = []
       
    def SetStringItem(self, index, col, data):
        if col in range(4):
            wx.ListCtrl.SetStringItem(self, index, col, data)
        else:
            try:
                datalen = int(data)
            except:
                return

            wx.ListCtrl.SetStringItem(self, index, col, data)
           
    
            
    
        