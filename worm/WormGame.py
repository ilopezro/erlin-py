# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# import packages
import random, pygame, sys
from pygame.locals import *

# set CONSTANTS
fps = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# set colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

# direction variables
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0 # syntactic sugar: index of the worm"s head

def main():
    global fpsClock, DISPLAYSURF, BASICFONT

    pygame.init()
    fpsClock = pygame.time.Clock()

    # display window
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # set font
    BASICFONT = pygame.font.Font("freesansbold.ttf", 18)
    pygame.display.set_caption("Wormy")

    # call showStartScreen function
    # showStartScreen()
    # playGame = False

    # run until user exits program
    while True:
        playGame = showMenu()

        if playGame:
            showStartScreen()
            fps = 15
            runGame()
            showGameOverScreen()


def runGame():
    global fps
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)

    # create a l
    wormCoords = [{"x": startx,     "y": starty},
                  {"x": startx - 1, "y": starty},
                  {"x": startx - 2, "y": starty}]
    direction = RIGHT

    # initilize a lives variable
    lives = 5
    score = 0
    level = 1

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]["x"] == -1 or wormCoords[HEAD]["x"] == CELLWIDTH or wormCoords[HEAD]["y"] == -1 or wormCoords[HEAD]["y"] == CELLHEIGHT:
            return # game over

        for wormBody in wormCoords[1:]:
            if wormBody["x"] == wormCoords[HEAD]["x"] and wormBody["y"] == wormCoords[HEAD]["y"]:
                return # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]["x"] == apple["x"] and wormCoords[HEAD]["y"] == apple["y"]:
            # don"t remove worm"s tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm"s tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"] - 1}
        elif direction == DOWN:
            newHead = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"] + 1}
        elif direction == LEFT:
            newHead = {"x": wormCoords[HEAD]["x"] - 1, "y": wormCoords[HEAD]["y"]}
        elif direction == RIGHT:
            newHead = {"x": wormCoords[HEAD]["x"] + 1, "y": wormCoords[HEAD]["y"]}
        wormCoords.insert(0, newHead)

        # old school debugging
        print(wormCoords)

        # re-render the display
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        fpsClock.tick(fps)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render("Press a key to play.", True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def showMenu():
    DISPLAYSURF.fill(BGCOLOR)
    menuFont = pygame.font.Font ("freesansbold.ttf", 20)

    #Draw the title
    menuTitleSurf = menuFont.render("Welcome to the Worm Game!", True, BLACK)
    DISPLAYSURF.blit(menuTitleSurf, (WINDOWWIDTH / 2 - 80, 10))
    menuItem1Surf = menuFont.render("1. Play Game", True, BLACK)
    DISPLAYSURF.blit(menuItem1Surf, (WINDOWWIDTH / 2 - 80, 100))
    menuItem2Surf = menuFont.render("2. View High Scores", True, BLACK)
    DISPLAYSURF.blit(menuItem2Surf, (WINDOWWIDTH / 2 - 80, 130))
    menuItem3Surf = menuFont.render("2. Quit :( ", True, BLACK)
    DISPLAYSURF.blit(menuItem3Surf, (WINDOWWIDTH / 2 - 80, 160))

    # drawPresskeyMSG
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    # process menu items
    while True:
        if checkForKeyPress():
           for events in events:
               if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_1:
                       print("User pressed Number 1")
                       return True
                   if event.key == pygame.K_2:
                        print("User pressed Number 2")
                        showHighScores()
                        return False
                   if event.key == pygame.K_3:
                        print("User pressed Number 3")
                        terminate()

def showHighScores():
    DISPLAYSURF.fill(BGCOLOR)
    menuFont = pygame.font.Font("freesansbold.tif", 20)
    highScoresTitle = menuFont.render("High Scores", True, BLACK)
    highScoresTitleRect = highScoresTitle.get.rect()
    highScoresTitleRect.midtop = (WINDOWWIDTH / 2, 10)
    DISPLAYSURF.blit(highScoresTitle, highScoresTitleRect)

    for i in range(score):
        # currentHighScores = scores[i]

        highScoreLabel = menuFont.render("Game %s %s" % str(i + 1), str(scores[i]), True, BLACK)
        highScoreLabelRect = highScoreLabel.get_rect()
        highScoreLabelRect.midtop = (WINDOWWIDTH / 2 - 25, 20 * i +100)

        DISPLAYSURF.blit(highScoreLabel, highScoreLabelRect)

        drawPressKeyMsg()

        pygame.display.update()

        # pygame.time.wait(500)
        # checkForKeyPress()
        while True:
            if checkForKeyPress():
                pygame.event.get()
                return

def drawLives(lives):
    livesSurf = BASICFONT.render("Lives: %5" %(Lives), True, BLACK)
    livesRect = livesSurf.get.rect()
    livesRect.topright = (WINOWWIDTH + 200, WINDOWWIDTH + 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

# def drawSpecialApple(coord):

def resetWorm(wormCoords, startx, starty, direction):
    previousWormLength = len(wormCoords)
    wormCoords = [{"x": startx,   "y": starty},
                  {"x": startx - 1, "y": starty},
                  {"x": startx - 2, "y": starty}]

    for i in range(3, previousWormLength):
        wormCoords.append("x": startx - 1, "y": starty -1)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font("freesansbold.ttf", 100)
    titleSurf1 = titleFont.render("Wormy!", True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render("Wormy!", True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

        pygame.display.update()
        fpsClock.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {"x": random.randint(0, CELLWIDTH - 1), "y": random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 150)
    gameSurf = gameOverFont.render("Game", True, WHITE)
    overSurf = gameOverFont.render("Over", True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render("Score: %s" % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord["x"] * CELLSIZE
        y = coord["y"] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == "__main__":
    main()
