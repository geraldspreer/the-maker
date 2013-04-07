import makerController
import makerEditorWxView
import makerCSSTools
import makerAutoComplete
import makerReplace
import os

def ensureCurrentFileSaved(func):
    def wrapped(*args, **kwds):
        self = args[0]
        if not self.isCurrentFileSaved(): self.saveCurrentFile()
        func(*args, **kwds)
    return wrapped

def updateInterfaceControls(func):
    def wrapped(*args, **kwds):
        self = args[0]
        func(*args, **kwds)
        self.updateStatusInformation()
    return wrapped


class MakerFileController(makerController.SuperController):
    """
    For each file that is opened a new instance of MakerFileController is
    created and also a new editor instance
    """
    @updateInterfaceControls
    def bindActions(self):
        
       
        self.view.previewButton.Unbind(self.view.wx.EVT_BUTTON)
        self.view.saveButton.Unbind(self.view.wx.EVT_BUTTON)
        self.view.Unbind(self.view.wx.EVT_MENU, self.view.MenuItemSaveFile)
        self.view.Unbind(self.view.wx.EVT_MENU, self.view.MenuItemPrint)
        
        self.view.Unbind(self.view.wx.EVT_TEXT, self.view.search)

        
        self.view.Unbind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CHANGED)
        self.view.Unbind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSED)
        self.view.Unbind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSING)
        
        
        
        # take control
        
        
        self.view.Bind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CHANGED, 
                       self.model.core.projectController.noteBookPageChanged)
        
        
        self.view.Bind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSED, 
                       self.model.core.projectController.noteBookPageClosed)
        
        # we need this event to make sure files are saved before they are closed
        self.view.Bind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSING, 
                       self.noteBookPageBeingClosed)
        
            
        
        self.view.Bind(self.view.wx.EVT_MENU, self.replace, self.view.MenuItemReplace)
        
        self.view.Bind(self.view.wx.EVT_TEXT, self.find, self.view.search)
        
        # preview
        
        self.view.previewButton.Bind(self.view.wx.EVT_BUTTON, self.preview)
        self.view.Bind(self.view.wx.EVT_MENU, self.preview,self.view.MenuItemPreview)
        
                
        self.view.saveButton.Bind(self.view.wx.EVT_BUTTON, self.model.save)
        self.view.Bind(self.view.wx.EVT_MENU, self.model.save, self.view.MenuItemSaveFile)
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemCloseFile
                  )
        
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemDeleteFile
                  )
        
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemRenameFile
                  )
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemSaveAsTemplate
                  )
        
        
        
        self.view.Bind(self.view.wx.EVT_MENU, self.findActionForEvent, self.view.MenuItemPrint)
    
        # Markdown
        
        self.view.Bind(self.view.wx.EVT_MENU, self.insertMarkdown, self.view.MenuItemMarkdown)
    
        
        # Markers
        self.view.Bind(self.view.wx.EVT_MENU, self.findActionForEvent, self.view.MenuItemMarkerTodaysDate)
        self.view.Bind(self.view.wx.EVT_MENU, self.findActionForEvent, self.view.MenuItemMarkerProjectName)
        self.view.Bind(self.view.wx.EVT_MENU, self.findActionForEvent, self.view.MenuItemMarkerPageName)
        self.view.Bind(self.view.wx.EVT_MENU, self.findActionForEvent, self.view.MenuItemMarkerCreationDate)
    
         # view
        
        self.view.Bind(self.view.wx.EVT_MENU, 
                  self.findActionForEvent,
                  self.view.MenuItemWrapWord
                  )
        
        
        # HTML
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_body)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_head)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_html)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_span)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_div)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_style)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_meta)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_link)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_DOCTYPE)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_title)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_em)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_pre)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_code)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_h2)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_h3)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_h1)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_h6)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_h4)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_ins)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_strong)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_bdo)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_dfn)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_var)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_samp)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_cite)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_blockquote)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_acronym)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_abbr)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_br)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_address)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_h5)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_q)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_p)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_del)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_kbd)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_a)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_base)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_map)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_object)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_param)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_img)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_area)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_dl)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_ol)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_dd)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_li)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_ul)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_dt)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_colgroup)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_tr)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_tbody)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_caption)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_tfoot)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_th)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_table)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_td)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_col)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_thead)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_fieldset)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_form)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_textarea)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_button)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_label)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_optgroup)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_input)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_legend)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_select)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_option)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_noscript)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_script)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_b)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_sub)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_i)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_big)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_tt)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_hr)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_sup)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemHTML_small)
        
        
        # css

        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_background)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_background_attachment)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_background_color)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_background_image)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_background_position)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_background_repeat)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_border)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_border_collapse)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_border_color)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_border_spacing)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_border_style)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_border_width)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_bottom)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_caption_side)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_clear)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_clip)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_color)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_content)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_counter_increment)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_counter_reset)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_cursor)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_direction)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_display)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_empty_cells)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_float)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_font)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_font_family)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_font_size)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_font_style)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_font_variant)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_font_weight)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_height)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_left)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_letter_spacing)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_line_height)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_list_style)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_list_style_image)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_list_style_position)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_list_style_type)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_margin)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_max_height)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_max_width)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_min_height)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_min_width)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_orphans)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_outline)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_outline_color)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_outline_style)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_outline_width)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_overflow)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_padding)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_page_break_after)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_page_break_before)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_page_break_inside)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_position)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_quotes)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_right)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_table_layout)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_text_align)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_text_decoration)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_text_indent)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_text_transform)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_top)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_unicode_bidi)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_vertical_align)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_visibility)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_white_space)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_widows)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_width)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_word_spacing)


        self.view.Bind(self.view.wx.EVT_MENU, 
        self.findActionForEvent,
        self.view.MenuItemCSS_z_index)
        
        # edit menu
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.undo,
        self.view.MenuItemUndo)

        self.view.Bind(self.view.wx.EVT_MENU,
        self.redo,
        self.view.MenuItemRedo)

        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.cut,
        self.view.MenuItemCut)
        
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.copy,
        self.view.MenuItemCopy)
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.paste,
        self.view.MenuItemPaste)
        
        # search 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.activateSearch,
        self.view.MenuItemFind)
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findNext,
        self.view.MenuItemFindNext)
        
        #
        # PopUp Menu
        #
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.undo,
        self.view.editorPopUpMenuItemUndo) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.redo,
        self.view.editorPopUpMenuItemRedo) 
                
        self.view.Bind(self.view.wx.EVT_MENU,
        self.cut,
        self.view.editorPopUpMenuItemCut) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.copy,
        self.view.editorPopUpMenuItemCopy) 
                
        self.view.Bind(self.view.wx.EVT_MENU,
        self.paste,
        self.view.editorPopUpMenuItemPaste)
          
        self.view.Bind(self.view.wx.EVT_MENU,
        self.replace,
        self.view.editorPopUpMenuItemReplace) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.activateSearch,
        self.view.editorPopUpMenuItemFind) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findNext,
        self.view.editorPopUpMenuItemFindNext) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.pickColor,
        self.view.editorPopUpMenuItemSelectColor) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.editorPopUpMenuItemLine_through) 
                     
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,                
        self.view.editorPopUpMenuItemUnderline) 
               
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.editorPopUpMenuItemOblique) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.editorPopUpMenuItemBold) 
        
        theList = [".dynamic", ".content", ".html", ".php"]
        
        if self.model.getType() == ".css":
            
            self.view.editorPopUpMenuItemLine_through.Enable(False)
            self.view.editorPopUpMenuItemUnderline.Enable(False)
            self.view.editorPopUpMenuItemBold.Enable(False)
            self.view.editorPopUpMenuItemOblique.Enable(False)
            
            self.view.editorPopUpMenuItemSelectColor.Enable(True)    
            
        elif self.model.getType() in theList:
            
            self.view.editorPopUpMenuItemSelectColor.Enable(False)
            
            self.view.editorPopUpMenuItemLine_through.Enable(True)
            self.view.editorPopUpMenuItemUnderline.Enable(True)
            self.view.editorPopUpMenuItemBold.Enable(True)
            self.view.editorPopUpMenuItemOblique.Enable(True)
            
        
        #
        #    end popup menu bindings
        #
        
        
        #
        # tools Menu
        #
        
       
        self.view.Bind(self.view.wx.EVT_MENU,
        self.pickColor,
        self.view.MenuItemSelectColor) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemLine_through) 
                     
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,                
        self.view.MenuItemUnderline) 
               
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemOblique) 
        
        self.view.Bind(self.view.wx.EVT_MENU,
        self.findActionForEvent,
        self.view.MenuItemBold) 
        
        theList = [".dynamic", ".content", ".html", ".php"]
        
        if self.model.getType() == ".css":
            
            self.view.MenuItemLine_through.Enable(False)
            self.view.MenuItemUnderline.Enable(False)
            self.view.MenuItemBold.Enable(False)
            self.view.MenuItemOblique.Enable(False)
            
            self.view.MenuItemSelectColor.Enable(True)    
            
        elif self.model.getType() in theList:
            
            self.view.MenuItemSelectColor.Enable(False)
            
            self.view.MenuItemLine_through.Enable(True)
            self.view.MenuItemUnderline.Enable(True)
            self.view.MenuItemBold.Enable(True)
            self.view.MenuItemOblique.Enable(True)
            
        
        #
        #    end tools menu bindings
        #
       
        
         
        
        
        
        
    def undo(self, event):
        self.editor.Undo()
    
    def redo(self, event):
        self.editor.Redo()
        
        
    def cut(self, event):
        self.editor.Cut()
    
    def copy(self, event):
        self.editor.Copy()
        
    
    def paste(self, event):
        self.editor.Paste()
        
    @ensureCurrentFileSaved
    def rename(self, event):
        self.model.rename()
        
    
    
    def pythonShell(self, scriptToRun=None):
        """ brings up python shell and runs scriptToRun if given """
        
        shell = self.view.doShell(self.view)
        
        if scriptToRun:
            shell.runfile(scriptToRun)
        
     
            
    def createAbstractNameForViewObjects(self):
        
        self.saveButton = self.view.saveButton
        self.saveMenu = self.view.MenuItemSaveFile
        
        self.noteBook = self.view.noteBook
        self.openEditor()
        
        self.publishMenu = self.view.MenuItemPublish
        self.publishButton = self.view.publishButton
        
        self.search = self.view.search
        
        
                
    def clearEditor(self):
        self.editor.ClearAll()
    
    def enableEditor(self):
        self.editor.Enable()
        
        # enable edit functions
    
    def disableEditor(self):
        self.editor.Disable()
        # disable edit functions
        
        
    def openEditor(self):
        """ create new instance """
    
        self.view.Unbind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CHANGED)
        self.view.Unbind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSED)
        self.view.Unbind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSING)
        
        self.editor = makerEditorWxView.editorView(self.view, self.model.getType()).editor
        
        self.setDefaultZoom()
        
        # - - delete welcome message - -
        
        # the noteBook is by default displaying a welcome message
        # this message is set when the GUI is created
        # the following two lines are here to make sure this message
        # goes away once the first file is edited
        
        if self.noteBook.GetPageCount() != 0:
            if self.noteBook.GetPage(0).GetId() == self.view.welcomeId:
                self.noteBook.DeletePage(0)
        
        # - - - - - - - - - - - - - - -
        
        self.noteBook.AddPage(self.editor, self.model.getFileName(), select=True)
                
        self.setReferringTreeItem(self.view.tree.GetSelection())
       
        # use fileController instance as value here
        self.model.core.projectManager.controller.noteBookPages[self.noteBook.GetSelection()] = self
        
        
        
        self.view.Bind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CHANGED, 
                       self.model.core.projectController.noteBookPageChanged)
        
        
        self.view.Bind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSED, 
                       self.model.core.projectController.noteBookPageClosed)
        
        # we need this event to make sure files are saved before they are closed
        self.view.Bind(self.view.wx.lib.flatnotebook.EVT_FLATNOTEBOOK_PAGE_CLOSING, 
                       self.noteBookPageBeingClosed)
        
         # editor right click
        
        self.editor.Bind(self.view.wx.EVT_RIGHT_DOWN, 
                       self.editorRightClick)
        
    
    def pickColor(self, event):
        """ bring up a color picker dialog"""
        
        color = self.colorDialog() 
        self.actionInsertText("rgb" + str(color))          
    
    
    def preview(self, event):
        text = self.getTextFromEditor()
        if not text:
            return
        self.model.preview(text)
        
  
    
    def textChanged(self, event):
	     
	self.model.core.currentFile.setSaved(False)
        
    
    def setDefaultZoom(self):
        
        self.defaultZoom = self.editor.GetZoom()
        
    def getDefaultZoom(self):
        
        return self.defaultZoom
    
    
    def setReferringTreeItem(self, item):
        """ set the tree item associated with that file"""
        self.referringTreeItem = item
    
    def getReferringTreeItem(self):
        """ get the tree item associated with that file"""
        return self.referringTreeItem
    
    
    
    
    
    
    def getTextFromEditor(self):
        try:
            text = self.editor.GetText().encode(self.model.core.encoding)
            return text
        except:
            #print self.editor.GetText()
            for c in range(self.editor.GetTextLength()):
                self.editor.SetSelection(c, c +1)
                try: 
                    print self.editor.GetSelectedText().encode(self.model.core.encoding)
                except:
                    
                    self.editor.SetSelBackground(True, self.view.wx.RED)
                    self.infoMessage("Bad charcater found at position " + 
                                     str(c) + 
                                     " ! Cannot encode using:" + self.model.core.encoding + 
                                     "\nPlease review and edit...")
                    self.editor.SetSelBackground(True, "#b5d4ff")
                    return
            
            
        
        
        
    def actionInsertText(self, text):
        """Insert text into the main editor."""
        currPos = self.editor.GetCurrentPos()
        self.editor.InsertText(currPos, text)
      
    def actionInsertImage(self):
        """Insert text into the main editor."""
        
        path = self.model.core.getPathParts()
        
        image = self.imageDialog(path)
        if not image: return

        # only use the image filename - not the full path
        image = os.path.split(image)
        
        if path.endswith("/"):
            origPath = path
        else:
            origPath = path + "/"
               
        image = image[1]
                    
        theTag = '<img class="" src="'+image+'" align="left" alt="'+image+'"/>'
        self.insertHtmlTags([theTag])
    
    
    
    def actionAddText(self, text):
        """Add text into the main editor."""
        self.editor.AddText(text)
        
    
    
    def actionFormatText(self, text, format):
        """Insert HTML tags in editor."""
        
        formats = {
            'bold'    : ['<span style="font-weight:bold;">', '</span>'],
            'oblique' : ['<span style="font-style:oblique;">', '</span>']
            }
        
        defaultTags = ['<span style="text-decoration:'+format+'">','</span>']
        tags = formats.get(format, defaultTags)
        self.insertHtmlTags(tags)    
    
    
    
    def insertMarkdown(self, event):
        # inserts a markdown area
        self.insertHtmlTags(["<markdown>", "</markdown>"])
    
    
    def insertHtmlTags(self, tags):
        """
        insert HTML tags into the main editor
        if text is selected , the tags are wrapped around it
        """
        sel = self.editor.GetSelectedText()
        if len(sel)==0:
            pass
        else:
            self.editor.Clear()
        if len(tags)==1:
            # one tag
            self.editor.AddText(tags[0]+"\n")
            
        else:
            # two tags
            self.editor.AddText(tags[0])
            self.editor.AddText(sel) 
            
            self.editor.AddText(tags[1])    
            pos = self.editor.GetCurrentPos()
            
            self.editor.SetCurrentPos(pos-(len(tags[1])))
            try:
                self.editor.SetSelection(self.editor.GetCurrentPos(),self.editor.GetCurrentPos())
            except Exception, e:
                print e
    
        
        
    
    def actionInsertCSS(self, text):
        self.editor.AddText(text)
        
        # now set the cursor to the position after the : character
        
        self.editor.SearchAnchor()
        pos = self.editor.SearchPrev(self.view.wx.stc.STC_FIND_REGEXP, ":")
        self.editor.GotoPos(pos + 1)
    
    
    def loadTextIntoEditor(self, text):
      
        self.editor.AddText(text)
        makerAutoComplete.AutoComplete(self.model, self.view, self.editor)
	self.view.wx.Yield()
	self.editor.Bind(self.view.wx.stc.EVT_STC_CHANGE, self.textChanged)

         
       
    def isCurrentFileSaved(self):
        
        return self.model.getSaved()

    
    
    def saveCurrentFile(self):
        
        if not self.model.getSaved():
            m = "Do you want to save "
            m += "the file %s?" % self.model.core.getCurrentFileName()
            if self.askYesOrNo(m) == "Yes":
                self.model.save()
                
                
                
    def closeCurrentFile(self, callModel = True, event=None):
        page = self.noteBook.GetSelection()
        self.noteBook.DeletePage(page)
        self.noteBook.Refresh()
        if callModel:
            self.model.closeFile(callController = False)
    
    
        
    
    @ensureCurrentFileSaved
    def noteBookPageBeingClosed(self, event=None):
        self.model.closeFile()
            
    @ensureCurrentFileSaved
    def actionPrint(self):
        # prints the source of the file if printable
        self.model.printViaBrowser()


#
#            self.view.search.GetId() : (self.searchInEditor, self.view.search.GetValue()),
#            self.view.MenuItemFind.GetId() : (self.activateSearch,),
#            self.view.MenuItemFindNext.GetId() : (self.findNext, self.view.search.GetValue()),        
#            self.view.MenuItemHTML_img.GetId() : (self.actionInsertImage,),


    def editorRightClick(self, event):
        """ shows popup menu """
        
        self.view.PopupMenu(self.view.editorPopUp, event.GetPosition())
   

    def buildPopupMenu(self):
        """
        builds the popup menu for the editor and binds events
        
        also enables / disables items according to the file type
        """
    

    def replace(self, evt):
        
        makerReplace.Replace(self.view, self.editor, self.model.getProjectInstance())

    
    def find(self, event):
        """ search text, select and make visible """
        string = self.search.GetValue()      
        location = self.editor.FindText(0, self.editor.GetTextLength(), string, 
                             self.view.wx.stc.STC_FIND_REGEXP)
                
        if location != -1:
            self.view.searchStatus.SetLabel("")
            self.editor.GotoPos(location)
            self.editor.SetSelection(location, location + len(string))
        elif location == -1:
            self.view.searchStatus.SetLabel("String not found!")
            
    # ------------------------------------------------------------         
   
    
    def activateSearch(self, event):
        """ sets the focus to the search field"""
        self.view.search.SetFocus()     
        
    def findNext(self, event):
        """ find next occurrence of search term"""
        
        searchTerm = self.search.GetValue()
        oldSelection = self.editor.GetSelection()
        
        # the SearchAnchor has to be set to the end of the selection
        
        self.editor.SetSelection(oldSelection[-1], oldSelection[-1])
        
        self.editor.SearchAnchor()
        location = self.editor.SearchNext(self.view.wx.stc.STC_FIND_REGEXP, searchTerm)
        
        if location != -1:
            self.view.searchStatus.SetLabel("")
            self.editor.GotoPos(location)
            self.editor.SetSelection(location, location + len(searchTerm))
        
        elif location == -1:
            self.view.searchStatus.SetLabel("Last one found!")
            self.editor.SetSelection(oldSelection[0], oldSelection[-1])
    
    # ------------------------------------------------------------  
        


    def findActionForEvent(self, event):
        """Find the right Action for the Menu item by his id."""
       
        theActions = {
            self.view.MenuItemPrint.GetId() : (self.actionPrint, ),
            self.view.MenuItemDeleteFile.GetId() : (self.model.delete, ),
            self.view.MenuItemCloseFile.GetId() : (self.closeCurrentFile, ),
            self.view.MenuItemRenameFile.GetId() : (self.rename, ),
            self.view.MenuItemSaveAsTemplate.GetId() : (self.model.saveAsTemplate, ),
            self.view.editorPopUpMenuItemLine_through.GetId() : (self.actionFormatText, (event, "line-through")),
            self.view.editorPopUpMenuItemUnderline.GetId() : (self.actionFormatText, (event, "underline")),
            self.view.editorPopUpMenuItemBold.GetId() : (self.actionFormatText, (event, "bold")),
            self.view.editorPopUpMenuItemOblique.GetId() : (self.actionFormatText, (event, "oblique")),
            
            self.view.MenuItemLine_through.GetId() : (self.actionFormatText, (event, "line-through")),
            self.view.MenuItemUnderline.GetId() : (self.actionFormatText, (event, "underline")),
            self.view.MenuItemBold.GetId() : (self.actionFormatText, (event, "bold")),
            self.view.MenuItemOblique.GetId() : (self.actionFormatText, (event, "oblique")),
                        
            self.view.MenuItemMarkerTodaysDate.GetId() : (self.actionAddText, "!todaysDate!"),
            self.view.MenuItemMarkerProjectName.GetId() : (self.actionAddText, "!projectName!"),
            self.view.MenuItemMarkerPageName.GetId() : (self.actionAddText, "!pageName!"),
            self.view.MenuItemMarkerCreationDate.GetId() : (self.actionAddText, "!creationDate!"),
            self.view.MenuItemHTML_img.GetId() : (self.actionInsertImage, ),
            self.view.MenuItemHTML_em.GetId() : (self.insertHtmlTags, ['<em>', '</em>']),
            self.view.MenuItemHTML_pre.GetId() : (self.insertHtmlTags, ['<pre>', '</pre>']),
            self.view.MenuItemHTML_code.GetId() : (self.insertHtmlTags, ['<code>', '</code>']),
            self.view.MenuItemHTML_h2.GetId() : (self.insertHtmlTags, ['<h2>', '</h2>']),
            self.view.MenuItemHTML_h3.GetId() : (self.insertHtmlTags, ['<h3>', '</h3>']),
            self.view.MenuItemHTML_h1.GetId() : (self.insertHtmlTags, ['<h1>', '</h1>']),
            self.view.MenuItemHTML_h6.GetId() : (self.insertHtmlTags, ['<h6>', '</h6>']),
            self.view.MenuItemHTML_DOCTYPE.GetId() : (self.insertHtmlTags, ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http"://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">']),
            self.view.MenuItemHTML_h4.GetId() : (self.insertHtmlTags, ['<h4>', '</h4>']),
            self.view.MenuItemHTML_h5.GetId() : (self.insertHtmlTags, ['<h5>', '</h5>']),
            self.view.MenuItemHTML_meta.GetId() : (self.insertHtmlTags, ['<meta />']),
            self.view.MenuItemHTML_table.GetId() : (self.insertHtmlTags, ['<table>', '</table>']),
            self.view.MenuItemHTML_dfn.GetId() : (self.insertHtmlTags, ['<dfn>', '</dfn>']),
            self.view.MenuItemHTML_label.GetId() : (self.insertHtmlTags, ['<label>', '</label>']),
            self.view.MenuItemHTML_select.GetId() : (self.insertHtmlTags, ['<select>', '</select>']),
            self.view.MenuItemHTML_noscript.GetId() : (self.insertHtmlTags, ['<noscript>', '</noscript>']),
            self.view.MenuItemHTML_kbd.GetId() : (self.insertHtmlTags, ['<kbd>', '</kbd>']),
            self.view.MenuItemHTML_style.GetId() : (self.insertHtmlTags, ['<style>', '</style>']),
            self.view.MenuItemHTML_strong.GetId() : (self.insertHtmlTags, ['<strong>', '</strong>']),
            self.view.MenuItemHTML_span.GetId() : (self.insertHtmlTags, ['<span>', '</span>']),
            self.view.MenuItemHTML_sub.GetId() : (self.insertHtmlTags, ['<sub>', '</sub>']),
            self.view.MenuItemHTML_title.GetId() : (self.insertHtmlTags, ['<title>', '</title>']),
            self.view.MenuItemHTML_bdo.GetId() : (self.insertHtmlTags, ['<bdo>', '</bdo>']),
            self.view.MenuItemHTML_tr.GetId() : (self.insertHtmlTags, ['<tr>', '</tr>']),
            self.view.MenuItemHTML_tbody.GetId() : (self.insertHtmlTags, ['<tbody>', '</tbody>']),
            self.view.MenuItemHTML_param.GetId() : (self.insertHtmlTags, ['<param>', '</param>']),
            self.view.MenuItemHTML_li.GetId() : (self.insertHtmlTags, ['<li>', '</li>']),
            self.view.MenuItemHTML_script.GetId() : (self.insertHtmlTags, ['<script type="text/javascript">', '</script>']),
            self.view.MenuItemHTML_html.GetId() : (self.insertHtmlTags, ['<html>', '</html>']),
            self.view.MenuItemHTML_tfoot.GetId() : (self.insertHtmlTags, ['<tfoot>', '</tfoot>']),
            self.view.MenuItemHTML_th.GetId() : (self.insertHtmlTags, ['<th>', '</th>']),
            self.view.MenuItemHTML_sup.GetId() : (self.insertHtmlTags, ['<sup>', '</sup>']),
            self.view.MenuItemHTML_var.GetId() : (self.insertHtmlTags, ['<var>', '</var>']),
            self.view.MenuItemHTML_input.GetId() : (self.insertHtmlTags, ['<input>', '</input>']),
            self.view.MenuItemHTML_td.GetId() : (self.insertHtmlTags, ['<td>', '</td>']),
            self.view.MenuItemHTML_samp.GetId() : (self.insertHtmlTags, ['<samp>', '</samp>']),
            self.view.MenuItemHTML_cite.GetId() : (self.insertHtmlTags, ['<cite>', '</cite>']),
            self.view.MenuItemHTML_thead.GetId() : (self.insertHtmlTags, ['<thead>', '</thead>']),
            self.view.MenuItemHTML_body.GetId() : (self.insertHtmlTags, ['<body>', '</body>']),
            self.view.MenuItemHTML_map.GetId() : (self.insertHtmlTags, ['<map>', '</map>']),
            self.view.MenuItemHTML_head.GetId() : (self.insertHtmlTags, ['<head>', '</head>']),
            self.view.MenuItemHTML_blockquote.GetId() : (self.insertHtmlTags, ['<blockquote>', '</blockquote>']),
            self.view.MenuItemHTML_fieldset.GetId() : (self.insertHtmlTags, ['<fieldset>', '</fieldset>']),
            self.view.MenuItemHTML_option.GetId() : (self.insertHtmlTags, ['<option>', '</option>']),
            self.view.MenuItemHTML_form.GetId() : (self.insertHtmlTags, ['<form>', '</form>']),
            self.view.MenuItemHTML_acronym.GetId() : (self.insertHtmlTags, ['<acronym>', '</acronym>']),
            self.view.MenuItemHTML_big.GetId() : (self.insertHtmlTags, ['<big>', '</big>']),
            self.view.MenuItemHTML_dd.GetId() : (self.insertHtmlTags, ['<dd>', '</dd>']),
            self.view.MenuItemHTML_object.GetId() : (self.insertHtmlTags, ['<object>', '</object>']),
            self.view.MenuItemHTML_small.GetId() : (self.insertHtmlTags, ['<small>', '</small>']),
            self.view.MenuItemHTML_base.GetId() : (self.insertHtmlTags, ['<base>', '</base>']),
            self.view.MenuItemHTML_link.GetId() : (self.insertHtmlTags, ['<link />']),
            self.view.MenuItemHTML_abbr.GetId() : (self.insertHtmlTags, ['<abbr>', '</abbr>']),
            self.view.MenuItemHTML_br.GetId() : (self.insertHtmlTags, ['<br />']),
            self.view.MenuItemHTML_address.GetId() : (self.insertHtmlTags, ['<address>', '</address>']),
            self.view.MenuItemHTML_optgroup.GetId() : (self.insertHtmlTags, ['<optgroup>', '</optgroup>']),
            self.view.MenuItemHTML_dt.GetId() : (self.insertHtmlTags, ['<dt>', '</dt>']),
            self.view.MenuItemHTML_ins.GetId() : (self.insertHtmlTags, ['<ins>', '</ins>']),
            self.view.MenuItemHTML_b.GetId() : (self.insertHtmlTags, ['<b>', '</b>']),
            self.view.MenuItemHTML_legend.GetId() : (self.insertHtmlTags, ['<legend>', '</legend>']),
            self.view.MenuItemHTML_hr.GetId() : (self.insertHtmlTags, ['<hr />']),
            self.view.MenuItemHTML_a.GetId() : (self.insertHtmlTags, ['<a href="">', '</a>']),
            self.view.MenuItemHTML_ol.GetId() : (self.insertHtmlTags, ['<ol>', '</ol>']),
            self.view.MenuItemHTML_dl.GetId() : (self.insertHtmlTags, ['<dl>', '</dl>']),
            self.view.MenuItemHTML_textarea.GetId() : (self.insertHtmlTags, ['<textarea>', '</textarea>']),
            self.view.MenuItemHTML_colgroup.GetId() : (self.insertHtmlTags, ['<colgroup>', '</colgroup>']),
            self.view.MenuItemHTML_i.GetId() : (self.insertHtmlTags, ['<i>', '</i>']),
            self.view.MenuItemHTML_caption.GetId() : (self.insertHtmlTags, ['<caption>', '</caption>']),
            self.view.MenuItemHTML_area.GetId() : (self.insertHtmlTags, ['<area>', '</area>']),
            self.view.MenuItemHTML_q.GetId() : (self.insertHtmlTags, ['<q>', '</q>']),
            self.view.MenuItemHTML_p.GetId() : (self.insertHtmlTags, ['<p>', '</p>']),
            self.view.MenuItemHTML_tt.GetId() : (self.insertHtmlTags, ['<tt>', '</tt>']),
            self.view.MenuItemHTML_del.GetId() : (self.insertHtmlTags, ['<del>', '</del>']),
            self.view.MenuItemHTML_button.GetId() : (self.insertHtmlTags, ['<button>', '</button>']),
            self.view.MenuItemHTML_div.GetId() : (self.insertHtmlTags, ['<div id="">', '</div>']),
            self.view.MenuItemHTML_col.GetId() : (self.insertHtmlTags, ['<col>', '</col>']),
            self.view.MenuItemHTML_ul.GetId() : (self.insertHtmlTags, ['<ul>', '</ul>']),
            self.view.MenuItemCSS_background.GetId() : (self.actionInsertCSS, "background: ;"),
            self.view.MenuItemCSS_background_attachment.GetId() : (self.actionInsertCSS, "background-attachment: ;"),
            self.view.MenuItemCSS_background_color.GetId() : (self.actionInsertCSS, "background-color: ;"),
            self.view.MenuItemCSS_background_image.GetId() : (self.actionInsertCSS, "background-image: ;"),
            self.view.MenuItemCSS_background_position.GetId() : (self.actionInsertCSS, "background-position: ;"),
            self.view.MenuItemCSS_background_repeat.GetId() : (self.actionInsertCSS, "background-repeat: ;"),
            self.view.MenuItemCSS_border.GetId() : (self.actionInsertCSS, "border: ;"),
            self.view.MenuItemCSS_border_collapse.GetId() : (self.actionInsertCSS, "border-collapse: ;"),
            self.view.MenuItemCSS_border_color.GetId() : (self.actionInsertCSS, "border-color: ;"),
            self.view.MenuItemCSS_border_spacing.GetId() : (self.actionInsertCSS, "border-spacing: ;"),
            self.view.MenuItemCSS_border_style.GetId() : (self.actionInsertCSS, "border-style: ;"),
            self.view.MenuItemCSS_border_width.GetId() : (self.actionInsertCSS, "border-width: ;"),
            self.view.MenuItemCSS_bottom.GetId() : (self.actionInsertCSS, "bottom: ;"),
            self.view.MenuItemCSS_caption_side.GetId() : (self.actionInsertCSS, "caption-side: ;"),
            self.view.MenuItemCSS_clear.GetId() : (self.actionInsertCSS, "clear: ;"),
            self.view.MenuItemCSS_clip.GetId() : (self.actionInsertCSS, "clip: ;"),
            self.view.MenuItemCSS_color.GetId() : (self.actionInsertCSS, "color: ;"),
            self.view.MenuItemCSS_content.GetId() : (self.actionInsertCSS, "content: ;"),
            self.view.MenuItemCSS_counter_increment.GetId() : (self.actionInsertCSS, "counter-increment: ;"),
            self.view.MenuItemCSS_counter_reset.GetId() : (self.actionInsertCSS, "counter-reset: ;"),
            self.view.MenuItemCSS_cursor.GetId() : (self.actionInsertCSS, "cursor: ;"),
            self.view.MenuItemCSS_direction.GetId() : (self.actionInsertCSS, "direction: ;"),
            self.view.MenuItemCSS_display.GetId() : (self.actionInsertCSS, "display: ;"),
            self.view.MenuItemCSS_empty_cells.GetId() : (self.actionInsertCSS, "empty-cells: ;"),
            self.view.MenuItemCSS_float.GetId() : (self.actionInsertCSS, "float: ;"),
            self.view.MenuItemCSS_font.GetId() : (self.actionInsertCSS, "font: ;"),
            self.view.MenuItemCSS_font_family.GetId() : (self.actionInsertCSS, "font-family: ;"),
            self.view.MenuItemCSS_font_size.GetId() : (self.actionInsertCSS, "font-size: ;"),
            self.view.MenuItemCSS_font_style.GetId() : (self.actionInsertCSS, "font-style: ;"),
            self.view.MenuItemCSS_font_variant.GetId() : (self.actionInsertCSS, "font-variant: ;"),
            self.view.MenuItemCSS_font_weight.GetId() : (self.actionInsertCSS, "font-weight: ;"),
            self.view.MenuItemCSS_height.GetId() : (self.actionInsertCSS, "height: ;"),
            self.view.MenuItemCSS_left.GetId() : (self.actionInsertCSS, "left: ;"),
            self.view.MenuItemCSS_letter_spacing.GetId() : (self.actionInsertCSS, "letter-spacing: ;"),
            self.view.MenuItemCSS_line_height.GetId() : (self.actionInsertCSS, "line-height: ;"),
            self.view.MenuItemCSS_list_style.GetId() : (self.actionInsertCSS, "list-style: ;"),
            self.view.MenuItemCSS_list_style_image.GetId() : (self.actionInsertCSS, "list-style-image: ;"),
            self.view.MenuItemCSS_list_style_position.GetId() : (self.actionInsertCSS, "list-style-position: ;"),
            self.view.MenuItemCSS_list_style_type.GetId() : (self.actionInsertCSS, "list-style-type: ;"),
            self.view.MenuItemCSS_margin.GetId() : (self.actionInsertCSS, "margin: ;"),
            self.view.MenuItemCSS_max_height.GetId() : (self.actionInsertCSS, "max-height: ;"),
            self.view.MenuItemCSS_max_width.GetId() : (self.actionInsertCSS, "max-width: ;"),
            self.view.MenuItemCSS_min_height.GetId() : (self.actionInsertCSS, "min-height: ;"),
            self.view.MenuItemCSS_min_width.GetId() : (self.actionInsertCSS, "min-width: ;"),
            self.view.MenuItemCSS_orphans.GetId() : (self.actionInsertCSS, "orphans: ;"),
            self.view.MenuItemCSS_outline.GetId() : (self.actionInsertCSS, "outline: ;"),
            self.view.MenuItemCSS_outline_color.GetId() : (self.actionInsertCSS, "outline-color: ;"),
            self.view.MenuItemCSS_outline_style.GetId() : (self.actionInsertCSS, "outline-style: ;"),
            self.view.MenuItemCSS_outline_width.GetId() : (self.actionInsertCSS, "outline-width: ;"),
            self.view.MenuItemCSS_overflow.GetId() : (self.actionInsertCSS, "overflow: ;"),
            self.view.MenuItemCSS_padding.GetId() : (self.actionInsertCSS, "padding: ;"),
            self.view.MenuItemCSS_page_break_after.GetId() : (self.actionInsertCSS, "page-break-after: ;"),
            self.view.MenuItemCSS_page_break_before.GetId() : (self.actionInsertCSS, "page-break-before: ;"),
            self.view.MenuItemCSS_page_break_inside.GetId() : (self.actionInsertCSS, "page-break-inside: ;"),
            self.view.MenuItemCSS_position.GetId() : (self.actionInsertCSS, "position: ;"),
            self.view.MenuItemCSS_quotes.GetId() : (self.actionInsertCSS, "quotes: ;"),
            self.view.MenuItemCSS_right.GetId() : (self.actionInsertCSS, "right: ;"),
            self.view.MenuItemCSS_table_layout.GetId() : (self.actionInsertCSS, "table-layout: ;"),
            self.view.MenuItemCSS_text_align.GetId() : (self.actionInsertCSS, "text-align: ;"),
            self.view.MenuItemCSS_text_decoration.GetId() : (self.actionInsertCSS, "text-decoration: ;"),
            self.view.MenuItemCSS_text_indent.GetId() : (self.actionInsertCSS, "text-indent: ;"),
            self.view.MenuItemCSS_text_transform.GetId() : (self.actionInsertCSS, "text-transform: ;"),
            self.view.MenuItemCSS_top.GetId() : (self.actionInsertCSS, "top: ;"),
            self.view.MenuItemCSS_unicode_bidi.GetId() : (self.actionInsertCSS, "unicode-bidi: ;"),
            self.view.MenuItemCSS_vertical_align.GetId() : (self.actionInsertCSS, "vertical-align: ;"),
            self.view.MenuItemCSS_visibility.GetId() : (self.actionInsertCSS, "visibility: ;"),
            self.view.MenuItemCSS_white_space.GetId() : (self.actionInsertCSS, "white-space: ;"),
            self.view.MenuItemCSS_widows.GetId() : (self.actionInsertCSS, "widows: ;"),
            self.view.MenuItemCSS_width.GetId() : (self.actionInsertCSS, "width: ;"),
            self.view.MenuItemCSS_word_spacing.GetId() : (self.actionInsertCSS, "word-spacing: ;"),
            self.view.MenuItemCSS_z_index.GetId() : (self.actionInsertCSS, "z-index: ;"),
            self.view.MenuItemWrapWord.GetId(): (self.actionWordWrap, ),
            }
        
        action = theActions[event.GetId()]
        
                        
        try:
            # one arg
            action[0](action[-1])
        except:
            try:
                # more than one argument
                action[0](*action[1])
            except:
                # no argument
                action[0]()
        
       
    def actionWordWrap(self):
        
        if self.editor.GetWrapMode() == self.view.wx.stc.STC_WRAP_WORD:
            self.editor.SetWrapMode(self.view.wx.stc.STC_WRAP_NONE)
            self.view.MenuItemWrapWord.Check(False)
        else:
            self.editor.SetWrapMode(self.view.wx.stc.STC_WRAP_WORD)
            self.view.MenuItemWrapWord.Check(True)
        
        


    def updateStatusInformation(self):
        """ file related """
            
        
        # Save button and menus
        
        page = self.noteBook.GetSelection()
        text = self.noteBook.GetPageText(page)
              
        # model = makerFile object
               
        # enable or disable Save As Template for .head files
        
        if self.model.getType() == ".head" and self.model.getName() != "rss":
            self.view.MenuItemSaveAsTemplate.Enable(True)
        else:
            self.view.MenuItemSaveAsTemplate.Enable(False)
                   
                
        if self.model.saved:
            self.saveButton.Disable()
            self.saveMenu.Enable(False)
            # noteBook
            if text.endswith("*"):
                self.noteBook.SetPageText(page, text.rstrip("*"))
            
            self.publishMenu.SetText("Publish [" + str(len(self.model.core.getFtpQueue())) + " Files in Queue]" )
            
            self.view.statusBar1.SetStatusText(number=4,
                                           text="FTP Queue: " + str(len(self.model.core.getFtpQueue())) 
                                           + " Files"
                                           )
        
            
                        
        else:
            self.saveButton.Enable()
            self.saveMenu.Enable(True)
            # noteBook
            if not text.endswith("*"):
                self.noteBook.SetPageText(page, text + "*")
                
                
  
      
        
