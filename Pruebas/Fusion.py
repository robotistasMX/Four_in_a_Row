import tkinter as tk
import numpy as np
import pygame
import sys
import math
import random
import time
import cv2 as cv
import numpy as np
import time
cap= cv.VideoCapture(0)

file= open("../data.txt", "r")
low= np.array( [int(file.readline()),int(file.readline()),int(file.readline())] )
upper=  np.array( [int(file.readline()),int(file.readline()),int(file.readline())] )
cA= int(file.readline())
c1= int(file.readline())
rA= int(file.readline())
r1= int(file.readline())
file.close()

grid=[]
for i in range(7):
    grid.append(list())
    for j in range(6):
        grid[i].append(0)

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate(window, piece):

	score = 0
	opp_piece = PLAYER_PIECE

	if window.count(piece) == 4:
		score += 10000000

	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5

	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 100000000

	if window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
		score -= 2

	return score

def score_position(board, piece):

	score = 0

	#Score center
	center = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center.count(piece)
	score += center_count * 6

	#Horizontal
	for r in range(ROW_COUNT):

		rows = [int(i) for i in list(board[r, :])]

		for c in range(COLUMN_COUNT - 3):

			window = rows[c : c + WINDOW_LENGTH]
			score += evaluate(window, piece)

	#Vertical
	for c in range(COLUMN_COUNT):

		colums = [int(i) for i in list(board[:, c])]

		for r in range(ROW_COUNT - 3):

			window = colums[r : r + WINDOW_LENGTH]
			score += evaluate(window, piece)


	#Positive diagonal
	for r in range(ROW_COUNT - 3):

		for c in range(COLUMN_COUNT - 3):

			window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
			score += evaluate(window, piece)

	#Negative diagonal
	for r in range(ROW_COUNT - 3):

		for c in range(COLUMN_COUNT - 3):

			window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
			score += evaluate(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizer):

	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)

	if depth == 0 or is_terminal:

		if is_terminal:

			if winning_move(board, AI_PIECE):
				return (None, 10000000000000)

			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)

			else:
				return (None, 0)

		else:
			return (None, score_position(board, AI_PIECE))

	if maximizer:

		value = -math.inf
		column = random.choice(valid_locations)

		for col in valid_locations:

			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]

			if new_score > value:
				value = new_score
				column = col

			alpha = max(alpha, value)

			if alpha >= beta:
				break

		return column, value

	else: #Minimizer

		value = math.inf
		column = random.choice(valid_locations)

		for col in valid_locations:

			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]

			if new_score < value:
				value = new_score
				column = col

			beta = min(beta, value)

			if alpha >= beta:
				break

		return column, value

def get_valid_locations(board):

	valid_locations = []

	for col in range(COLUMN_COUNT):

		if is_valid_location(board, col):
			valid_locations.append(col)

	return valid_locations

def easy_mode(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = 0
	best_col = random.choice(valid_locations)

	for col in valid_locations:

		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)

		if score > best_score:

			best_score = score
			best_col = col

	return best_col

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def sf():

	dificultad.set(1)
	time.sleep(1)
	ventana.destroy()
	print(dificultad)

def f():

	dificultad.set(2)
	time.sleep(1)
	ventana.destroy()
	print(dificultad)

def im():

	dificultad.set(3)
	time.sleep(1)
	ventana.destroy()
	print(dificultad)

def df():

	dificultad.set(4)
	time.sleep(1)
	ventana.destroy()
	print(dificultad)

#dificultad = input("Escoge un nivel:\n1.Super facil\n2.Facil\n3.Intermedio\n4.Dificil\n")

ventana = tk.Tk()

ventana.title("HolaMundo")
ventana.geometry('500x500')
ventana.configure(background = 'steel blue')
dificultad = tk.IntVar()

titulo = tk.Label(ventana, text = "Conecta4 IA", bg = "black", fg = "white")
titulo.pack(fill = tk.X)

espacio = tk.Label(ventana, bg = "steel blue")
espacio.pack(pady = 30)

sfacil = tk.Button(ventana, text = "Super Facil", bg = "green", fg = "black", command = sf)
sfacil.pack(fill = tk.X, ipady = 20)

facil = tk.Button(ventana, text = "Facil", bg = "yellow", fg = "black", command = f)
facil.pack(fill = tk.X, ipady = 20)

intermedio = tk.Button(ventana, text = "Intermedio", bg = "orange", fg = "black", command = im)
intermedio.pack(fill = tk.X, ipady = 20)

dificil = tk.Button(ventana, text = "Dificil", bg = "red", fg = "black", command = df)
dificil.pack(fill = tk.X, ipady = 20)

ventana.mainloop()

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()
pygame.display.set_mode((0, 0))

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)
#turn = AI

while not game_over:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			sys.exit()

		if turn == PLAYER:
	    # imprime en la consola la tecla presionada
	#pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			event.pos=0
		# Ask for Player 1 Input
			print("ENTER")

			while(True):
				ret, frame= cap.read()
				hsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)

				#Fichas rojas
				filter =cv.inRange(hsv, low, upper)
				filter = cv.GaussianBlur(filter, (1,1), 2)
				filter = cv.medianBlur(filter,5)
				filter = cv.dilate(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
				filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
				filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
				result = cv.bitwise_and(frame, frame, mask = filter)

				gray= cv.cvtColor(result, cv.COLOR_BGR2GRAY)
				gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,19,3)
				circles =  cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50, np.array([]), 100, 20, 10, 70)
				if circles is not None:
					try:
						for c in circles[0]:
							cv.circle(frame, (c[0],c[1]), c[2], (0,0,255),2)
						print(len(circles[0]))
					except:
						pass

				cv.imshow('result',result)
				cv.imshow('frame', frame)

				w=cv.waitKey(1)
				if w & 0xFF == ord("x"):
					print("asdfg")
					ans= -1
					for c in circles[0]:
						column= int((c[0]-c1+cA/2)/cA)
						row= int((c[1]-r1+rA/2)/rA)
						if grid[column][row]==0:
							ans=column
						grid[column][row]=1
					print(grid)
					time.sleep(1)
					break

			columna=ans+1
			print((columna)*100)
			event.pos=[(columna*100)-1,0]
			if turn == PLAYER:

				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):

					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):

						label = myfont.render("Humanity wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)

	# # Ask for Player 2 Input
	if turn == AI and not game_over:

		if dificultad.get() == 1:
			col = random.randint(0, COLUMN_COUNT-1)

		elif dificultad.get() == 2:
			col = easy_mode(board, AI_PIECE)

		elif dificultad.get() == 3:
			col, minimax_score = minimax(board, 3, -math.inf, math.inf, True)

		elif dificultad.get() == 4:
			col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)

		if is_valid_location(board, col):

			#pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = myfont.render("Robots win!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)

cap.release()
cv.destroyAllWindows()