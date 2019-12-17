# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# import packages
import random
import pygame
import sys
from pygame.locals import *

# set CONSTANTS
FPS = 15
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
BLUE      = ( 0,    0, 255)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

# direction variables
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0 # syntactic sugar: index of the worm"s head
SCORE = []
LIVES = 5

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, SCORE, LIVES
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # display window
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # set font
    BASICFONT = pygame.font.Font("freesansbold.ttf", 18)
    pygame.display.set_caption("Wormy")

    # call showStartScreen function
    showStartScreen()

    # call showMenu function
    showMenu()

    # run until user exits program
    while LIVES >= 0:
        scoreOfGame = runGame()
        pygame.time.wait(500)
        SCORE.append(scoreOfGame)
        SCORE.sort(reverse=True)
        if len(SCORE) > 5:
            SCORE.pop(-1)
        if(LIVES == 0):
            showGameOverScreen()
            pygame.time.wait(500)
            showMenu()

def runGame():
    global LIVES
    isSpecialApple = False
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)

    # create a l
    wormCoords = [{"x": startx,     "y": starty},
                  {"x": startx - 1, "y": starty},
                  {"x": startx - 2, "y": starty}]
    direction = RIGHT

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
            LIVES -= 1
            return len(wormCoords) - 3 # game over

        for wormBody in wormCoords[1:]:
            if wormBody["x"] == wormCoords[HEAD]["x"] and wormBody["y"] == wormCoords[HEAD]["y"]:
                LIVES -= 1
                return len(wormCoords) - 3 # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]["x"] == apple["x"] and wormCoords[HEAD]["y"] == apple["y"]:
            # don"t remove worm"s tail segment
            if isSpecialApple:
                LIVES += 1
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
        if (len(wormCoords) - 3) % 5 == 0 and (len(wormCoords) - 3) != 0:
            drawSpecialApple(apple)
            isSpecialApple = True
        else:
            isSpecialApple = False
            drawApple(apple)

        drawScore(len(wormCoords) - 3)
        drawLives()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render("Press a key to play.", True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


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
        FPSCLOCK.tick(FPS)
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
    scoreSurf = BASICFONT.render("Score: %s" % score, True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawLives():
    livesSurf = BASICFONT.render("Lives: %s" % LIVES, True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (WINDOWWIDTH - 200, 10)
    DISPLAYSURF.blit(livesSurf, livesRect)

def showMenu():
    DISPLAYSURF.fill(BGCOLOR)
    menuFont = pygame.font.Font("freesansbold.ttf", 20)

    menuTitleSurf = menuFont.render("Welcome to the Worm Game!", True, WHITE)
    DISPLAYSURF.blit(menuTitleSurf, (WINDOWWIDTH / 2 - 140, 10))
    menuItem1Surf = menuFont.render("1. Play Game", True, WHITE)
    DISPLAYSURF.blit(menuItem1Surf, (WINDOWWIDTH / 2 - 80, 50))
    menuItem2Surf = menuFont.render("2. View High Scores", True, WHITE)
    DISPLAYSURF.blit(menuItem2Surf, (WINDOWWIDTH / 2 - 80, 80))
    menuItem3Surf = menuFont.render("3. Quit :( ", True, WHITE)
    DISPLAYSURF.blit(menuItem3Surf, (WINDOWWIDTH / 2 - 80, 110))

    # drawPresskeyMSG
    pygame.display.update()
    pygame.time.wait(500)

    # process menu items
    while True:
        errorMessage = menuFont.render("Pressed invalid key. Try again.", True, BLACK)
        DISPLAYSURF.blit(errorMessage, (WINDOWWIDTH / 2 - 130, 150))
        pygame.display.update()
        event = checkForKeyPress()
        if event:
            if event == K_1:
                print("User pressed Number 1")
                return
            if event == K_2:
                print("User pressed Number 2")
                showHighScores()
                return
            if event == K_3:
                print("User pressed Number 3")
                terminate()
            else:
                errorMessage = menuFont.render("Pressed invalid key. Try again.", True, WHITE)
                DISPLAYSURF.blit(errorMessage, (WINDOWWIDTH / 2 - 130, 150))
                pygame.display.update()
                pygame.time.wait(500)
                continue

def showHighScores():
    global LIVES
    DISPLAYSURF.fill(BGCOLOR)
    menuFont = pygame.font.Font("freesansbold.ttf", 20)
    highScoreMessage = menuFont.render("Current High Scores", True, WHITE)
    DISPLAYSURF.blit(highScoreMessage, (WINDOWWIDTH / 2 - 100, 10))
    pygame.display.update()
    pygame.time.wait(500)

    if len(SCORE) == 0:
        highScoreMessage = menuFont.render("No Scores Available Right Now", True, WHITE)
        DISPLAYSURF.blit(highScoreMessage, (WINDOWWIDTH / 2 - 130, 60))
        pygame.display.update()
    else:
        SCORE.sort(reverse=True)
        startHeight = 50;
        counter = 1;
        for i in SCORE:
            highScoreMessage = menuFont.render("%d: %d" % (counter, i), True, WHITE)
            DISPLAYSURF.blit(highScoreMessage, (WINDOWWIDTH / 2 - 30, startHeight))
            pygame.display.update()
            startHeight += 30;
            counter += 1;

    menuItem1 = menuFont.render("1. Go Back", True, WHITE)
    DISPLAYSURF.blit(menuItem1, (WINDOWWIDTH / 2 - 150, 230))

    menuItem2 = menuFont.render("2. Play On", True, WHITE)
    DISPLAYSURF.blit(menuItem2, (WINDOWWIDTH / 2 + 30, 230))

    menuItem3 = menuFont.render("3. Quit", True, WHITE)
    DISPLAYSURF.blit(menuItem3, (WINDOWWIDTH / 2 - 40, 260))
    pygame.display.update()

    while True:
        errorMessage = menuFont.render("Pressed invalid key. Try again.", True, BLACK)
        DISPLAYSURF.blit(errorMessage, (WINDOWWIDTH / 2 - 130, 300))
        pygame.display.update()
        event = checkForKeyPress()
        if event:
            if event == K_1:
                showMenu()
                return
            if event == K_2:
                LIVES = 5
                return
            if event == K_3:
                print("User pressed Number 3")
                terminate()
            else:
                errorMessage = menuFont.render("Pressed invalid key. Try again.", True, WHITE)
                DISPLAYSURF.blit(errorMessage, (WINDOWWIDTH / 2 - 130, 300))
                pygame.display.update()
                pygame.time.wait(500)
                continue


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

def drawSpecialApple(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BLUE, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == "__main__":
    main()
