"""
Sokoban OOD

1. Requirement gathering and use case

	[. . . T]
	[# . # #]
	[. B . .]
	[. . . S]


	S: start point
	B: box
	. : empty cell
	#: wall
	T: target

	Cases when player makes a new move to up/down/left/right
		1. Either that new cell was invalid
		2. That new cell was empty and user can go there
		3. That new cell had box
			a. dir + 1 was occupied or invalid
				we cannot move
			b. dir + 1 was empty and we move there 

	Input:
		1. Starting index
		2. Up, down,left,right

	Ouput:
		1. If valid move then print the board
		2. If we reached the end reset the box to source and say you won

2. Identifying the entities and services

	Entities:
		1. Player
			Attributes
				a. name

		2. Board
			Attributes
				a. size
			Methods
				+ setSource()
				+ setDestination()
				+ addObstacle()

	Services
		1. GameManager
			Methods
				+ registerPlayer()
				+ registerBoard()
				+ play()
				- __validateMove()
				- __move() 
				- __checkWon()


3. Design
4. Refine : refactor, singleton, factory etc
"""

from abc import ABC, abstractmethod

class Player:
	def __init__(self,name):
		self.name = name

	def getName(self):
		return self.name


class Board:
	def __init__(self,size):
		self.size = size
		self.grid = []
		self.makeGrid()
		self.source = [-1,-1]
		self.destination = [-1,-1]

	def makeGrid(self):

		for x in range(self.size):
			currRow = []
			for y in range(self.size):
				currRow.append('.')
			self.grid.append(currRow)

	def setSource(self,i,j):
		self.source = [i,j]
		self.grid[i][j] = 'S'

	def setDestination(self,i,j):
		self.destination = [i,j]
		self.grid[i][j] = 'D'

	def addObstacle(self,i,j):
		self.grid[i][j] = '#'

	def getSize(self):
		return self.size

	def getGrid(self):
		return self.grid

class AbstractGameManager(ABC):

	@abstractmethod
	def registerPlayer(self,name):
		pass

	@abstractmethod
	def registerBoard(self,board):
		pass

	@abstractmethod
	def __validateMove(self,i,j):
		pass

	@abstractmethod
	def play(self,i,j):
		pass

	@abstractmethod
	def move(self,i,j):
		pass

	@abstractmethod
	def checkWon(self,i,j):
		pass
