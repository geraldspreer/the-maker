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
              'size' : 12,
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
                  size=wx.Size(160, 120), style=wx.VSCROLL | wx.HSCROLL )
            
            self.editor.SetAutoLayout(True)
            self.editor.SetConstraints(LayoutAnchors(self.editor,
                  True, True, True, True))
            #self.editor.SetText(self.BoilerPlate)
            self.editor.SetThemeEnabled(True)
            
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

            elif fileType == ".js":
                """ 
                    The .js lexer is based on the .cpp lexer so 
                    we are just using that one...
                
                """
                self.editor.SetLexer(wx.stc.STC_LEX_CPP)
                
                js_kw = ("abstract else instanceof super"   
                         " boolean enum int switch"
                         " break export interface synchronized"
                         " byte extends let this"
                         " case false long throw"
                         " catch final native throws"
                         " char finally new transient"
                         " class float null true"
                         " const for package try"
                         " continue function private typeof"
                         " debugger goto protected var"
                         " default if public void"
                         " delete implements return volatile"
                         " do import short while"
                         " double in static with")

                self.editor.SetKeyWords(0, js_kw)
                
                
            else: 
                
                self.editor.SetLexer(wx.stc.STC_LEX_HTML)

                
                kw = ("a abbr acronym address applet area b base basefont bdo big"
                " blockquote body br button caption center cite code col colgroup dd del"
                " dfn dir div dl dt em fieldset font form frame frameset h1 h2 h3 h4 h5 h6"
                " head hr html i iframe img input ins isindex kbd label legend li link map"
                " menu meta noframes noscript object ol optgroup option p param pre q s"
                " samp script select small span strike strong style sub sup table tbody"
                " td textarea tfoot th thead title tr tt u ul var xml xmlns abbr"
                " accept-charset accept accesskey action align alink alt archive axis"
                " background bgcolor border cellpadding cellspacing char charoff charset"
                " checked cite class classid clear codebase codetype color cols colspan"
                " compact content coords data datafld dataformatas datapagesize datasrc"
                " datetime declare defer dir disabled enctype event face for frame"
                " frameborder headers height href hreflang hspace http-equiv id ismap"
                " label lang language leftmargin link longdesc marginwidth marginheight"
                " maxlength media method multiple name nohref noresize noshade nowrap"
                " object onblur onchange onclick ondblclick onfocus onkeydown onkeypress"
                " onkeyup onload onmousedown onmousemove onmouseover onmouseout onmouseup"
                " onreset onselect onsubmit onunload profile prompt readonly rel rev rows"
                " rowspan rules scheme scope selected shape size span src standby start"
                " style summary tabindex target text title topmargin type usemap valign"
                " value valuetype version vlink vspace width text password checkbox radio"
                " submit reset file hidden image article aside calendar canvas card"
                " command commandset datagrid datatree footer gauge header m menubar"
                " menulabel nav progress section switch tabbox active command"
                " contenteditable ping public !doctype")
                            
                
                self.editor.SetKeyWords(0, kw)
                self.editor.SetLexerLanguage("hypertext")

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
            
            self.editorCodeStyle = style
            
            if not style:
            
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
                

 
            self.editor.SetCaretLineBack(style["meta.highlight.currentline"]['background-color'])
            self.editor.SetCaretForeground(style["meta.default"]['color'])
            self.editor.SetCaretLineBackAlpha(10)
            
            self.editor.SetSelBackground(True, "#b5d4ff")
            self.editor.SetSelAlpha(120)
            
            
            if self.editor.GetLexer() == wx.stc.STC_LEX_HTML:
                # HTML Styles
                
                # <p>[This is text]</p>
                self.editor.StyleSetSpec(wx.stc.STC_H_DEFAULT,     "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [<p>]This is text</p>
                self.editor.StyleSetSpec(wx.stc.STC_H_TAG, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # ??
                self.editor.StyleSetSpec(wx.stc.STC_H_TAGUNKNOWN, "fore:" + style["meta.invalid"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # <img src="foo" [/>]
                self.editor.StyleSetSpec(wx.stc.STC_H_TAGEND, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [href]
                self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, "fore:" + style["markup.tag.attribute.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                #  ["doublestring"]
                self.editor.StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                #  ['singlestring'] 
                self.editor.StyleSetSpec(wx.stc.STC_H_SINGLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [<!-- comment -->]
                self.editor.StyleSetSpec(wx.stc.STC_H_COMMENT, "fore:" + style["markup.comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                
                # vspace = [4] 
                self.editor.StyleSetSpec(wx.stc.STC_H_NUMBER, "fore:" + style["markup.tag.attribute.value"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # vspace [=] 4
                self.editor.StyleSetSpec(wx.stc.STC_H_OTHER, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [&amp;]
                self.editor.StyleSetSpec(wx.stc.STC_H_ENTITY, "fore:" + style["markup.constant.entity"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [<?] xml version="1.0" encoding="ISO-8859-1" ?>
                self.editor.StyleSetSpec(wx.stc.STC_H_XMLSTART, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # <?xml version="1.0" encoding="ISO-8859-1" [?>]
                self.editor.StyleSetSpec(wx.stc.STC_H_XMLEND, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_VALUE, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [<?php ]  [?>]
                self.editor.StyleSetSpec(wx.stc.STC_H_QUESTION, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # ??
                self.editor.StyleSetSpec(wx.stc.STC_H_ATTRIBUTEUNKNOWN, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_H_CDATA, "fore:" + style["markup.inline.cdata"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_H_SCRIPT, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
             
                self.editor.StyleSetSpec(wx.stc.STC_H_SGML_DEFAULT, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_SGML_ERROR, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_SGML_1ST_PARAM, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_SGML_COMMAND, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_H_SGML_COMMAND, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)

                
                # <script>[ ]
                self.editor.StyleSetSpec(wx.stc.STC_HJ_START, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_DEFAULT, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_HJ_WORD, "fore:" + style["markup.tag"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_HJ_COMMENTLINE, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_COMMENT, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_COMMENTDOC, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_HJ_SINGLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_DOUBLESTRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_STRINGEOL, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_HJ_NUMBER, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_KEYWORD, "fore:" + style["keyword"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_SYMBOLS, "fore:" + style["language.operator"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_STRINGEOL, "fore:" + style["keyword"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJ_REGEX, "fore:" + style["keyword"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_HJA_DEFAULT, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_DOUBLESTRING, 'fore:' + style['string']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_KEYWORD, 'fore:' + style['keyword']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_NUMBER, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_REGEX, 'fore:' + style['string']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_SINGLESTRING, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_START, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_STRINGEOL, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_SYMBOLS, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HJA_WORD, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
              
           
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_CHARACTER, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_CLASSNAME, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_COMMENTLINE, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPA_DEFAULT, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_DEFNAME, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_IDENTIFIER, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_NUMBER, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_OPERATOR, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPA_START, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_STRING, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_TRIPLE, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
#                self.editor.StyleSetSpec(wx.stc.STC_HPA_TRIPLEDOUBLE, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)
                self.editor.StyleSetSpec(wx.stc.STC_HPA_WORD, 'fore:' + style['keyword']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)


                #===============================================================================
                # 
                #===============================================================================
                self.editor.StyleSetSpec(wx.stc.STC_H_ASP, 'fore:' + style['meta.default']['color'] +',back:'+style['meta.default']['background-color']+',face:%(other)s,size:%(size)d' % faces)


                
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
     
            elif self.editor.GetLexer() == wx.stc.STC_LEX_CSS:
 
                # CSS
               
                self.editor.StyleSetSpec(wx.stc.STC_CSS_DEFAULT, "fore:" + style["markup.processing"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                # [img] {  
                self.editor.StyleSetSpec(wx.stc.STC_CSS_TAG, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                # { } : ;
                self.editor.StyleSetSpec(wx.stc.STC_CSS_OPERATOR, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                # /* Comment */
                self.editor.StyleSetSpec(wx.stc.STC_CSS_COMMENT, "fore:" + style["markup.comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                
                # float:[left];
                self.editor.StyleSetSpec(wx.stc.STC_CSS_VALUE, "fore:" + style["style.value.numeric"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # input[ [type=checkbox] ]
                self.editor.StyleSetSpec(wx.stc.STC_CSS_ATTRIBUTE, "fore:" + style["style.value.keyword"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # Strings
                
                self.editor.StyleSetSpec(wx.stc.STC_CSS_SINGLESTRING, "fore:" + style["style.value.string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_DOUBLESTRING, "fore:" + style["style.value.string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [.class] {    }
                self.editor.StyleSetSpec(wx.stc.STC_CSS_CLASS, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [#id] {    }
                self.editor.StyleSetSpec(wx.stc.STC_CSS_ID, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # ??
                self.editor.StyleSetSpec(wx.stc.STC_CSS_IDENTIFIER, "fore:" + style["style.property.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_IDENTIFIER2, "fore:" + style["style.property.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_IDENTIFIER3, "fore:" + style["style.property.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # [float]: left;
                self.editor.StyleSetSpec(wx.stc.STC_CSS_UNKNOWN_IDENTIFIER, "fore:" + style["style.property.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # img[:hover]
                self.editor.StyleSetSpec(wx.stc.STC_CSS_UNKNOWN_PSEUDOCLASS, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_PSEUDOCLASS, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_CSS_PSEUDOELEMENT, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # @import 
                self.editor.StyleSetSpec(wx.stc.STC_CSS_DIRECTIVE, "fore:" + style["style.at-rule"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                # p { color: #ff0000 ! [ important ] ; }
                self.editor.StyleSetSpec(wx.stc.STC_CSS_IMPORTANT, "fore:" + style["meta.important"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
    
                self.editor.StyleSetSpec(wx.stc.STC_CSS_EXTENDED_IDENTIFIER,     "fore:" + style["style.property.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_EXTENDED_PSEUDOCLASS,  "fore:" + style["style.property.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size3)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_CSS_EXTENDED_PSEUDOELEMENT,  "fore:" + style["style.property.name"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size3)d" % faces)
            
            elif self.editor.GetLexer() == wx.stc.STC_LEX_PYTHON:

                self.editor.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:" + style["constant.numeric"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_STRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                
                self.editor.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                try:
                    self.editor.StyleSetSpec(wx.stc.STC_P_WORD, "fore:" + style["keyword.control"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                    self.editor.StyleSetSpec(wx.stc.STC_P_WORD2, "fore:" + style["keyword.control"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                except:
                    self.editor.StyleSetSpec(wx.stc.STC_P_WORD, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                    self.editor.StyleSetSpec(wx.stc.STC_P_WORD2, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                
                
                self.editor.StyleSetSpec(wx.stc.STC_P_OPERATOR, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_DECORATOR, "fore:" + style["meta.important"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                
                
                self.editor.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
            
            
            elif self.editor.GetLexer() == wx.stc.STC_LEX_CPP:
                # This is for javascript
                
                self.editor.StyleSetSpec(wx.stc.STC_C_DEFAULT, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_COMMENTLINE, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_COMMENTLINEDOC, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_COMMENT, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_COMMENTDOC, "fore:" + style["comment"]['color'] +",back:"+style["meta.default"]['background-color']+",italic,face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_NUMBER, "fore:" + style["constant.numeric"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_STRING, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_STRINGEOL, "fore:" + style["string"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_CHARACTER, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                try:
                    self.editor.StyleSetSpec(wx.stc.STC_C_WORD, "fore:" + style["keyword"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                    self.editor.StyleSetSpec(wx.stc.STC_C_WORD2, "fore:" + style["keyword.control"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                except:
                    self.editor.StyleSetSpec(wx.stc.STC_C_WORD, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                    self.editor.StyleSetSpec(wx.stc.STC_C_WORD2, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_C_OPERATOR, "fore:" + style["language.operator"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_C_GLOBALCLASS, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                #self.editor.StyleSetSpec(wx.stc.STC_C_DEFNAME, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                self.editor.StyleSetSpec(wx.stc.STC_C_IDENTIFIER, "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                self.editor.StyleSetSpec(wx.stc.STC_C_REGEX, "fore:" + style["string.regex"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
                
                        
            else:
                pass

         
            # hack for unidentified entities
            self.editor.SetBackgroundColour(style["meta.default"]['background-color'])
            
              # Global default styles for all languages
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  "fore:" + style["meta.default"]['color'] +",back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size3)d" % faces)
            self.editor.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,  "fore:#ff0000,back:"+style["meta.default"]['background-color']+",face:%(other)s,size:%(size3)d" % faces)
            
           
