
import pygame,sys, math
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
BROWN	=	(150, 110, 40)


def main():
	global SCREEN
	pygame.init()

	SCREEN = pygame.display.set_mode((W_WIDTH,W_HEIGHT))
	pygame.display.set_caption("CARS MANIA")
	clock = pygame.time.Clock()

	Distance = 0.0				# Distance car has travelled around track
	Curvature = 0.0				# Current track curvature, lerped between track sections
	TrackCurvature = 0.0		# Accumulation of track curvature
	TrackDistance = 0.0			# Total distance of track

	CarPos = 0.0				# Current car position
	PlayerCurvature = 0.0		# Accumulation of player curvature
	Speed = 0.0					# Current player speed

	Track = []					# Track sections, sharpness of bend, length of section

	listLapTimes = []			# List of previous lap times
	CurrentLapTime = 0			# Current lap time
	
	# Direction booleans
	UP = False
	LEFT = False
	RIGHT = False


	# Define track
	Track.append((0.0, 10.0))	# Short section for start/finish line
	Track.append((0.0, 200.0))
	Track.append((0.5, 200.0))
	Track.append((0.0, 400.0))
	Track.append((-0.5, 100.0))
	Track.append((0.0, 200.0))
	Track.append((-0.5, 200.0))
	Track.append((0.5, 200.0))
	Track.append((0.0, 200.0))
	Track.append((0.2, 500.0))
	Track.append((0.0, 200.0))

	# Calculate total track distance, so we can set lap times
	for t in Track:
		TrackDistance += t[1]

	listLapTimes = ['0','0','0','0','0']
	fCurrentLapTime = 0.0
	print(listLapTimes)

	while True: # main game loop

		# Handle control input
		CarDirection = 0
		timeElapsed = clock.get_time()/1000
		#~ print(timeElapsed)

		SCREEN.fill(WHITE)

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
				
			if event.type == KEYDOWN:
				if event.key in (K_LEFT, K_a) and not gameOver():
					LEFT = True
				elif event.key in (K_RIGHT, K_d) and not gameOver():
					RIGHT = True
				elif event.key in (K_UP, K_w) and not gameOver():
					UP = True
				elif event.key in (K_DOWN, K_s) and not gameOver():
					pass
			
			if event.type == KEYUP:
				if event.key in (K_LEFT, K_a) and not gameOver():
					LEFT = False
				elif event.key in (K_RIGHT, K_d) and not gameOver():
					RIGHT = False
				elif event.key in (K_UP, K_w) and not gameOver():
					UP = False
				elif event.key in (K_DOWN, K_s) and not gameOver():
					pass
				elif event.key == 13 and gameOver():		# Press Enter to restart
					pass
		
		if (UP):
			Speed += 2.0 * timeElapsed
		else:
			Speed -= 1.0 * timeElapsed
		
		# Car Curvature is accumulated left/right input, but inversely proportional to speed
		# i.e. it is harder to turn at high speed
		if (LEFT):
			PlayerCurvature -= 0.7 * timeElapsed * (1.0 - Speed / 2.0)
			CarDirection = -1

		if (RIGHT):
			PlayerCurvature += 0.7 * timeElapsed * (1.0 - Speed / 2.0)
			CarDirection = +1

		# If car curvature is too different to track curvature, slow down
		# as car has gone off track
		if (math.fabs(PlayerCurvature - TrackCurvature) >= 0.8):
			Speed -= 5.0 * timeElapsed

		# Clamp Speed
		if (Speed < 0.0):
			Speed = 0.0;
		if (Speed > 1.0):
			Speed = 1.0;
		
		# Move car along track according to car speed
		Distance += (70 * Speed) * timeElapsed
		#~ print(Distance)

		# Get Point on track
		Offset = 0;
		TrackSection = 0;

		# Lap Timing and counting
		CurrentLapTime += timeElapsed
		if (Distance >= TrackDistance):
			Distance -= TrackDistance
			listLapTimes.append('%.3f' %CurrentLapTime)
			del(listLapTimes[0])
			print(listLapTimes)
			CurrentLapTime = 0.0

		# Find position on track
		while (TrackSection < len(Track) and Offset <= Distance):
			Offset += Track[TrackSection][1]
			TrackSection += 1

		# Interpolate towards target track curvature
		TargetCurvature = Track[TrackSection - 1][0]
		TrackCurveDiff = (TargetCurvature - Curvature) * timeElapsed * Speed

		# Accumulate player curvature
		Curvature += TrackCurveDiff
		#~ print(Curvature)

		# Accumulate track curvature
		TrackCurvature += (Curvature) * timeElapsed * Speed

		# Draw Sky
		pygame.draw.rect(SCREEN, SKYBLUE, (0, 0, W_WIDTH, W_HEIGHT//2))
		
		# Draw Scenery - our hills are a rectified sine wave, where the phase is adjusted by the
		# accumulated track curvature
		for x in range(W_WIDTH):
			HillHeight = int(math.fabs(math.sin(x * 0.01 + TrackCurvature) * 128))
			pygame.draw.line(SCREEN, BROWN, (x, W_HEIGHT//2), (x, W_HEIGHT//2 - HillHeight))

		# Draw road
		for i in range(0, W_HEIGHT//2):
			Perspective = i/W_HEIGHT
			RoadWidth = 0.04 + Perspective
			ClipWidth = RoadWidth * 0.15

			MiddlePoint = 0.5 + Curvature * ((1.0 - Perspective) ** 6)

			LeftGrass = (MiddlePoint - RoadWidth - ClipWidth) * W_WIDTH
			LeftClip = (MiddlePoint - RoadWidth) * W_WIDTH
			RightClip = (MiddlePoint + RoadWidth) * W_WIDTH
			RightGrass = (MiddlePoint + RoadWidth + ClipWidth) * W_WIDTH

			GrassColour = GREEN if (math.sin(20.0 * (1.0 - Perspective)**6 + Distance * 0.1) > 0.0) else GRASS
			ClipColour 	= RED 	if (math.sin(80.0 * (1.0 - Perspective)**2 + Distance) > 0.0) else WHITE
			RoadColour = WHITE 	if (TrackSection-1) == 0 else GREY

			h = i + W_HEIGHT//2
			pygame.draw.line(SCREEN, GrassColour, (0, h), (LeftGrass, h))
			pygame.draw.line(SCREEN, ClipColour, (LeftGrass, h), (LeftClip, h))
			pygame.draw.line(SCREEN, RoadColour, (LeftClip, h), (RightClip, h))
			pygame.draw.line(SCREEN, ClipColour, (RightClip, h), (RightGrass, h))
			pygame.draw.line(SCREEN, GrassColour, (RightGrass, h), (W_WIDTH, h))

		# Draw car
		CarPos = PlayerCurvature - TrackCurvature
		CarPos = W_WIDTH / 2 + (W_WIDTH * CarPos) / 2
		pygame.draw.rect(SCREEN, BLACK, (CarPos, W_HEIGHT-100, 100, 50))

		pygame.display.update()
		clock.tick(FPS)

def gameOver():
	return False

if __name__ == '__main__':
	main()
