# From https://github.com/kidscancode/pygame_tutorials

import sys
import pygame
import pygame.gfxdraw
import random
import copy
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
TITLE = "BLOCKUDU"
FPS = 30

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)

colors = [0xFFFFFF, 0xDC3C3C, 0x2DD22D, 0x1464C8, 0x32C819,
0xFFA500, 0x1E90FF, 0xFF3A5C, 0x36AED5, 0xFFFF00, 0x33EE44]

rows = 9
cols = 9
gap = 40
size = (HEIGHT-2*gap)//rows
rects = []
board = []
overlay = []
score = 0

pieces = [ [[0,1,0],
			[0,1,0],
			[0,1,0]],

		   [[0,1,0],
			[0,1,0],
			[0,0,0]],

		   [[0,1,0],
			[0,1,1],
			[0,0,0]],

		   [[1,1,0],
			[0,1,1],
			[0,0,0]],

		   [[0,1,1],
			[1,1,0],
			[0,0,0]],

		   [[0,0,0],
			[0,1,0],
			[0,0,0]],

		   [[0,1,0],
			[1,1,1],
			[0,0,0]],

		   [[0,1,0],
			[0,1,0],
			[0,1,1]],

		   [[0,0,0],
			[0,1,1],
			[0,1,1]],

		   [[0,1,0],
			[0,1,0],
			[1,1,0]] ]

class Board :
	def __init__(self):
		pass

class Cell :
	def __init__(self, rect, board, group):
		self.board = board
		self.group = group
		self.rect = rect

def blank_board():
	for i in range(cols+2):
		overlay.append([])
		for j in range(rows+2):
			overlay[i].append(0)

	for i in range(cols):
		rects.append([])
		board.append([])
		for j in range(rows):
			r = i*size, j*size, size, size
			rects[i].append(r)
			board[i].append(0)

def draw_board(surf, pos):
	surf.fill(WHITE)
	for i in range(cols):
		for j in range(rows):
			if overlay[i+1][j+1]: alpha = 100
			else: alpha = 0
			# index = board[i][j] % len(color)
			pygame.draw.rect(surf, colors[board[i][j]], rects[i][j])
			pygame.gfxdraw.box(surf, rects[i][j], (0,0,150,alpha))
			pygame.draw.rect(surf, BLACK, rects[i][j], 1)
	screen.blit(surf, pos)

def clear_overlay():
	for i in range(cols+2):
		for j in range(rows+2):
			overlay[i][j] = 0

def is_valid():
	# check left and right cols
	for i in [-1,0]:
		for j in range(rows+2):
			if overlay[i][j]:
				return 0

	# check top and bottom rows
	for i in range(cols+2):
		for j in [-1,0]:
			if overlay[i][j]:
				return 0

	# check if overlapping
	for i in range(cols):
		for j in range(rows):
			if board[i][j] and overlay[i+1][j+1]:
				return 0
	return 1

def clear_matches():
	row = []
	col = []
	# check if lines are formed
	for i in range(cols):
		r = 0
		c = 0
		global score
		for j in range(rows):
			if board[i][j]:
				r += 1
			if board[j][i]:    # this works, since rows=cols
				c += 1
		if r == rows:
			col.append(i)
			score += 1
		if c == cols:
			row.append(i)
			score += 1

	# clear the matched lines on board
	if row or col:
		for i in range(cols):
			for j in row:
				board[i][j] = 0
		for i in col:
			for j in range(rows):
				board[i][j] = 0

def set_overlay(piece, pos):
	x, y = pos
	clear_overlay()
	for i in range(3):
		for j in range(3):
			overlay[x+i][y+j] = piece[i][j]

def get_next_piece():
	n = random.randint(0, len(pieces)-1)
	piece = copy.deepcopy(pieces[n])
	if n > 1:
		for i in range(3):
			for j in range(3):
				if piece[i][j]:
					piece[i][j] = n
	return piece

def draw_next_piece(rect, piece):
	w = rect.width // 4
	r = pygame.Rect(0, 0, w, w)
	for i in range(3):
		for j in range(3):
			r.centerx = rect.x + (i+1)*w
			r.centery = rect.y + (j+1)*w
			# index = piece[i][j] % len(color)
			pygame.draw.rect(screen, colors[piece[i][j]], r)
	pygame.draw.rect(screen, BLACK, rect, 4)


def draw_score(score_rect):
	pygame.draw.rect(screen, BLACK, score_rect, 4)

	# Draw the label "Score"
	font = pygame.font.Font('freesansbold.ttf', 20)
	surf = font.render("Score", True, BLACK)
	rect = surf.get_rect()
	rect.center = score_rect.centerx, score_rect.top+20
	screen.blit(surf, rect)

	# Draw the score value
	font = pygame.font.Font('freesansbold.ttf', 30)
	surf = font.render(str(score), True, GREY)
	rect = surf.get_rect()
	rect.center = score_rect.center
	screen.blit(surf, rect)

def text_screen(text):
	# This function displays large text in the
	# center of the screen until clicked.
	# Draw the text drop shadow
	font = pygame.font.Font('freesansbold.ttf', 100)
	surf = font.render(text, True, GREY)
	rect = surf.get_rect()
	rect.center = (WIDTH // 2, HEIGHT // 2)
	screen.blit(surf, rect)

	# Draw the text
	surf = font.render(text, True, WHITE)
	rect = surf.get_rect()
	rect.center = (WIDTH // 2 - 3, HEIGHT // 2 - 3)
	screen.blit(surf, rect)

	# Draw the additional "Click to continue." text.
	font = pygame.font.Font('freesansbold.ttf', 18)
	surf = font.render('Click to continue.', True, WHITE)
	rect = surf.get_rect()
	rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
	screen.blit(surf, rect)

	pygame.display.flip()

	pause = True
	while pause:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				pause = False
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

def get_index(pos, rect):
	x, y = pos
	if x<rect.left or y<rect.top or x>rect.right-1 or y>rect.bottom-1:
		return None
	else:
		i = (x-rect.x) // size
		j = (y-rect.y) // size
		return i, j

def rotate(piece):
	N = len(piece)
	for i in range(0, N//2):
		for j in range(i, N-i-1):
			temp = piece[i][j]
			piece[i][j] = piece[j][N-1-i]
			piece[j][N-1-i] = piece[N-1-i][N-1-j]
			piece[N-1-i][N-1-j] = piece[N-1-j][i]
			piece[N-1-j][i] = temp
	return piece

def main():
	# initialize pygame and create window
	global screen, clock

	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(TITLE)
	clock = pygame.time.Clock()

	text_screen(TITLE)

	board_rect = pygame.Rect(gap, gap, size*cols, size*rows)
	next_rect = pygame.Rect(size*cols+2*gap, gap, 120, 120)
	score_rect = pygame.Rect(size*cols+2*gap, 200, 120, 240)

	board_surf = pygame.Surface(board_rect.size)

	blank_board()

	piece = get_next_piece()
	next_piece = get_next_piece()

	# Game loop
	while True:
		# Process input events
		for event in pygame.event.get():
			# check for closing window
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == MOUSEBUTTONUP:
				if event.button == 2:
					print(board)
				if event.button == 3:
					piece = rotate(piece)
					pos = get_index(event.pos, board_rect)
					if pos:
						set_overlay(piece, pos)
				if event.button == 1 and is_valid():
					piece = next_piece
					next_piece = get_next_piece()
					for i in range(cols):
						for j in range(rows):
							board[i][j] += overlay[i+1][j+1]

			if event.type == MOUSEMOTION:
				pos = get_index(event.pos, board_rect)
				if pos:
					set_overlay(piece, pos)

		# Update
		clear_matches()

		# Draw / render
		screen.fill(WHITE)

		draw_board(board_surf, board_rect.topleft)
		draw_next_piece(next_rect, next_piece)
		draw_score(score_rect)

		pygame.display.flip()
		clock.tick(FPS)


if __name__=='__main__':
	main()
