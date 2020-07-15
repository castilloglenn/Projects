from math import inf as infinity
import numpy as np
import random as r
import time, os


human = "O"
computer = "X"
count = 0


def newBoard(board):
	return [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
		
		
def winCheck(board):
	isWinner = ""
	validPiece = ["X", "O"]
	
	for i in range(len(validPiece)):
		# HORIZONTAL
		if board[1] == board[2] == board[3] == validPiece[i] or board[4] == board[5] == board[6] == validPiece[i] or board[7] == board[8] == board[9] == validPiece[i]:
			return validPiece[i]
		
		# VERTICAL
		if board[1] == board[4] == board[7] == validPiece[i] or board[2] == board[5] == board[8] == validPiece[i] or board[3] == board[6] == board[9] == validPiece[i]:
			return validPiece[i]
			
		# DIAGONAL
		if board[1] == board[5] == board[9] == validPiece[i] or board[3] == board[5] == board[7] == validPiece[i]:
			return validPiece[i]
			
	if boardCheck(board) == True:
		return "draw"
	
	return False
	
	
def boardCheck(board):
	filledSpots = 0
	for i in range(1, 10):
		if board[i] != " ":
			filledSpots += 1
	return filledSpots == 9
	
	
def showBoard(thisBoard):
	print(f"""      BOARD             GUIDE
   --- --- ---       --- --- --- 
  | {thisBoard[1]} | {thisBoard[2]} | {thisBoard[3]} |     | 1 | 2 | 3 |
   --- --- ---       --- --- --- 
  | {thisBoard[4]} | {thisBoard[5]} | {thisBoard[6]} |     | 4 | 5 | 6 |
   --- --- ---       --- --- --- 
  | {thisBoard[7]} | {thisBoard[8]} | {thisBoard[9]} |     | 7 | 8 | 9 |
   --- --- ---       --- --- --- 
	""")
	

def flickSwitch(index, turn):
	flickList = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
	flickList[index] = turn
	
	print(f"""      BOARD             GUIDE
   --- --- ---       --- --- --- 
  | {flickList[1]} | {flickList[2]} | {flickList[3]} |     | 1 | 2 | 3 |
   --- --- ---       --- --- --- 
  | {flickList[4]} | {flickList[5]} | {flickList[6]} |     | 4 | 5 | 6 |
   --- --- ---       --- --- --- 
  | {flickList[7]} | {flickList[8]} | {flickList[9]} |     | 7 | 8 | 9 |
   --- --- ---       --- --- --- 
	""")


def flickerBoard(board, index, turn, score1, score2, draw):
	os.system("clear")
	dashboard(score1, score2, draw)
	flickSwitch(index, turn)
	# print(f"Computer placing the turn")
	time.sleep(0.5)


def dashboard(score1, score2, draw):
	os.system("clear")
	print(f"You: {score1}   Computer: {score2}   Draw: {draw}\n")
	
	
def availableTurns(aboard):
	availableTurns = []
	for i in range(1, 10):
		if aboard[i] == " ":
			availableTurns.append(i)
			
	shuffle = np.copy(availableTurns)
	for i in range(len(availableTurns)):
		shuffle[i] = r.choice(availableTurns)
		availableTurns.remove(shuffle[i])
	
	return shuffle
	
	
def minimax(board, depth, alpha, beta, is_max):
	global count
	count += 1
	
	terminalState = winCheck(board)
	if terminalState == computer:
		return 10 - depth
	elif terminalState == human:
		return -10 + depth
	elif terminalState == "draw":
		return 0
	
	if is_max:
		maxValue = -infinity
		turns = availableTurns(board)
		for move in range(len(turns)):
			tempBoard = np.copy(board)
			tempBoard[turns[move]] = computer
			child = minimax(tempBoard, depth + 1, alpha, beta, False)
			if child > maxValue:
				maxValue = child
				bestIndex = turns[move]
			if child >= beta:
				break
			alpha = max(child, alpha)
		if depth == 0:
			return bestIndex
		return maxValue
	else:
		minValue = infinity
		turns = availableTurns(board)
		for move in range(len(turns)):
			tempBoard = np.copy(board)
			tempBoard[turns[move]] = human
			child = minimax(tempBoard, depth + 1, alpha, beta, True)
			if child < minValue:
				minValue = child
			if child <= alpha:
				break
			beta = min(child, minValue)
		return minValue


def main():
	global count
	score1 = score2 = draw = 0
	continuity = True
	while continuity:
		board = ["0", "1", "2", "3", "4", 
				 "5", "6", "7", "8", "9"]
		board = newBoard(board)
		unavailableTurn = []
		userInput = 0
		while True:
			# computer turn
			count = 0
			dashboard(score1, score2, draw)
			showBoard(board)
			print("Thinking...")
			bestTurn = minimax(board, 0, -infinity, infinity, True)
			unavailableTurn.append(bestTurn)
			board[bestTurn] = computer
			flickerBoard(board, bestTurn, computer, score1, score2, draw)
			hasWinner = winCheck(board)
			if hasWinner == computer:
				score2 += 1
				dashboard(score1, score2, draw)
				showBoard(board)
				print("COMPUTER WINS!")
				time.sleep(1)
				break
			elif hasWinner == "draw":
				draw += 1
				dashboard(score1, score2, draw)
				showBoard(board)
				print("Draw!")
				time.sleep(1)
				break
			# player 1 turn
			dashboard(score1, score2, draw)
			showBoard(board)
			while True:
				try:
					userInput = int(input("[O] Enter your turn: "))
				except ValueError:
					pass
				if userInput >= 1 and userInput <= 9 and userInput not in unavailableTurn:
					unavailableTurn.append(userInput)
					board[userInput] = human
					break
			hasWinner = winCheck(board)
			if hasWinner == human:
				score1 += 1
				dashboard(score1, score2, draw)
				showBoard(board)
				print("YOU WIN!")
				time.sleep(1)
				break
			elif hasWinner == "draw":
				draw += 1
				dashboard(score1, score2, draw)
				showBoard(board)
				print("Draw!")
				time.sleep(1)
				break
		ask = input("Next Game? [Enter \"N\" to close]: ").lower()
		if ask == "n":
			continuity = False


if __name__ == "__main__":
	main()
