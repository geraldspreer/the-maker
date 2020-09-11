import wx


def getFaces():
    if wx.Platform == "__WXMSW__":
        faces = {
            "times": "Times New Roman",
            "mono": "Courier New",
            "helv": "Arial",
            "other": "Comic Sans MS",
            "size": 10,
            "size2": 8,
        }
    elif wx.Platform == "__WXMAC__":
        faces = {
            "times": "Times New Roman",
            "mono": "Courier New",
            "helv": "Arial",
            "other": "Comic Sans MS",
            "size": 13,
            "size2": 10,
        }
    else:
        faces = {
            "times": "Times",
            "mono": "Courier",
            "helv": "Helvetica",
            "other": "new century schoolbook",
            "size": 12,
            "size2": 10,
        }
    return faces


def styleTextCtrl(textCtrlToStyle):
    faces = getFaces()

    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_STYLE_DEFAULT, "face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleClearAll()  # Reset all to be like the default

    # Global default styles for all languages
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_STYLE_DEFAULT, "fore:#000000,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_STYLE_LINENUMBER,
        "back:#C0C0C0,face:%(other)s,size:%(size2)d" % faces,
    )
    textCtrlToStyle.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold"
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold"
    )

    # Python styles
    # Default
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_DEFAULT, "fore:#000000,face:%(other)s,size:%(size)d" % faces
    )

    # HTML tags
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_TAG, "fore:#882288,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_ATTRIBUTE, "fore:#993300,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_ATTRIBUTEUNKNOWN,
        "fore:#993300,face:%(other)s,size:%(size)d" % faces,
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_TAGEND, "fore:#993399,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_OTHER, "fore:#882288,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_COMMENT, "fore:#006600,face:%(other)s,size:%(size)d" % faces
    )

    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_SINGLESTRING, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_DOUBLESTRING, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_H_NUMBER, "fore:#00ff00,face:%(other)s,size:%(size)d" % faces
    )

    # php
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_DEFAULT, "fore:#2200bb,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_COMMENT, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_COMMENTLINE, "fore:#00aa00,face:%(other)s,size:%(size)d" % faces
    )

    # " foo "
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_HSTRING, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_HSTRING_VARIABLE,
        "fore:#000000,face:%(other)s,size:%(size)d" % faces,
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_NUMBER, "fore:#aa0000,face:%(other)s,size:%(size)d" % faces
    )

    # {} () =
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_OPERATOR, "fore:#000000,face:%(other)s,size:%(size)d" % faces
    )
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_SIMPLESTRING,
        "fore:#2244bb,face:%(other)s,size:%(size)d" % faces,
    )

    # $foo
    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_VARIABLE, "fore:#993300,face:%(other)s,size:%(size)d" % faces
    )

    textCtrlToStyle.StyleSetSpec(
        wx.stc.STC_HPHP_WORD, "fore:#ff0000,face:%(other)s,size:%(size)d" % faces
    )

    textCtrlToStyle.SetCaretForeground("BLUE")

    textCtrlToStyle.SetMarginWidth(0, 30)
    textCtrlToStyle.SetMarginWidth(1, 0)
    textCtrlToStyle.SetMarginType(0, 1)
