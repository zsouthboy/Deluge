#!/usr/bin/env python
import display, events, console, globalvars, pygame, deluge

size = width, height = 440, 480
framerate = 30

#Since it's going to be used a ton, short name gv for global variable access
#TODO add in config.ini class to fill in globalvars


gv = globalvars.globalvars(size, framerate)

gv.version = u"Deluge 0.2 | Perineum."

#should toss time in a class eventually
gv.Clock = pygame.time.Clock()
gv.Clock.tick()

displayinstance = display.display(gv)
#playfieldinstance = playfield.playfield(gv, displayinstance)
consoleinstance = console.console(gv, displayinstance)
eventsinstance = events.events(gv, displayinstance, consoleinstance)
gameinstance = deluge.deluge(gv, displayinstance)
gameinstance.initBoard()


while 1:
    
    eventsinstance.handleevents()
    displayinstance.begin()

    #---- deluge
    #playfieldinstance.drawplayfield()
    gameinstance.checkEvents()
    gameinstance.drawBoard()
    
    
    #----

    consoleinstance.begin()
    ##these should both be moved to displayinstance##
    ##consoleinstance.textout(gv.version, (255,0,0)) ##DONE
    ##consoleinstance.textout(u"FPS: %s" % int(Clock.get_fps()), (0,255,0))
    consoleinstance.draw()

    displayinstance.paint()
    gv.Clock.tick(gv.framerate)
