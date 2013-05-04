import sys
import wx
import  wx.lib.mixins.listctrl  as  listmix

from makerWidgets import MakerDialog

class DistributionTableEditor(MakerDialog):

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
                              'size'       : wx.Size(754, 616),
                              'style'      : wx.DEFAULT_DIALOG_STYLE, 
                              'title'      : 'Edit the Distribution Table',
                              'clientSize' : wx.Size(746, 582),
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
                                            'size'   : wx.Size(746, 28),
                                            'style'  : wx.TB_HORIZONTAL | wx.NO_BORDER})
        
	# ----- WINDOW -----
        self.window = self.add('window', {'name'   : 'window',
                                          'parent' : self,
                                          'pos'    : wx.Point(0, 545),
                                          'size'   : wx.Size(746, 80),
                                          'style'  : wx.FULL_REPAINT_ON_RESIZE
                                          })
        
                
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


    # ----- Edit Preferences BUTTON -----
        self.defaultFolderButton = self.add('buttonNoHandler', {'label'   : 'default Folders',
                                                'name'    : 'defaultFolders', 
                                                'parent'  : self.window, 
                                                'pos'     : None,
                                                'size'    : None, 
                                                'style'   : 0})


        
        self.createSizers()


    # ------------------------------------------------------------    

    def createSizers(self):
        boxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        boxSizer.AddWindow(self.toolBar, 0, border=0, flag=wx.EXPAND)
        boxSizer.AddWindow(self.listCtrl, 1, border=10, flag=wx.EXPAND)
        boxSizer.AddWindow(self.window, 0, border=0, flag=wx.EXPAND | wx.FIXED_MINSIZE)
        
        #self.window.SetBackgroundColour(wx.BLACK)
        
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.buttonSizer.Add(self.defaultFolderButton, 0, wx.ALIGN_CENTER | wx.WEST, 20)
        self.buttonSizer.AddStretchSpacer(1)
        self.buttonSizer.Add(self.cancelButton, 0, wx.ALIGN_CENTER | wx.EAST, 20)
        self.buttonSizer.Add(self.saveButton, 0, wx.ALIGN_CENTER | wx.EAST, 20)
        
        self.window.SetAutoLayout(True)
        self.window.SetMinSize((0,80))
        
        self.window.SetSizer(self.buttonSizer)
        
        self.SetSizer(boxSizer)
        self.window.Layout()
    # ------------------------------------------------------------    
        
    def onCancelButton(self, event):
        self.saved = False
        self.Close()
        event.Skip()
        
    def onEditFolders(self, event):
        self.parent.controller.actionEditDefaultRemoteFolders()
        event.Skip()
        
        
    # ------------------------------------------------------------    
    
    def onSaveButton(self, event):
        # HACK trigger another select event so the data is checked before we go on
        
        if self.listCtrl.GetFocusedItem() != -1:
            
            self.listCtrl.Select(self.listCtrl.GetFocusedItem(), False)
            self.listCtrl.Select(self.listCtrl.GetFocusedItem(), True)
        # HACK END
        
        def getCorrectMessage():
            if len(self.markedItems) > 1:
                m = "There are " +  str(len(self.markedItems)) 
                m += " conflicts in the table! "  
                m += " Would you like to resolve them ?"
                
            elif len(self.markedItems) == 1:
                m = "There is " +  str(len(self.markedItems)) 
                m += " conflict in the table! " 
                m += " Would you like to resolve it ?"
            
            return m
        
        if len(self.markedItems) != 0:
            answer = self.parent.Ask_YesOrNo(getCorrectMessage())
        
        
            if answer == "Yes":
                if self.listCtrl.GetFocusedItem() != -1:
                    self.listCtrl.Select(self.listCtrl.GetFocusedItem(),False )
                    return
                else:
                    return

        self.data = self.readData()                
        self.saved = True
        self.Close()   
        event.Skip()

    # ------------------------------------------------------------    
        
    def readData(self):
        columns = self.listCtrl.GetColumnCount()
        items = self.listCtrl.GetItemCount()
        dictlist = []
        
        for t in range(items):
            keys = ["ftp_source", "remote_dir", "ftp_mode", "target"]
            new = {}
            for x in range(columns):
                z = self.listCtrl.GetItem(t,x)
                new[keys[x]] = z.GetText()            
            dictlist.append(new)
            
        return dictlist
        
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
        self.listCtrl.InsertColumn(0, "Local File")
        self.listCtrl.InsertColumn(1, "Remote Dir")
        self.listCtrl.InsertColumn(2, "FTP Mode")
        self.listCtrl.InsertColumn(3, "Remote File", wx.LIST_FORMAT_RIGHT)
        
        # flag for zebra tables
        self.value = 0
        
        for key, data in enumerate(theData):
            key += 1 # enumerate starts from 0 so bump this by 1
            localFile  = data['ftp_source']
            remoteDir  = data['remote_dir']
            ftpMode    = data['ftp_mode']
            remoteFile = data['target']
            
            index = self.listCtrl.InsertStringItem(sys.maxint, localFile)
            self.listCtrl.SetStringItem(index, 0, localFile)
            
            self.listCtrl.SetStringItem(index, 1, remoteDir)
            self.listCtrl.SetStringItem(index, 2, ftpMode)
            self.listCtrl.SetStringItem(index, 3, remoteFile)
            self.listCtrl.SetItemData(index, key)
            
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
          
        self.listCtrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.listCtrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.listCtrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        self.listCtrl.SetColumnWidth(3, wx.LIST_AUTOSIZE)

        #self.currentItem = 0

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
           
    
            
    
        