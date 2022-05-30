import os
import makerCSSTools
import makerController

class AutoComplete(makerController.SuperController):
    def __init__(self, model, view, editor):
        self.editor = editor
        self.view = view
        self.model = model
        self.createAbstractNameForViewObjects()
        self.bindActions()

    def bindActions(self):
        self.editor.Bind(self.view.wx.stc.EVT_STC_CHARADDED, self.autoComplete)

    def createAbstractNameForViewObjects(self):
        pass

    def autoComplete(self, event):
        # support functions
        def showAutoCompList(function):
            self.editor.SetAnchor(self.editor.GetCurrentPos())

            items = function()
            if items == []:
                return
            items.sort()
            self.editor.AutoCompSetSeparator(124)  # 124 == |
            self.editor.AutoCompShow(0, "|".join(items))

        def showAutoCompListForTags(function):
            items = function()
            items.sort()

            self.editor.AutoCompSetSeparator(124)  # 124 == |
            self.editor.AutoCompShow(0, "|".join(items))

        def makeListOfPossibleLinks():
            listOfLinks = [u"http://www.", u"mailto:", u"callto:"]

            for item in self.model.core.getLocalFilesFromDistTable():
                listOfLinks.append(item + self.quotes + " ")
                #                         can either be ' or " and a space is added
                # so that after inserting the user can continue to
                # type in the proper position

            return listOfLinks

        def getArgument(leftOfArg, rightOfArg, searchRange):
            """For completing quotes we find out what the argument is

            e.g. arg="
            """

            startingPos = self.editor.GetCurrentPos()
            self.editor.SearchAnchor()
            result = self.editor.FindText(
                startingPos - searchRange,
                startingPos,
                leftOfArg + ".*" + rightOfArg,
                self.view.wx.stc.STC_FIND_REGEXP,
            )

            if result == -1:
                self.editor.SetCurrentPos(startingPos)
                self.editor.SetSelection(startingPos, startingPos)
                return False

            self.editor.SetSelection(result, startingPos)
            argument = self.editor.GetSelectedText()[1:-1]  # trim
            self.editor.SetCurrentPos(startingPos)

            return argument

        def getCSSIds():
            name = os.path.join(
                self.model.core.getPathParts(), self.model.core.getCurrentFileName()
            )
            css = cssTool.listUsedStyleSheetsForFilename(name)
            if not css:
                return None
            listOfIds = []
            for sheet in css:
                for id in cssTool.getIDsFromStyleSheet(
                    os.path.join(self.model.core.getPathParts(), sheet)
                ):
                    listOfIds.append(id)

            return listOfIds

        def getCSSClasses():
            name = os.path.join(
                self.model.core.getPathParts(), self.model.core.getCurrentFileName()
            )
            css = cssTool.listUsedStyleSheetsForFilename(name)
            if not css:
                return None
            listOfClasses = []
            for sheet in css:
                for id in cssTool.getClassesFromStyleSheet(
                    os.path.join(self.model.core.getPathParts(), sheet)
                ):
                    listOfClasses.append(id)

            return listOfClasses

        def getListOfDynamics():
            list = self.model.core.getFilesByExtension(".dynamic")
            finalList = []
            for item in list:
                finalList.append(item + " />")

            return finalList

        def getImageList():
            final = []
            q = self.quotes
            for image in self.model.core.getImageFiles():
                final.append(image + self.quotes)
            return final

        def autoCompleteHTML():
            """
            is autocompleting XHTML tags
            <tag> becomes </tag>
            with the cursor in between the tags like this
            <tag>|</tag>
            """
            currentPosition = self.editor.GetCurrentPos()

            if (
                self.editor.GetTextRange(currentPosition - 2, currentPosition - 1)
                == "/"
            ):
                # slash found, this is a complete tag
                # eg. <br />
                return

            elif (
                self.editor.GetTextRange(currentPosition - 2, currentPosition - 1)
                == "-"
            ):
                # dash found, this is a comment
                # eg. <!-- -->
                return

            self.editor.SearchAnchor()
            openB = self.editor.SearchPrev(self.view.wx.stc.STC_FIND_REGEXP, "<")

            if openB == -1:
                # there is no matching open brace
                # so > is a bigger than sign
                self.editor.GotoPos(currentPosition)
                return

            else:
                # openB is our matching < brace

                self.editor.GotoPos(openB)
                self.editor.SearchAnchor()
                space = self.editor.SearchNext(self.view.wx.stc.STC_FIND_REGEXP, " ")

                if space == -1 or space > currentPosition:
                    # there is no space or:
                    #     the space is from somewhere else in the text
                    complete = self.editor.GetTextRange(openB + 1, currentPosition - 1)
                else:

                    if space < currentPosition:
                        complete = self.editor.GetTextRange(openB + 1, space)
                    else:
                        # for all other cases
                        complete = ""

                #                # < a href="#"> fix for leading spaces
                #  ^- trouble
                if len(complete) == 0:
                    self.editor.GotoPos(currentPosition)

                # check for slashes

                elif "/" in complete:
                    self.editor.GotoPos(currentPosition)

                else:
                    self.editor.GotoPos(currentPosition)
                    self.editor.AddText("</" + complete + ">")
                    # set the cursor in between the tags
                    self.editor.GotoPos(currentPosition)

        def autoCompleteHTMLArgument():

            currentPosition = self.editor.GetCurrentPos()
            argument = getArgument(" ", self.quotes, 8)
            if argument == "src=":

                showAutoCompList(getImageList)

            elif argument == "href=":

                showAutoCompList(makeListOfPossibleLinks)

            elif argument == "class=":
                if getCSSClasses():
                    showAutoCompList(getCSSClasses)

            elif argument == "id=":
                if getCSSIds():
                    showAutoCompList(getCSSIds)

            cssArgument = getArgument(":", "(", 10)

            if cssArgument != False and cssArgument.count("url") != 0:
                showAutoCompList(getImageList)

        def autoCompleteDynamic():
            currentPosition = self.editor.GetCurrentPos()
            argument = getArgument("_", "c", 10)

            if argument == "dynamic":

                showAutoCompList(getListOfDynamics)

        def autoCompleteTag():

            showAutoCompListForTags(getTagList)

        def getTagList():
            return [
                "maker_dynamic",
                "body",
                "head",
                "html",
                "span",
                "div id=",
                "style",
                "meta",
                "link",
                "DOCTYPE",
                "title",
                "em",
                "pre",
                "code",
                "h2",
                "h3",
                "h1",
                "h6",
                "h4",
                "ins",
                "strong",
                "bdo",
                "dfn",
                "var",
                "samp",
                "cite",
                "blockquote",
                "acronym",
                "abbr",
                "br />",
                "address",
                "h5",
                "q",
                "p",
                "del",
                "kbd",
                "a name=",
                "a href=",
                "base",
                "map",
                "object",
                "param",
                "img src=",
                "area",
                "dl",
                "ol",
                "dd",
                "li",
                "ul",
                "dt",
                "colgroup",
                "tr",
                "tbody",
                "caption",
                "tfoot",
                "th",
                "table",
                "td",
                "col",
                "thead",
                "fieldset",
                "form",
                "textarea",
                "button",
                "label",
                "optgroup",
                "input",
                "legend",
                "select",
                "option",
                "noscript",
                "script",
                "b",
                "sub",
                "i",
                "big",
                "tt",
                "hr />",
                "sup",
                "small",
            ]

        # end support functions

        cssTool = makerCSSTools.CSSTools()
        key = event.GetKey()

        if key == 62:
            autoCompleteHTML()
        elif key == self.view.wx.WXK_RETURN:
            indentPrev = self.editor.GetLineIndentation(
                self.editor.GetCurrentLine() - 1
            )
            self.editor.SetLineIndentation(self.editor.GetCurrentLine(), indentPrev)
            self.editor.GotoPos(
                self.editor.GetLineIndentPosition(self.editor.GetCurrentLine())
            )

        elif key == 60:
            autoCompleteTag()
        elif key == 34 or key == 39:  # checking for quotes
            self.quotes = '"'
            if key == 39:
                self.quotes = "'"
            autoCompleteHTMLArgument()
        # css autocomplete
        elif key == 40:  # check for (
            self.quotes = ""
            autoCompleteHTMLArgument()
        elif key == 58:
            autoCompleteDynamic()
        else:
            pass
