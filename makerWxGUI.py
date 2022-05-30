# -*- coding: latin-1 -*-

import os
import sys
import shutil
import string

import makerEditorWxView
import makerCopyright
import wx.lib.buttons
import wx.gizmos
import wx.lib.imagebrowser as ib
from wx.lib.anchors import LayoutAnchors
import wx.lib.flatnotebook as nb
import wx.py as pyShell
import math

# Used on OSX to get access to carbon api constants
if wx.Platform == '__WXMAC__':
    import Carbon.Appearance


def create(app):
    return wxPythonGUI(app)

class wxPythonGUI(wx.Frame):
    def _init_coll_boxSizer1_Items(self, parent):
        parent.Add(self.splitter, 1, border=0, flag=wx.EXPAND | wx.GROW)

    def _init_coll_boxSizer2_Items(self, parent):
        pass

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
        self.MenuItemComment = parent.Append(help='Insert Comment !',
                           id=-1,
                           kind=wx.ITEM_NORMAL, 
                           text=u'Comment\tCtrl+Shift+c'
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
                                                 text=u'Publish\tCtrl+u'
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
        parent.Append(wx.ID_ABOUT,   "&About")

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

        self.subMenuStructure = wx.Menu(title=u'')
        self.subMenuMeta_Information = wx.Menu(title=u'')
        self.subMenuText = wx.Menu(title=u'')
        self.subMenuLinks = wx.Menu(title=u'')
        self.subMenuImages_and_Objects = wx.Menu(title=u'')
        self.subMenuLists = wx.Menu(title=u'')
        self.subMenuTables = wx.Menu(title=u'')
        self.subMenuForms = wx.Menu(title=u'')
        self.subMenuScripting = wx.Menu(title=u'')
        self.subMenuPresentational = wx.Menu(title=u'')
        self.subMenuHTML = wx.Menu(title=u'')
        self.subMenuCSS = wx.Menu(title=u'')
        
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
        text=u'<div>   Division. Defines a block of HTML\tCtrl+Shift+D')
        
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

        self._init_coll_code_Items(self.insert)

    def _init_sizers(self):
        # generated method, don't edit

        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self.SetSizer(self.boxSizer1)

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
        self.splitter = MySplitter(self, -1,None)

# and the stc is added to it

        # it is very important to keep the NODRAG style
        #
        # if dragging is added at some point the 
        # makerProjectController.py method noteBookPageClosed has to be
        # changed where the noteBoolPages dict is updated
        #

        self.noteBook = MyCustomNoteBook(self.splitter, -1, None, None)
        self.noteBook.SetPadding(wx.Size(20))
        # add a welcome message to the noteBook        
        self.styledTextCtrl1 = (makerEditorWxView.editorView(self, "default")).editor
        self.welcomeId = self.styledTextCtrl1.GetId()
        self.noteBook.AddPage(self.styledTextCtrl1, "Thank you for using The Maker.")
        self.styledTextCtrl1.SetText(self.BoilerPlate)
        self.listWindow = wx.Panel(self.splitter, -1, style = wx.NO_BORDER)
        self.listSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.tree = wx.TreeCtrl(self.listWindow, -1, 
                                style=wx.TR_HAS_BUTTONS
                                |wx.TR_LINES_AT_ROOT
                                |wx.TR_DEFAULT_STYLE)
        
        def drawAfterPaint(evt):
            Size = self.tree.GetClientSizeTuple()
            dc = wx.ClientDC(self.tree)
            dc.SetPen(self.treePen)
            dc.DrawLine(Size[0]-1, 0, 
                        Size[0]-1, Size[1])
           
        def onTreePaint(evt):
            wx.CallAfter(drawAfterPaint, evt)
            evt.Skip()
            
        self.treePen = wx.Pen('#666666', 1)
        self.tree.Bind(wx.EVT_PAINT, onTreePaint)
        image_size = (16,16)

        projectArt = wx.Image(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/114.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        folderArt = wx.Image(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/99.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        folderOpenArt = wx.Image(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/107.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        fileArt = wx.Image(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/93.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        fileChangeArt = wx.Image(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/118.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        partArt = wx.Image(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/24-16.png"), 
                              wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        
        il = wx.ImageList(image_size[0], image_size[1])
        self.projidx     = il.Add(projectArt)
        self.fldridx     = il.Add(folderArt)
        self.fldropenidx = il.Add(folderOpenArt)
        self.fileidx     = il.Add(fileArt)
        self.filechange  = il.Add(fileChangeArt)
        self.part = il.Add(partArt)
        
        #self.partArt(il, image_size)
        
        self.tree.SetImageList(il)
        self.il = il
   
        self.listSizer.Add(self.tree, 1, border=0, flag=wx.EXPAND)
            
        self.listWindow.SetAutoLayout(True)
        self.listWindow.SetSizer(self.listSizer)
        self.listSizer.Fit(self.listWindow)

        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SplitVertically(self.listWindow, self.noteBook, 180)    

        self.toolBar = self.CreateToolBar( style =  wx.TB_HORIZONTAL
            | wx.NO_BORDER
            #| wx.TB_FLAT
            | wx.TB_TEXT
            )
        
        self.search = wx.SearchCtrl(self.toolBar, id= -1,  pos=(750,-1), size=(180,25), style=wx.TE_PROCESS_ENTER)
        
        #extract the searchCtrl's textCtrl 
        self.searchStatus = wx.StaticText(self.toolBar, -1, size=wx.DefaultSize, pos=wx.DefaultPosition, style=0)             
        self.searchStatus.SetLabel("                         ")
        
        saveArt = wx.Bitmap(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/23.png"))
        
        publishArt = wx.Bitmap(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/53.png"))
        previewArt = wx.Bitmap(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/25.png"))
        makeAllArt = wx.Bitmap(os.path.join(os.path.dirname(sys.argv[0]), 
                                 "./system/ToolBarIcons/24.png"))
        self.toolBar.AddSeparator()

        self.toolBar.AddLabelTool(10, "Save", saveArt)
        self.toolBar.AddLabelTool(20, "Publish", publishArt)
        self.toolBar.AddLabelTool(30, "Preview", previewArt)
        self.toolBar.AddLabelTool(40, "Make All", makeAllArt)
        
        self.toolBar.AddStretchableSpace()

        self.toolBar.AddControl(self.searchStatus)
        self.toolBar.AddControl(self.search)
        
        self.toolBar.Realize()
        
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

    def Input(self, Question="?", title=""):
        """
        user input Dialog 
        returns a string or Null
        """
        value = None
        dlg = wx.TextEntryDialog(
                self, Question,
                title, "")

        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()

        dlg.Destroy()
        return value
   
    def OnFtpDistributiontableMenu(self, event):
        self.controller.actionEditDistributionTable()
    
    #===========================================================================
    #  all kinds of dialogs
    #===========================================================================
    
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
        dlg = wx.MessageDialog(self, Message,
          'Alert', wx.OK | wx.ICON_EXCLAMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        return
          
    def Error(self,Message):
        dlg = wx.MessageDialog(self, Message,
          'Error', wx.OK | wx.ICON_ERROR)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        return
        
    def PulseProgress(self, Message=""):
                
        self.PulseBar = self.GetLastProgressBar()
        self.PulseBar.Pulse(Message)
        self.fitRefreshAndCenter(self.PulseBar)
    
    def fitRefreshAndCenter(self, widget):
        """
        is calling .Fit(), .Refresh() and .CenterOnScreen() for the widget
        """
        widget.Fit()
        widget.Refresh()
        widget.CenterOnScreen()
    
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

    def Onli_buttonButton(self, event):
        self.insert_xhtml_tag(['<li>','</li>'])
        
    def Onol_buttonButton(self, event):
        self.insert_xhtml_tag(['<ol>','</ol>'])

    def OnImageButton(self, event):
        
        dir = self.cms.path_parts+'gfx/'
        # set the initial directory for the demo bitmaps
        initial_dir = os.path.join(dir, 'bitmaps')

        # open the image browser dialog
        dlg = ib.ImageDialog(self, dir)
        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            Image=dlg.GetFile()
        else:
           pass
        dlg.Destroy()
        try:
            Image=os.path.split(Image)
            Image=Image[1]
            self.styledTextCtrl1.AddText('<img src="'+self.cms.url+self.cms.gfxFolder+Image+'" align="left" alt="'+Image+' " />')
            self.saved= False
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
        self.relax()        

    def look_busy(self):
        cursor = wx.StockCursor(wx.CURSOR_WATCH)
        wx.BeginBusyCursor(cursor)
   
    def busy(self):
        cursor = wx.StockCursor(wx.CURSOR_WATCH)
        wx.BeginBusyCursor(cursor)
   
    def relax(self):
        if wx.IsBusy()==True:
            wx.EndBusyCursor()
        else:
            pass
        print 'done...'
    
    def OnEditReduceMenu(self,event):
        """
        reduce the editor font
        """
        zoom = self.styledTextCtrl1.GetZoom()
        newZoom=int(zoom)-1
        try:
            self.styledTextCtrl1.SetZoom(newZoom)
        except:
            self.Error("You cannot reduce the Font size any further...")
    
    def OnaddToListButton(self,event):
        self.Message("this is not working")
    
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
              self, message = prompt, style=wx.OPEN | wx.CHANGE_DIR )
              # If the user selects OK, then we process the dialog's data.
              # This is done by getting the path data from the dialog - BEFORE
              # we destroy it.
        try:
            dlg.ShowModal()
        finally:
            paths =  dlg.GetPaths()
            dlg.Destroy()
            return paths
    
    def getDirFromUser(self, dialogMessage = None):
        self.dirDialog = wx.DirDialog(self, message = dialogMessage,
                                      style=wx.DD_DEFAULT_STYLE|
                                      wx.DD_NEW_DIR_BUTTON)

#===============================================================================
# Custom FlatNoteBook
#===============================================================================

class MyCustomNoteBook(nb.FlatNotebook):
    def __init__(self, parent, ID, 
                 pos=wx.DefaultPosition, 
                 size=wx.DefaultSize, 
                 agwStyle = wx.lib.flatnotebook.FNB_FF2,
                 style= wx.lib.flatnotebook.FNB_NODRAG | wx.lib.flatnotebook.FNB_X_ON_TAB):
    
        self._bForceSelection = False
        self._nPadding = 60
        self._nFrom = 0
        self._pages = None
        self._windows = []
        self._popupWin = None
        self._naviIcon = None
        self._agwStyle = agwStyle
        self._orientation = None
        self._customPanel = None
    
        wx.PyPanel.__init__(self, parent, ID, pos, size, style)
        attr = self.GetDefaultAttributes()
        self.SetOwnForegroundColour(attr.colFg)
        self.SetOwnBackgroundColour(attr.colBg)
    
        self._pages = MyPageContainer(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, style)
    
        self.Bind(wx.EVT_NAVIGATION_KEY, self.OnNavigationKey)
    
        self.Init()
        
class MyPageContainer(nb.PageContainer):
    """
    This class acts as a container for the pages you add to :class:`FlatNotebook`.
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """
        Default class constructor.

        Used internally, do not call it in your code!

        :param `parent`: the :class:`PageContainer` parent;
        :param `id`: an identifier for the control: a value of -1 is taken to mean a default;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the window style.
        """

        self._ImageList = None
        self._iActivePage = -1
        self._pDropTarget = None
        self._nLeftClickZone = nb.FNB_NOWHERE
        self._iPreviousActivePage = -1

        self._pRightClickMenu = None
        self._nXButtonStatus = nb.FNB_BTN_NONE
        self._nArrowDownButtonStatus = nb.FNB_BTN_NONE
        self._pParent = parent
        self._nRightButtonStatus = nb.FNB_BTN_NONE
        self._nLeftButtonStatus = nb.FNB_BTN_NONE
        self._nTabXButtonStatus = nb.FNB_BTN_NONE

        self._nHoveringOverTabIndex = -1
        self._nHoveringOverLastTabIndex = -1

        self._setCursor = False

        self._pagesInfoVec = []

        self._colourTo = wx.SystemSettings_GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        self._colourFrom = wx.WHITE
        self._activeTabColour = wx.WHITE
        self._activeTextColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNTEXT)
        self._nonActiveTextColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNTEXT)
        self._tabAreaColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE)

        self._nFrom = 0
        self._isdragging = False

        # Set default page height, this is done according to the system font
        memDc = wx.MemoryDC()
        memDc.SelectObject(wx.EmptyBitmap(1,1))

        if "__WXGTK__" in wx.PlatformInfo:
            boldFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            boldFont.SetWeight(wx.BOLD)
            memDc.SetFont(boldFont)

        height = memDc.GetCharHeight()
        tabHeight = height + nb.FNB_HEIGHT_SPACER # We use 10 pixels as padding

        wx.PyPanel.__init__(self, parent, id, pos, wx.Size(size.x, tabHeight),
                            style|wx.NO_BORDER|wx.NO_FULL_REPAINT_ON_RESIZE|wx.WANTS_CHARS)

        attr = self.GetDefaultAttributes()
        self.SetOwnForegroundColour(attr.colFg)
        self.SetOwnBackgroundColour(attr.colBg)

        self._pDropTarget = nb.FNBDropTarget(self)
        self.SetDropTarget(self._pDropTarget)
        
        #=======================================================================
        #  Here we plug in our custom Renderer Manager
        #=======================================================================
        
        self._mgr = MyRendererMgr()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnterWindow)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
    def IsTabVisible(self, page):
        """
        Returns whether a tab is visible or not.

        :param `page`: an integer specifying the page index.
        """
        iLastVisiblePage = self.GetLastVisibleTab()
        return page <= iLastVisiblePage and page >= self._nFrom

    def GetLastVisibleTab(self):
        """ Returns the last visible tab in the tab area. """
        if self._nFrom < 0:
            return -1
        ii = 0
        for ii in xrange(self._nFrom, len(self._pagesInfoVec)):
            if self._pagesInfoVec[ii].GetPosition() == wx.Point(-1, -1):
                break

        return ii-1

    def OnSetFocus(self, event=None):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`PageContainer`.
        :param `event`: a :class:`FocusEvent` event to be processed.
        """
        if self._iActivePage < 0:
            if event:
                event.Skip()
            return

        self.SetFocusedPage(self._iActivePage)
        try:
            self.SetSelection(self._iActivePage)
        except:
            pass

# ---------------------------------------------------------------------------- #
# Class FNBRendererMgr
# A manager that handles all the renderers defined below and calls the
# appropriate one when drawing is needed
# ---------------------------------------------------------------------------- #


class MyRendererMgr(nb.FNBRendererMgr):
    """
    This class represents a manager that handles all the 6 renderers defined
    and calls the appropriate one when drawing is needed.
    """

    def __init__(self):
        """ Default class constructor. """

    def GetRenderer(self, style):
        return MakerRenderer()

class MakerRenderer(nb.FNBRenderer):
    def __init__(self):
        """ Default class constructor. """

        self._tabHeight = None
        self.renderPen = wx.Pen("#444444",1 )
        if wx.Platform == "__WXMAC__":
            # Get proper highlight colour for focus rectangle from the
            # current Mac theme.  kThemeBrushFocusHighlight is
            # available on Mac OS 8.5 and higher
            if hasattr(wx, 'MacThemeColour'):
                c = wx.MacThemeColour(Carbon.Appearance.kThemeBrushFocusHighlight)
            else:
                brush = wx.Brush(wx.BLACK)
                brush.MacSetTheme(Carbon.Appearance.kThemeBrushFocusHighlight)
                c = brush.GetColour()
            self._focusPen = wx.Pen(c, 3)

    def DrawTabs(self, pageContainer, dc):
        """
        Actually draws the tabs in :class:`FlatNotebook`.
        :param `pageContainer`: an instance of :class:`FlatNotebook`;
        :param `dc`: an instance of :class:`DC`.
        """
        pc = pageContainer
        if "__WXMAC__" in wx.PlatformInfo:
            # Works well on MSW & GTK, however this lines should be skipped on MAC
            if not pc._pagesInfoVec or pc._nFrom >= len(pc._pagesInfoVec):
                pc.Hide()
                return

        # Get the text hight
        tabHeight = self.CalcTabHeight(pageContainer)
        agwStyle = pc.GetParent().GetAGWWindowStyleFlag()

        # Calculate the number of rows required for drawing the tabs
        rect = pc.GetClientRect()
        clientWidth = rect.width

        # Set the maximum client size
        pc.SetSizeHints(self.GetButtonsAreaLength(pc), tabHeight)
        borderPen = wx.Pen(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNSHADOW))

        backBrush = wx.Brush(pc._tabAreaColour)

        noselBrush = wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE))
        selBrush = wx.Brush(pc._activeTabColour)

        size = pc.GetSize()

        dc.SetTextBackground(pc.GetBackgroundColour())
        dc.SetTextForeground(pc._activeTextColour)
        dc.SetBrush(backBrush)

        # If border style is set, set the pen to be border pen

        colr = pc.GetBackgroundColour()
        dc.SetPen(wx.Pen(colr))

        dc.DrawRectangle(0, 0, size.x, size.y)

        # We always draw the bottom/upper line of the tabs
        # regradless the style
        dc.SetPen(borderPen)

        # Draw labels
        normalFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldFont.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(boldFont)

        posx = pc._pParent.GetPadding()

        # Update all the tabs from 0 to 'pc._nFrom' to be non visible
        for i in xrange(pc._nFrom):

            pc._pagesInfoVec[i].SetPosition(wx.Point(-1, -1))
            pc._pagesInfoVec[i].GetRegion().Clear()

        count = pc._nFrom

        #----------------------------------------------------------
        # Go over and draw the visible tabs
        #----------------------------------------------------------
        x1 = x2 = -1
        for i in xrange(pc._nFrom, len(pc._pagesInfoVec)):
            dc.SetPen(borderPen)
            # Now set the font to the correct font
            dc.SetFont((i==pc.GetSelection() and [boldFont] or [normalFont])[0])

            # Add the padding to the tab width
            # Tab width:
            # +-----------------------------------------------------------+
            # | PADDING | IMG | IMG_PADDING | TEXT | PADDING | x |PADDING |
            # +-----------------------------------------------------------+
            tabWidth = self.CalcTabWidth(pageContainer, i, tabHeight)

            # Check if we can draw more
            if posx + tabWidth + self.GetButtonsAreaLength(pc) >= clientWidth:
                break

            count = count + 1

            # By default we clean the tab region
            pc._pagesInfoVec[i].GetRegion().Clear()

            # Clean the 'x' buttn on the tab.
            # A 'Clean' rectangle, is a rectangle with width or height
            # with values lower than or equal to 0
            pc._pagesInfoVec[i].GetXRect().SetSize(wx.Size(-1, -1))

            # Draw the tab (border, text, image & 'x' on tab)
            self.DrawTab(pc, dc, posx, i, tabWidth, tabHeight, pc._nTabXButtonStatus)

            if pc.GetSelection() == i:
                x1 = posx
                x2 = posx + tabWidth + 2

            # Restore the text forground
            dc.SetTextForeground(pc._activeTextColour)

            # Update the tab position & size
            posy = (pc.HasAGWFlag(wx.lib.flatnotebook.FNB_BOTTOM) and [0] or [wx.lib.flatnotebook.VERTICAL_BORDER_PADDING])[0]

            pc._pagesInfoVec[i].SetPosition(wx.Point(posx, posy))
            pc._pagesInfoVec[i].SetSize(wx.Size(tabWidth, tabHeight))
            self.DrawFocusRectangle(dc, pc, pc._pagesInfoVec[i])

            posx += tabWidth

        # Update all tabs that can not fit into the screen as non-visible
        for i in xrange(count, len(pc._pagesInfoVec)):
            pc._pagesInfoVec[i].SetPosition(wx.Point(-1, -1))
            pc._pagesInfoVec[i].GetRegion().Clear()

        # Draw the left/right/close buttons
        # Left arrow
        self.DrawLeftArrow(pc, dc)
        self.DrawRightArrow(pc, dc)
        self.DrawX(pc, dc)
        self.DrawDropDownArrow(pc, dc)

        if pc.HasAGWFlag(wx.lib.flatnotebook.FNB_FF2):
            self.DrawTabsLine(pc, dc, x1, x2)

    def DrawFocusRectangle(self, dc, pageContainer, page):
        """
        Draws a focus rectangle like the native :class:`Notebook`.

        :param `dc`: an instance of :class:`DC`;
        :param `pageContainer`: an instance of :class:`FlatNotebook`;
        :param `page`: an instance of :class:`PageInfo`, representing a page in the notebook.
        """
        return
    
    def DrawTabsLine(self, pageContainer, dc, selTabX1=-1, selTabX2=-1):
        """
        Draws a line over the tabs.

        :param `pageContainer`: an instance of :class:`FlatNotebook`;
        :param `dc`: an instance of :class:`DC`;
        :param `selTabX1`: first x coordinate of the tab line;
        :param `selTabX2`: second x coordinate of the tab line.
        """
        pc = pageContainer
        clntRect = pc.GetClientRect()
        dc.SetPen(self.renderPen)
        dc.DrawLine(1, clntRect.height, clntRect.width-1, clntRect.height)

    def DrawTab(self, pageContainer, dc, posx, tabIdx, tabWidth, tabHeight, btnStatus):
        """
        Draws a tab using the `Firefox 2` style.

        :param `pageContainer`: an instance of :class:`FlatNotebook`;
        :param `dc`: an instance of :class:`DC`;
        :param `posx`: the x position of the tab;
        :param `tabIdx`: the index of the tab;
        :param `tabWidth`: the tab's width;
        :param `tabHeight`: the tab's height;
        :param `btnStatus`: the status of the 'X' button inside this tab.
        """

        pc = pageContainer

        if tabIdx == pc.GetSelection():
            borderPen = self._focusPen
        else:
            borderPen = wx.Pen("#888888",1)

        #------------------------------------
        # Paint the tab with gradient
        #------------------------------------
        rr = wx.RectPP((posx + 4, nb.VERTICAL_BORDER_PADDING), (posx + tabWidth ,tabHeight))
        nb.DrawButton(dc, rr, pc.GetSelection() == tabIdx , not pc.HasAGWFlag(nb.FNB_BOTTOM))

        #dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(borderPen)

        # Draw the tab as rounded rectangle
        dc.DrawRoundedRectangle(posx + 2, nb.VERTICAL_BORDER_PADDING, tabWidth-2, tabHeight, 4)

        # -----------------------------------
        # Text and image drawing
        # -----------------------------------

        # The width of the images are 16 pixels
        padding = pc.GetParent().GetPadding()
        shapePoints = int(tabHeight*math.tan(float(pc._pagesInfoVec[tabIdx].GetTabAngle())/180.0*math.pi))
        hasImage = pc._pagesInfoVec[tabIdx].GetImageIndex() != -1
        imageYCoord = (pc.HasAGWFlag(nb.FNB_BOTTOM) and [6] or [8])[0]

        if hasImage:
            textOffset = 2*padding + 16 + shapePoints/2
        else:
            textOffset = padding + shapePoints/2

        textOffset += 2

        if tabIdx != pc.GetSelection():

            # Set the text background to be like the vertical lines
            dc.SetTextForeground("#666666")

        if hasImage:
            imageXOffset = textOffset - 16 - padding
            pc._ImageList.Draw(pc._pagesInfoVec[tabIdx].GetImageIndex(), dc,
                               posx + imageXOffset, imageYCoord,
                               wx.IMAGELIST_DRAW_TRANSPARENT, True)

        pageTextColour = pc._pParent.GetPageTextColour(tabIdx)
        if pageTextColour is not None:
            dc.SetTextForeground(pageTextColour)

        dc.DrawText(pc.GetPageText(tabIdx), posx + textOffset, imageYCoord)

        # draw 'x' on tab (if enabled)
        if pc.HasAGWFlag(nb.FNB_X_ON_TAB) and tabIdx == pc.GetSelection():

            textWidth, textHeight = dc.GetTextExtent(pc.GetPageText(tabIdx))
            tabCloseButtonXCoord = posx + textOffset + textWidth + 1

            # take a bitmap from the position of the 'x' button (the x on tab button)
            # this bitmap will be used later to delete old buttons
            tabCloseButtonYCoord = imageYCoord
            x_rect = wx.Rect(tabCloseButtonXCoord, tabCloseButtonYCoord, 16, 16)

            # Draw the tab
            self.DrawTabX(pc, dc, x_rect, tabIdx, btnStatus)

#===============================================================================
# 
#    End Custom Flat Notebook
#
#===============================================================================

class MySplitter(wx.SplitterWindow):
    def __init__(self, parent, ID, log):
        wx.SplitterWindow.__init__(self, parent, ID,
                                   style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH | wx.SP_THIN_SASH)

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
