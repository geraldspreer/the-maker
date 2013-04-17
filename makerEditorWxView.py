import wx
import wx.stc
from wx.lib.anchors import LayoutAnchors



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
              'other': 'Monaco',
              'size' : 11,
              'size2': 11,
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
        
            self.editor.StyleClearAll()  # Reset all to be like the default
            
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
                       
            elif fileType == ".css":
                
                self.editor.SetLexer(wx.stc.STC_LEX_CSS)

            else: 
                
                self.editor.SetLexer(wx.stc.STC_LEX_HTML)
                    
            self.applyCodeStyle(style = None)
        
            # default word wrapping            
            self.editor.SetWrapMode(wx.stc.STC_WRAP_WORD)
                                    
            self.editor.SetCurrentPos(0)
            
            self.editor.SetEdgeMode(wx.stc.STC_EDGE_LINE)
            self.editor.SetEdgeColumn(200)
            
            self.editor.SetHighlightGuide(1)
            # indentation
            self.editor.SetIndentationGuides(False)
            self.editor.SetIndent(4)
            
            self.editor.SetCaretWidth(1)
            self.editor.SetControlCharSymbol(0)
            self.editor.SetCaretLineVisible(True)
            

            self.editor.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
            # Text Margins    
            self.editor.SetMargins(10, 10)
            self.editor.SetMarginWidth(0, 25)
            self.editor.SetMarginWidth(1, 5)
            
            self.editor.UsePopUp(0)   
        
        
        def applyCodeStyle(self, style = None ):
            # make use style passed to it.
            
            style = {'comment':{'color':'#bc9458','font-style':'italic'},
                'constant.numeric':{'color':'#a5c261','font-weight':'normal'},
                'constant.numeric.keyword':{'color':'#6d9cbe'},
                'keyword':{'color':'#cc7833','font-strike-through':'none','font-weight':'normal'},
                'keyword.control':{'color':'#cc7833'},
                'keyword.type':{'color':'#cc7833'},
                'language.function':{'color':'#fac56d'},
                'language.operator':{'color':'#b96619'},
                'language.variable':{'color':'#d0d1ff'},
                'markup.comment':{'color':'#bc9458','font-style':'italic'},
                'markup.constant.entity':{'color':'#6e9cbe'},
                'markup.declaration':{'color':'#e8c06a'},
                'markup.inline.cdata':{'color':'#e9c053'},
                'markup.processing':{'color':'#68685b','font-weight':'bold'},
                'markup.tag':{'color':'#e8c06a'},  #
                'markup.tag.attribute.name':{'color':'#e8c06a'},
                'markup.tag.attribute.value':{'color':'#a5c261','font-style':'italic'},
                'meta.default':{'background-color':'#2b2b2b','color':'#e6e1dc'},
                'meta.highlight.currentline':{'background-color':'#d9d9d9'},
                'meta.important':{'color':'#b66418','font-style':'italic'},
                'meta.invalid':{'background-color':'#990201','color':'#ffffff','font-weight':'bold'},
                'meta.invisible.characters':{'color':'#404040'},
                'meta.link':{'color':'#a5c261','font-style':'normal','font-underline':'none'},
                'string':{'color':'#a5c261','font-style':'italic'},
                'string.regex':{'color':'#99b93e'},
                'string.regex.escaped':{'color':'#4b8928'},
                'style.at-rule':{'color':'#b96619','font-weight':'bold'},
                'style.comment':{'color':'#bc9458','font-style':'italic','font-weight':'normal'},
                'style.property.name':{'color':'#6e9cbe'},
                'style.value.color.rgb-value':{'color':'#6d9cbe'},
                'style.value.keyword':{'color':'#a5c261'},
                'style.value.numeric':{'color':'#99b62d'},
                'style.value.string':{'color':'#a5c261','font-style':'italic'},
                'support':{'color':'#da4939'}
                }
                
#            self.editor.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:#007f00,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:#007f7f,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_STRING, "fore:#7f007f,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:#7f007f,face:%(other)s,size:%(size)d" % faces)                
#            self.editor.StyleSetSpec(wx.stc.STC_P_WORD,  "fore:#00007F,bold,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:#7f0000,face:%(other)s,size:%(size)d" % faces)
#                
#            self.editor.StyleSetSpec(wx.stc.STC_P_DECORATOR, "fore:#777777,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:#7f0000,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:#0000FF,bold, size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:#007f7f,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_OPERATOR, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:#7f7f7f,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
#                
#        
   
#                
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_DEFAULT, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_COMMENT, "fore:#00aa00,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_COMMENTLINE, "fore:#00aa00,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_HSTRING, "fore:#aaaa00,face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_HSTRING_VARIABLE, "fore:#00aa00,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_NUMBER, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)
#                    # {} () = 
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_OPERATOR, "fore:#00aa00,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_SIMPLESTRING, "fore:#2244bb,face:%(other)s,size:%(size)d" % faces)
#                    # $foo
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_VARIABLE, "fore:#993300,face:%(other)s,size:%(size)d" % faces)
#                    
#            self.editor.StyleSetSpec(wx.stc.STC_HPHP_WORD, "fore:#ff0000,face:%(other)s,size:%(size)d" % faces)
#            
#                
#            self.editor.SetLexer(wx.stc.STC_LEX_CSS)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_DEFAULT, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_OPERATOR, "fore:#000000,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_TAG, "fore:#0000aa,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_DOUBLESTRING, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_SINGLESTRING, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_CLASS, "fore:#0000aa,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_COMMENT, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_ID, "fore:#0000aa,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_VALUE, "fore:#882288,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_IDENTIFIER, "fore:#882288,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_VALUE, "fore:#882288,face:%(other)s,size:%(size)d" % faces)
#            self.editor.StyleSetSpec(wx.stc.STC_CSS_ATTRIBUTE, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces)
#
#
#                
            
           # misc stuff
            self.editor.SetCaretLineBack(style["meta.default"]['background-color'])
            self.editor.SetCaretForeground(style["meta.highlight.currentline"]['background-color'])
            self.editor.SetSelBackground(True, "#b5d4ff")
            
             
            # HTML Styles
            
            # <p>[This is text]</p>
            self.editor.StyleSetSpec(wx.stc.STC_H_DEFAULT,     "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # [<p>]This is text</p>
            self.editor.StyleSetSpec(wx.stc.STC_H_TAG, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # ??
            self.editor.StyleSetSpec(wx.stc.STC_H_TAGUNKNOWN, "fore:" + style["meta.invalid"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # <img src="foo" [/>]
            self.editor.StyleSetSpec(wx.stc.STC_H_TAGEND, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # [href]
            self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, "fore:" + style["markup.tag.attribute.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            #  ["doublestring"]
            self.editor.StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            #  ['singlestring'] 
            self.editor.StyleSetSpec(wx.stc.STC_H_SINGLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # [<!-- comment -->]
            self.editor.StyleSetSpec(wx.stc.STC_H_COMMENT, "fore:" + style["markup.comment"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # vspace = [4] 
            self.editor.StyleSetSpec(wx.stc.STC_H_NUMBER, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # vspace [=] 4
            self.editor.StyleSetSpec(wx.stc.STC_H_OTHER, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # [&amp;]
            self.editor.StyleSetSpec(wx.stc.STC_H_ENTITY, "fore:" + style["markup.constant.entity"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            #self.editor.StyleSetSpec(wx.stc.STC_H_XMLSTART, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            #self.editor.StyleSetSpec(wx.stc.STC_H_XMLEND, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # [<?php ]  [?>]
            self.editor.StyleSetSpec(wx.stc.STC_H_QUESTION, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # ??
            self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTEUNKNOWN, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            self.editor.StyleSetSpec(wx.stc.STC_H_CDATA, "fore:" + style["markup.inline.cdata"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            self.editor.StyleSetSpec(wx.stc.STC_H_SCRIPT, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
         
            self.editor.StyleSetSpec(wx.stc.STC_H_SGML_DEFAULT, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_H_SGML_ERROR, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            self.editor.StyleSetSpec(wx.stc.STC_HJ_DEFAULT, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            # <script>[ ]
            self.editor.StyleSetSpec(wx.stc.STC_HJ_START, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            self.editor.StyleSetSpec(wx.stc.STC_HJ_WORD, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HJ_SINGLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HJ_DOUBLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HJ_NUMBER, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
            
            self.editor.StyleSetSpec(wx.stc.STC_HJ_SYMBOLS, "fore:" + style["language.operator"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HJ_STRINGEOL, "fore:" + style["keyword"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            
         
            
            # php is part of the html lexer
            # {} () = 
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_OPERATOR, "fore:" + style["language.operator"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)

            self.editor.StyleSetSpec(wx.stc.STC_HPHP_DEFAULT, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
 
                                     
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_COMMENT, "fore:" + style["markup.comment"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_COMMENTLINE, "fore:" + style["markup.comment"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
 


            self.editor.StyleSetSpec(wx.stc.STC_HPHP_HSTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_SIMPLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
 
            
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_VARIABLE, "fore:" + style["language.variable"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_HSTRING_VARIABLE, "fore:" + style["language.variable"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
 
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_NUMBER, "fore:" + style["constant.numeric.keyword"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
  
                                     
            self.editor.StyleSetSpec(wx.stc.STC_HPHP_WORD, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
 
         
            # hack for unidentified entities
            self.editor.SetBackgroundColour(style["meta.default"]['background-color'])
            
              # Global default styles for all languages
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size3)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,  "fore:#ff0000,back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size3)d" % faces)
            
        
        
        
        def OnKeyDown(self, evt):
            """ keep current indent level """
            if evt.GetKeyCode() == wx.WXK_RETURN:
                pass
            evt.Skip()
            return
        
        def OnCharAdded(self, evt):
            """ keep current indent level """
            for it in dir(evt):
                print it 
            
            
        
