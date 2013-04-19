# -*- coding: latin-1 -*-


import os
import sys
import shutil
import string

#import wx
#import wx.stc
import makerEditorWxView
import makerCopyright
import wx.lib.buttons
import wx.gizmos
import wx.lib.imagebrowser as ib
from wx.lib.anchors import LayoutAnchors
import wx.lib.flatnotebook as nb
import wx.py as pyShell

def create(app):
    
    return wxPythonGUI(app)

class wxPythonGUI(wx.Frame):

    def _init_coll_boxSizer1_Items(self, parent):
        
        
        #this is actually a wxWindow

        parent.Add(self.topPanel, 0, border=0, flag=wx.FIXED_MINSIZE | wx.EXPAND)
       
        parent.Add(self.splitter, 1, border=0, flag=wx.EXPAND | wx.GROW)
      

    def _init_coll_boxSizer2_Items(self, parent):
        

        pass
        #parent.Add(self.notebook1, 0, border=0, flag=wx.EXPAND)
        #parent.Add(self.styledTextCtrl1, 1, border=0, flag=wx.EXPAND)
        


#this is some menu items
       

    def _init_coll_code_Items(self, parent):
        
        self.MenuItemHTML = parent.AppendMenu(help='(X)HTML Tags',
                           id=-1,
                           submenu = self.subMenuHTML, 
                           text=u'HTML'
                           )
        
        
        parent.AppendSeparator()
        
        self.MenuItemCSS = parent.AppendMenu(help='CSS',
                           id=-1,
                           submenu = self.subMenuCSS, 
                           text=u'CSS'
                           )
        
        
        
        parent.AppendSeparator()
        
        self.MenuItemMarkers = parent.AppendMenu(help='insert a marker',
                           id=-1,
                           submenu = self.SubMenuMarkers, 
                           text=u'Markers'
                           )
        
        parent.AppendSeparator()
        
        self.MenuItemMarkdown = parent.Append(help='Markdown !',
                           id=-1,
                           kind=wx.ITEM_NORMAL, 
                           text=u'Markdown\tCtrl+Shift+m'
                           )
           
        

    def _init_coll_ftp_Items(self, parent):
        

        self.MenuItemEditDist = parent.Append(help='edit the distribution table',
                                              id=-1,
                                              kind=wx.ITEM_NORMAL,
                                              text=u'Edit Distribution Table'
                                              )
        
        parent.AppendSeparator()
        
        self.MenuItemPublish = parent.Append(help='',
                                                 id=-1,
                                                 kind=wx.ITEM_NORMAL,
                                                 text=u'Publish'
                                                 )


        self.MenuItemFullUpload = parent.Append(help='upload everything',
                                                 id=-1,
                                                 kind=wx.ITEM_NORMAL,
                                                 text=u'Upload Everything'
                                                 )






        self.MenuItemBrowseFtp = parent.Append(help='',
                                               id=-1,
                                               kind=wx.ITEM_NORMAL,
                                               text=u'Browse Server'
                                               )
        parent.AppendSeparator() 
        
        self.MenuItemSetupFTP = parent.Append(help='setup your project',
                                                id=-1,
                                                kind=wx.ITEM_NORMAL,
                                                text=u'Setup FTP Connection'
                                                )
        
        
        
               
        self.Bind(wx.EVT_MENU,
                  self.OnFtpDistributiontableMenu,
                  self.MenuItemEditDist
                  )
        
#        self.Bind(wx.EVT_MENU,
#                  self.OnFtpUploadMenu,
#                  self.MenuItemUploadFile                  
#                  )
        
        self.Bind(wx.EVT_MENU,
                  self.CallController,
                  self.MenuItemFullUpload                  
                  )
        
        





    def _init_coll_edit_Items(self, parent):
        
        self.MenuItemUndo = parent.Append(help='undo',
                                         id=-1,
                                         kind=wx.ITEM_NORMAL,
                                         text=u'Undo\tCtrl+z'
                                         )
        
        self.MenuItemRedo = parent.Append(help=u'copy selection',
                                          id=-1,
                                          kind=wx.ITEM_NORMAL,
                                          text=u'Redo\tCtrl+y'
                                          )
      
        
        parent.AppendSeparator()
        
        self.MenuItemCut = parent.Append(help='cut',
                                         id=-1,
                                         kind=wx.ITEM_NORMAL,
                                         text=u'Cut\tCtrl+x'
                                         )
        
        self.MenuItemCopy = parent.Append(help=u'copy selection',
                                          id=-1,
                                          kind=wx.ITEM_NORMAL,
                                          text=u'Copy\tCtrl+c'
                                          )
        
        self.MenuItemPaste = parent.Append(help='paste selection',
                                           id=-1,
                                           kind=wx.ITEM_NORMAL,
                                           text=u'Paste\tCtrl+v'
                                           )
        
        parent.AppendSeparator()
        
        
        self.MenuItemReplace = parent.Append(help='Replace',
                                           id=-1,
                                           kind=wx.ITEM_NORMAL,
                                           text=u'Replace\tCtrl+r'
                                           )
        
        self.MenuItemFind = parent.Append(help='Find',
                                           id=-1,
                                           kind=wx.ITEM_NORMAL,
                                           text=u'Find\tCtrl+f'
                                           )
        
        self.MenuItemFindNext = parent.Append(help='Find Next',
                                           id=-1,
                                           kind=wx.ITEM_NORMAL,
                                           text=u'Find Next\tCtrl+g'
                                           )
        
        
        
                
        
              
#        
#        self.Bind(wx.EVT_MENU,
#                  self.CallController,
#                  self.MenuItemFind
#                  )
#        
#        self.Bind(wx.EVT_MENU,
#                  self.CallController,
#                  self.MenuItemFindNext
#                  )
#        
#        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnEditEnlargeMenu, 
#                  self.MenuItemFontInc
#                  )
#        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnEditReduceMenu, 
#                  self.MenuItemFontDec
#                  )
#   
   
    def _init_coll_view_Items(self, parent):
        
        
        self.MenuItemWrapWord = parent.Append(help='Wrap Words In Editor',
                                              id=-1, 
                                              kind=wx.ITEM_CHECK, 
                                              text=u'Wrap Words In Editor\tCtrl+Shift+w')



        parent.AppendSeparator()
        
        
        self.MenuItemEditorStyles =  parent.AppendMenu(help='Editor Styles',
                                             id=-1,
                                              submenu = self.subMenuEditorStyles,
                                              text=u'Editor Styles'
                                              )
         
        parent.AppendSeparator()
        
        self.MenuItemFontInc = parent.Append(help='Increase Font Size', 
                                             id=-1,
                                              kind=wx.ITEM_NORMAL,
                                              text=u'Increase Font Size\tCtrl+='
                                              )
        
        self.MenuItemFontDec = parent.Append(help='reduce Font Size',
                                             id=-1, 
                                             kind=wx.ITEM_NORMAL,
                                             text=u'Decrease Font Size\tCtrl+-'
                                             )


        self.MenuItemFontNormal = parent.Append(help='Font Size to default',
                                             id=-1, 
                                             kind=wx.ITEM_NORMAL,
                                             text=u'Font Size To Normal\tCtrl+0'
                                             )



    def _init_coll_filetypes_Items(self, parent):
        

        self.MenuItemEditHead = parent.Append(help='',
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL, 
                                              text=u'Edit .head')
        
        self.MenuItemEditRssHead = parent.Append(help='edit title for RSS feed', 
                                                id=-1,
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'Edit RSS Title'
                                                )
        
        
        self.MenuItemLanguages = parent.AppendMenu(help='manage project languages',
                           id=-1,
                           submenu = self.subMenuLanguages, 
                           text=u'Project Languages'
                           )
        
        parent.AppendSeparator()
        
        self.MenuItemSelectColor = parent.Append(help='Choose a color',
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL, 
                                              text=u'Select Color')
        
        parent.AppendSeparator()
        
                
        self.MenuItemUnderline = parent.Append(help='Underline',
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL, 
                                              text=u'Underline')
        
        self.MenuItemOblique = parent.Append(help='Oblique',
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL, 
                                              text=u'Oblique')
        
        self.MenuItemBold = parent.Append(help='Bold',
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL, 
                                              text=u'Bold')
        
        self.MenuItemLine_through = parent.Append(help='Line Through',
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL, 
                                              text=u'Line Through')
        
        
  
    
    def _init_coll_sub_menu_markers(self, parent):
        
        self.MenuItemMarkerTodaysDate = parent.Append(help='', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'Todays date - !todaysDate!')
    
        self.MenuItemMarkerProjectName = parent.Append(help='', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'Project Name - !projectName!')
    
        self.MenuItemMarkerPageName = parent.Append(help='', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'Page Name - !pageName!')
        
        self.MenuItemMarkerCreationDate = parent.Append(help='', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'Creation Date - !creationDate!')
    




    
    def _init_coll_sub_menu_languages(self, parent):
        
        self.MenuItemAddLanguage = parent.Append(help='add a language to this project', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'Add Language')
    
        self.MenuItemRemoveLanguage = parent.Append(help='remove language from project', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'Remove Language')
    

        
    
    
    def _init_coll_new_files_Items(self, parent):
       

        self.MenuItemNewContentFile = parent.Append(help='', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'.content\tCtrl-N')
        
        self.MenuItemNewCssFile = parent.Append(help='', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'.css'
                                                )
            
        self.MenuItemNewCgiFile = parent.Append(help='', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'.cgi'
                                                )
        
        self.MenuItemNewJsFile = parent.Append(help='', 
                                               id=-1, 
                                               kind=wx.ITEM_NORMAL, 
                                               text=u'.js'
                                               )
        
        self.MenuItemNewTxtFile = parent.Append(help='', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'.txt'
                                                )
        


# added by Gerald July 7th 07
        

        self.MenuItemNewHtmlFile = parent.Append(help='add new .html file', 
                                                 id=-1,
                                                 kind=wx.ITEM_NORMAL, 
                                                 text=u'.html'
                                                 )
        
       
       
        self.MenuItemNewXmlFile = parent.Append(help='add new .xml file', 
                                                id=-1,
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'.xml'
                                                )
       
       
        self.MenuItemNewPhpFile = parent.Append(help='add new .php file', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'.php'
                                                )
        
        
        self.MenuItemNewDynamicFile = parent.Append(help='', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'.dynamic'
                                                    )
        
        parent.AppendSeparator()
        
        self.MenuItemNewOtherFile = parent.Append(help='add any file', 
                                                    id=-1,
                                                    kind=wx.ITEM_NORMAL, 
                                                    text=u'other...'
                                                    )
      
      
 
    
    def _init_coll_pages_Items(self, parent):
                

        
        self.MenuItemAddProject = parent.Append(help='create new project', 
                                                id=-1,
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'New Project\tCtrl+Shift+N'
                                                )
        
        self.MenuItemOpenProject = parent.Append(help='Open A Maker Project', 
                                                   id=-1,
                                                   kind=wx.ITEM_NORMAL, 
                                                   text=u'Open Project\tCtrl+O')
        
        parent.AppendSeparator()
        
        self.MenuItemNewFiles = parent.AppendMenu(help='Add New File',
                           id=-1,
                           submenu = self.new_files, 
                           text=u'New File'
                           )

        
        self.MenuItemSaveFile = parent.Append(help=u'save File',
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL,
                                              text=u'Save File\tCtrl+S'
                                              )
        
        self.MenuItemDeleteFile = parent.Append(help='delete file', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL,
                                                text=u'Delete File'
                                                )
        
        self.MenuItemRenameFile = parent.Append(help='rename file', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL,
                                                text=u'Rename File'
                                                )
        
        self.MenuItemSaveAsTemplate = parent.Append(help='Save As Template', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL,
                                                text=u'Save As Template'
                                                )
        
        self.MenuItemAddToFTPQueue = parent.Append(help='Add To FTP Queue', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL,
                                                text=u'Add To FTP Queue'
                                                )
        
     
        self.MenuItemCloseFile = parent.Append(help='close file', 
                                                id=-1, 
                                                kind=wx.ITEM_NORMAL,
                                                text=u'Close File\tCtrl+W'
                                                )
              
        parent.AppendSeparator()
               
        self.MenuItemPreview = parent.Append(help=u'preview',
                                             id=-1,
                                             kind=wx.ITEM_NORMAL, 
                                             text=u'Preview File\tF5'
                                             )
        parent.AppendSeparator()
        
        self.MenuItemImportFile = parent.Append(help=u'import File', 
                                                id=-1,
                                                kind=wx.ITEM_NORMAL, 
                                                text=u'Import File(s)'
                                                )
        
        parent.AppendSeparator()

        self.MenuItemManageProjects = parent.Append(help='Manage Projects', 
                                                   id=-1,
                                                   kind=wx.ITEM_NORMAL, 
                                                   text=u'Manage Projects')

        
        self.MenuItemImportProject = parent.Append(help="Import 'Classic' Maker Project", 
                                                   id=-1,
                                                   kind=wx.ITEM_NORMAL, 
                                                   text=u"Import 'Classic' Project")
        
#        
#        self.MenuItemDeleteProject = parent.Append(help='Delete a maker project', 
#                                                   id=-1,
#                                                   kind=wx.ITEM_NORMAL, 
#                                                   text=u'Delete Project')
        
        
       
        parent.AppendSeparator()
        
        
        self.MenuItemSaveProjectAsTemplate = parent.Append(help='Save project as template', 
                                                   id=-1,
                                                   kind=wx.ITEM_NORMAL, 
                                                   text=u'Save Project As Template')
        
        
        parent.AppendSeparator()
        
        
        
        self.MenuItemPrint = parent.Append(help='Print file', 
                                                   id=-1,
                                                   kind=wx.ITEM_NORMAL, 
                                                   text=u'Print '
                                                   )
        
        parent.AppendSeparator()
        
        self.MenuItemQuit = parent.Append(help=u'leave program', 
                                          id=wx.ID_EXIT,
                                          kind=wx.ITEM_NORMAL, 
                                          text=u'Exit'
                                          )
        
        
#        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnDeleteFile, 
#                  self.MenuItemDeleteFile
#                  )
#        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnPagesAddprojectMenu, 
#                  self.MenuItemAddProject
#                  )
#        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnPagesImportProject, 
#                  self.MenuItemImportProject
#                  )
#        
#        
#        
        
        
        


#    def _init_coll_languages_Items(self, parent):
#        
#
#        self.MenuItemDeutsch = parent.Append(help='', 
#                                             id=-1,
#                                             kind=wx.ITEM_NORMAL, 
#                                             text=u'German (de)'
#                                             )
#        
#        self.MenuItemEnglish = parent.Append(help='', 
#                                             id=-1,
#                                             kind=wx.ITEM_NORMAL, 
#                                             text=u'English (en)'
#                                             )
#        
#    

    def _init_coll_mainMenuBar_Menus(self, parent):
        

        parent.Append(menu=self.pages, 
                      title=u'Files'
                      )
        
        parent.Append(menu=self.edit, 
                      title=u'Edit'
                      )
        
        
        parent.Append(menu=self.view, 
                      title=u'View'
                      )
        
        
#        parent.Append(menu=self.parts, 
#                      title=u'Parts'
#                      )
        
        parent.Append(menu=self.images, 
                      title=u'Images'
                      )
        
        parent.Append(menu=self.ftp, 
                      title=u'FTP'
                      )
        
        
        parent.Append(menu=self.filetypes, 
                      title=u'Tools'
                      )
        
                
        parent.Append(menu=self.insert, 
                      title=u'Insert'
                      )
        
        parent.Append(menu=self.help, 
                      title=u'Help'
                      )
        

#    def _init_coll_parts_Items(self, parent):
#
#        
#        self.MenuItemEditNav = parent.Append(help='', 
#                                             id=-1,
#                                             kind=wx.ITEM_NORMAL, 
#                                             text=u'Edit Navigation'
#                                             )
#        
#        self.MenuItemEditBody = parent.Append(help='', 
#                                         id=-1, 
#                                         kind=wx.ITEM_NORMAL,
#                                         text=u'Edit Top of Page'
#                                         )
#        
#        self.MenuItemEditFoot = parent.Append(help='', 
#                                              id=-1, 
#                                              kind=wx.ITEM_NORMAL,
#                                              text=u'Edit Foot'
#                                              )
#        parent.AppendSeparator()
#       
       
     
    
    
    def _init_coll_help_Items(self, parent):
       
        parent.AppendSeparator() 

        self.MenuItemTutorial = parent.Append(help='', 
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL,
                                              text=u'Tutorial'
                                              )
        
        parent.AppendSeparator()
        
        
        self.MenuItemLearnHTMLandCSS = parent.Append(help='', 
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL,
                                              text=u'HTML and CSS Resources'
                                              )

       
        parent.AppendSeparator()
       
        
        self.MenuItemFeedback = parent.Append(help='', 
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL,
                                              text=u'Feedback'
                                              )
        
        self.MenuItemBugReport = parent.Append(help='', 
                                               id=-1,
                                               kind=wx.ITEM_NORMAL, 
                                               text=u'Bugreport'
                                               )
        
        self.MenuItemWebsite = parent.Append(help='', 
                                             id=-1, 
                                             kind=wx.ITEM_NORMAL,
                                             text=u'Visit Project Website'
                                             )
       
        parent.AppendSeparator()
        self.MenuItemLicense = parent.Append(help='', 
                                              id=-1, 
                                              kind=wx.ITEM_NORMAL,
                                              text=u'License')
  
# this part is for the Mac App About Dialog is putting the About on Win in the
# Help menu
#------------------------------------------
       
        parent.Append(wx.ID_ABOUT,   "&About")
       
#        self.Bind(wx.EVT_MENU, 
#                  self.OnHelpItemsAbout, 
#                  id=wx.ID_ABOUT
#                  )
    
# ------------------------------------------
        
#        self.MenuItemAbout = parent.Append(help='',id = -1, kind=wx.ITEM_NORMAL, text=u'About')
#        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnHelpItemsAbout, 
#                  self.MenuItemAbout
#                  )
        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnHelpItemsTutorial, 
#                  self.MenuItemTutorial
#                  )
        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnCheckForUpdate, 
#                  self.MenuItemUpdate
#                  )
        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnFeedbackMenu, 
#                  self.MenuItemFeedback
#                  )
#        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnHelpWebsiteMenu, 
#                  self.MenuItemWebsite
#                  )
        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnHelpReport_a_bugMenu,  
#                  self.MenuItemBugReport
#                  )
        
#        self.Bind(wx.EVT_MENU, 
#                  self.OnHelpDonateMenu, 
#                  self.MenuItemDonation
#                  )



    def _init_coll_images_Items(self, parent):
        

        self.MenuItemImportImage = parent.Append(help='', 
                                                 id=-1,
                                                 kind=wx.ITEM_NORMAL, 
                                                 text=u'Import Image'
                                                 )
        
        self.MenuItemDeleteImage = parent.Append(help='', 
                                                 id=-1,
                                                 kind=wx.ITEM_NORMAL, 
                                                 text=u'Delete Image'
                                                 )
        
        
        parent.AppendSeparator()
        
        self.MenuItemSyncImages = parent.Append(help='sync images', 
                                                 id=-1,
                                                 kind=wx.ITEM_NORMAL, 
                                                 text=u'Sync Images With Server'
                                                 )
        
        
        
        



#status bar


    def _init_coll_statusBar1_Fields(self, parent):
        
        parent.SetFieldsCount(5)

        parent.SetStatusText(number=0, text=u'Status')
        parent.SetStatusText(number=1, text=u'Current Project')
        parent.SetStatusText(number=2, text=u'Language')
        parent.SetStatusText(number=3, text=u'Current File')
        parent.SetStatusText(number=4, text=u'Files in queue ')
        parent.SetStatusWidths([-1, -1, -1, -1, 200])








    
    
    def _init_utils(self):
        
        self.mainMenuBar = wx.MenuBar()

        self.pages = wx.Menu(title=u'')

        self.edit = wx.Menu(title=u'')
        
        self.view = wx.Menu(title=u'')

        self.ftp = wx.Menu(title=u'')

        self.insert = wx.Menu(title=u'')

        self.images = wx.Menu(title=u'')

        self.filetypes = wx.Menu(title=u'')

        self.help = wx.Menu(title=u'')

        self.additional_projects = wx.Menu(title=u'')

        self.editorStyles = wx.Menu(title=u'')
        
        self.new_files = wx.Menu(title=u'')
        
        self.SubMenuMarkers = wx.Menu(title='')
        
        self.subMenuLanguages = wx.Menu(title='')
        
        self.subMenuEditorStyles = wx.Menu(title='')
        
        self._init_coll_mainMenuBar_Menus(self.mainMenuBar)
        self._init_coll_pages_Items(self.pages)
        self._init_coll_edit_Items(self.edit)
        self._init_coll_view_Items(self.view)
        
        self._init_coll_ftp_Items(self.ftp)
        
        
        self._init_coll_images_Items(self.images)
        self._init_coll_filetypes_Items(self.filetypes)
       
        self._init_coll_help_Items(self.help)
       
        
        self._init_coll_new_files_Items(self.new_files)
        self._init_coll_sub_menu_markers(self.SubMenuMarkers)
        self._init_coll_sub_menu_languages(self.subMenuLanguages)
        
        
                # the submenus
        #---------
        #---------
        #---------
        self.subMenuStructure = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuMeta_Information = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuText = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuLinks = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuImages_and_Objects = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuLists = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuTables = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuForms = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuScripting = wx.Menu(title=u'')
        
        #---------
        #---------
        #---------
        self.subMenuPresentational = wx.Menu(title=u'')
        
        self.subMenuHTML = wx.Menu(title=u'')
        
        self.subMenuCSS = wx.Menu(title=u'')
        
#--------
#--------
        
        self.subMenuHTML.AppendMenu(help='Structure', 
        id=-1, 
        submenu = self.subMenuStructure, 
        text=u'Structure')
        
        self.subMenuHTML.AppendMenu(help='Meta_Information', 
        id=-1, 
        submenu = self.subMenuMeta_Information, 
        text=u'Meta_Information')
        
        self.subMenuHTML.AppendMenu(help='Text', 
        id=-1, 
        submenu = self.subMenuText, 
        text=u'Text')
        
        self.subMenuHTML.AppendMenu(help='Links', 
        id=-1, 
        submenu = self.subMenuLinks, 
        text=u'Links')
        
        self.subMenuHTML.AppendMenu(help='Images_and_Objects', 
        id=-1, 
        submenu = self.subMenuImages_and_Objects, 
        text=u'Images_and_Objects')
        
        self.subMenuHTML.AppendMenu(help='Lists', 
        id=-1, 
        submenu = self.subMenuLists, 
        text=u'Lists')
        
        self.subMenuHTML.AppendMenu(help='Tables', 
        id=-1, 
        submenu = self.subMenuTables, 
        text=u'Tables')
        
        self.subMenuHTML.AppendMenu(help='Forms', 
        id=-1, 
        submenu = self.subMenuForms, 
        text=u'Forms')
        
        self.subMenuHTML.AppendMenu(help='Scripting', 
        id=-1, 
        submenu = self.subMenuScripting, 
        text=u'Scripting')
        
        self.subMenuHTML.AppendMenu(help='Presentational', 
        id=-1, 
        submenu = self.subMenuPresentational, 
        text=u'Presentational')


# Menu Items
        
                
        self.MenuItemHTML_body = self.subMenuStructure.Append(help='The main body of an HTML document',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<body>   The main body of an HTML document')
        
        
        
        
        
        self.MenuItemHTML_div = self.subMenuStructure.Append(help='Division. Defines a block of HTML',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<div>   Division. Defines a block of HTML')
        
        
        
        
        
        self.MenuItemHTML_head = self.subMenuStructure.Append(help='The header of an HTML document',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<head>   The header of an HTML document')
        
        
        
        
        
        self.MenuItemHTML_html = self.subMenuStructure.Append(help='The root element of the (X)HTML document',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<html>   The root element of the (X)HTML document')
        
        
        self.MenuItemHTML_span = self.subMenuStructure.Append(help='Used to group in-line HTML',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<span>   Used to group in-line HTML')
        
        
        
        
        
        # menu items
        
        self.MenuItemHTML_DOCTYPE = self.subMenuMeta_Information.Append(help='Document type declaration',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<DOCTYPE>   Document type declaration')
        
        
        
        
        self.MenuItemHTML_link = self.subMenuMeta_Information.Append(help='Defines a link to an external resource',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<link>   Defines a link to an external resource')
        
        
        
        self.MenuItemHTML_meta = self.subMenuMeta_Information.Append(help='Meta information',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<meta>   Meta information')
        
      
        
        
        self.MenuItemHTML_style = self.subMenuMeta_Information.Append(help='Used to define CSS at a page-level ',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<style>   Used to define CSS at a page-level ')
        
        
        
        
        self.MenuItemHTML_title = self.subMenuMeta_Information.Append(help='The title of a page',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<title>   The title of a page')
        
       
        
        # menu items
        
        self.MenuItemHTML_abbr = self.subMenuText.Append(help='Abbreviation',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<abbr>   Abbreviation')
       
        
        self.MenuItemHTML_acronym = self.subMenuText.Append(help='Acronym',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<acronym>   Acronym')
        
       
        
        
        self.MenuItemHTML_address = self.subMenuText.Append(help='Address',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<address>   Address')
        
       
        
        self.MenuItemHTML_bdo = self.subMenuText.Append(help='Bi-directional text',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<bdo>   Bi-directional text')
        
        
        
        self.MenuItemHTML_blockquote = self.subMenuText.Append(help='A large quotation',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<blockquote>   A large quotation')
        
       
        
        
        
        self.MenuItemHTML_br = self.subMenuText.Append(help='A line break',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<br />   A line break\tCtrl+Return')
        
        
        
        
        
        self.MenuItemHTML_cite = self.subMenuText.Append(help='in-line citation',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<cite>   in-line citation')
      
        
        
        
        self.MenuItemHTML_code = self.subMenuText.Append(help='Computer code',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<code>   Computer code')
        
       
        
        
        
        self.MenuItemHTML_del = self.subMenuText.Append(help='Deletion',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<del>   Deletion')
        
        
        
        
        
        self.MenuItemHTML_dfn = self.subMenuText.Append(help='Definition term',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<dfn>   Definition term')
        
        
        
        
        
        self.MenuItemHTML_em = self.subMenuText.Append(help='Emphasis',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<em>   Emphasis')
        
        
        
        
        self.MenuItemHTML_h1 = self.subMenuText.Append(help='Heading size 1',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<h1>   Heading size 1\tCtrl+Shift+h')
        
        
        
        
        self.MenuItemHTML_h2 = self.subMenuText.Append(help='Heading size 2',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<h2>   Heading size 2')
        
      
        
        
        
        self.MenuItemHTML_h3 = self.subMenuText.Append(help='Heading size 3',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<h3>   Heading size 3')
     
        
        
        
        self.MenuItemHTML_h4 = self.subMenuText.Append(help='Heading size 4',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<h4>   Heading size 4')
        
      
        
        
        
        self.MenuItemHTML_h5 = self.subMenuText.Append(help='Heading size 5',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<h5>   Heading size 5')
        
      
        
        
        self.MenuItemHTML_h6 = self.subMenuText.Append(help='Heading size 6',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<h6>   Heading size 6')
        
      
        
        
        self.MenuItemHTML_ins = self.subMenuText.Append(help='Insertion',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<ins>   Insertion')
        
     
        
        
        
        self.MenuItemHTML_kbd = self.subMenuText.Append(help='text that should be typed in by the user',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<kbd>   text that should be typed in by the user')
        
   
        
        self.MenuItemHTML_p = self.subMenuText.Append(help='Paragraph',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<p>   Paragraph\tCtrl+Shift+p')
        
     
        
        
        self.MenuItemHTML_pre = self.subMenuText.Append(help='Preformatted text',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<pre>   Preformatted text')
        
       
        
        
        self.MenuItemHTML_q = self.subMenuText.Append(help='An in-line quote',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<q>   An in-line quote')
        
     
        
        
        self.MenuItemHTML_samp = self.subMenuText.Append(help='Sample',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<samp>   Sample')
        
       
        
        self.MenuItemHTML_strong = self.subMenuText.Append(help='Strong emphasis.',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<strong>   Strong emphasis.')
        
       
        
        
        self.MenuItemHTML_var = self.subMenuText.Append(help='Variable',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<var>   Variable')
        
    
        
        
        # menu items
        
        self.MenuItemHTML_a = self.subMenuLinks.Append(help='Anchor. Primarily used as a hypertext link.',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<a>   Anchor. Primarily used as a hypertext link.\tCtrl+Shift+a')
        
        
        self.MenuItemHTML_base = self.subMenuLinks.Append(help='base location for links on a page',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<base>   base location for links on a page')
        
     
        
        
        
        # menu items
        
        self.MenuItemHTML_area = self.subMenuImages_and_Objects.Append(help='A region of a client-side image map',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<area>   A region of a client-side image map')
        
     
        self.MenuItemHTML_img = self.subMenuImages_and_Objects.Append(help='Image',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<img>   Image')
        
      
        
        
        self.MenuItemHTML_map = self.subMenuImages_and_Objects.Append(help='client-side image map',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<map>   client-side image map')
        
        
        
        self.MenuItemHTML_object = self.subMenuImages_and_Objects.Append(help='An embedded multimedia object',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<object>   An embedded multimedia object')
        
        
        
        self.MenuItemHTML_param = self.subMenuImages_and_Objects.Append(help='Parameter of an object',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<param>   Parameter of an object')
        
       
        
        # menu items
        
        self.MenuItemHTML_dd = self.subMenuLists.Append(help='Definition description',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<dd>   Definition description')
        
       
        
        self.MenuItemHTML_dl = self.subMenuLists.Append(help='Definition list',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<dl>   Definition list')
      
        
        
        self.MenuItemHTML_dt = self.subMenuLists.Append(help='Definition term',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<dt>   Definition term')
        
     
        
        self.MenuItemHTML_li = self.subMenuLists.Append(help='List item',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<li>   List item')
        
      
        
        
        self.MenuItemHTML_ol = self.subMenuLists.Append(help='Ordered list',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<ol>   Ordered list')
        
      
        
        self.MenuItemHTML_ul = self.subMenuLists.Append(help='Unordered list',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<ul>   Unordered list')
        
     
        
        # menu items
        
        self.MenuItemHTML_caption = self.subMenuTables.Append(help='caption for a table',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<caption>   caption for a table')
        
        
        
        
        self.MenuItemHTML_col = self.subMenuTables.Append(help='Table column',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<col>   Table column')
        
       
        
        self.MenuItemHTML_colgroup = self.subMenuTables.Append(help='Column group',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<colgroup>   Column group')
        
       
        self.MenuItemHTML_table = self.subMenuTables.Append(help='Table used for tabular data',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<table>   Table used for tabular data')
        
      
        
        self.MenuItemHTML_tbody = self.subMenuTables.Append(help='Table body',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<tbody>   Table body')
        
     
        
        self.MenuItemHTML_td = self.subMenuTables.Append(help='Table data cell',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<td>   Table data cell')
        
       
        
        
        self.MenuItemHTML_tfoot = self.subMenuTables.Append(help='Table foot',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<tfoot>   Table foot')
       
        
        
        
        self.MenuItemHTML_th = self.subMenuTables.Append(help='Table header cell',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<th>   Table header cell')
     
        
        self.MenuItemHTML_thead = self.subMenuTables.Append(help='Table header',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<thead>   Table header')
        
      
        
        self.MenuItemHTML_tr = self.subMenuTables.Append(help='Table row',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<tr>   Table row')
        
       
        # menu items
        
        self.MenuItemHTML_button = self.subMenuForms.Append(help='Defines a form button',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<button>   Defines a form button')
        
     
        
        
        self.MenuItemHTML_fieldset = self.subMenuForms.Append(help='Defines a group of related form items',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<fieldset>   Defines a group of related form items')
        
    
        
        self.MenuItemHTML_form = self.subMenuForms.Append(help='Defines a form',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<form>   Defines a form')
        
     
        
        
        self.MenuItemHTML_input = self.subMenuForms.Append(help='Form field for user input',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<input>   Form field for user input')
        
      
        
        self.MenuItemHTML_label = self.subMenuForms.Append(help='Label for a form element',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<label>   Label for a form element')
        
      
        
        self.MenuItemHTML_legend = self.subMenuForms.Append(help='Defines a caption for a fieldset',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<legend>   Defines a caption for a fieldset')
        
  
        
        
        self.MenuItemHTML_optgroup = self.subMenuForms.Append(help='Option group',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<optgroup>   Option group')
        
     
        
        
        self.MenuItemHTML_option = self.subMenuForms.Append(help='Defines an option of a <select> form field',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<option>   Defines an option of a <select> form field')
        
       
        
        self.MenuItemHTML_select = self.subMenuForms.Append(help='A drop-down list form element',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<select>   A drop-down list form element')
    
        
        
        self.MenuItemHTML_textarea = self.subMenuForms.Append(help='A multi-row text area form element',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<textarea>   A multi-row text area form element')
        
     
        # menu items
        
        self.MenuItemHTML_noscript = self.subMenuScripting.Append(help='content to be used when a script can not be used',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<noscript>   content to be used when a script can not be used')
        
      
        self.MenuItemHTML_script = self.subMenuScripting.Append(help='Defines a scripting language, eg. JavaScript',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<script>   Defines a scripting language, eg. JavaScript')
        
   
        
        # menu items
        
        self.MenuItemHTML_b = self.subMenuPresentational.Append(help='Bold',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<b>   Bold')
       
        
        
        self.MenuItemHTML_big = self.subMenuPresentational.Append(help='Big',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<big>   Big')
        
      
        
        self.MenuItemHTML_hr = self.subMenuPresentational.Append(help='Horizontal ruler',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<hr>   Horizontal ruler')
        
       
        
        self.MenuItemHTML_i = self.subMenuPresentational.Append(help='Italic',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<i>   Italic')
        
       
        
        
        self.MenuItemHTML_small = self.subMenuPresentational.Append(help='Small',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<small>   Small')
        
      
        
        self.MenuItemHTML_sub = self.subMenuPresentational.Append(help='Subscript',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<sub>   Subscript')
        
     
        
        
        self.MenuItemHTML_sup = self.subMenuPresentational.Append(help='Superscript',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<sup>   Superscript')
        
     
        self.MenuItemHTML_tt = self.subMenuPresentational.Append(help='Teletype',
        id=-1,
        kind=wx.ITEM_NORMAL,
        text=u'<tt>   Teletype')
      

        
        # CSS Menu Items
        
        self.MenuItemCSS_background = self.subMenuCSS.Append(help='background', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'background'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_background)
        
        
        self.MenuItemCSS_background_attachment = self.subMenuCSS.Append(help='background-attachment', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'background_attachment'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_background_attachment)
        
        
        self.MenuItemCSS_background_color = self.subMenuCSS.Append(help='background-color', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'background_color'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_background_color)
        
        
        self.MenuItemCSS_background_image = self.subMenuCSS.Append(help='background-image', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'background_image'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_background_image)
        
        
        self.MenuItemCSS_background_position = self.subMenuCSS.Append(help='background-position', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'background_position'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_background_position)
        
        
        self.MenuItemCSS_background_repeat = self.subMenuCSS.Append(help='background-repeat', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'background_repeat'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_background_repeat)
        
        
        self.MenuItemCSS_border = self.subMenuCSS.Append(help='border', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'border'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_border)
        
        
        self.MenuItemCSS_border_collapse = self.subMenuCSS.Append(help='border-collapse', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'border_collapse'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_border_collapse)
        
        
        self.MenuItemCSS_border_color = self.subMenuCSS.Append(help='border-color', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'border_color'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_border_color)
        
        
        self.MenuItemCSS_border_spacing = self.subMenuCSS.Append(help='border-spacing', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'border_spacing'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_border_spacing)
        
        
        self.MenuItemCSS_border_style = self.subMenuCSS.Append(help='border-style', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'border_style'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_border_style)
        
        
        self.MenuItemCSS_border_width = self.subMenuCSS.Append(help='border-width', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'border_width'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_border_width)
        
        
        self.MenuItemCSS_bottom = self.subMenuCSS.Append(help='bottom', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'bottom'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_bottom)
        
        
        self.MenuItemCSS_caption_side = self.subMenuCSS.Append(help='caption-side', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'caption_side'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_caption_side)
        
        
        self.MenuItemCSS_clear = self.subMenuCSS.Append(help='clear', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'clear'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_clear)
        
        
        self.MenuItemCSS_clip = self.subMenuCSS.Append(help='clip', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'clip'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_clip)
        
        
        self.MenuItemCSS_color = self.subMenuCSS.Append(help='color', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'color'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_color)
        
        
        self.MenuItemCSS_content = self.subMenuCSS.Append(help='content', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'content'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_content)
        
        
        self.MenuItemCSS_counter_increment = self.subMenuCSS.Append(help='counter-increment', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'counter_increment'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_counter_increment)
        
        
        self.MenuItemCSS_counter_reset = self.subMenuCSS.Append(help='counter-reset', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'counter_reset'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_counter_reset)
        
        
        self.MenuItemCSS_cursor = self.subMenuCSS.Append(help='cursor', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'cursor'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_cursor)
        
        
        self.MenuItemCSS_direction = self.subMenuCSS.Append(help='direction', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'direction'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_direction)
        
        
        self.MenuItemCSS_display = self.subMenuCSS.Append(help='display', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'display'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_display)
        
        
        self.MenuItemCSS_empty_cells = self.subMenuCSS.Append(help='empty-cells', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'empty_cells'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_empty_cells)
        
        
        self.MenuItemCSS_float = self.subMenuCSS.Append(help='float', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'float'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_float)
        
        
        self.MenuItemCSS_font = self.subMenuCSS.Append(help='font', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'font'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_font)
        
        
        self.MenuItemCSS_font_family = self.subMenuCSS.Append(help='font-family', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'font_family'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_font_family)
        
        
        self.MenuItemCSS_font_size = self.subMenuCSS.Append(help='font-size', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'font_size'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_font_size)
        
        
        self.MenuItemCSS_font_style = self.subMenuCSS.Append(help='font-style', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'font_style'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_font_style)
        
        
        self.MenuItemCSS_font_variant = self.subMenuCSS.Append(help='font-variant', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'font_variant'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_font_variant)
        
        
        self.MenuItemCSS_font_weight = self.subMenuCSS.Append(help='font-weight', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'font_weight'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_font_weight)
        
        
        self.MenuItemCSS_height = self.subMenuCSS.Append(help='height', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'height'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_height)
        
        
        self.MenuItemCSS_left = self.subMenuCSS.Append(help='left', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'left'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_left)
        
        
        self.MenuItemCSS_letter_spacing = self.subMenuCSS.Append(help='letter-spacing', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'letter_spacing'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_letter_spacing)
        
        
        self.MenuItemCSS_line_height = self.subMenuCSS.Append(help='line-height', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'line_height'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_line_height)
        
        
        self.MenuItemCSS_list_style = self.subMenuCSS.Append(help='list-style', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'list_style'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_list_style)
        
        
        self.MenuItemCSS_list_style_image = self.subMenuCSS.Append(help='list-style-image', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'list_style_image'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_list_style_image)
        
        
        self.MenuItemCSS_list_style_position = self.subMenuCSS.Append(help='list-style-position', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'list_style_position'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_list_style_position)
        
        
        self.MenuItemCSS_list_style_type = self.subMenuCSS.Append(help='list-style-type', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'list_style_type'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_list_style_type)
        
        
        self.MenuItemCSS_margin = self.subMenuCSS.Append(help='margin', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'margin'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_margin)
        
        
        self.MenuItemCSS_max_height = self.subMenuCSS.Append(help='max-height', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'max_height'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_max_height)
        
        
        self.MenuItemCSS_max_width = self.subMenuCSS.Append(help='max-width', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'max_width'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_max_width)
        
        
        self.MenuItemCSS_min_height = self.subMenuCSS.Append(help='min-height', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'min_height'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_min_height)
        
        
        self.MenuItemCSS_min_width = self.subMenuCSS.Append(help='min-width', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'min_width'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_min_width)
        
        
        self.MenuItemCSS_orphans = self.subMenuCSS.Append(help='orphans', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'orphans'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_orphans)
        
        
        self.MenuItemCSS_outline = self.subMenuCSS.Append(help='outline', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'outline'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_outline)
        
        
        self.MenuItemCSS_outline_color = self.subMenuCSS.Append(help='outline-color', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'outline_color'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_outline_color)
        
        
        self.MenuItemCSS_outline_style = self.subMenuCSS.Append(help='outline-style', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'outline_style'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_outline_style)
        
        
        self.MenuItemCSS_outline_width = self.subMenuCSS.Append(help='outline-width', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'outline_width'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_outline_width)
        
        
        self.MenuItemCSS_overflow = self.subMenuCSS.Append(help='overflow', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'overflow'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_overflow)
        
        
        self.MenuItemCSS_padding = self.subMenuCSS.Append(help='padding', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'padding'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_padding)
        
        
        self.MenuItemCSS_page_break_after = self.subMenuCSS.Append(help='page-break-after', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'page_break_after'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_page_break_after)
        
        
        self.MenuItemCSS_page_break_before = self.subMenuCSS.Append(help='page-break-before', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'page_break_before'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_page_break_before)
        
        
        self.MenuItemCSS_page_break_inside = self.subMenuCSS.Append(help='page-break-inside', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'page_break_inside'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_page_break_inside)
        
        
        self.MenuItemCSS_position = self.subMenuCSS.Append(help='position', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'position'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_position)
        
        
        self.MenuItemCSS_quotes = self.subMenuCSS.Append(help='quotes', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'quotes'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_quotes)
        
        
        self.MenuItemCSS_right = self.subMenuCSS.Append(help='right', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'right'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_right)
        
        
        self.MenuItemCSS_table_layout = self.subMenuCSS.Append(help='table-layout', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'table_layout'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_table_layout)
        
        
        self.MenuItemCSS_text_align = self.subMenuCSS.Append(help='text-align', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'text_align'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_text_align)
        
        
        self.MenuItemCSS_text_decoration = self.subMenuCSS.Append(help='text-decoration', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'text_decoration'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_text_decoration)
        
        
        self.MenuItemCSS_text_indent = self.subMenuCSS.Append(help='text-indent', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'text_indent'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_text_indent)
        
        
        self.MenuItemCSS_text_transform = self.subMenuCSS.Append(help='text-transform', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'text_transform'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_text_transform)
        
        
        self.MenuItemCSS_top = self.subMenuCSS.Append(help='top', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'top'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_top)
        
        
        self.MenuItemCSS_unicode_bidi = self.subMenuCSS.Append(help='unicode-bidi', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'unicode_bidi'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_unicode_bidi)
        
        
        self.MenuItemCSS_vertical_align = self.subMenuCSS.Append(help='vertical-align', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'vertical_align'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_vertical_align)
        
        
        self.MenuItemCSS_visibility = self.subMenuCSS.Append(help='visibility', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'visibility'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_visibility)
        
        
        self.MenuItemCSS_white_space = self.subMenuCSS.Append(help='white-space', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'white_space'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_white_space)
        
        
        self.MenuItemCSS_widows = self.subMenuCSS.Append(help='widows', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'widows'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_widows)
        
        
        self.MenuItemCSS_width = self.subMenuCSS.Append(help='width', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'width'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_width)
        
        
        self.MenuItemCSS_word_spacing = self.subMenuCSS.Append(help='word-spacing', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'word_spacing'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_word_spacing)
        
        
        self.MenuItemCSS_z_index = self.subMenuCSS.Append(help='z-index', id=-1, 
                    kind=wx.ITEM_NORMAL,
                    text=u'z_index'
                    )
        
        self.Bind(wx.EVT_MENU, 
                self.CallController,
                self.MenuItemCSS_z_index)


# end of css menu items
        
        

        self._init_coll_code_Items(self.insert)




#the sizers


    def _init_sizers(self):
        # generated method, don't edit

        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        #self.boxSizer2 = wx.BoxSizer(orient=wx.VERTICAL)
        


        self._init_coll_boxSizer1_Items(self.boxSizer1)
        #self._init_coll_boxSizer2_Items(self.boxSizer2)
       

#here the sizer for the window is set
        
        self.SetSizer(self.boxSizer1)
        
        
        
        
#deprecated

        #self.flexGridSizer1 = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=0)
        #self._init_coll_flexGridSizer1_Items(self.flexGridSizer1)
        #self._init_coll_flexGridSizer1_Growables(self.flexGridSizer1)
        



    def partArt(self, il, image_size):
        # called in init ctrls 
        # moved out here to make testing easier
        
        wx.ArtProvider.Push(MyArtProvider())
        self.part     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, image_size))
        wx.ArtProvider.Pop()


    def _init_ctrls(self, prnt):
        
        wx.Frame.__init__(self, id=-1, name='', parent=prnt,
              pos=wx.Point(0,0 ), size=wx.Size(1200, 700),
              style=wx.DEFAULT_FRAME_STYLE, title=u'the maker')
        
        
        try:            # - don't sweat it if it doesn't load
            self.SetIcon(wx.Icon(os.path.join(os.path.dirname(sys.argv[0]), "system/tags.ico"), wx.BITMAP_TYPE_ICO))
        finally:
            pass
        
                    
        self._init_utils()
        
        
        self.SetMenuBar(self.mainMenuBar)
        self.SetStatusBarPane(0)


#the other splitter

        #self.splitter2 = MySplitter(self, -1,None)
                
#the top splitter        
        self.splitter = MySplitter(self, -1,None)
        #self.splitter.SetSashSize(10)




# and the stc is added to it

        # it is very importat to keep the NODRAG style
        #
        # if dragging is added at some point the 
        # makerProjectController.py method noteBookPageClosed has to be
        # changed where the noteBoolPages dict is updated
        #
        self.noteBook = nb.FlatNotebook(self.splitter, wx.ID_ANY, agwStyle = wx.lib.flatnotebook.FNB_FF2,
                                        style= wx.lib.flatnotebook.FNB_NODRAG | 
                                        wx.lib.flatnotebook.FNB_X_ON_TAB)
        self.noteBook.SetPadding(wx.Size(20))
        
        # add a welcome message to the noteBook        
        
        self.styledTextCtrl1 = (makerEditorWxView.editorView(self, "default")).editor
        self.welcomeId = self.styledTextCtrl1.GetId()
        self.noteBook.AddPage(self.styledTextCtrl1, "Thank you for using The Maker.")
        self.styledTextCtrl1.SetText(self.BoilerPlate)



#switch off popup

        #self.styledTextCtrl1.Bind(wx.EVT_RIGHT_DOWN, self.OnSTCRightDown)

        

#add widgets to the first splitter

        self.listWindow = wx.Panel(self.splitter, -1, style = wx.NO_BORDER)
        #self.listWindow.SetBackgroundColour(wx.RED)

        self.listSizer = wx.BoxSizer(orient=wx.VERTICAL)


# the listbox is added to the splitter too
        self.tree = wx.TreeCtrl(self.listWindow, -1, 
                                style=wx.TR_HAS_BUTTONS
                                |wx.TR_LINES_AT_ROOT
                                |wx.TR_DEFAULT_STYLE)
        
        
        
        image_size = (16,16)
        il = wx.ImageList(image_size[0], image_size[1])
        self.projidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_REMOVABLE, wx.ART_OTHER, image_size))
        self.fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,  wx.ART_OTHER, image_size))
        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, image_size))
        self.fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, image_size))
        try:
            self.filechange  = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NEW, wx.ART_OTHER, image_size))
        except:
            
            self.filechange  = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, image_size))
        
        
        self.partArt(il, image_size)
        
        self.tree.SetImageList(il)
        self.il = il
   
        self.listSizer.Add(self.tree, 1, border=0, flag=wx.EXPAND)
            
        self.listWindow.SetAutoLayout(True)
        self.listWindow.SetSizer(self.listSizer)
        self.listSizer.Fit(self.listWindow)

        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SplitVertically(self.listWindow, self.noteBook, 180)    

        self.topPanel = wx.Panel(self, -1, pos=(0,0), size=(180,50), style=wx.TB_HORIZONTAL)
        self.topPanel.SetAutoLayout(True)

        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topPanel.SetMinSize((0,50))
        self.topPanel.SetSizer(self.topSizer)
        
        self.saveButton = wx.Button(id=-1, label=u'Save',
              name='saveButton', parent=self, pos=wx.Point(4, 10),
              style=0)

        self.publishButton = wx.Button(id=-1, label=u'Publish',
              name='publishButton', parent=self, pos=wx.Point(84, 10),
              style=0)
        
        self.previewButton = wx.Button(id=-1, label=u'Preview',
              name=u'preview', parent=self, pos=wx.Point(164, 10),
              style=0)
        
        
        self.makeAllButton = wx.Button(id=-1,
              label=u'Make All', name=u'make_all_button', parent=self,
              pos=wx.Point(244, 10), style=0)
        
        
        self.search = wx.SearchCtrl(self, -1, pos=(750,10), size=(180,25), style=wx.TE_PROCESS_ENTER)
        
        #extract the searchCtrl's textCtrl 
        self.searchStatus = wx.StaticText(self, -1, pos=(750,10), size=(106,20),style=0)             
        self.searchStatus.SetLabel("")

        
        
        self.topSizer.Add(self.saveButton,0,wx.ALIGN_CENTER | wx.WEST, 20)
        self.topSizer.Add(self.publishButton,0, wx.ALIGN_CENTER | wx.WEST, 6)
        self.topSizer.Add(self.previewButton,0, wx.ALIGN_CENTER | wx.WEST, 6)
        self.topSizer.Add(self.makeAllButton,0, wx.ALIGN_CENTER | wx.WEST, 6)
        self.topSizer.AddStretchSpacer(1)
        self.topSizer.Add(self.searchStatus,0, wx.ALIGN_CENTER | wx.WEST | wx.EAST, 10)
        self.topSizer.Add(self.search,0, wx.ALIGN_CENTER | wx.EAST, 10)
        

        self.statusBar1 = wx.StatusBar(id=-1,
              name='statusBar1', parent=self, style=wx.ST_SIZEGRIP)
        
        self.statusBar1.SetConstraints(LayoutAnchors(self.statusBar1, True,
              True, False, False))
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

 
        
        self.styledTextCtrl1.Bind(wx.EVT_PAINT, self.OnStyledTextCtrl1Paint)
        self.styledTextCtrl1.Bind(wx.EVT_ERASE_BACKGROUND,
              self.OnStyledTextCtrl1EraseBackground)

        
        
    def __init__(self, app):  
        
        
        self.BoilerPlate = makerCopyright.getCopyright()
              
        self.ProgressBars = [] # this is a stack for progress bars
        
        self.ModifierBind = False
        
        self.application = app
        
        self._init_ctrls(None)
        self._init_sizers()
        self.wx = wx
        
        self.saved= True
        self.selection= None
        
        # set interface fonts
        if wx.Platform == '__WXMSW__':
            self.interfaceSetFonts(10,-2)
            
        elif wx.Platform == '__WXMAC__':
            self.interfaceSetFonts(12,0)
        
        # Linux and others
        else:
            self.interfaceSetFonts(10,0, special = True)
        
        self.createPopUpMenus()
        
  
    
    def interfaceSetFonts(self,value, zoom, special = False):
        """
        value is the size for Fonts
        zoom is the zoom for the editor
        """
        if special:
            theFont = wx.SystemSettings.GetFont(0)
        else:
            theFont = wx.Font(value, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
        
        self.styledTextCtrl1.SetZoom(zoom)

        self.statusBar1.SetFont(theFont)
        self.SetFont(theFont)
        self.makeAllButton.SetFont(theFont)
        self.previewButton.SetFont(theFont)
        self.publishButton.SetFont(theFont)
        self.saveButton.SetFont(theFont)
        self.tree.SetFont(theFont)
        self.tree.SetBackgroundColour('#e2e6ec')
        self.tree.SetIndent(20)
    
    
    def CallController(self, event):
        """
        This is a universal method sending the event to the
        controller and the controller method findActionForEvent(event)
        will trigger the right action
        """
        
        self.controller.findActionForEvent(event)
         
    
    def createPopUpMenus(self):
        
        self.treePopUp = self.wx.Menu()
        


        
        
        # Bind this in Maker File Controller

        self.treePopUpMenuItemDeleteFile = self.treePopUp.Append(help='Delete Current File',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Delete File'
                                         )


        self.treePopUpMenuItemRenameFile = self.treePopUp.Append(help='Rename Current File',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Rename File'
                                         )
        
        self.treePopUpMenuItemCloseFile = self.treePopUp.Append(help='Close Current File',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Close File'
                                         )

        self.treePopUp.AppendSeparator()

        self.treePopUpMenuItemPreview = self.treePopUp.Append(help='Preview File',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Preview'
                                         )
  
        self.treePopUp.AppendSeparator()
        

        self.treePopUpMenuItemExpandAll = self.treePopUp.Append(help='Expand All Items',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Expand All Items'
                                         )

        self.treePopUpMenuItemCollapseAll = self.treePopUp.Append(help='Collapse All Items',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Collapse All Items'
                                         )


        self.treePopUpMenuItemCollapseOther = self.treePopUp.Append(help='Collapse Other Projects',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Collapse Other Projects'
                                         )
        
        
        
  
  
        self.treePopUp.AppendSeparator()
        
        self.treePopUpMenuItemPrint = self.treePopUp.Append(help='Print File',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Print'
                                         )
        
        
        
        # Editor 
        
        self.editorPopUp = self.wx.Menu()
               
        self.editorPopUpMenuItemUndo = self.editorPopUp.Append(help='undo',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Undo\tCtrl+z'
                                         )
        
        self.editorPopUpMenuItemRedo = self.editorPopUp.Append(help=u'copy selection',
                                          id=-1,
                                          kind=self.wx.ITEM_NORMAL,
                                          text=u'Redo\tCtrl+y'
                                          )
              
        self.editorPopUp.AppendSeparator()
        
        self.editorPopUpMenuItemCut = self.editorPopUp.Append(help='cut',
                                         id=-1,
                                         kind=self.wx.ITEM_NORMAL,
                                         text=u'Cut\tCtrl+x'
                                         )
        
        self.editorPopUpMenuItemCopy = self.editorPopUp.Append(help=u'copy selection',
                                          id=-1,
                                          kind=self.wx.ITEM_NORMAL,
                                          text=u'Copy\tCtrl+c'
                                          )
        
        self.editorPopUpMenuItemPaste = self.editorPopUp.Append(help='paste selection',
                                           id=-1,
                                           kind=self.wx.ITEM_NORMAL,
                                           text=u'Paste\tCtrl+v'
                                           )
        
        self.editorPopUp.AppendSeparator()
        
        self.editorPopUpMenuItemReplace = self.editorPopUp.Append(help='Replace',
                                           id=-1,
                                           kind=self.wx.ITEM_NORMAL,
                                           text=u'Replace\tCtrl+r'
                                           )
        
        self.editorPopUpMenuItemFind = self.editorPopUp.Append(help='Find',
                                           id=-1,
                                           kind=self.wx.ITEM_NORMAL,
                                           text=u'Find\tCtrl+f'
                                           )
        
        self.editorPopUpMenuItemFindNext = self.editorPopUp.Append(help='Find Next',
                                           id=-1,
                                           kind=self.wx.ITEM_NORMAL,
                                           text=u'Find Next\tCtrl+g'
                                           )
        
        self.editorPopUp.AppendSeparator()
        
        self.editorPopUpMenuItemSelectColor = self.editorPopUp.Append(help='Choose a color',
                                              id=-1, 
                                              kind=self.wx.ITEM_NORMAL, 
                                              text=u'Select Color')
        
        self.editorPopUp.AppendSeparator()
        
                
        self.editorPopUpMenuItemUnderline = self.editorPopUp.Append(help='Underline',
                                              id=-1, 
                                              kind=self.wx.ITEM_NORMAL, 
                                              text=u'Underline')
        
        self.editorPopUpMenuItemOblique = self.editorPopUp.Append(help='Oblique',
                                              id=-1, 
                                              kind=self.wx.ITEM_NORMAL, 
                                              text=u'Oblique')
        
        self.editorPopUpMenuItemBold = self.editorPopUp.Append(help='Bold',
                                              id=-1, 
                                              kind=self.wx.ITEM_NORMAL, 
                                              text=u'Bold')
        
        self.editorPopUpMenuItemLine_through = self.editorPopUp.Append(help='Line Through',
                                              id=-1, 
                                              kind=self.wx.ITEM_NORMAL, 
                                              text=u'Line Through')
        
        
       


        
    def OnFrameSize(self,event):
        self.splitter2.SetSashPosition(self.Splitter2SashStart)    
        event.Skip()      
        
    def OnStyledTextCtrl1Paint(self, event):
        event.Skip()

    def OnStyledTextCtrl1EraseBackground(self, event):
        event.Skip()
    
    def OnPagesExitMenu(self, event):
        
        self.controller.actionGUIClose()
	

#    def OnHelpItemsAbout(self, event):
#        self.controller.actionShowAbout()
    
    def openSpecialEditor(self,Filename):        
        self.controller.actionSpecialEdit(Filename)
    
    
    
    def Password(self, Question):
        """
        user input Dialog for Password 
        returns a string or None
        """
        value = None
        dlg = wx.TextEntryDialog(
            self, Question,
            '','', wx.TE_PASSWORD | wx.CENTER | wx.CANCEL | wx.OK )

        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()

        dlg.Destroy()
        #print "PASSW VALUE ", value
        return value
    
    
    
    def InputWithValue(self, question="?", value=""):
        """
        user input Dialog 
        returns a string or None
        """
        dlg = wx.TextEntryDialog(self, question, 'Question', value)

        value = None
        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()

        dlg.Destroy()
        return value
    
    
    def SingleChoiceDialog(self, choices, title="", message="Please choose..."):
        
        value = None
        dlg = wx.SingleChoiceDialog(
                self, message, title,
                choices, 
                wx.CHOICEDLG_STYLE
                )

        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetStringSelection()

        dlg.Destroy()
        return value
    

    def Input(self, Question="?", title=None):
        """
        user input Dialog 
        returns a string or Null
        """
        value = None
        dlg = wx.TextEntryDialog(
                self, Question,
                title, '')

        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()

        dlg.Destroy()
        return value


    # Tree functions 
#    def OnActivate(self, event):
#        event.Skip()

  

    def OntreeEdit(self, event):
        self.controller.actionOnEditTreeItem(event)

    def OntreeEditEnd(self, event):
        self.controller.actionTreeEditFinish(event)

#    def OnHelpItemsTutorial(self, event):
#        self.look_busy()
#        self.controller.actionHelp('#all')
#        self.relax()

    def OnRenameItem(self, event):
        self.controller.actionEditTreeItemLabel()

#    def OnCheckForUpdate(self, event):
#        self.controller.actionCheckForUpdate()

    def OnFeedbackMenu(self, event):
        self.controller.actionFeedback()
        
    def OnPreviewButton(self, event):
        self.controller.actionPreview()
    
#    def OnSaveButton(self, event):
#        self.controller.actionSave(event)

    def OnSystemSystemsetupMenu(self, event):
        self.Message("this would be some code - code")
        event.Skip()
            
   
            
    def OnExtraEditbodyMenu(self, event):
        self.controller.actionEditBody()

    def OnExtraEditfootMenu(self, event):
        self.controller.actionEditFoot()

    def OnFiletypesHeadMenu(self, event):
        self.controller.editHead()
   
    def OnFtpDistributiontableMenu(self, event):
        self.controller.actionEditDistributionTable()
    
    def OnFtpUploadMenu(self, event):
        self.controller.actionPublish()

    def OnProjectProject_setupMenu(self, event):
        self.controller.actionProjectSetup()
           
#    def OnLanguagesEnglishMenu(self, event):
#        try:
#            self.controller.actionSwitchLanguage("en")
#        except:
#            pass
#
#    def OnLanguagesDeutschMenu(self, event):
#        try:
#            self.controller.actionSwitchLanguage("de")
#        except:
#            pass
    
    def OnImagesAddimageMenu(self, event):
        self.controller.actionAddImage()
    
    # several dialogs    
    
    
    def ImageDialogWithDir(self, dir):        
        """
        Display an image select dialog
        returns filename of image
        returns None if no image was selected
        """
        dlg = ib.ImageDialog(self, dir)
        
        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:            
            
            if dlg.GetDirectory() == dir:
            
                Image = dlg.GetFile()
            
            else:
                self.Error("Image is not in the project folder ! Please import first...")
                Image = None
            
        else:
           
           Image = None
        
        dlg.Destroy()
        
        return Image
 
 
 

    def ImageDialog(self):
        """
        Display an image select dialog
        returns filename of image
        returns None if no image was selected
        """
                
        dlg = ib.ImageDialog(self)
        

        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            Image=dlg.GetFile()
        else:
            Image=None
        dlg.Destroy()
        
        return Image
        
    def Ask_YesOrNo(self,Message):
        """Returns Yes or No."""

        dlg = wx.MessageDialog(self, Message,
          'Question', wx.YES | wx.NO | wx.ICON_QUESTION)
        try:
            ret = dlg.ShowModal()
        finally:
            dlg.Destroy()
        
        if ret == wx.ID_YES:
            Answer = 'Yes'
        elif ret == wx.ID_NO:
            Answer = 'No'
           
        
        return Answer

    
    def doShell(self, frame, nb=None, log=None):
        
        frame = ShellFrame(self, -1, "Python Shell", size=(700, 400), pos=(150,150),
        style = wx.DEFAULT_FRAME_STYLE)
        
        frame.Show(True)
        
        return frame.getShell()
    
    

    def Ask(self,Message):
        """
        returns Ok or Cancel
        """
        dlg = wx.MessageDialog(self, Message,
          'Question', wx.OK | wx.CANCEL | wx.ICON_WARNING)
        try:
            ret = dlg.ShowModal()
        finally:
            dlg.Destroy()
        
        if ret == wx.ID_OK:
            Answer = 'Ok'
        elif ret == wx.ID_CANCEL:
            Answer = 'Cancel'
           
        
        return Answer
        
    
    def MessageNotModal(self, Message):    
        
        
        dlg = wx.MessageDialog(self, Message,
          'Info', wx.OK | wx.ICON_INFORMATION)
        dlg.Show()
          
    
    def Message(self,Message):    
        
        dlg = wx.MessageDialog(self, Message,
          'Info', wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
      
        return
 
    def Warning (self,Message):
        
        #self.errorhandler.write(Message)
        dlg = wx.MessageDialog(self, Message,
          'Alert', wx.OK | wx.ICON_EXCLAMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        
        
        
        return
       
          
    def Error(self,Message):
        
        #sys.stderr.write(Message)
        dlg = wx.MessageDialog(self, Message,
          'Error', wx.OK | wx.ICON_ERROR)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        
        
        
        return
        
    # -------
    #
    # some functions for a pulsing progress bar
    #
    
        
    def PulseProgress(self, Message=""):
                
        self.PulseBar = self.GetLastProgressBar()
        self.PulseBar.Pulse(Message)
        self.fitRefreshAndCenter(self.PulseBar)

        
    
    # ------- Pulse stuff end -----------------------------------------------
    
#    def ShowProgress(self,max,Message):
#        
#
#        self.Progress = wx.ProgressDialog("Progress...",
#                               Message,
#                               maximum = max,
#                               parent=self,
#                               style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
#        self.AddProgressBar(self.Progress)
#
#
#    def UpdateProgress(self,count):
#        #print self.Progress.max
#        Bar = self.GetLastProgressBar()
#        Bar.Update(count)
#        self.fitRefreshAndCenter(Bar)
#
#        
#    
#    def UpdateProgressMessage(self,count,message):
#        Bar = self.GetLastProgressBar()
#        Bar.Update(count,message)
#        self.fitRefreshAndCenter(Bar)
        
    
    def fitRefreshAndCenter(self, widget):
        """
        is calling .Fit(), .Refresh() and .CenterOnScreen() for the widget
        """
        
        widget.Fit()
        widget.Refresh()
        widget.CenterOnScreen()
    
    
    
#    def KillProgress(self):
#        try:
#          Bar = self.GetLastProgressBar()
#          self.DeleteProgressBar(Bar)
#          Bar.Destroy()
#          if self.keepGoing:
#              self.StopPulse()
#        except:
#          print "unable to Kill Progress Bar"
#    
#    def DeleteProgressBar(self,ThisOne):
#        """
#        ! is deleting the instance from the stack 
#                
#        """                        
#        self.ProgressBars.remove(ThisOne)
#        
#                               
#    def AddProgressBar(self,ThisOne):
#        """
#        ThisOne is an instance of a wxProgressbar
#        """
#        self.ProgressBars.append(ThisOne)                       
#    
#    
#    def GetLastProgressBar(self):
#        """
#        returns the instance of the progressbar that was last added to the stack
#        """
#        
#        return self.ProgressBars[-1]
#    
#    
#    def GetAllProgressBars(self):    
#        return self.ProgressBars
#    
#    
    
    
    
    def OnDeleteFile(self, event):        
        self.controller.actionDeleteCurrentFile()


    

    # here are the tag tools
    def OnP_buttonButton(self, event):
        self.insert_xhtml_tag(['<p>','</p>'])

    def OnBr_buttonButton(self, event):
        self.insert_xhtml_tag(['<br />'])

    def OnH1_buttonButton(self, event):
        self.insert_xhtml_tag(['<h1>','</h1>'])

    def OnHr_buttonButton(self, event):
        self.insert_xhtml_tag(['<hr />'])

    def OnA_buttonButton(self, event):
        self.insert_xhtml_tag(['<a href=" ">','</a>'])

    def Onul_buttonButton(self, event):
        self.insert_xhtml_tag(['<ul>','</ul>'])
        #event.Skip()


    def Onli_buttonButton(self, event):
        self.insert_xhtml_tag(['<li>','</li>'])
        #event.Skip()
        
    def Onol_buttonButton(self, event):
        self.insert_xhtml_tag(['<ol>','</ol>'])
        #event.Skip()


   

    def OnImageButton(self, event):
        
        dir = self.cms.path_parts+'gfx/'
        #print dir
        # set the initial directory for the demo bitmaps
        initial_dir = os.path.join(dir, 'bitmaps')

        # open the image browser dialog
        dlg = ib.ImageDialog(self, dir)

        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            
            # show the selected file
            #print "You Selected File: " + dlg.GetFile()
            Image=dlg.GetFile()
            
        else:
           pass
        dlg.Destroy()
        
        
        
        try:
            Image=os.path.split(Image)
            Image=Image[1]
            self.styledTextCtrl1.AddText('<img src="'+self.cms.url+self.cms.gfxFolder+Image+'" align="left" alt="'+Image+' " />')
            self.saved= False
            #self.saveButton.Enable()
            #self.publishButton.Enable()
        except:
            pass
    
    
    
    def OnProjectEdittemplatesMenu(self, event):
        self.controller.actionEditTemplate()

    def OnImagesDelete_imageMenu(self, event):
        self.controller.actionDeleteImage()

          
    
    def OnPagesAddprojectMenu(self, event):
        self.controller.addNewProject()

    

    def OnFtpBrowseServerMenu(self, event):        
        self.look_busy()
        
        path = self.controller.actionBrowseServer() 
        #print "this is the returned path", path
        self.relax()        

    def look_busy(self):
        #print 'getting busy'
        cursor = wx.StockCursor(wx.CURSOR_WATCH)
        wx.BeginBusyCursor(cursor)
        
   
    def busy(self):
        #print 'getting busy'
        cursor = wx.StockCursor(wx.CURSOR_WATCH)
        wx.BeginBusyCursor(cursor)
   
   
    def relax(self):
        
        if wx.IsBusy()==True:
            wx.EndBusyCursor()
        else:
            pass
        
        print 'done...'
        

  

    
    
    
    def OnEditReduceMenu(self,event):
        #size = str((self.tree.GetFont()).GetPointSize())
        """
        reduce the editor font
        """
        
        zoom = self.styledTextCtrl1.GetZoom()
        
        
        newZoom=int(zoom)-1
        try:
            self.styledTextCtrl1.SetZoom(newZoom)
        except:
            self.Error("You cannot reduce the Font size any further...")
        #event.Skip()
        
        
   




    
    def OnaddToListButton(self,event):
        self.Message("this is not working")
        #event.Skip()
    
    
    
    
    
    def Version(self):
        
        return "0.5.9"
        
  
    def ColorDialog(self):

        dlg = wx.ColourDialog(self)

        # Ensure the full colour dialog is displayed, 
        # not the abbreviated version.
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will
            # contain valid information. Fetch the data ...
            data = dlg.GetColourData()
            self.color_data = str(data.GetColour().Get())
            
            

            # ... then do something with it. The actual colour data will be
            # returned as a three-tuple (r, g, b) in this particular case.
            

        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()






    def SelectProject(self):

        dlg = wx.DirDialog(self, "Select a project to import:",
        style=wx.DD_DEFAULT_STYLE)
    
            # If the user selects OK, then we process the dialog's data.
            # This is done by getting the path data from the dialog - BEFORE
            # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
        
            return  dlg.GetPath()
        else:
            return None



   
        
 # --------------------------------------------------------------------------
    
  
    def getFileFromUser(self, dir=None, prompt = None):
 
        if not dir:
            dir = os.getcwd()
            
        if not prompt:
            prompt = "Choose a file..." 
        
        wildcard = "all files (*.*)|*.*|"                   \
             "content Files (*.content)|*.content|"           \
             "CSS Files (*.css)|*.css|"                       \
             "CGI scripts (*.cgi)|*.cgi|"                     \
             "Javascript file (*.js)|*.js|"                   \
             "plain Text file (*.txt)|*.txt|"                 \
             "maker Dynamic (*.dynamic)|*.dynamic"            \
             "Quicktime movie (*.mov) | *.mov"
        
        dlg = wx.FileDialog(
              self.topPanel, message = prompt, style=wx.OPEN | wx.CHANGE_DIR )
  
              # If the user selects OK, then we process the dialog's data.
              # This is done by getting the path data from the dialog - BEFORE
              # we destroy it.
        try:
            dlg.ShowModal()
  
        finally:
  
            paths =  dlg.GetPaths()
            dlg.Destroy()
            return paths

               

 # ------------------------------------------------------------------------
        
        
    
    def getDirFromUser(self, dialogMessage = None):

        self.dirDialog = wx.DirDialog(self, message = dialogMessage,
                                      style=wx.DD_DEFAULT_STYLE|
                                      wx.DD_NEW_DIR_BUTTON)
        
        
          
# ------------------------------------------------------------------------
 


class MySplitter(wx.SplitterWindow):
    def __init__(self, parent, ID, log):
        wx.SplitterWindow.__init__(self, parent, ID,
                                   style = wx.SP_3D
                                   | wx.SP_LIVE_UPDATE)
        
        
class MyArtProvider(wx.ArtProvider):
    def __init__(self):
        wx.ArtProvider.__init__(self)
        

    def CreateBitmap(self, artid, client, size):
       
        bmp = wx.NullBitmap
        bmp = makeCustomArt()

        return bmp        


class ShellFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):

        
        self.parent = parent
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.shell = pyShell.shell.Shell(self, -1, introText="")
        self.shell.zoom(-1)
        self.Bind(wx.EVT_CLOSE,  self.onClose)
 
    
 
    def onClose(self, event):
        
        w = "Your script is still running! "
        w += "Wait for it to finish or kill it..."
        
        if not self.shell.GetText().endswith(">>> "):
            self.parent.Warning(w)
            return
        
        self.Destroy()
 
    def getShell(self):
        return self.shell



def makeCustomArt():
    
    return wx.Image(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/makerPart.png"), 
                                 wx.BITMAP_TYPE_PNG).ConvertToBitmap()
   
