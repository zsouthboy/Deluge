#!/usr/bin/env python
import pygame, sys
from pygame.locals import *

class events():
    def __init__(self, globalvariables, displayinstance, consoleinstance):
        #remember to grab a console instance DONE, and a mouse instance eventually
        self.gv = globalvariables
        self.display = displayinstance
        self.console = consoleinstance
    
    def handleevents(self):
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                if event.type == QUIT or \
                   event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_BACKQUOTE:
                    self.gv.consoleenabled = \
                        not self.gv.consoleenabled
                    #print "Console: %s" % self.console.enabled
                if event.type == KEYDOWN:                    
                    #print event.unicode
                    self.console.getkeys(event)
            if event.type == MOUSEBUTTONDOWN:
                if self.gv.mousehandled != False:
                    self.gv.mousehandled = False
                    self.gv.mousedown = True
                    #self.gv.mouseup = False
                    self.gv.mousexy = pygame.mouse.get_pos()
            if event.type == MOUSEMOTION:
                self.gv.mousexy = pygame.mouse.get_pos()

                
