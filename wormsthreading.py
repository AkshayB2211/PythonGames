import random, sys, pygame, threading
from pygame.locals import *

#Constants

NUM_WORMS = 20
FPS =30
CELL_SIZE = 20
CELL_ROWS = 30
CELL_COLS = 20

GRID = []
for x in range(CELL_ROWS):
	GRID.append([None]*CELL_COLS)

GRID_LOCK = threading.Lock()

# Constants for some colors.
#             R    G    B

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK             # color to use for the background of the grid
GRID_LINES_COLOR = DARKGRAY # color to use for the lines of the grid

# Calculate total pixels wide and high that the full window is
WINDOWWIDTH = CELL_SIZE * CELL_ROWS
WINDOWHEIGHT = CELL_SIZE * CELL_COLS

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0
TAIL = -1

RUNNING = True


class Worm(threading.Thread):

	def __init__(self, name='Worm', maxsize=None, color = None, speed = None):
		threading.Thread.__init__(self)
		self.name = name

		if maxsize == None:
			self.maxsize = random.randint(4, 10)
			if random.randint(0,4)==0:
				self.maxsize+=random.randint(10,20)
		else:
			self.maxsize = maxsize

		if color == None:
			self.color = (random.randint(60,255), random.randint(60,255), random.randint(60,255))
		else:
			self.color = color

		if speed == None:
			self.speed = random.randint(20,500)
		else:
			self.speed = speed

		GRID_LOCK.acquire()

		while True:
			startx = random.randint(0, CELL_ROWS-1)
			starty = random.randint(0, CELL_COLS-1)
			if GRID[startx][starty] == None:
				break

		GRID[startx][starty] = self.color

		GRID_LOCK.release()

		self.body = [{'x':startx, 'y':starty}]
		self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

	def run(self):
		while True:
			if not RUNNING:
				return

			# Randomly decide to change direction
			if random.randint(0, 100) < 20: # 20% to change direction
				self.direction = random.choice((UP, DOWN, LEFT, RIGHT))

			GRID_LOCK.acquire()
			# don't return until this thread can acquire the lock

			nextx, nexty = self.getNextPosition()

			if ( nextx in (-1, CELL_ROWS) or nexty in (-1, CELL_COLS) or
				GRID[nextx][nexty] is not None):

				# The space the worm is heading towards is taken, so find a new direction.
				self.direction = self.getNewDirection()

				if self.direction is None:
					# No places to move, so try reversing our worm.
					self.body.reverse()
					# Now the head is the tail and the tail is the head. Magic!
					self.direction = self.getNewDirection()
				
				if self.direction is not None:
					nextx, nexty = self.getNextPosition()

			if self.direction is not None:
				# Space on the grid is free, so move there.

				GRID[nextx][nexty] = self.color # update the GRID state
				self.body.insert(0, {'x': nextx, 'y': nexty})
				# update this worm's own state

				# Check if we've grown too long, and cut off tail if we have.
				# This gives the illusion of the worm moving.
				if len(self.body) > self.maxsize:
					GRID[self.body[TAIL]['x']][self.body[TAIL]['y']] = None
					# update the GRID state

					del self.body[TAIL]
					# update this worm's own state

			else:
				self.direction = random.choice((UP, DOWN, LEFT, RIGHT))
				# can't move, so just do nothing for now but set a new random direction

			GRID_LOCK.release()
			pygame.time.wait(self.speed)

	def getNextPosition(self):
		# Figure out the x and y of where the worm's head would be next, based
		# on the current position of its "head" and direction member.

		if self.direction == UP:
			nextx = self.body[HEAD]['x']
			nexty = self.body[HEAD]['y'] - 1

		elif self.direction == DOWN:
			nextx = self.body[HEAD]['x']
			nexty = self.body[HEAD]['y'] + 1

		elif self.direction == LEFT:
			nextx = self.body[HEAD]['x'] - 1
			nexty = self.body[HEAD]['y']

		elif self.direction == RIGHT:
			nextx = self.body[HEAD]['x'] + 1
			nexty = self.body[HEAD]['y']

		else:
			assert False, 'Bad value for self.direction: %s' % self.direction

		return nextx, nexty

	def getNewDirection(self):

		# syntactic sugar, makes the code below more readable
		x = self.body[HEAD]['x']
		y = self.body[HEAD]['y']

		# Compile a list of possible directions the worm can move.
		newDirection = []

		if y - 1 not in (-1, CELL_COLS) and GRID[x][y - 1] is None:
			newDirection.append(UP)

		if y + 1 not in (-1, CELL_COLS) and GRID[x][y + 1] is None:
			newDirection.append(DOWN)

		if x - 1 not in (-1, CELL_ROWS) and GRID[x - 1][y] is None:
			newDirection.append(LEFT)

		if x + 1 not in (-1, CELL_ROWS) and GRID[x + 1][y] is None:
			newDirection.append(RIGHT)

		if newDirection == []:
			return None

		return random.choice(newDirection)










def main():

	global FPSCLOCK, DISPLAYSURF

	# Draw some walls on the grid
	squares = """
...........................
...........................
...........................
.H..H..EEE..L....L.....OO..
.H..H..E....L....L....O..O.
.HHHH..EE...L....L....O..O.
.H..H..E....L....L....O..O.
.H..H..EEE..LLL..LLL...OO..
...........................
.W.....W...OO...RRR..MM.MM.
.W.....W..O..O..R.R..M.M.M.
.W..W..W..O..O..RR...M.M.M.
.W..W..W..O..O..R.R..M...M.
..WW.WW....OO...R.R..M...M.
...........................
...........................
"""
	#~ setGridSquares(squares)

	# Pygame window set up.
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Threadworms')

	# create Worm Objects
	worms = []
	for i in range(NUM_WORMS):
		worms.append(Worm())
		worms[-1].start()

	# Game LOOP
	while True:
		handleEvents()
		drawGrid()

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def handleEvents():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			RUNNING = False
			pygame.quit()
			sys.exit()

def drawGrid():
	# Draw the grid lines.
	DISPLAYSURF.fill(BGCOLOR)

	for x in range(0, WINDOWWIDTH, CELL_SIZE): # draw vertical lines
		pygame.draw.line(DISPLAYSURF, GRID_LINES_COLOR, (x, 0), (x, WINDOWHEIGHT))

	for y in range(0, WINDOWHEIGHT, CELL_SIZE): # draw horizontal lines
		pygame.draw.line(DISPLAYSURF, GRID_LINES_COLOR, (0, y), (WINDOWWIDTH, y))

	# The main thread that stays in the main loop (which calls drawGrid) also
	# needs to acquire the GRID_LOCK lock before modifying the GRID variable.

	GRID_LOCK.acquire()

	for x in range(0, CELL_ROWS):
		for y in range(0, CELL_COLS):
			if GRID[x][y] is None:
				continue # No body segment at this cell to draw, so skip it

			color = GRID[x][y] # modify the GRID data structure

			# Draw the body segment on the screen
			darkerColor = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
			pygame.draw.rect(DISPLAYSURF, darkerColor, (x * CELL_SIZE,     y * CELL_SIZE,     CELL_SIZE,     CELL_SIZE    ))
			pygame.draw.rect(DISPLAYSURF, color,       (x * CELL_SIZE + 4, y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))

	GRID_LOCK.release() # We're done messing with GRID, so release the lock.


def setGridSquares(squares, color=(192, 192, 192)):

# squares is set to a value like:
# """
# ......
# ...XX.
# ...XX.
# ......
# """

	squares = squares.split('\n')

	if squares[0] == '':
		del squares[0]

	if squares[-1] == '':
		del squares[-1]

	GRID_LOCK.acquire()

	for y in range(min(len(squares), CELL_COLS)):
		for x in range(min(len(squares[y]), CELL_ROWS)):
			if squares[y][x] == ' ':
				GRID[x][y] = None
			elif squares[y][x] == '.':
				pass
			else:
				GRID[x][y] = color

	GRID_LOCK.release()


if __name__ == '__main__':
	main()
