class User:
	def __init__(self, name):
		self.name = name

	def getName(self):
		return self.name


class Board:
	def __init__(self, size):
		self.size = size
		self.grid = []
		self.initializeBoard()

	def initializeBoard(self):
		for i in range(self.size):
			currRow = []
			for j in range(self.size):
				currRow.append("EMPTY")
			self.grid.append(currRow)


class Session:

	def __init__(self, sessionId):
		self.sessionId = sessionId
		self.playerList = []
		self.turn = 0
		self.board = None
		self.gameOver = False

	def setGameOver(self, isGameOver):
		self.gameOver = isGameOver

	def addBoard(self, size):
		self.board = Board(size)

	def addPlayer(self, playerObj):
		if len(self.playerList) == 2:
			print("Two players already registered!")
			return

		self.playerList.append(playerObj)
		print("Player registered successfully!")

	def setTurn(self, turn):
		self.turn = turn

	def isGameOver(self):
		return self.gameOver

	def getPlayer(self, turn):
		return self.playerList[turn]

	def getBoard(self):
		return self.board

	def getTurn(self):
		return self.turn


class GameManagerService:

	def __init__(self):
		self.sessionIdToObject = {}

	def isValidMove(self, i, j, boardObj):
		pass

	def hasCurrentPlayerWon(self, boardObj):
		return True
		pass

	def makeMove(self, i, j, sessionId):

		if sessionId not in self.sessionIdToObject:
			print("Invalid session id!")
			return

		sessionObj = self.sessionIdToObject[sessionId]
		
		if sessionObj.isGameOver() is True:
			print("Game is already over!")
			return
		
		boardObj = sessionObj.getBoard()
		currTurn = sessionObj.getTurn()
		currPlayer = sessionObj.getPlayer(currTurn)
		sessionObj.setTurn((currTurn + 1) % 2)

		if currTurn == 0:
			symbol = 'X'
		else:
			symbol = 'O'

		if self.isValidMove(i, j, boardObj):
			grid = boardObj.getGrid()
			grid[i][j] = symbol

			hasWon = self.hasCurrentPlayerWon(boardObj)

			if hasWon is True:
				sessionObj.setGameOver(True)
				print(currPlayer.getName(), "has won the game!")
				
