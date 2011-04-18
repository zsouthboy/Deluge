#!/usr/bin env python
import display, pygame, delugeconfig, solver
from random import randint

class deluge:
    def __init__(self, globalvariables, displayinstance):
        self.gv = globalvariables
        self.display = displayinstance
        self.config = delugeconfig.ini("config.ini")        
        self.beatRecord = False
        self.waitforuser = False
        self.won = False
        #TODO: split this out into a function to be reused
        self.size = 0 #must be square playfield
        #for the solver lets init some variables
        self.numberOfBlocks = 0 #will be updated so we spend less time
        #multiplying self.size over and over again        
        self.maxBlocksSolved = 0
        self.moveList = []
        #/solver
        self.turns = 0
        self.blocksize = 0 # size, in pixels, of each block (width / height)
        self.sizeletter = "S"
        self.boardSizing()
        #TODO: allow setting these particular colors afterwards
        self.color = ((237,113,161), \
                 (70,178,227), \
                 (246,197,1), \
                 (125,155,30), \
                 (98,94,166), \
                 (220,75,33))
        self.RDPColor = ()
        #RDPColor is a list of fake colors with 1 to 1 mapping between this
        #tuple and self.color. fill in this after painting the board once
        self.RDPColorGet()
        
        #size of the circles users interact with
        #self.circleradius = ((self.blocksize * self.size / 6) - 5) / 2
        self.circleradius = 29 #hard coded since i'm now using images
        self.circlediameter = (self.circleradius * 2) + 5
        #load the 6 colored balls into a list
        self.circlebutton = []
        for i in range(6):
            self.circlebutton.append(pygame.image.load("circle" + str(i), \
                                                    "circle" + str(i) + ".png"))
            self.circlebutton[i].convert_alpha()
            self.circlebutton[i].convert()
            self.circlebutton[i] = pygame.transform.smoothscale( \
                                    self.circlebutton[i], (47,52))
        #again, not worth making a function for this. the buttons are static
        self.circlex = []
        self.circlex.append(36)
        self.circlex.append(101)
        self.circlex.append(166)
        self.circlex.append(231)
        self.circlex.append(296)
        self.circlex.append(361)
        #they're all the same distance from the top, hence one entry
        self.circley = 410
        self.background = pygame.image.load("background", "background.png")
        self.background.convert()
        
        #holy shit this is annoying fuck lists.
        self.blockarray = []
        self.flaggedlist = []
        self.flaggedlist.append([0,0])
        #----------------------------------------------
        #figured out how to arrange a list like i want:
        #if this is not generated all at once, the array ends up referencing
        #the same row objects
        self.blockarray = [[[0 for width in range(2)] \
                            for x in range(self.size)] \
                           for y in range(self.size)]
        self.blockarray[0][0][1] = 1
        #-----------------------------------------------
        #holy shit that fucking worked.
        #it just goes to show, if something simple is taking many lines
        #in python, UR DOIN IT RONG!
        #blockarray has two members at each cell. an index for the color and a flag
        self.xoffset = (self.gv.width - (self.size * self.blocksize)) / 2
        self.yoffset = ((self.gv.height - (self.size * self.blocksize)) / 2) - \
                       (self.circleradius)
        self.buttonposition = []
        self.buttonpositionset = False
        #the star for the UI
        
        self.star = pygame.image.load("star", "star.png")
        self.star.convert_alpha()
        self.star.convert()        
        self.turns = 0
        self.maxturns = 22
        self.boardSurface = pygame.surface.Surface((self.size * self.blocksize,\
                                                    self.size * self.blocksize))
        self.boardSurface.convert()
        self.block = []
        self.boardUpdated = True
        #circleButtonInfo is just to store the current size of the circle
        #buttons
        self.circleButtonInfo = []
        for i in range(6):
            self.circleButtonInfo.append(0)
        self.winSurface = pygame.image.load("gameoverhappy", "gameoverhappy.png")
        self.loseSurface = pygame.image.load("gameoversad", "gameoversad.png")
        self.gameOverXOffset = (self.gv.width - 300) / 2
        self.gameOverYOffset = (self.gv.height - 300) / 2
        
    def boardSizing(self):
        if self.sizeletter == "S":
            self.size = 12
            self.numberOfBlocks = 144
            self.maxturns = 22
            self.blocksize = 32
        elif self.sizeletter == "M":
            self.size = 16
            self.numberOfBlocks = 256
            self.maxturns = 30
            self.blocksize = 24
        elif self.sizeletter == "L":
            self.size = 32
            self.numberOfBlocks = 1024
            self.maxturns = 50
            self.blocksize = 12
        self.config.SetValue("LastSize", self.sizeletter)

    def initBoard(self):
        self.boardSizing()
        #generate the colored blocks surfaces. this has to be done
        #in case the size changes
        self.block = []
        for i in range(6):
            temp = pygame.surface.Surface((self.blocksize, self.blocksize))
            temp.fill((self.color[i]))
            temp.convert()
            self.block.append(temp)
            
        #initialize an array, size across and down, with a random color, 0 through 5
        self.blockarray = [[[0 for width in range(2)] \
                            for x in range(self.size)] \
                           for y in range(self.size)]
        temp = 0
        for x in range(self.size):
            for y in range(self.size):
                temp = randint(0, 5)
                #print x, y
                #print self.blockarray[x][y]
                #self.blockarray[x][y] = [[],[]]
                self.blockarray[x][y][0] = int(temp)
                #self.blockarray[x][y][1] = 0
                #print self.blockarray[x][y]
        self.blockarray[0][0][1] = 1
        self.flipBlocks(self.blockarray[0][0][0])
        self.turns = 0
        #make the first cell in the top right corner flagged
        
        #for i in range(self.size):
        #    print self.blockarray[i]

    def drawBoard(self):
        #BIG TODO: stop painting everything once a frame. it kills us at
        #L and medium size boards. perhaps for next version?
        #draw background first
        self.display.drawitem(self.background, (0,0), self.gv.zorder_bg)
        positionx = 0
        positiony = 0
        #TODO: allocate 6 pygame surfaces and use a LUT, rather than allocating
        #a new one for each block.
        #TODO: split both block drawing and circle drawing into
        #functions, so they can be handed a time (for animation)
        if self.boardUpdated == True:
            #let's get some smooth animation. keep the old surface, then
            #blend in a few steps to the new one (paint both for that period of
            #time)
            self.boardSurfaceOld = self.boardSurface.copy()
            self.boardSurfaceOldStep = 250
            #draw everything to one surface until it needs to be changed
            for x in range(self.size):
                for y in range(self.size):
                    positionx = (x * self.blocksize)
                    positiony = (y * self.blocksize)
                    block = self.block[self.blockarray[x][y][0]]                    
                    self.boardSurface.blit(block, (positionx,positiony))
                
            self.boardUpdated = False
            
        if self.boardSurfaceOldStep != 0:
            self.boardSurfaceOld.set_alpha(self.boardSurfaceOldStep)
            self.display.drawitem(self.boardSurfaceOld, (self.xoffset, \
                                                      self.yoffset), \
                                  self.gv.zorder_actor + 1)
            self.boardSurfaceOldStep -= 50
        self.display.drawitem(self.boardSurface, (self.xoffset, \
                                                      self.yoffset), \
                                  self.gv.zorder_actor)
            
        self.drawMenu()

        #TODO: keep a count of plays, sessions, wins, losses, etc.
    def pressButton(self, button, recieveBacon = False):        
        #print self.turns
        #self.turns = self.turns + 1
        self.turns+=1
        self.config.AddValueInt("NumberOfClicks", 1)
        #print self.turns
        self.flipBlocks(button)        
        #print "you clicked button %i!" % (button + 1)
                    
        if len(self.flaggedlist) == (self.size * self.size):
            self.gameOver(True)                
        elif self.turns == self.maxturns:
            self.gameOver(False)
    def mouseOverButton(self, button):
        self.circleButtonInfo[button] = 100
        #print "mousing over button %i, eh?" % button

    def gameOver(self, won):
        #inform the user.
        #probably should make a game over graphic that the user clicks through
        #pass OK to get a new game
        if won:
            #print "You win."
            self.config.AddValueInt("Wins", 1)
            if int(self.config.GetValue("BestSize" + self.sizeletter)) > self.turns:
                self.config.AddValueInt("BestSize" + self.sizeletter, self.turns)
                self.beatRecord = True
            self.won = True
            self.waitforuser = True
        else:
            #print "You lose."
            self.config.AddValueInt("Losses", 1)
            self.won = False
            self.waitforuser = True
        #tell the stats to be written to the ini file
        self.config.FlushToDisk()
            
    def buttonAcceptResults(self):
        self.newGame()
        self.drawBoard()
        self.waitforuser = False
    
    def newGame(self):
        self.buttonposition = []
        self.buttonpositionset = False
        self.flaggedlist = []
        self.flaggedlist.append([0,0])
        self.initBoard()
        
    def drawMenu(self):        
        #let's see, how about new game for right now
        #maybe a star for New Game?
        #TODO: board size and a statistics button
        #MOVED to init so we don't keep doing this every frame.
        self.display.drawitem(self.star, (0,0), self.gv.zorder_ui)        
        self.display.drawtext("Turns: " + str(self.turns) + " / " + str(self.maxturns), \
                              (255,255,255), (27,1), self.gv.zorder_ui)
        self.display.drawtext("Blocks: " + str(len(self.flaggedlist)) + \
                              " / " + str(self.size * self.size), \
                              (255,255,255), ((32+25+200),1), \
                              self.gv.zorder_ui)
        self.display.drawtext(str(self.sizeletter), \
                              (255,255,255), ((6),(25)), \
                              self.gv.zorder_ui)
        
        #next draw the colored circles at the bottom that the user is going
        #is going to click on to choose
        self.drawCircles()
        

        if self.waitforuser == True:
            #stats, etc.
            temp = pygame.surface.Surface((self.gv.width,self.gv.height))
            temp.fill((0,0,0))
            temp.set_alpha(200)
            self.display.drawitem(temp,(0,0), self.gv.zorder_aboveui - 2)
            if self.won == True:
                #TODO: make a pretty win screen with stats
                #TODO: make a pretty loss screen with stats
                self.display.drawitem(self.winSurface, \
                    (self.gameOverXOffset,self.gameOverYOffset), \
                                      self.gv.zorder_aboveui - 1)
            else:
                self.display.drawitem(self.loseSurface, \
                    (self.gameOverXOffset,self.gameOverYOffset), \
                                      self.gv.zorder_aboveui - 1)
                
                #self.display.drawtext("You lost this one. :(", \
                #                  (255,255,255),(self.gv.width / 8, \
                #                                 (self.gv.height / 2) - 20), \
                #                  self.gv.zorder_aboveui + 2)
            #stats go here so they're agnostic of what happened
            #set beatRecord back to false because we've shown the user
            #set it back in newgame, i think.
            shittodraw =["Wins", self.config.GetValue("Wins"), \
                         "Losses", self.config.GetValue("Losses"), \
                         "","All Time:", "Blocks", \
                         self.config.GetValue("NumberOfBlocks"), "Clicks", \
                         self.config.GetValue("NumberOfClicks")]
            
            for i in range(len(shittodraw)):
                self.display.drawtext(shittodraw[i], (18,18,18), \
                    (self.gameOverXOffset + 200, \
                     (self.gameOverYOffset + (i * 20) + 40)),\
                                      self.gv.zorder_aboveui + 2)
                
            self.display.drawtext("Best " + self.sizeletter + " Game: " +\
                    self.config.GetValue("BestSize" + self.sizeletter) + " turns", \
                                  (200,200,200), (self.gameOverXOffset + 60,\
                                               self.gameOverXOffset + 10),\
                                  self.gv.zorder_aboveui + 2)
                        
    def drawCircles(self):
        
        #define an array with an entry for each circle
        #the entry will have the current size of the circle out of 100
        #calculate the correct size for that, then subtract something
        for i in range(6):
            if self.circleButtonInfo[i] != 0:
                #42 -> 63
                #52 -> 70
                #0 -> 100
                
                
                
                scaledx = int(self.circlex[i] - ((self.circleButtonInfo[i] / 4.76) / 2)) + 2
                scaledy = int(self.circley - ((self.circleButtonInfo[i] / 4.76) / 2))
                
                temp = pygame.transform.smoothscale(self.circlebutton[i], \
                            (int(42 + (self.circleButtonInfo[i] / 4.76)), \
                            int(52 + (self.circleButtonInfo[i] / 5.55))))
                self.display.drawitem(temp, \
                      (scaledx, scaledy), \
                                  self.gv.zorder_actor)
                
                self.circleButtonInfo[i] -= 10 #ten steps to go back to normal
                #.3 sec at 30 fps, my target
            else:
                self.display.drawitem(self.circlebutton[i], \
                                      (self.circlex[i], self.circley), \
                                      self.gv.zorder_actor)
            
    def flipBlocks(self, colorindex):
        #for each flagged block, search above, side and side, and below for
        #a block matching the new color
        #
        #
        #new idea, keep two lists of the flagged blocks.
        #one is a "permanent" list: each time a block is flagged, add it here
        #the other is a "change this turn" list: at the beginning of each turn
        #the permanent list is copied to this anew
        #each time a block is flagged, add it to both lists
        #the main function of flipping blocks simply goes through the second
        #list. we've checked every potential play on the board when it's done.
        #this saves time from checking every single square 4 times (up, left
        #right, down)... until we get over 1/2 the board filled. then it
        #doesn't save time.
        #eventually put in logic that flips the lists to both be !lists
        #probably fine without this though.
        #
        templist = self.flaggedlist[:] #start with all the currently flagged blocks
        while len(templist) != 0:
            i = templist.pop() #remove the last item on the list
            #print "i:",i
            #set that block to the new color
            self.blockarray[i[0]][i[1]][0] = colorindex
            #
            #start testing. check above this block's entry for the color
            if i[1] != 0:
                if self.blockarray[i[0]][i[1] - 1][1] == 0:
                    if self.blockarray[i[0]][i[1] - 1][0] == colorindex:
                        #print "found above", i
                        self.blockarray[i[0]][i[1] - 1][1] = 1
                        self.flaggedlist.append((i[0],i[1] - 1))
                        templist.append((i[0],i[1] - 1))
                        self.config.AddValueInt("NumberOfBlocks", 1)
            #below
            if i[1] != self.size - 1:
                if self.blockarray[i[0]][i[1] + 1][1] == 0:
                    if self.blockarray[i[0]][i[1] + 1][0] == colorindex:
                        #print "found below", i
                        self.blockarray[i[0]][i[1] + 1][1] = 1
                        self.flaggedlist.append((i[0],i[1] + 1))
                        templist.append((i[0],i[1] + 1))
                        self.config.AddValueInt("NumberOfBlocks", 1)
            #left
            if i[0] != 0:
                if self.blockarray[i[0] - 1][i[1]][1] == 0:
                    if self.blockarray[i[0] - 1][i[1]][0] == colorindex:
                        #print "found left", i
                        self.blockarray[i[0] - 1][i[1]][1] = 1
                        self.flaggedlist.append((i[0] - 1,i[1]))
                        templist.append((i[0] - 1,i[1]))
                        self.config.AddValueInt("NumberOfBlocks", 1)
                        
            #right
            if i[0] != self.size - 1:
                if self.blockarray[i[0] + 1][i[1]][1] == 0:
                    if self.blockarray[i[0] + 1][i[1]][0] == colorindex:
                        #print "found right", i
                        self.blockarray[i[0] + 1][i[1]][1] = 1
                        self.flaggedlist.append((i[0] + 1,i[1]))
                        templist.append((i[0] + 1,i[1]))
                        self.config.AddValueInt("NumberOfBlocks", 1)
            self.boardUpdated = True
            #print "temp left:",len(templist)
            #print "permanent:",len(self.flaggedlist)
                        
    def checkEvents(self):
        #query for things like refreshing the board
        if self.waitforuser == False:
            #new tests for mouseover
            for i in range(6):
                        #print i
                        #print self.gv.mousexy,self.buttonposition[i]
                        if self.circlex[i] <= self.gv.mousexy[0] and \
                             (self.circlex[i] + 63) >= self.gv.mousexy[0]:
                            if self.circley <= self.gv.mousexy[1] and \
                             (self.circley + 70) >= self.gv.mousexy[1]:                            
                                self.mouseOverButton(i)
            if self.gv.mousehandled == False:
                if self.gv.mousedown == True:
                    #TODO: check against every surface that is clickable
                    #print self.gv.mousexy
                    #TODO: create a generic menuing system that keeps track
                    #of hotspots, etc. this is hacky
                    if self.gv.mousexy[0] >= self.xoffset and \
                       self.gv.mousexy[0] <= (self.xoffset + (self.size * \
                                                self.blocksize) - 1) and \
                       self.gv.mousexy[1] >= self.yoffset and \
                       self.gv.mousexy[1] <= (self.yoffset + (self.size * \
                                                self.blocksize) - 1):
                        #get the color of the block and "press" that button
                        #ouch, get index out of range. gotta remember that
                        #get_at is referring only to the rect of the surface
                        x = self.gv.mousexy[0] - self.xoffset
                        y = self.gv.mousexy[1] - self.yoffset
                        color = self.boardSurface.get_at((x,y))
                        #surface is 0-based indexed, so we test above for -1
                        #but actually test the unmodified x,y
                        #TODO:fix pushbutton so it doesn't fire if we press the
                        #same color as we just did (that is, no change)
                        #print color[:-1]
                        #self.display.drawtext(str(color[:-1]), (255,255,255), \
                        #                      (20,20), 200)
                        for i in range(6):
                            #print color, self.color[i]
                            if color[:-1] == self.color[i]:
                                self.pressButton(i)
                        #OKAY WHAT THE FUCK, getting the pixel RGB is very
                        #slightly OFF by a few values. WHAT THE FUCK
                        #if the output device isn't 24- or 32- bit, we get back
                        #...well, exactly what you'd expect.
                        #should this be FIXME: check against the array itself
                        #rather than the output surface?
                        #confirmed this is the issue. only going to affect me
                        #via RDP
                        #TODO: correct this, grab each color once to compare to
                        #at startup

                    #check if click is inside a button
                    for i in range(6):
                        #print i
                        #print self.gv.mousexy,self.buttonposition[i]
                        if self.circlex[i] <= self.gv.mousexy[0] and \
                             (self.circlex[i] + 63) >= self.gv.mousexy[0]:
                            if self.circley <= self.gv.mousexy[1] and \
                             (self.circley + 70) >= self.gv.mousexy[1]:                            
                                self.pressButton(i)
                        #print "check if this is in", self.buttonposition[i]
                    #check if it's in the new star:
                    if self.gv.mousexy[0] >=0 and \
                       self.gv.mousexy[0] <=21 and \
                       self.gv.mousexy[1] >=0 and \
                       self.gv.mousexy[1] <=21:
                        self.newGame()
                    #check if we're changing board size
                    if self.gv.mousexy[0] >=5 and \
                       self.gv.mousexy[0] <=27 and \
                       self.gv.mousexy[1] >=25 and \
                       self.gv.mousexy[1] <=42:
                        #print "changing size"
                        if self.sizeletter == "S":
                            self.sizeletter = "M"
                        elif self.sizeletter == "M":
                            self.sizeletter = "L"
                        else:
                            self.sizeletter = "S"                        
                        self.boardSizing()
                        self.initBoard()
                        self.newGame()

                    if self.gv.mousexy[0] >=420 and \
                       self.gv.mousexy[0] <=441 and \
                       self.gv.mousexy[1] >=460 and \
                       self.gv.mousexy[1] <=481:
                        self.solve()
                        
                    self.gv.mousedown = False                        
                    self.gv.mousehandled = True
        else:
            if self.gv.mousedown == True:
                if self.gv.mousehandled == False:
                    #print self.gv.mousexy
                    if self.gv.mousexy[1] >=(self.gameOverXOffset + 260) and \
                           self.gv.mousexy[1] <=(self.gameOverXOffset + 300):
                        self.buttonAcceptResults()
                self.gv.mousehandled = True
    
    def solve(self):
        #first get our array into what the solver expects
        array = []
        for x in range(self.size):
            array.append([])
            for y in range(self.size):
                array[x].append(self.blockarray[x][y][0])
                
        print self.blockarray
        print array

        self.pressButton(solver.solve_one_turn(array, self.size, 4))
    def RDPColorGet(self):
        #TODO: fix the game on lower bit displays. here.
        pass
