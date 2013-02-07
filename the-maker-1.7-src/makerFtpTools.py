#!/usr/bin/env python

import sys
from ftplib import FTP
import wx

class Browser:
    
    def __init__(self, server, root, user, password):
        """
        This class provides essential FTP functions like
        ls, isdir, etc. It is intended to be used with makerFtpBrowser 
        via a controller object.
        """
        
        # set this to True to get a little more information on stdout
        self.debug = False
        
        self.root = root
        self.log('init ftp browser; logging in...')

        self.ftp = FTP(server)

        result = self.ftp.login(user, password)
        
        self.ftp.cwd(root)
        
        
    
    # ------------------------------------------------------------        
    
    def logout(self):
        self.log('logging out...')       
        self.ftp.close()
        
    # ------------------------------------------------------------
        
    def ls(self):
        self.log('command : ls')
        self.aList = ["this directory is empty..."]
        try:
            self.aList = self.ftp.nlst()
            self.rootlist = self.aList # ITB 14/09/2007 corrected typo missing 's' from self
            return self.aList
        except:
           return self.aList
        
    # ------------------------------------------------------------    
    
    def pwd(self):       
        return self.ftp.pwd()       
    
    # ------------------------------------------------------------

    def cd(self, aDir):
        self.log('switching dir...')        
        self.ftp.cwd(str(aDir))

    # ------------------------------------------------------------        
    
    def isdir(self, aDir):
        self.log('checking if this is a dir...')
        if aDir in ['/', '.']: return True

        try:
            self.ftp.cwd(str(aDir))
            self.ftp.cwd('..')
            return True
        except:
            return False

    # ------------------------------------------------------------    

    def mkd(self, aDir):
        self.log('making dir %s' % str(aDir))
        try:
            self.ftp.mkd(str(aDir))
            return True
        except Exception, e:
            return False
    
    # ------------------------------------------------------------
    
    def deleteFile(self, filePath):
        current = self.ftp.pwd()
        self.ftp.cwd(self.root)
        try:
            print "deleting:", filePath
            self.ftp.delete(filePath)
            self.ftp.cwd(current)
            return True
        except Exception, e:
            self.ftp.cwd(current)
            return str(e)
    
    
    
    def rmd(self, aDir):
        print 'deleting dir %s' % str(aDir)
       
        try:
            self.ftp.rmd(str(aDir))
            return True
        except Exception, e:
            print str(e)
            return str(e)

    # ------------------------------------------------------------

    def isfile(self, aPath, aFile):
        self.log('checking for file %s' % str(aFile))
                
        #self.ftp.cwd(aPath)
        list = self.ftp.nlst()	
        if aFile in list:
            try:
                self.ftp.cwd(aFile)
                
            except Exception, e:
                self.log('this is a file ' + str(e))
                return True
            
            self.ftp.cwd("..")
            return False
                        
    # ------------------------------------------------------------        
         
    def log(self, theText):
        if self.debug:
            print "makerFtpTools: %s" % str(theText)
