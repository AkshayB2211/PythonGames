
import pygame,sys
from pygame.locals import *

# Game constants
W_HEIGHT = 600
W_WIDTH  = 800
FPS 	 = 30

# Define some colors
BLACK	=	(0, 0, 0)
WHITE	=	(255, 255, 255)
BLUE	=	(0, 0, 255)
GREEN	=	(0, 255,   0)
RED		=	(255, 0, 0)
SKYBLUE	=	(0, 240, 255)
GRASS	=	(50,170,20)
GREY	=	(127, 127, 127)

def main():
	global SCREEN
	pygame.init()

	SCREEN = pygame.display.set_mode((W_WIDTH,W_HEIGHT))
	pygame.display.set_caption("CARS MANIA")
	clock = pygame.time.Clock()
	
	while True: # main game loop

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()

			if event.type == KEYUP:
				
				if event.key in (K_LEFT, K_a) and not gameOver():
					print('left')
				elif event.key in (K_RIGHT, K_d) and not gameOver():
					print(clock.get_fps())
				elif event.key in (K_UP, K_w) and not gameOver():
					pass
				elif event.key in (K_DOWN, K_s) and not gameOver():
					pass
				elif event.key == 13 and gameOver():
					pass

		drawScreen()
		updateDisp()
		
		clock.tick(FPS)
		
		
def drawScreen():
	pass

def updateDisp():
	offset = 100
	
	SCREEN.fill(WHITE)
	pygame.draw.rect(SCREEN, SKYBLUE, (0, 0, W_WIDTH, W_HEIGHT//2))
	pygame.draw.rect(SCREEN, GRASS, (0, W_HEIGHT//2, W_WIDTH, W_HEIGHT//2))
	
	l = 50
	for i in range(0, W_HEIGHT//2):	
		j = W_HEIGHT-i
		pygame.draw.line(SCREEN, RED, (50, j), (l+50, j))
		pygame.draw.line(SCREEN, GREY, (l+50, j), (W_WIDTH-l-50, j))
		pygame.draw.line(SCREEN, RED, (W_WIDTH-l-50, j), (W_WIDTH-50, j))
	
	pygame.display.update()
	
def gameOver():
	return False

if __name__ == '__main__':
	main();
