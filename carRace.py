
import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

done = False

while not done:
	for event in pygame.event.get():
		print(event)
		if event.type == pygame.QUIT:
			done = True

	screen.fill(WHITE)

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
