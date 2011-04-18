#!/usr/bin/env python

class globalvars:

    def __init__(self, size, framerate):
        #TODO really gotta pull these from an INI instead.
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.framerate = framerate
        self.consoleenabled = False
        self.showFPS = False
        self.blinkrate = 200 #blinkrate is a misnomer, it's actually ms between blinks
        #for each layer, a new z order that allows us to paint everything, while
        #stil getting overwritten correctly
        self.zorder_bg = -10
        self.zorder_actor = 0
        self.zorder_ui = 10
        self.zorder_aboveui = 20
        self.mousedown = False
        self.mouseup = False
        self.mousexy = [0,0]
        self.mousehandled = True
