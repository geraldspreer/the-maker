#script to create folder structure for windows distribution
#and compile python files to windows maker.exe using py2exe
#all folders (except .svn folders)and files from system are copied to dist
#maker.exe.manfest copied to dist
#all .txt files except path.txt copied to dist
#Ian Barrow 11/11/2007

import sys
import os
import shutil
from distutils.core import setup
import py2exe

path="system"
dst_root= ".\\dist\\"

def moveFiles(dirList, src_path_string, dst_path_string):
    if dirList !=[]:
        print "     copying files:"
        for files in dirList:
            shutil.copy(src_path_string+files, dst_path_string+files)
            print src_path_string+files+" To "+dst_path_string+files
            
def createDirectory(dirEntry):
    src_path_string=dirEntry[0] + "\\"
    dst_path_string=dst_root+dirEntry[0] + "\\"
    if ".svn" not in src_path_string:
        print "     creating folder:",
        print dst_path_string
        os.mkdir(dst_path_string)
        moveFiles(dirEntry[2], src_path_string,dst_path_string)
    elif ".svn" in src_path_string:
        print "ignoring "+src_path_string

print "deleting "+dst_root+" folder tree and files"
shutil.rmtree(dst_root,1)#,1 to ignor any errors ie no folders to remove
print "creating new "+dst_root+" folder for system tree"
os.mkdir(dst_root)

tree=os.walk(path)
for directory in tree:
    createDirectory(directory)

print "copying maker.exe.manifest and other .txt files to dist except path.txt"
shutil.copy("maker.exe.manifest",dst_root+"maker.exe.manifest")
directory=os.listdir(".")
for item in directory:
    if item[-4:]==".txt" and  item!="path.txt":
        shutil.copy(item,dst_root+item)

print "compiling...."
sys.argv.append("py2exe")
setup(
    windows = [
        {
            "script": "maker.py",
            "icon_resources": [(1, "system/tags.ico")]
        }
    ],
)
