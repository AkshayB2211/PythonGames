
import pygame, sys, random, copy, math
from pygame.locals import *

# Create the constants (go ahead and experiment with different values)
NUM_CELLS = 4 # number of rows in the BOARD
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = 0

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
PINK = 			(220, 	0, 255)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 60
TILECOLORS = [0xEEE4DA, 0xE8DCC4, 0xF3B077, 0xE78D57, 0xED815D, 0xE55D33,
	0xF6D76D, 0xDFC923, 0x61DA94, 0xF46674, 0x66B6DD, 0x007FC2, 0x19668F]

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * NUM_CELLS + (NUM_CELLS - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * NUM_CELLS + (NUM_CELLS - 1))) / 2)


def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, BOARD

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('2048')
	BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

	
	startingBoard()
	while True: # main game loop

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				RUNNING = False
				pygame.quit()
				sys.exit()

			if event.type == KEYUP:
				# check if the user pressed a key to slide a tile
				if event.key in (K_LEFT, K_a) and not gameOver():
					moveLeft()
				elif event.key in (K_RIGHT, K_d) and not gameOver():
					moveRight()
				elif event.key in (K_UP, K_w) and not gameOver():
					moveUp()
				elif event.key in (K_DOWN, K_s) and not gameOver():
					moveDown()
				elif event.key == 13 and gameOver():
					startingBoard()

		FPSCLOCK.tick(FPS)



def startingBoard():
	global BOARD
	BOARD = [BLANK]*NUM_CELLS
	for i in range(NUM_CELLS):
		BOARD[i] = [BLANK]*NUM_CELLS
	
	putRandom()
	putRandom()
	updateDisp()

def countBlank():
	count = 0
	for x in range(NUM_CELLS):
		for y in range(NUM_CELLS):
			if BOARD[x][y] == BLANK:
				count += 1
	return count


def getLeftTopOfTile(tileX, tileY):
	left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
	top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
	return (left, top)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
	# draw a tile at BOARD coordinates tilex and tiley, optionally a few
	# pixels over (determined by adjx and adjy)
	left, top = getLeftTopOfTile(tilex, tiley)
	index = int(math.log2(number)) -1
	pygame.draw.rect(DISPLAYSURF, TILECOLORS[index], (left + adjx, top + adjy, TILESIZE, TILESIZE))
	
	numsize = len(str(number))
	if numsize > 1:
		TILEFONT = pygame.font.Font('freesansbold.ttf', int((1 - numsize/10)*BASICFONTSIZE))
	else:
		TILEFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
	textSurf = TILEFONT.render(str(number), True, TEXTCOLOR)
	textRect = textSurf.get_rect()
	textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
	DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, midX, midY):
	# create the Surface and Rect objects for some text.
	
	textSurf = BASICFONT.render(text, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.center = (midX, midY)
	return (textSurf, textRect)

def getTestBoard():
	for x in range(NUM_CELLS):
		for y in range(NUM_CELLS):
			BOARD[x][y] = x*4 + y

def slideArray():
	for x in range(NUM_CELLS):
		for y in range(NUM_CELLS-1, -1, -1):
				if (BOARD[x][y] == 0):
					del(BOARD[x][y])
					BOARD[x].append(0)
					
def addArray():
	for x in range(NUM_CELLS):
		for y in range(NUM_CELLS-1):
				if BOARD[x][y] == BOARD[x][y+1]:
					BOARD[x][y] += BOARD[x][y+1]
					del(BOARD[x][y+1])
					BOARD[x].append(0)

def rotateBoard(d):
	n= NUM_CELLS
	for i in range(int(n/2)):
		for j in range(i, n-i-1):
			tmp = BOARD[i][j]
			k = n-i-1
			l = n-j-1
			if d == 1:
				BOARD[i][j] = BOARD[j][k];
				BOARD[j][k] = BOARD[k][l];
				BOARD[k][l] = BOARD[l][i];
				BOARD[l][i] = tmp;
			elif d == -1:
				BOARD[i][j] = BOARD[l][i];
				BOARD[l][i] = BOARD[k][l];
				BOARD[k][l] = BOARD[j][k];
				BOARD[j][k] = tmp;


def putRandom():
	if countBlank() > 0 :
		x = random.randint(0, NUM_CELLS-1)
		y = random.randint(0, NUM_CELLS-1)
		
		if BOARD[x][y] != 0 :
			putRandom()
		else:
			BOARD[x][y] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])

def updateDisp():
	DISPLAYSURF.fill(BGCOLOR)
	textSurf, textRect = makeText('2048', MESSAGECOLOR, BGCOLOR, WINDOWWIDTH/2, 30)
	DISPLAYSURF.blit(textSurf, textRect)

	for x in range(NUM_CELLS):
		for y in range(NUM_CELLS):
			a,b = getLeftTopOfTile(x,y)
			pygame.draw.rect(DISPLAYSURF, WHITE,(a,b,TILESIZE, TILESIZE),1)
			if BOARD[x][y] != 0:
				drawTile(x, y, BOARD[x][y])

	left, top = getLeftTopOfTile(0, 0)
	width = NUM_CELLS * TILESIZE
	height = NUM_CELLS * TILESIZE
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
	
	if gameOver():
		textSurf, textRect = makeText('GAME OVER', MESSAGECOLOR, BGCOLOR, WINDOWWIDTH/2, WINDOWHEIGHT/2)
		DISPLAYSURF.blit(textSurf, textRect)
		
	pygame.display.update()


def moveLeft():
	temp = copy.deepcopy(BOARD)
	rotateBoard(1)
	slideArray()
	addArray()
	rotateBoard(-1)
	if temp != BOARD:
		putRandom()
	updateDisp()

def moveRight():
	temp = copy.deepcopy(BOARD)
	rotateBoard(-1)
	slideArray()
	addArray()
	rotateBoard(1)
	if temp != BOARD:
		putRandom()
	updateDisp()

def moveDown():
	temp = copy.deepcopy(BOARD)
	rotateBoard(1)
	rotateBoard(1)
	slideArray()
	addArray()
	rotateBoard(-1)
	rotateBoard(-1)
	if temp != BOARD:
		putRandom()
	updateDisp()

def moveUp():
	temp = copy.deepcopy(BOARD)
	slideArray()
	addArray()
	if temp != BOARD:
		putRandom()
	updateDisp()
	
def foundPair():
	for x in range(NUM_CELLS):
		for y in range(NUM_CELLS-1):
			if BOARD[x][y] == BOARD[x][y+1]:
				return True

def gameOver():
	end = True
	if countBlank() > 0:
		return False
	if foundPair():
		return False
		
	rotateBoard(1)
	if foundPair():
		end = False
		
	rotateBoard(-1)
	return end


if __name__ == '__main__':
	main()
