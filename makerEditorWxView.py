import wx
import wx.stc
from wx.lib.anchors import LayoutAnchors

#wx.LIGHT_GREY

if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 10,
             }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Monaco',
              'helv' : 'Helvetica',
              'other': 'Comic Sans MS',
              'size' : 13,
              'size2': 12,
              'size3': 10,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'Courier',
              'size' : 10,
              'size2': 8,
             }


class editorView:
        def __init__(self, parent, fileType):        
        
            self.editor = wx.stc.StyledTextCtrl(id=-1,
                  name='makerEditorView', parent=parent, pos=wx.Point(192, 87),
                  size=wx.Size(160, 120), style=wx.VSCROLL | wx.HSCROLL)
            
      
            self.editor.SetAutoLayout(True)
            self.editor.SetConstraints(LayoutAnchors(self.editor,
                  True, True, True, True))
            #self.editor.SetText(self.BoilerPlate)
            self.editor.SetThemeEnabled(True)
            
            #self.editor.SetLexer(wx.stc.STC_LEX_HTML)
            
            self.editor.SetStyleBits(7)
        
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleClearAll()  # Reset all to be like the default
            
            self.editor.SetTabIndents(1)
            self.editor.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
            
            if fileType == ".py":
                                
                kw =  [
        #--start keywords--
                'and',
                'assert',
                'break',
                'class',
                'continue',
                'def',
                'del',
                'elif',
                'else',
                'except',
                'exec',
                'finally',
                'for',
                'from',
                'global',
                'if',
                'import',
                'in',
                'is',
                'lambda',
                'not',
                'or',
                'pass',
                'print',
                'raise',
                'return',
                'try',
                'while',
                #--end keywords--
                ]
                self.editor.SetLexer(wx.stc.STC_LEX_PYTHON)
                self.editor.SetKeyWords(0, " ".join(kw))
                #self.editor.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:#cccccc,face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:#007f00,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:#007f7f,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_STRING, "fore:#7f007f,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:#7f007f,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_WORD,  "fore:#00007F,bold,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:#7f0000,face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_P_DECORATOR, "fore:#777777,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:#7f0000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:#0000FF,bold, size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:#007f7f,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_OPERATOR, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:#7f7f7f,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                
        
            elif fileType == ".content": 
                
                self.editor.SetLexer(wx.stc.STC_LEX_HTML)
                self.editor.StyleSetSpec(wx.stc.STC_H_DEFAULT, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                # HTML tags
                self.editor.StyleSetSpec(wx.stc.STC_H_TAG, "fore:#882288,bold,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, "fore:#993300,bold,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTEUNKNOWN, "fore:#993300,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_TAGEND, "fore:#882288,bold,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_OTHER, "fore:#993300,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_COMMENT, "fore:#006600,face:%(other)s,size:%(size)d" % faces)
                    
                self.editor.StyleSetSpec(wx.stc.STC_H_SINGLESTRING, "fore:#2200bb,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, "fore:#2200bb,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_NUMBER, "fore:#00ff00,face:%(other)s,size:%(size)d" % faces)
            
            elif fileType == ".php": 
                
                self.editor.SetLexer(wx.stc.STC_LEX_HTML)
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_DEFAULT, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_COMMENT, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_COMMENTLINE, "fore:#00aa00,face:%(other)s,size:%(size)d" % faces)
                    # " foo "
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_HSTRING, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_HSTRING_VARIABLE, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_NUMBER, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)
                    # {} () = 
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_OPERATOR, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_SIMPLESTRING, "fore:#2244bb,face:%(other)s,size:%(size)d" % faces)
                    # $foo
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_VARIABLE, "fore:#993300,face:%(other)s,size:%(size)d" % faces)
                    
                self.editor.StyleSetSpec(wx.stc.STC_HPHP_WORD, "fore:#ff0000,face:%(other)s,size:%(size)d" % faces)
            
            elif fileType == ".css":
                
                self.editor.SetLexer(wx.stc.STC_LEX_CSS)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_DEFAULT, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_OPERATOR, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_TAG, "fore:#0000aa,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_DOUBLESTRING, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_SINGLESTRING, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_CLASS, "fore:#0000aa,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_COMMENT, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_ID, "fore:#0000aa,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_VALUE, "fore:#882288,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_IDENTIFIER, "fore:#882288,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_VALUE, "fore:#882288,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_ATTRIBUTE, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)


            else: 
                
                self.editor.SetLexer(wx.stc.STC_LEX_HTML)
                self.editor.StyleSetSpec(wx.stc.STC_H_DEFAULT, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
                # HTML tags
                self.editor.StyleSetSpec(wx.stc.STC_H_TAG, "fore:#882288,bold,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, "fore:#993300,bold,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTEUNKNOWN, "fore:#993300,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_TAGEND, "fore:#882288,bold,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_OTHER, "fore:#993300,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_COMMENT, "fore:#006600,face:%(other)s,size:%(size)d" % faces)
                    
                self.editor.StyleSetSpec(wx.stc.STC_H_SINGLESTRING, "fore:#2200bb,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, "fore:#2200bb,face:%(mono)s,size:%(size2)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_NUMBER, "fore:#00ff00,face:%(other)s,size:%(size)d" % faces)

            
            # Global default styles for all languages
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     "fore:#000000,face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  "fore:#777777,back:#eeeeee,face:%(mono)s,size:%(size3)d"  % faces)
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "fore:#ff0000, face:%(other)s" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")
        
            # default word wrapping            
            self.editor.SetWrapMode(wx.stc.STC_WRAP_WORD)
                                    
            self.editor.SetCurrentPos(0)
            
            self.editor.SetEdgeMode(wx.stc.STC_EDGE_LINE)
            self.editor.SetEdgeColumn(200)
            
            self.editor.SetHighlightGuide(1)
            self.editor.SetIndentationGuides(False)
            self.editor.SetCaretWidth(1)
            self.editor.SetControlCharSymbol(0)
            self.editor.SetCaretLineVisible(True)
            self.editor.SetCaretLineBack(wx.Colour(240, 246, 254))
          
            self.editor.SetCaretForeground("BLUE")
            self.editor.SetSelBackground(True, "#b5d4ff")
            self.editor.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
            # Text Margins    
            self.editor.SetMargins(10, 10)
            self.editor.SetMarginWidth(0, 25)
            self.editor.SetMarginWidth(1, 5)
            
            self.editor.UsePopUp(0)   
        
        def OnKeyDown(self, evt):
            """ keep current indent level """
            if evt.GetKeyCode() == wx.WXK_RETURN:
                pass
            evt.Skip()
            return 
        
        
