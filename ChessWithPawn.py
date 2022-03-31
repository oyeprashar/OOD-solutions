"""
Chess OOD with functionality of Pawn

1. Requirement gathering and use cases: (always ask questions and never assume!)
	
	How does a pawn move on the chess board?
		> If it is the first move of the game then pawn moves two step foward
		> If one step forward cell is blocked (by an alive piece) then the pawn cannot move
		> If there is some piece of opponent at one step forward dia right or left then pawn can move there and can capture that piece

	a. Chess board of n*n
	b. We need to implement the pawn for just now
	c. 2 player game, one takes white and other takes black colored pieces

2. Identifying the entities and services

	Entities
		a. Piece 
			Atrributes
				* type
				* alive
				* color

		b. board
			Attribute
				* size

		c. Player
			Attributes
				* name
				* color

	Services
		a. GameManager
			Methods
				+ play()
				+ registerPlayer()
				+ initializeGame()
				- validateMove()

3. Designing
4. Refining
"""

from abc import ABC, abstractmethod

class Piece:

	def __init__(self,alive,color):
		self.alive = alive
		self.color = color

# It makes sense to use inheritance because the child class will have multiple objects

class Pawn(Piece):

	def __init__(self,alive,color):
		super().__init__(alive,color)

	def isAlive(self):
		return self.isAlive

	def getColor(self):
		return self.color

class PieceFactory:
	__instance = None

	def getInstance():
		if PieceFactory.__instance == None:
			PieceFactory.__instance = PieceFactory()

		return PieceFactory.__instance

	def __init__(self):
		if PieceFactory.__instance != None:
			raise Exception("Object already exists! Use getInstance method!")

	def getPiece(self,type,color):

		if type == "pawn":
			return Pawn(True,color)

		else:
			print("No more pieces available!")
			return None


class Player:

	def __init__(self,name,color):
		self.name = name
		self.color = color

	def getName(self):
		return self.name

	def getColor(self):
		return self.color

	def getPos(self):
		return self.pos


class Board:
	def __init__(self,size):
		self.size = size
		self.grid = []
		self.initializeGrid()

	def getSize(self):
		return self.size

	def getGrid(self):
		return self.grid

	def initializeGrid(self):

		for x in range(self.size):
			currRow = []
			for y in range(self.size):
				currRow.append(-1)
			self.grid.append(currRow)

		self.populate()

	def populate(self):

		# white pawns are at row indexed 1
		# black pawns are at second last index

		pieceFactory = PieceFactory()

		for col in range(self.size):
			self.grid[1][col] = pieceFactory.getPiece("pawn","white")
			self.grid[self.size-2][col] = pieceFactory.getPiece("pawn","black")

class AbstractGameManager(ABC):

	@abstractmethod
	def play(self,i,j,board):
		pass

	@abstractmethod
	def registerPlayer(self,name,color):
		pass

	@abstractmethod
	def initializeGame(self):
		pass

	@abstractmethod
	def __validateMove(self,i,j):
		pass


# this can be singleton
class GameManager(AbstractGameManager):

	__instance = None

	def getInstance():
		if GameManager.__instance != None:
			GameManager.__instance = GameManager()

		return GameManager.__instance

	def __init__(self):

		if GameManager.__instance != None:
			raise Exception("Object already exists! Use getInstance method!")

		GameManager.__instance = self
		self.turn = 0
		self.colorToPlayerObj = {}

	def initializeGame(self):
		pass

	def registerPlayer(self,name,color):

		color = color.lower()

		if len(self.colorToPlayerObj) == 2:
			print("2 players already registered!")
			return

		elif color != "black" and color != "white":
			print("Choose from black or white")
			return

		elif color in self.colorToPlayerObj:
			print("Color already choosen!")
			return

		self.colorToPlayerObj[color] = Player(name,color)

	def __validateCurrentCell(self,currPlayerColor,i,j,board):

		if i < 0 or j < 0 or i >= board.getSize() or j >= board.getSize():
			return False

		if board.getGrid()[i][j] == -1 or board.getGrid()[i][j].getColor() != currPlayerColor:
			return False

		return True

	def __validateMove(self,fromRow,fromCol,toRow,toCol,currPlayerColor,board):

		"""
		We just need to validate the move and not move it ourselves

		Invalid Moves
			1. User is tring to take jump of more than 1 and user cannot move backwards
			1. User wants to move to diagonal cell but there are no opponents there! 
			2. User tried to move to an occupied cell

		Valid Moves:
			1. If not invalid then its valid
		"""

		if currPlayerColor == "white":

			# more than one jump
			if toRow < fromRow or toRow - fromRow > 1 or abs(toCol - fromCol) > 1 or toRow == fromRow:
				return False

			# validating the forward move
			elif toRow == fromRow + 1 and toCol == fromCol and board.getGrid()[toRow][toCol] != -1:
				return False

			# validating the diagonal move
			elif ((toRow == fromRow +1 and toCol == fromCol -1) or (toRow == fromRow +1 and toCol == fromCol + 1)) and (board.getGrid()[toRow][toCol] == -1 or board.getGrid()[toRow][toCol].getColor() == currPlayerColor):
				return False

		elif currPlayerColor == "black":

			# more than one jump
			if toRow > fromRow or toRow - fromRow > 1 or abs(toCol - fromCol) > 1 or toRow == fromRow:
				return False

			# validating the forward move
			elif toRow == fromRow - 1 and toCol == fromCol and board.getGrid()[toRow][toCol] != -1:
				return False

			# validating the diagonal move
			elif ((toRow == fromRow - 1 and toCol == fromCol - 1) or (toRow == fromRow - 1 and toCol == fromCol + 1)) and (board.getGrid()[toRow][toCol] == -1 or board.getGrid()[toRow][toCol].getColor() == currPlayerColor):
				return False

		return True

	def __move(self,fromRow,fromCol,toRow,toCol,board):

		currPiece = board.getGrid()[fromRow][fromCol]

		# remove the piece from old pos
		board.getGrid()[fromRow][fromCol] = -1

		# putting it to the new pos
		board.getGrid()[toRow][toRow] = currPiece

	def play(self,fromRow,fromCol,toRow,toCol,board):
		
		"""
		1. We need to validate the fromRow and frowCol
		2. Then we need to validate toRow and toCol
		3. Then we move
		"""

		if self.turn == 0:
			currPlayer = self.colorToPlayerObj["white"]

		else:
			currPlayer = self.colorToPlayerObj["black"]


		if self.__validateCurrentCell(currPlayer.getColor(),fromRow,fromCol,board) == False or self.__validateMove(fromRow,fromCol,toRow,toCol,currPlayer.getColor(),board) == False:
			print("Invalid move!")
			return

		self.__move(fromRow,fromCol,toRow,toCol,board)
		self.turn = (self.turn + 1) % 2


board = Board(8)
gameManager = GameManager()
gameManager.registerPlayer("Shubham","white")
gameManager.registerPlayer("Shikha","Black")
gameManager.play(1,0,2,0,board)
# gameManager.play(1,0,2,0,board)
gameManager.play(2,2,3,3,board)
