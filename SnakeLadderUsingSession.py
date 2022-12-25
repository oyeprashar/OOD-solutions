"""
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
		2. Cells are numbers from 1 to 100
		3. if curr + dice > 100, player doesn't move
		4. There are ladders and snakes
		5. It is always possible to reach the 100th cell

Identiying the entities and services:

	Entities:
		1. Board:
			Attributes:
				a. size
				b. specialCellDictionary (snakes and ladders)

		2. Session:
			Attributes:
				a. sessionId
				b. playersList
				c. boardObj
				d. turn = 0

		3. Player:
			Attributes:
				a. name

	Services:
		1. GameManagerService
			Attributes:
				a. sessionIdToSessionObjDict = {}

			APIs:
				a. makeMove(sessionId)
				b. registerPlayer(playerObj)
"""
import random
from abc import ABC, abstractmethod


class Player:
	def __init__(self, name):
		self.name = name
		self.currrentCell = 0
		self.hasWon = False

	def setCurrentCell(self, cell):
		self.currrentCell = cell

	def setHasWon(self, hasWon):
		self.hasWon = hasWon

	def getName(self):
		return self.name

	def getCurrentCell(self):
		return self.currrentCell

	def getHasWon(self):
		return self.hasWon


class Board:
	def __init__(self, lastCell):
		self.lastCell = lastCell
		self.specialCellDictionary = {}

	def addSpecialCell(self, u, v):
		self.specialCellDictionary[u] = v

	def getLastCell(self):
		return self.lastCell

	def getSpecialCellDictionary(self):
		return self.specialCellDictionary


class Session:
	def __init__(self, sessionId):
		self.sessionId = sessionId
		self.playerList = []
		self.boardObj = None
		self.turn = 0

	def addPlayer(self, playerObj):
		self.playerList.append(playerObj)
		return self

	def setBoardObj(self, boardObj):
		self.boardObj = boardObj
		return self

	def incrementTurn(self):
		self.turn = (self.turn + 1) % len(self.playerList)

	def getCurrentPlayer(self):
		return self.playerList[self.turn]

	def getBoardObj(self):
		return self.boardObj


class AbstractGameManagerService(ABC):

	@abstractmethod
	def makeMove(self, sessionId):
		pass


# making this class a singleton since only one object is requried
class GameManagerService(AbstractGameManagerService):

	__instance = None
	__sessionIdToSessionObjDict = {}

	@staticmethod
	def getInstance():
		if GameManagerService.__instance is None:
			GameManagerService.__instance = GameManagerService()

		return GameManagerService.__instance

	def __init__(self):
		if GameManagerService.__instance is not None:
			raise Exception("Object already exists!")

		GameManagerService.__instance = self

	def rollDice(self):
		return random.randint(1, 6)

	def addSession(self, sessionId, sessionObj):
		GameManagerService.__sessionIdToSessionObjDict[sessionId] = sessionObj

	def makeMove(self, sessionId):

		if sessionId not in GameManagerService.__sessionIdToSessionObjDict:
			print("Invalid sesssion id")
			return

		sessionObj = GameManagerService.__sessionIdToSessionObjDict[sessionId]
		boardObj = sessionObj.getBoardObj()
		lastCell = boardObj.getLastCell()
		currentPlayer = sessionObj.getCurrentPlayer()

		if currentPlayer.getHasWon() is not True:
			currCell = currentPlayer.getCurrentCell()
			diceRoll = self.rollDice()

			if currCell + diceRoll <= lastCell:
				newCell = currCell + diceRoll
				currentPlayer.setCurrentCell(newCell)

				if newCell == lastCell:
					print(currentPlayer.getName(), "has won!")
					currentPlayer.setHasWon(True)
				else:
					print(currentPlayer.getName(), "moved from", currCell, "to", newCell)

		sessionObj.incrementTurn()


player1 = Player("Shubham")
player2 = Player("Shikha")
boardObj = Board(10)
sessionObj = Session(122)
sessionObj.addPlayer(player1).addPlayer(player2).setBoardObj(boardObj)
gameManagerService = GameManagerService()
gameManagerService.addSession(122, sessionObj)
for _ in range(30):
	gameManagerService.makeMove(122)
