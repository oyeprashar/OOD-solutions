"""
Snake and ladder OOD

1. Requirement gathering and use cases

	Input:
		1. Number of snakes (s) followed by s lines each containing 2 numbers denoting the head and tail positions of the snake.
		2. Number of ladders (l) followed by l lines each containing 2 numbers denoting the start and end positions of the ladder.
		3. Number of players (p) followed by p lines each containing a name.

	Output:

		No winner yet:
			Format: <player_name> rolled a <dice_value> and moved from <initial_position> to <final_position>

		Winner found:
			Format: <player_name> wins the game


	Rules:
		1. All players start from cell 0
		2. Cells are numbers from 1 - 100
		3. if curr + dice > 100, player doesn't move
		4. There are ladders and snakes
		5. It is always possible to reach the 100th cell

2. Identifying the entities and services

	Entities:
		1. Dice 
			Attributes: maximum number

		2. Board
			Attributes: maximum cell number

		3. Player
			Attributes: Name

	Services:
		1. GameManager 
			Methods:
				+ play()
				- validateMove()
				- findWinner()

3. Design
4. Refine ~ Singleton, factory etc
"""
from abc import ABC, abstractmethod
from random import randint

class Player:

	def __init__(self,name):
		self.name = name
		self.postion = 0
		self.finished = False


	def getPosition(self):
		return self.postion

	def getName(self):
		return self.name

	def setPostion(self,postion):
		self.postion = postion

	def setFinished(self,finished):
		self.finished = finished

	def getFinished(self):
		return self.finished

class Dice:

	def __init__(self,maximumNum):
		self.maximumNum = maximumNum

	def roll(self):
		return randint(1,self.maximumNum)


class Board:
	def __init__(self,maxCell):
		self.maxCell = maxCell
		self.specialMoves = {}

	def getMaxCell(self):
		return self.maxCell

	def addSpecialMoves(self,fromCell,toCell):
		self.specialMoves[fromCell] = toCell

	def getSpecialMoves(self):
		return self.specialMoves


class AbstractGameManager(ABC):

	@abstractmethod
	def registerPlayer(self,name):
		pass

	@abstractmethod
	def play(self,board,dice):
		pass

	@abstractmethod
	def validate(self,newCell,board):
		pass

	# @abstractmethod
	# def __findWinner(self,board)
	# 	pass


# this can be singleton
class GameManager(AbstractGameManager):

	__instance = None

	def getInstance():
		if GameManager.__instance == None:
			GameManager.__instance = GameManager()

		return GameManager.__instance

	def __init__(self):

		if GameManager.__instance != None:
			raise Exception("Object already exists! Use the getInstance method")

		GameManager.__instance = self
		self.playerCountToObject = {}
		self.playerCount = 0 
		self.numberOfPlayersWon = 0
		self.turn = 0 
		self.end = False

	def initialize(self):
		self.end = False


	def registerPlayer(self,name):
		self.playerCountToObject[self.playerCount] = Player(name)
		self.playerCount += 1

	def allPlayersWon(self):
		if self.numberOfPlayersWon == len(self.playerCountToObject):
			print("All players have won the match! Reseting!")

			self.numberOfPlayersWon = 0
			self.turn = 0

			for id in self.playerCountToObject:
				self.playerCountToObject[id].setPostion(0)

			self.end = True


	def validate(self,newCell,board):
		return newCell <= board.getMaxCell()


	def play(self,board,dice):

		if self.end == True:
			print("Game ended!")
			return

		if self.playerCount == 0:
			print("Please register players before playing!")
			return

		currPlayer = self.playerCountToObject[self.turn]

		diceJump = dice.roll()

		if currPlayer.getFinished() == False:

			newPos = currPlayer.getPosition() + diceJump
			oldPos = currPlayer.getPosition()

			if newPos in board.getSpecialMoves():
				newPos = board.getSpecialMoves()[newPos]

			if newPos > board.getMaxCell(): 
				print("Invalid move try again!")
				return

			elif newPos < board.getMaxCell():
				print(currPlayer.getName(),"moved from",oldPos,"to",newPos,"dice =",diceJump)
				currPlayer.setPostion(newPos)

			else:
				currPlayer.setPostion(newPos)
				currPlayer.setFinished(True)
				print(currPlayer.getName(),"won the game by moving from",oldPos,"to",newPos,"dice =",diceJump)
				self.numberOfPlayersWon += 1

		self.allPlayersWon()
		self.turn = (self.turn + 1) % len(self.playerCountToObject)


dice = Dice(6)
board = Board(10)
board.addSpecialMoves(1,10)

gameManager = GameManager()
gameManager.registerPlayer("Shubham")
gameManager.registerPlayer("Shikha")

gameManager.initialize()
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)
gameManager.play(board,dice)

