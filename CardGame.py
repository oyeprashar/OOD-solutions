"""
Asked me to build a matching cards game, it was somehing like, we have to select one card and next another card,
and if both are the same you have to keep them in an open state otherwise both of them should be closed, this was the requirement.

1. Requirement gathering:
	1. We have a matrix of cards
	2. A user can select two cards at a time
	3. If these cards are same, they remain in open state
	4. If these cards are not same, they are hidden again
	5. We will be counting the number of flips
	5. If a card is open then you cannot open it again

2. Identifying the entities and services

	Entities:
		1. Board
			a. size
			b. grid

		2. Card
			a. state
			b. symbol

	Service:
		1. AbstractGameService
			+ makeMove(slot1, slot2)

		2. GameService
			+ makeMove(slot1, slot2)
			- validateInput()
			- checkIsGameOver()

3. Design
4. Refine
"""
from abc import ABC, abstractmethod
import threading


class Board:

	def __init__(self, size):
		self.size = size
		self.grid = []
		self.initializeEmptyBoard()

	def initializeEmptyBoard(self):

		for i in range(self.size):
			currRow = []
			for j in range(self.size):
				currRow.append("EMPTY")
			self.grid.append(currRow)

	def addCardToBoard(self, i, j, cardObj):

		if i < 0 or i >= self.size or j < 0 or j >= self.size or self.grid[i][j] != "EMPTY":
			print("Invalid slot")
			return self

		self.grid[i][j] = cardObj
		return self

	def printGrid(self):
		print("----------------------------------------------------------------")
		for i in range(self.size):
			currRow = []
			for j in range(self.size):
				if self.grid[i][j] == "EMPTY":
					currRow.append("EMPTY")
				else:
					currRow.append(self.grid[i][j].getSymbolforBoard())
			print(currRow)

	def getSize(self):
		return self.size

	def getGrid(self):
		return self.grid


class Card:
	def __init__(self, symbol):
		self.symbol = symbol
		self.isVisible = False

	def getSymbolforBoard(self):
		if not self.isVisible:
			return "-"
		else:
			return self.symbol

	def setVisibility(self, visibility):
		self.isVisible = visibility

	def getIsVisible(self):
		return self.isVisible

	def getSymbol(self):
		return self.symbol


class AbstractGameManager(ABC):

	@abstractmethod
	def makeMove(self, slot1, slot2):
		pass


class GameManager(AbstractGameManager):

	def __init__(self, board):
		self.board = board
		self.flips = 0
		self.gameOver = False
		self.makeMoveLock = threading.Lock()

	def isValid(self, slot1, slot2):
		if slot1[0] < 0 or slot1[0] >= self.board.getSize() or slot1[1] < 0 or slot1[1] >= self.board.getSize():
			return False

		if slot2[0] < 0 or slot2[0] >= self.board.getSize() or slot2[1] < 0 or slot2[1] >= self.board.getSize():
			return False

		# if the visibility of the card is already true then we cannot pick it
		card1 = self.board.getGrid()[slot1[0]][slot1[1]]
		card2 = self.board.getGrid()[slot2[0]][slot2[1]]

		if card1.getIsVisible() is True or card2.getIsVisible() is True:
			return False

		return True

	def checkIsGameOver(self):
		grid = self.board.getGrid()

		for i in range(self.board.getSize()):
			for j in range(self.board.getSize()):

				currVisibility = grid[i][j].getIsVisible()

				if currVisibility is False:
					return False

		self.gameOver = True
		return True

	def makeMove(self, slot1, slot2):
		
		self.makeMoveLock.acquire()
		
		if self.isValid(slot1, slot2) and not self.gameOver:

			# if symbol of both slots matches then we keep them open else we close them
			card1 = self.board.getGrid()[slot1[0]][slot1[1]]
			card2 = self.board.getGrid()[slot2[0]][slot2[1]]

			if card1.getSymbol() != "-" and card2.getSymbol() != "-" and card1.getSymbol() == card2.getSymbol():

				card1.setVisibility(True)
				card2.setVisibility(True)

			self.flips += 1
			print("TOTAL FLIPS :", self.flips)

			self.board.printGrid()
			self.checkIsGameOver()

			if self.gameOver:
				print("GAME OVER!")
				
		self.makeMoveLock.release()


board = Board(2)
card00 = Card("S")
card01 = Card("A")
card10 = Card("A")
card11 = Card("S")

# THIS IS BUILDER PATTERN
board.addCardToBoard(0, 0, card00).addCardToBoard(0, 1, card01).addCardToBoard(1, 0, card10).addCardToBoard(1, 1, card11)
gameManager = GameManager(board)
gameManager.makeMove([0, 0], [0, 1])
gameManager.makeMove([0, 1], [1, 0])
