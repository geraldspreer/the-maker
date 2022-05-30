import os
import re
from sets import Set
import time
import shutil
import re
import urllib
import urlparse
import cPickle
import string
from xml.sax import parse
from xml.sax.handler import ContentHandler
import sys
import webbrowser
import subprocess

import makerFileController
from makerUtilities import readFile, writeFile
import makerRenameFile
import makerCSSTools
import markdown2

def afterThisUpdateStatus(func):
    def wrapped(*args, **kwds):
        self = args[0]
        func(*args, **kwds)
        # for now we have to do this check
        #print "here we go"
        try:
            if self.fileController:
                self.fileController.updateStatusInformation()
        except Exception, e:
            print "makerFile"
            print "unable to process: afterThisUpdateInfo"
            print "exception: ", str(e)
    return wrapped

class MakerFile:
    def __init__(self, projectModel, filename, view=True, newFile = False):
        """
        This is a super class for all MakerFiles 
        a MakerFile is always stored in the /parts
        Folder of the project
        """
        self.saved = True
        self.flag  = None
        self.name  = filename
        self.core  = projectModel
        self.setType()
        self.setEditable()
        if newFile:
            self.firstWrite()
        self.setPrintable()
        if view:
            self.fileController = makerFileController.MakerFileController(self, self.core.projectController.view)
        else:
            self.fileController = None

    def firstWrite(self):
        """ is a new file of this kind is created this method is called 
            writing the template to the file
        """
        writeFile(os.path.join(self.core.getPathParts(), 
                               self.getName() + self.type), 
                               self.getNewFileTemplate())
    def getCommentTags(self):
        """ tags for comments used in this file type """
        return ["<!--  ","  -->"]
    
    def publish(self):
        if self.getEditable():
            self.core.backupLocalFile()
            self.core.updateAllImageReferences()

        for target in self.getFTPInformation():
            remDir = target[0]
            remFileName = target[1]
            ftpMode = target[2]
            if not self.core.checkIfRemoteDirIsDir(remDir):
                self.core.makeRemoteDir(remDir)
            self.core.uploadFile(self.core.getPathParts() + self.getRealName(),
                                 str(remDir),
                                 str(remFileName),
                                 str(ftpMode))
        self.core.restoreLocalFile()
  
    def closeFile(self, callController=False):
        if callController:
            self.fileController.closeCurrentFile(callModel = False)
        if len(self.core.projectManager.controller.noteBookPages) == 0:
               self.core.setCurrentFile(None)

    def saveAsTemplate(self):
        """ overridden in .head files"""
        pass

    def getLanguage(self):
        """ returns None 
        this is default for all language independent files
        """
        return None
    
    def getNameGroupAndProject(self):
        """ returns [name , group, project]"""
        return [self.getName(), self.getType(), self.core.getProject()]
    
    def getProject(self):
        """ returns the name of the project that the file belongs to
            as String
        """
        return self.core.getProject()
    
    def getProjectInstance(self):
        """ returns the instance of the project that the file belongs to
        """
        return self.core
      
    def output(self, message):
        pass

    def setPrintable(self):
        self.printable = True

    def getPrintable(self):
        return self.printable

    def getEditable(self):
        """Returns a boolean indicating if this file is editable or not."""
        return self.editable
    
    def setEditable(self):
        """A MakerFile by default is editable. Override this method to alter."""
        self.editable = True
    
    def setName(self, theName):
        self.name = theName
        
    def getName(self):
        return self.name

    def getFileName(self):
        """Refers to the filename as it is in project directory parts/."""
        return self.getName() + self.getType()

    def getFullName(self):
        """Returns full path to file, including path parts."""
        # TO DO: convert to use os.path.join()
        return self.core.getPathParts() + self.getRealName()

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag
    
    def getRealName(self):
        """Returns the full filename. Overridden for some files"""
        return self.getName() + self.getType()

    def preview(self, theContent):
        filePath = self.core.getPathParts() + "tmp.htm" 
        writeFile(filePath, theContent)
        try:
            webbrowser.open('file://' + filePath, autoraise=0)
        except: 
            print "unable to open ", urlToOpen

    def getFTPInformation(self):
        return self.core.distribute(self.getRealName())

    def setType(self):
        self.output('Setting type')
        self.type ="!makerFile"
    
    def getType(self):
        return self.type
    
    @afterThisUpdateStatus
    def load(self):
        try:
            self.fileController.loadTextIntoEditor(readFile(self.getFullName()).decode(self.core.encoding))
        except:
            self.fileController.loadTextIntoEditor(readFile(self.getFullName()).decode('latin-1'))
        
    def unEditableFileMessage(self):
        m  = '    %s \n\n    cannot be edited with TheMaker\n ' % self.getRealName()
        m += '    as it is a binary (%s) file.\n\n' % self.getType()
        m += '    You may only preview and publish it.'
        return m
    
    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        
        writeFile(os.path.join(self.core.getPathParts(), self.getName() + self.type), text)
        self.setSaved()
        self.core.addToFtpQueue(self.getFileName())
    
    def setOpen(self):
        """Sets the saved flag to False."""
        self.output('File %s has changed' % self.getFileName())
        self.saved = False
        
    # ------------------------------------------------------------        
    
    @afterThisUpdateStatus
    def setSaved(self, saved=True):
        """Sets self.saved flag to True  or false"""
        self.saved = saved
        
    def getSaved(self):
        return self.saved
        
    def delete(self):
        def deleteRemote():
            if self.core.serverLogin() == False:
                print "unable to perform login"
                return False
            info = self.getFTPInformation()
            results = []
            # multiple remote locations are possible
            for i in info:
                result = self.core.deleteRemoteFile(i[0], i[1])
                results.append(result)
            self.core.serverLogout()
            if False in results:
                return False
            else:
                return True 
        
        m = "Do you really want to delete the file: '" + self.getRealName() 
        m += "' from project: '" + self.core.getProject() 
        if self.fileController.askYesOrNo(m) == "No":
            return
        if self.core.checkIfProjectIsSetUp():
            if not deleteRemote():
                if self.fileController.askYesOrNo("Unable to delete remote file!\n " +
                                                  "Would you like to delete the local file anyway ?") == "No":
                    return
        
        os.remove(self.getFullName())
        self.core.deleteFromDistributionTable(self.getRealName())
        self.core.projectController.treeViewDeleteItem(self.fileController.getReferringTreeItem())
        self.closeFile(callController = True)
        if self.core.isFileInQueue(self.getFileName()):
            self.core.deleteFromFtpQueue(self.getFileName())
    
    def printViaBrowser(self):
        """
        Is sending the contents of the current file to a webbrowser for printing
        This printing method works for most text files 
        It is overridden in some derived classes
        """
        printHeader = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="expires" content="0" />
    <title></title>
</head>
<body onLoad="javascript:window.print();">
<pre>"""
        source = readFile(os.path.join(self.core.getPathParts(), self.getName() + 
                                       self.getType()))
        aSource = source.replace("<", "&lt;")
        bSource = aSource.replace(">", "&gt;")
        theContent = printHeader + bSource
        theContent += "</pre></html>" 
        writeFile(os.path.join(self.core.getProjectPath(), "makerPrintOut.html"), theContent)
        webbrowser.open("file:///" + os.path.join(self.core.getProjectPath(), "makerPrintOut.html"))
    
    def rename(self):
        """
        Renames the current MakerFile to the new name (after ensuring the name
        is not taken already) as well as renaming the source name in the 
        distribution table.
        """
        makerRenameFile.MakerFileRename(self, self.fileController.view)

# ------------------------------------------------------------            
# ------------------------------------------------------------            
# ------------------------------------------------------------            

class MakerFileHeadTemplate(MakerFile):
    def __init__(self, projectModel, filename, view=True, newFile = False):
        """
        This is a super class for all MakerFiles 
        a MakerFile is always stored in the /parts
        Folder of the project
        """
        self.saved = True
        self.flag  = None
        self.name  = filename
        self.core  = projectModel
        self.setType()
        self.setEditable()
        self.setPrintable()
        if view:
            self.fileController = makerFileController.MakerFileController(self, self.core.projectController.view)
        else:
            self.fileController = None
  
    def firstWrite(self):
        """ is a new file of this kind is created this method is called 
            writing the template to the file
        """
        self.fileController.errorMessage("you cannot create .head template files")
    def publish(self):
        self.fileController.infoMessage("This is a local file")
        return None        
  
    def closeFile(self, callController=False):
        if callController:
            self.fileController.closeCurrentFile(callModel = False)
        if len(self.core.projectManager.controller.noteBookPages) == 0:
               self.core.setCurrentFile(None)
  
    def getLanguage(self):
        """ returns None 
        this is default for all language independent files
        """
        return None
    
    def setName(self, theName):
        self.name = theName
        
    def getName(self):
        return self.name

    def getFileName(self):
        """Refers to the filename as it is in project directory parts/."""
        return self.getName() + self.getType()

    def getFullName(self):
        """Returns full path to file, including path parts."""
        # TO DO: convert to use os.path.join()
        return self.core.getProjectPath()+"/"+"templates/" + self.getRealName()

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag        

    def getRealName(self):
        """Returns the full filename. Overridden for some files"""
        return self.getName() + self.getType()

    def preview(self, theContent):
        filePath = self.core.getPathParts() + "tmp.htm" 
        writeFile(filePath, theContent)
        try:
            webbrowser.open('file://' + filePath, autoraise=0)    
        except: 
            print "unable to open ", urlToOpen

    def getFTPInformation(self):
        return None

    def setType(self):
        self.output('Setting type')
        self.type =".head"
    
    def getType(self):
        return self.type

    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(self.getFullName(), text)
        self.setSaved()
        
    def delete(self):
        self.fileController.infoMessage("You cannot delete this file.")    
    
    def rename(self):
        """
        Renames the current MakerFile to the new name (after ensuring the name
        is not taken already) as well as renaming the source name in the 
        distribution table.
        """
        self.fileController.infoMessage("You cannot rename this file.")
    
    @afterThisUpdateStatus
    def load(self):
        self.fileController.infoMessage(readFile(self.getFullName()))
        self.fileController.loadTextIntoEditor(readFile(self.getFullName()).decode(self.core.encoding))

# ------------------------------------------------------------            
# ------------------------------------------------------------            
# ------------------------------------------------------------            


class MakerFilePython(MakerFile):
    def setType(self):
        self.type = '.py'
    
    def setEditable(self):
        self.editable = True
    
    def getCommentTags(self):
        """ tags for comments used in this file type """
        return ['#','']
    
    def preview(self, content = None):
        """ in this case == Run """
        filePath = self.core.getPathParts() + self.getFileName()
        self.fileController.pythonShell(filePath)

# ------------------------------------------------------------ 
# ------------------------------------------------------------ 
# ------------------------------------------------------------ 

class MakerFilePhp(MakerFile):
    def setType(self):
        self.type = '.php'
    
    def setEditable(self):
        self.editable = True
  
    def getCommentTags(self):
        """ tags for comments used in this file type """
        return ["/*  ","  */"]

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   

class MakerFileMov(MakerFile):     
    def save(self):
        pass
    
    def setPrintable(self):
        self.printable = False
    
    def setType(self):
        self.type = ".mov"
    
    def load(self):
        self.fileController.loadTextIntoEditor(self.unEditableFileMessage(), binary = True)
        self.fileController.disableEditor()

    def setEditable(self):
        self.editable = False
    
    def preview(self, Content=None):
        """Content is ignored since it is not editable."""
        webbrowser.open('file://'+self.getFullName(), autoraise=1)

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------      

class MakerFilePdf(MakerFile):     
    def setType(self):
        self.type = ".pdf"
     
    def save(self):
        pass

    def load(self):
        self.fileController.loadTextIntoEditor(self.unEditableFileMessage(), binary = True)
        self.fileController.disableEditor()
   
    def setEditable(self):
        self.editable = False

    def preview(self, theContent=None):
        """Content is ignored since it is not editable."""
        webbrowser.open('file://'+self.getFullName(), autoraise=1)

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------

class MakerFileZip(MakerFile):
    def setPrintable(self):
        self.printable = False

    def setType(self):
        self.type = ".zip"

    def load(self):
        self.fileController.loadTextIntoEditor(self.unEditableFileMessage(), binary = True)
        self.fileController.disableEditor()
    def save(self):
        pass
    
    def setEditable(self):
        self.editable = False

    def preview(self, theContent=None):
        pass

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   

class MakerFileXml(MakerFile):     
    def setType(self):
        self.type = ".xml"

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   

class MakerFileHtml(MakerFile):
    def setType(self):
        self.type = '.html'

    def preview(self, Content=None):
        """Content is ignored since it is not editable."""
        webbrowser.open('file://'+self.getFullName(), autoraise=1)
   
# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------           
        
class MakerFileContent(MakerFile):
    def publish(self):
        self.core.backupLocalFile()
        self.core.updateAllImageReferences()
        self.core.applyMakerMetaStamp()
        self.makeWebSite()
        self.updateFileBase()
        
        for target in self.getFTPInformation():
            remDir = target[0]
            remFileName = target[1]
            ftpMode = target[2]
            if not self.core.checkIfRemoteDirIsDir(remDir):
                self.core.makeRemoteDir(remDir)
            self.core.uploadFile(self.core.getPathParts() + self.getRealName(),
                                 str(remDir),
                                 str(remFileName),
                                 str(ftpMode))
            # store RSS since this is .content file
            self.core.uploadFile(self.core.getPathParts() + self.core.currentFile.getRSSName(),
                                 str(remDir),
                                 self.core.currentFile.getRSSName(),
                                 str(ftpMode))
        self.core.restoreLocalFile()
  
    def getHead(self):
        return os.path.splitext(self.getName())[0] 
    
    def setType(self):
        self.type = ".content"   

    def getRealName(self):
        """Returns the full filename."""
        return self.getName()+".htm"

    def getEditModeName(self):
        return self.core.getPathParts()+self.getName()+self.core.getContentEditMode()
        
    def getRSSName(self):
        return self.getName()+'.rss'    

    @afterThisUpdateStatus
    def load(self):
        self.fileController.loadTextIntoEditor(readFile(self.getEditModeName()).decode(self.core.encoding))
    
    def preview(self, theContent):
        """Invokes MakeWebsite."""
        the_content = readFile(self.getEditModeName())
        writeFile(self.getEditModeName(), theContent)
        self.makeWebSite(preview = True)

        urlToOpen = 'file://'+self.core.getPathParts()+self.getRealName()
        webbrowser.open(urlToOpen, autoraise=1)
        writeFile(self.getEditModeName(), the_content)

    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(os.path.join(self.core.getPathParts(), self.getName() + self.type), text)
        self.setSaved()
        self.makeWebSite(preview = True)
        self.core.addToFtpQueue(self.getFileName())

    def getFTPInformation(self):
        return self.core.distribute(self.getRealName())
    
    def getLanguage(self):
        possibleLanguages = self.core.getProjectLanguages()
        
        for lang in possibleLanguages:
            if self.getName().endswith("_" + lang):
                return lang
    
    def makeWebSite(self , preview = False):
        """
        Build website from parts - invoked by preview
        rss creation has been removed !        
        Calls self.updateDynamic().
        """
        pathParts = self.core.getPathParts()
        lang = self.getLanguage()
        writeFile(self.core.getPathParts()+self.getRealName(), ' ')
        name0 = pathParts + self.name + '.head'
        name1 = pathParts + lang + '.body'
        name2 = pathParts + lang + '.nav'
        name3 = pathParts + self.name+self.type
        name4 = pathParts + lang + '.foot'
        sourceMarkers = ['head', 'top of page', 'navigation', 'content', 'foot']
        theList = [name0, name1, name2, name3, name4]      
        for aFile, sMarker in zip(theList, sourceMarkers):
            out  = readFile(aFile)
            out += "\n\n\n<!-- end of part: %s -->\n\n" % sMarker
            writeFile(self.getFullName(), out, append=True)
        self.updateDynamic()
        text = readFile(self.getFullName())

        for marker in self.core.markers:
            this = marker.encode(self.core.encoding)
            that = self.core.getDataForMakerMarker(marker).encode(self.core.encoding)
            something = text.replace(this, that)
            text = something

        # Handle markdown
        markD = re.compile('<markdown>(.*?)</markdown>', re.DOTALL | re.IGNORECASE).findall(text)
        for md in markD:
            #ITB 25/10/2011 add support for tables and footnotes in markdown
            mdHTML = (markdown2.markdown(md.decode("latin-1"), extras=["wiki-tables","footnotes"])).encode("latin-1")
            text = text.replace('<markdown>' + md + '</markdown>', mdHTML)

        writeFile(self.getFullName(), text)
        self.createRSSFeed(self.getFullName())
        if not preview:
            self.core.addToFtpQueue(self.getFileName())

    def createRSSFeed(self, HTMLFile):
        """
        Creates an RSS 2.0 Feed from a given HTML File.
        The feed is saved under the same filename but with the extension .rss.
        It also extends the existing HTML file with a list of anchors.
        """
        content = readFile(HTMLFile)
        headlines  = re.compile('<h1>(.*?)</h1>', 
                                re.DOTALL |  re.IGNORECASE).findall(content)
        uniqueSet = Set(headlines)
        headlines = list(uniqueSet)
        for i in headlines:
            #
            # this might need some explanation
            #
            # * the anchor is attached BEFORE the h1 so we do not get in trouble
            # with exising anchors inside the h1 tag
            #
            # the style of the a tag is set to display none so it does not 
            # interfere with existing styles and settings
            #
            this = "<h1>%s</h1>" % str(i)
            that = "<a name='" + i.replace(" ", "_") + "'> </a>\n<h1>" + i + "</h1>"
            new = content.replace(this, that)
            content = new
        
        # replace RSS link placeholder        
        new = content.replace("!RSS!", self.name.encode(self.core.encoding)+".rss")
        content = new
        
        # write the updated HTML to File        
        writeFile(HTMLFile, content)
        location = (self.core.getPageLocationsBySource(self.name+".htm"))[0]
        rss = ""
        
        for i in headlines:
            link = urlparse.urljoin(self.core.getProjectURL(), location)
            link = link.encode(self.core.encoding) + "#" + i.replace(" ", "_")
            rss +=  "<item>"
            rss += "<title>%s</title>" % str(i)
            rss += "<link>%s</link>" % str(link)
            rss += "</item>\n"
        
        _head = readFile(os.path.join(self.core.getPathParts(),'rss.head'))
        _foot = readFile(os.path.join(self.core.getPathParts(),'rss.foot'))

        fName  = os.path.join(self.core.getPathParts(),self.name+'.rss')
        writeFile(fName, _head + rss + _foot)

    def updateDynamic(self):
        text = readFile(self.getFullName())
        if text.find("<maker_dynamic") == -1:
            return
        
        if self.core.getFilesByExtension(".dynamic") != []:
            for i in self.core.filterFilesByLanguage(self.core.getFilesByExtension(".dynamic")):
                # self.output("replacing dynamic: %s" % str(i))
                # TO DO 
                # make this faster
                dynamicContent = readFile(self.core.getPathParts()+i+".dynamic")
                newtext = text.replace(str("<maker_dynamic:" + i + " />").encode(self.core.encoding), dynamicContent) 
                text = newtext
            writeFile(self.getFullName(), newtext)

    def updateFileBase(self):
        """
        Works on the finished HTML file and searches the distribution 
        table and current file for ftp_sources. In a second step the 
        file references are completed with the absolute path of the file.
        """
        text = readFile(self.getFullName())
        sourceList = []
        
        class XmlReader(ContentHandler):
            def __init__(XmlReader, scrwid=79, *args):
                ContentHandler.__init__(XmlReader, *args)
                
            def startElement(XmlReader, name, attrs):
                XmlReader.start_name = name
                        
                if XmlReader.start_name == "rule":
                    sourceList.append(attrs.get("ftp_source"))

            def endElement(XmlReader, name):
                pass
                
            def characters(XmlReader, chars):                        
                pass
                
        parse(self.core.getDistributionTableFilename(), XmlReader())
              
        for i in sourceList:
            try:
                print text.index(i.encode(self.core.encoding))
            except:
                print 'Unable to print text.index(i) for: %s' % str(i)
            
            if text.find(i.encode(self.core.encoding))==-1:
                print "DEBUG: cannot find ",i," in file..."
            else:
                loc = self.core.getPageLocationsBySource(i)
                location = urlparse.urljoin(self.core.url,loc[0])
                toReplace = [['"','"'],["'","'"],['"','?'],["'","?"]]
                for quotes in toReplace:
                    this = quotes[0] + i.encode(self.core.encoding) + quotes[1]
                    that = quotes[0] + location.encode(self.core.encoding) + quotes[1]
                    newtext = text.replace(this, that)
                    text = newtext
        bar = text
        imagelist = self.core.getImageFiles()
        for image in imagelist:
            image = image.encode(self.core.encoding)
            if bar.find('"'+image+'"')==-1:
                pass
            else:
                this = '"'+image+'"'
                that = '"'+urlparse.urljoin(self.core.getProjectURL(),
                                            self.core.getRemoteGfxFolder())
                that += image+'"'
                that = str(that).encode(self.core.encoding)
                new = bar.replace(this, that)
                bar = new
                text = new
        writeFile(self.core.getPathParts()+self.name+".htm", text)

    def delete(self):
        def deleteRemote():
            if self.core.serverLogin() == False:
                return False
            info = self.getFTPInformation()
            results = []
            # multiple remote locations are possible
            for i in info:
                results.append(self.core.deleteRemoteFile(i[0], i[1]))
            self.core.serverLogout()
            if False in results:
                return False
            else:
                return True 
        
        m = "Do you really want to delete the file: '" + self.getRealName() 
        m += "' from project: '" + self.core.getProject()
        
        if self.fileController.askYesOrNo(m) == "No":
            return
        
        if self.core.checkIfProjectIsSetUp():
            if not deleteRemote():
                if self.fileController.askYesOrNo("Could not delete remote file. " +
                                                      " Would you like to delete the local file anyway ?") == "No":
                    return
        
        os.remove(self.core.getPathParts()+self.getName()+".head")
        os.remove(self.core.getPathParts()+self.getName()+".content")
        self.core.deleteFromDistributionTable(self.getRealName())
        self.core.projectController.treeViewDeleteItem(self.fileController.getReferringTreeItem())
        self.closeFile(callController = True)

        print self.core.getFtpQueue()
        if self.core.isFileInQueue(self.getFileName()):
            self.core.deleteFromFtpQueue(self.getFileName())

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   

class MakerFileCss(MakerFile):
    def setType(self):
        self.type = ".css"

    def getCommentTags(self):
        """ tags for comments used in this file type """
        return ["/*  "," */"]
     
    def preview(self, theContent):
        """
        Preview for .css files is using either an already opened .content file or
        one from inside the project to show changes to the stylesheet in the browser
        """
        current_version = readFile(self.getFullName())
        writeFile(self.getFullName(), theContent)
        openFiles = self.core.projectManager.openFiles
        contentFiles = []

        # get open .content files
        for instance in openFiles:
            if instance.getType() == ".content":
                contentFiles.append(instance.getFullName())
        if contentFiles == []:
            contentFiles = self.core.getFilesByExtension(".content")
            # ok there are .content files in the project
            if contentFiles == []:
                writeFile(self.getFullName(), current_version)
                return
            else:
                # use right extensions
                correctExtensions = []
                for f in contentFiles:
                    correctExtensions.append(os.path.join(self.core.getPathParts(), f + ".htm"))
                contentFiles = correctExtensions
        tool = makerCSSTools.CSSTools()
        for file in contentFiles:
            if self.getRealName() in tool.listUsedStyleSheetsForFilename(file):
                urlToOpen = 'file://'+ file
                webbrowser.open(urlToOpen, autoraise=0)    
                writeFile(self.getFullName(), current_version)
                return

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   
class MakerFileCgi(MakerFile):
    def setType(self):
        self.type =".cgi"

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   
class MakerFileJs(MakerFile):
    def setType(self):
        self.type =".js"

    def getCommentTags(self):
        """ tags for comments used in this file type """
        return ["/*  ","  */"]

# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   
class MakerFileTxt(MakerFile):
    def setType(self):
        self.type =".txt"
# ------------------------------------------------------------ 
# ------------------------------------------------------------   
# ------------------------------------------------------------   

class MakerFileDynamic(MakerFile):
    def getLanguage(self):
        possibleLanguages = self.core.getProjectLanguages()
        for lang in possibleLanguages:
            if self.getName().endswith("_" + lang):
                return lang
    def delete(self):
        m = "Do you really want to delete the file: '" + self.getRealName() 
        m += "' from project: '" + self.core.getProject()
        if self.fileController.askYesOrNo(m) == "No":
            return
        os.remove(self.getFullName())
        self.core.projectController.treeViewDeleteItem(self.fileController.getReferringTreeItem())
        self.closeFile(callController = True)
        
    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(os.path.join(self.core.getPathParts(), self.getName() + self.type), text)
        self.setSaved()
        self.curr = self.core.getCurrentFile()
        filesUsingThisDynamic = self.core.findContentFilesContainingThisDynamic(self.getName())
        if filesUsingThisDynamic != []:
            fileList = ""
            for x in filesUsingThisDynamic:
                self.core.addToFtpQueue(x + ".content")                
                fileList = fileList + x + ".content\n"
                self.core.justInitFile(x,".content")
                self.core.currentFile.makeWebSite()
            self.core.setCurrentFile(self.curr)
    
    def preview(self, theContent):
        """Preview for dynamic files."""
        filePath = self.core.getPathParts()+"tmp.htm" 
        writeFile(filePath, theContent)
        
        try:
            webbrowser.open('file://' + filePath, autoraise=0)    
        except: 
            print "unable to open ", urlToOpen
        
    def setType(self):
        self.type =".dynamic"

class MakerFileUnsupportedTextFile(MakerFile):
    def __init__(self, core, filename, view=True):
        """
        this is a class that handles imported text files
        inherits from MakerFile but overrides a couple of
        methods
        """
        theFileName = os.path.splitext(filename)
        self.output('Creating instance...')
        self.saved = True
        self.flag  = None
        self.name  = theFileName[0]
        self.core  = core
        self.setType(theFileName[-1])
        self.setEditable()
        self.setPrintable()
        if view:
            self.fileController = makerFileController.MakerFileController(self, 
                                                                          self.core.projectController.view)
        else:
            self.fileController = None
    def getCommentTags(self):
        """ tags for comments used in this file type """
        return ["#",""]
              
    def setType(self, typeOfFile):
        self.output('Setting type')
        self.type = typeOfFile
    
    def getType(self):
        return self.type


class MakerFileUnsupportedBinaryFile(MakerFile):    
    def __init__(self, core, filename, view=True):
        """
        this is a class that handles imported binary files
        inherits from MakerFile but overrides a couple of
        methods
        """
        theFileName = os.path.splitext(filename)
        self.output('Creating instance...')
        self.saved = True
        self.flag  = None
        self.name  = theFileName[0]
        self.core  = core
        self.setType(theFileName[-1])
        self.setEditable()
        if view:
            self.fileController = makerFileController.MakerFileController(self, self.core.projectController.view)
        else:
            self.fileController = None
        
    def setPrintable(self):
        self.printable = False
        
    def load(self):
        self.fileController.loadTextIntoEditor(self.unEditableFileMessage(), binary = True)
        self.fileController.disableEditor()
     
    def save(self):
        pass
    
    def preview(self, Content=None):
        """Content is ignored since it is not editable."""
        webbrowser.open('file://'+self.getFullName(), autoraise=1)
    
    def getEditable(self):
        """Returns a boolean indicating if this file is editable or not."""
        return self.editable
    
    def setEditable(self):
        """A binary file by default is not editable. Override this method to alter."""
        self.editable = False
            
    def setType(self, typeOfFile):
        self.output('Setting type')
        self.type = typeOfFile
    
    def getType(self):
        return self.type

# ---------------------------
# ---------------------------

class MakerFileNav(MakerFile):
    
    def getLanguage(self):
        return self.getName()
    
    def setType(self):
        self.type =".nav"
    
    def delete(self):
        self.fileController.infoMessage("You cannot delete " + self.getType() + 
                                        " files.")

    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(os.path.join(self.core.getPathParts(), self.getName() + self.type), text)
        self.setSaved()
        self.core.makeAll()

# ---------------------------
# ---------------------------

class MakerFileBody(MakerFile):
    def getLanguage(self):
        return self.getName()
        
    def setType(self):
        self.type =".body"
   
    def delete(self):
        self.fileController.infoMessage("You cannot delete " + self.getType() + 
                                        " files.")
   
    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(os.path.join(self.core.getPathParts(), self.getName() + self.type), text)
        self.setSaved()
        self.core.makeAll()

# ---------------------------
# ---------------------------

class MakerFileFoot(MakerFile):
    def getLanguage(self):
        return self.getName()
    
    def setType(self):
        self.type =".foot"
    
    def delete(self):
        self.fileController.infoMessage("You cannot delete " + self.getType() + 
                                        " files.")
       
    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(os.path.join(self.core.getPathParts(), self.getName() + self.type), text)
        self.setSaved()
        if self.getName() != "rss":
            self.core.makeAll()

# ---------------------------
# ---------------------------

class MakerFileHead(MakerFile):
    def setType(self):
        self.type =".head"
    
    def delete(self):
        self.fileController.infoMessage("You cannot delete " + self.getType() + 
                                        " files.")
       
    def save(self, event=None):
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(os.path.join(self.core.getPathParts(), self.getName() + self.type), text)
        self.setSaved()
        # this class is also used for the rss head 
        if self.getName() != "rss": 
            self.core.addToFtpQueue(self.getName() + ".content")
        
    def saveAsTemplate(self):
        # check if valid 
        text = self.fileController.getTextFromEditor()
        if text == "Encoding Error":
            return
        writeFile(os.path.join(self.core.getProjectPath(),"templates", self.getLanguage() + self.type), text)
        self.setSaved()
    
    def getLanguage(self):
        possibleLanguages = self.core.getProjectLanguages()
        for lang in possibleLanguages:
            if self.getName().endswith("_" + lang):
                return lang

