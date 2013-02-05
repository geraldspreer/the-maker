import sys
import os
import shutil
import time
import cPickle



def readFile(pathToFile, asLines=False, lineRange=[], binary=False):
    conts = ''    
    if asLines: conts = []
    if not os.path.exists(pathToFile): return conts

    flag = 'r'
    if binary: flag = 'rb'
    handle = None
    try:
        handle = open(pathToFile, flag)
        if asLines:
            conts = handle.readlines()
            if lineRange:
                start = lineRange[0]
                try:
                    stop = lineRange[1]
                    conts = conts[start:stop]
                except:
                    if not conts: 
                        conts = ''
                    else: 
                        conts = conts[start]
        else:
            conts = handle.read()
    finally:
        if handle: handle.close()
        return conts

# ---------------------------------------------------------------

def writeFile(pathToFile, fileConts, asLines=False, binary=False, append=False):
    flag = 'w'
    if append: flag = 'a'    
    if binary: flag += 'b'
    handle = None
    try:
        handle = open(pathToFile, flag)
        if asLines:
            handle.writelines(fileConts)
        else:
            handle.write(fileConts)
    finally:
        if handle: handle.close()



def copyFileTree(src, dst, callback = None, *args):
    """
        
    is copying a tree of files one file at a time
    
    callback is a function to be called after each file 
    e.g. to indicate progress, the callback function has to
    accept a string as argument
    """
    
    if not src.endswith("/"):
        src += "/"
    
    if not os.path.isdir(dst):
        os.mkdir(dst)
    
    tree = os.walk(src)
    
    for item in tree:
        try:
            # remove the leading dirs from the src path
            aditionalPath = item[0].replace(src, "")
            
            #call callback function 
            if callback:
                callback("copying: " + aditionalPath)
            
            # create dir tree
            if aditionalPath != "":
                os.mkdir(os.path.join(dst, aditionalPath))
            
        except Exception, e:
            print "\nUnable to create dir: ", str(e)
            raise e
                
        for file in item[2]:
            
            if callback:
                callback(file)
            
            try:
                shutil.copyfile(os.path.join(item[0], file), 
                                os.path.join(dst, aditionalPath, file))     
            except Exception, e:
                print "\ncopy failed: ", str(e)
                raise e
            
def verifyLatinChars(string):
    """ returns True if string contains only Latin chars"""
    
    try:
        new = string.encode("latin-1")
        return True
    
    except:
        return False


def readDataFromFile(fileName):
    """
    read serialized data from a file
    
    """
    bFile = open(fileName, "rb")
    data = cPickle.load(bFile)
    finalData = cPickle.loads(data)
    bFile.close() 
            
    return finalData
        
        
def writeDataToFile(data, fileName):
    """
    write serialized data to a file
    
    """
    bytes = cPickle.dumps(data, 2)
    bFile = open(fileName, "wb")
    cPickle.dump(bytes, bFile, 2)
    bFile.close()
        
            
            