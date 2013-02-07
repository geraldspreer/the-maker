#!/usr/bin/env python
# This is the server link for the maker

import os
import sys
from ftplib import FTP

class Server:
    # arguments : cms - instance of the cms.Core

    def __init__(self, core):
        self.server_link_message('Retrieving server information')    
        self.core = core
        self.host = core.ftpHost
        self.user = core.ftpUser
        self.root = core.ftpRoot
        self.status = 'disconnected'
    
    # ----------------------------------------------------------

    def login(self):
        if not self.core.getRemotePassword():
            self.server_link_message("! ! ! NO FTP PASSWORD SET ! ! ! ")
            return False
        else:
            
            m = "Logging in ... " 
            self.server_link_message(m)
        
        try:
            self.ftp = FTP(self.host)
            #print 'host'
            self.ftp.set_debuglevel(1)
            self.ftp.login(self.user,self.core.getRemotePassword())
            #print 'login'
            try:
                self.ftp.cwd(self.root)
            except Exception, e:
                m = "Error while logging into FTP server.\n"
                m += "Unable to switch to your projects root folder "
                m += "called:" + self.root + " \n"
                m += "Here is why: " + str(e) + "\n"
                m += "Please go to FTP > Setup FTP Connection, to choose a valid\n"
                m += "path to your project."
                self.core.projectController.errorMessage(m)
                self.logout()
                return False
            #print 'root'
            self.status = 'connected'
            return True
        except:
            passW = self.core.getRemotePassword()
            m  = 'Unable to login with: \n'
            m += 'host: %s, user: %s, root: %s, password: %s' % (self.host,
                                                                     self.user,
                                                                     self.root,
                                                                     passW)
            self.server_link_message(m)
            return False

    # ----------------------------------------------------------

    def logout(self):
        try:
            self.server_link_message('Logging out ')
            self.ftp.close()
            self.status = 'disconnected'
        except:
            self.server_link_message('Unable to logout ')

    # ----------------------------------------------------------
    
    def ls(self):
        list = []
        self.server_link_message('ls')
        try:
            list = self.ftp.nlst()
            return list
        except Exception, e:
            print "Serverlink command 'ls' failed: ", str(e)
            return []
    
    # ----------------------------------------------------------
    
    def rename(self, oldName, newName):
        self.server_link_message('renaming ' + oldName + " to "+ newName)
        try:
            self.home()
            self.ftp.rename(oldName, newName)
            return True
        except Exception, e:
            self.core.projectController.errorMessage("Unable to rename remote file: " + 
                                                     oldName + "\nReason:" + str(e))
            return str(e)

    
    
    # ----------------------------------------------------------    
    
    def isdir(self, aDir):
        #print "checking for existing dir %s" % aDir
        if aDir.strip() in ['/', '.']:
            return True

        try:
            self.ftp.cwd(aDir.strip())
            self.ftp.cwd('..')
            return True
        except:
            return False
    
    # ----------------------------------------------------------    

    def mkd(self, aDir):                
        try:
            self.ftp.mkd(str(aDir))
            return True
        except Exception, e:
            return False
            
    # ----------------------------------------------------------        

    def upload(self, aFile, aRemoteFolder, aTarget, theFtpMode):
        """
        If the upload fails for some reason, try again for 10 times 
        before stopping the attempt to upload. After an attempt has 
        failed, log out from the server and establish a new connection.
        """                
        self.server_link_message('uploading file')
        ob = open(aFile,'rb')
        self.ftp.cwd(self.root)
        
        def store_():            
            if not aRemoteFolder in ['.', '/']: # i.e. we are not in root
                #print "switching to remote folder..."
                self.ftp.cwd(aRemoteFolder)        # ins Verzeichnis wechseln
            
            print "Storing...%s" % aTarget
            
            try:
                if theFtpMode == 'lines':
                    self.server_link_message('storing lines')
                    self.ftp.storlines("STOR "+ aTarget, ob)                
                elif theFtpMode == 'binary':
                    self.server_link_message('storing binary')
                    self.ftp.storbinary("STOR "+ aTarget, ob)
                return True                
            except:
                print ' !! Serverlink: unable to store !!'
                return False
        
        for x in range(10):
            if store_():
                print "done at attempt ", x
                ob.close()
                m = 'Wrote %s/%s.\nUpload successful' % (aRemoteFolder, aTarget)
                self.server_link_message(m)
                self.ftp.cwd(self.root)
                return
            else:
                print "failed at attempt ", x
                # logout and in and try again
                self.logout()
                self.login()
                self.home()                
                #print "trying again to store..."
                
        ob.close()
        self.server_link_message('upload failed')
        m  = 'Upload failed after 10 attempts for'
        m += '%s/%s' % (aRemoteFolder, aTarget)
        sys.stderr.write(m)
        self.ftp.cwd(self.root)
        
    # ----------------------------------------------------------              
    
    def download(self, remoteFilename, localFilename, theFtpMode):
        """
                
        """                
        if os.path.isfile(localFilename):
            print "Download Error! A file :", localFilename, " already exists!"
            return False
        
        self.server_link_message('downloading file')
        
        self.ftp.cwd(self.root)
        
        print "downloading...", remoteFilename
        try:        
            if theFtpMode == 'lines':
                fileToGet = open(localFilename,"w")
                self.server_link_message('downloading lines')
                self.ftp.retrlines("RETR "+ remoteFilename, fileToGet.write)                
            elif theFtpMode == 'binary':
                fileToGet = open(localFilename,"wb")
                self.server_link_message('downloading binary')
                self.ftp.retrbinary("RETR "+ remoteFilename, fileToGet.write)
            fileToGet.close()
            return True
        except Exception, e:
            print e
            return False
        
        
        
    # ----------------------------------------------------------     
    
    def delete(self, aRemoteFolder, aFile):        
        self.server_link_message('Deleting remote file...' + aRemoteFolder + "/" + aFile)
                
        self.ftp.cwd(aRemoteFolder)	    # ins Verzeichnis wechseln
       
        try:
            self.ftp.delete(aFile)
            self.server_link_message('File deleted!')
            return True
        
        except Exception, e:
            print "Unable to delete remote file! ", str(e)
            return False
        
    # ----------------------------------------------------------                
    
    def home(self):
        self.server_link_message('cd to ftp root')
        self.ftp.cwd(self.root)
        
    # ----------------------------------------------------------            
    
    def server_link_message(self, message):
        print 'serverlink: %s' % message
        
        
    
