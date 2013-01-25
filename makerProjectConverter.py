import os
import shutil
from xml.sax import parse
from xml.sax.handler import ContentHandler
import time

#    09-Nov-2009
#    Gerald: Trying to get the madness out of here.
#
#    
#
#





class Verify:
    def __init__(self, project, callback=None, *args):
        """
        the project will be converted wherever it is
        
        for projects in version > 0.6 there are some differences to earlier 
            application versions
        -    all images are in parts/ not in parts/gfx/
        -    there is only one distribution Table not one for each language
        -    in early projects there is a feed file called feed.content  
        """
       
        self.project = project
        gfxDir = os.path.join(self.project,"parts","gfx")
        
        if not os.path.isdir(gfxDir):
            return
                
        tables = self.getExistingDistTables()
        fullTable = []
        for i in tables:
            fullTable.extend(self.readDistributionTable(i))
        
        self.writeDistributionTable(fullTable)
        
        files = os.listdir(gfxDir)
        for aFile in files:
            if aFile.startswith('.'):
                pass
            else:
                shutil.move(os.path.join(gfxDir, aFile),
                                os.path.join(self.project,"parts"))
            
        files = os.listdir(gfxDir)
        for aFile in files:
            try:
                os.remove(os.path.join(gfxDir, aFile))
                
            except:
                print "Cannot delete: %s" % aFile
        
        try:
            os.rmdir(gfxDir)
        except:
            os.rename(gfxDir, os.path.join(self.project,"parts","old-gfx"))
        
        # delete old feed file
        try:
            os.remove(os.path.join(self.project,"parts/feed.content"))
        except:
            print "No old feed files..."
        
        #self.markProject()
        
    # ----------------------------------------------------------
    
#    def checkIfProjectIsUpToDate(self):
#        '''Returns True of False.'''        
#        thePath = os.path.join(self.project, 'setup', 'projectVersion.txt')
#        return os.path.isfile(thePath)
#        
#    # ----------------------------------------------------------
#
#    def markProject(self):
#        """
#        Puts a file named projectVersion.txt into the projects
#        setup folder to check if a project is up to date with 
#        the running maker version.
#        """
#        thePath = os.path.join(self.project, 'setup', 'projectVersion.txt')
#        afile = open(thePath,'w')
#        afile.write('1')
#        afile.close()
#        
#    # ----------------------------------------------------------    
    
    def getExistingDistTables(self):
        list   = os.listdir(os.path.join(self.project, "setup"))
        tables = [i for i in list if i.startswith("distribution")]        
        return tables
    
    # ----------------------------------------------------------        
        
    def readDistributionTable(self, table):
        """
        returns a list conataining dictionaries with the distribution data   
        reads from the current file
       
        """
        self._dist_data={}
        self._dist_list=[]
         
        class XmlReader(ContentHandler):
            def __init__(XmlReader, scrwid=79, *args):
                ContentHandler.__init__(XmlReader, *args)
                    
            def startElement(XmlReader, name, attrs):
                #print "start element",name
                if name=="rule":
                    self._dist_data["ftp_source"]=attrs.get("ftp_source")
                    self._dist_data["remote_dir"]=attrs.get("remote_dir")
                    self._dist_data["target"]=attrs.get("target")
                    self._dist_data["ftp_mode"]=attrs.get("ftp_mode")

            def endElement(XmlReader, name):
                if name=="rule":
                    self._dist_list.append(dict(self._dist_data))
                    self._dist_data.clear()
                    
            def characters(XmlReader, chars):                        
                pass
                    
        parse(os.path.join(self.project,"setup",table), XmlReader())            
        return self._dist_list
        
    # ----------------------------------------------------------        
        
    def writeDistributionTable(self, data):        
        # TO DO: use DOM methods
        info  = ""            
        info += '<?xml version="1.0" encoding="iso-8859-1"?>'
        info += "<!-- file was created @: %s -->\n" % str(time.ctime())
        info += "<distribution>\n"
            
        for i in data:
            xl = i.keys()
            info += "<rule "
            for t in xl:
                info += t+'="'+i[t]+'" '
            info += "></rule>\n"
                
        info += "</distribution>"
            
        new = open(os.path.join(self.project,"setup","distribution.xml"),'w')
        new.write(info)
        new.close()
        
