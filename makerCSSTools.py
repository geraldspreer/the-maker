import os
import re


class CSSTools:
    def listAllStyleSheetsInPath(self, path, ext=".css"):
        theResult = []

        for thing in os.listdir(path):
            (path, file) = os.path.split(thing)
            (one, two) = os.path.splitext(file)
            if two == ext:
                theResult.append(one + ext)

        return theResult

    def getIDsFromStyleSheet(self, fileName):
        f = open(fileName, "r")
        contents = f.read()
        f.close()

        ids = re.compile("#(.*?) |{", re.IGNORECASE).findall(contents)
        finalIDList = []
        new = []
        for item in ids:
            if new.count(item) == 0:
                if item != "":
                    new.append(item)
                    finalIDList.append(item)

        return finalIDList

    def getClassesFromStyleSheet(self, fileName):

        f = open(fileName, "r")
        contents = f.read()
        f.close()

        classes = re.compile("[.](.*?) |{", re.IGNORECASE).findall(contents)
        finalClassList = []
        new = []
        for item in classes:
            if new.count(item) == 0:
                if item != "":
                    new.append(item)
                    finalClassList.append(item)

        return finalClassList

    def listUsedStyleSheetsForFilename(self, fileName):
        """
        returns a list of stylesheets used in that file
        or False

        """
        name = os.path.splitext(fileName)[0]

        if os.path.isfile(name + ".head"):
            f = open(name + ".head", "r")
            contents = f.read()
            f.close()
            list = []
            # print self.listAllStyleSheetsInPath(os.path.split(fileName)[0] + "/")
            for stylesheet in self.listAllStyleSheetsInPath(
                os.path.split(fileName)[0] + "/"
            ):
                # print "looking for ", stylesheet
                quotes = ['"', "'"]
                for q in quotes:
                    if contents.count(q + stylesheet + q) < 1:
                        list.append(stylesheet)

            return list

        else:
            return False

        # return listOfFiles
