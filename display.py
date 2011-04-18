#!/usr/bin/env python
import pygame
from pygame.locals import *

class display:
    def __init__(self, globalvariables, background=None):
        #TODO: add background handling
        self.gv = globalvariables
        self.size = self.gv.size
        self.width = self.gv.size[0]
        self.height = self.gv.size[1]
        self.background = background
        self.displaylist = []
        pygame.display.init()
        pygame.key.set_repeat(350, 100)
        ##TODO remember to create and set an icon
        icon = pygame.image.load("icon", "icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption(self.gv.version)
        self.screen = pygame.display.set_mode((self.gv.size))
        
        pygame.font.init()
        self.UItext = pygame.font.Font("LiberationMono-Regular.ttf", 15)

    def drawtext(self, text, color, rect, zorder):
        '''
        Pass unicode text, a color tuple(RGB), a rect to draw at.
        Get a rect back that represents the size of the text.
        '''        
        temp = self.UItext.render(text, 1, color)
        self.drawitem(temp, rect, zorder)       
        #return the rect it got drawn at
        return temp.get_rect()
        
    def begin(self):
        
        self.screen.fill((0,0,0))
        
    def drawitem(self, item, itemxy, zorder):
        '''
        Blits pygame surface item to screen at itemrect.
        '''
        #TODO: add z-order as a parameter
        #TODO: then, instead of painting, queue items into a list
        #then paint a z-order at a time

        #print "before ", self.displaylist
        #print "and we're adding ", item, itemxy, zorder
        self.displaylist.append((item.copy(), itemxy[:], zorder))
        #print "after ", self.displaylist
        
        #self.screen.blit(item, itemxy)
        #WHAT THE FUCKING FUCK. BLITTING DIRECTLY IS FINE?!

    def paint(self):
        
        #obviously paint the FPS marker last
        if self.gv.showFPS == True:
            self.drawtext(u"FPS: %s" % int(self.gv.Clock.get_fps()), (0,255,0), (0, self.height - 15), self.gv.zorder_aboveui)

        #print "before sort:",self.displaylist
        #iterate through our list and paint, in z order, from lowest to highest
        #holy shit, i get lambda functions now! My first use!
        self.displaylist.sort(key=lambda x: x[2])
        #print "after sort:",self.displaylist
        
        #return
        for item in self.displaylist:
            self.screen.blit(item[0], item[1])
            
        
        pygame.display.flip()
        self.displaylist = []
    
    
