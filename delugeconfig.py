#!/usr/bin/env python
from __future__ import with_statement
"""
Reads from config.ini in the same directory.
"""
class ini:
    def __init__(self, configpath):        
        # at some point, a test to make sure the file exists, is readable, \
        #etc. should go here
        self.configpath = configpath
        self.keyValuePair = {}
        with open(self.configpath) as f:
            self.allLines = f.readlines()

        for x in self.allLines:
            if x.rstrip != '':
                if x[0] != '#':
                    self.keyValuePair[x.split('=')[0]] = x.split('=')[1].rstrip()
        
    def GetValue(self, key):
        """
        Get the value referenced by 'key' in the config file.
        """        

        #should really test to make sure this exists first
        
        if key in self.keyValuePair:
            return self.keyValuePair[key]
        else:
            return -1
        
    def SetValue(self, key, newValue):
    
        #write this in the file right away or not? not sure which
        #for now, immediately open the file, write, then close.
        #should be "fine", for small values of fine
        #wait, should I just keep the file open and write to it?
        
        
        self.keyValuePair[key] = str(newValue)
        for x in range(len(self.allLines)):
            #print self.allLines[x][:len(key)], key
            if self.allLines[x][:len(key)] == key:
                #print "something got written!"
                self.allLines[x] = str(key + "=" + str(newValue) + "\n")
        #print self.allLines
                
    def AddValueInt(self, key, newValue):
        """
        Adds newValue to key's current int(value). Easier than the ugly looking
        transformations that need to happen if I don't create this method.
        """
        #The reason for this rather specific method:
        #it turns:
        #self.config.SetValue("NumberOfClicks", int(self.config.GetValue \
        #("NumberOfClicks")) + 1)
        #into:
        #self.config.AddValueInt("NumberOfClicks", 1)
        #
        currentValue = int(self.GetValue(key))
        self.SetValue(key, currentValue + newValue)        
                
    def FlushToDisk(self):
        #There's my answer, probably should only do this when winning or losing
        #a game
        with open(self.configpath, "w") as f:
            f.writelines(self.allLines)
            f.flush()
