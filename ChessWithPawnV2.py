"""
1. Requirement gathering and use cases

	- The chess board have multiple types of pices eight pawns, two bishops, two knights, two rooks, one queen, and one king
	- We will put all the pieces at their respective places
	- Only the functionality of the pawns will be implemented

	How Pawn moves:
		1. if left diagonal and right diagonal is empty (or occupied by the same color) then the pawn can moves straight and moving to the diagonal is invalid
		2. Can move one step to the left and the right diagonal if left or the right dia is occupied by the other color

	How a player moves their piece?
		1. Choose a piece at a position --> i,j
		2. Choose a destination for this piece --> p,q

 
2. Identifying the entities and services
	
	Entities
		a. Piece
			+ color

		b. Player
			+ name
			+ collectedPieces
			+ reset()

		c. Board
			+ size
			+ resetPieces()


	Services
		a. GameProcessor
			+ move(self,i,j,p,q)
			- isValidMove(self,i,j,p,q)

3. Design
4. Refine
"""

from abc import ABC, abstractmethod

class ChessPiece:

	def __init__(self,color):
		self.color = color

	def getColor(self):
		return self.color

class Pawn(ChessPiece):

	def __init__(self,color):
		ChessPiece.__init__(self,color)

class Bishop(ChessPiece):

	def __init__(self,color):
		ChessPiece.__init__(self,color)

class Knight(ChessPiece):

	def __init__(self,color):
		ChessPiece.__init__(self,color)

class Rook(ChessPiece):

	def __init__(self,color):
		ChessPiece.__init__(self,color)

class Queen(ChessPiece):

	def __init__(self,color):
		ChessPiece.__init__(self,color)

class King(ChessPiece):

	def __init__(self,color):
		ChessPiece.__init__(self,color)

class PieceFactory:

	def getPiece(type,color):

		type = type.lower()

		if type == "pawn":
			return Pawn(color)

		elif type == "bishop":
			return Bishop(color)

		elif type == "knight":
			return Knight(color)

		elif type == "rook":
			return Rook(color)
		
		elif type == "queen":
			return Queen(color)

		elif type == "king":
			return King(color)

		else:
			print("Invalid type")

class Player:

	def __init__(self,name,color):
		self.name = name
		self.color = color
		self.collectedPieces = []

	def getName(self):
		return self.name

	def getColor(self):
		return self.color

	def getCollectedPieces(self):
		return self.collectedPieces

	def addCollectedPiece(self,pieceObj):
		self.collectedPieces.append(pieceObj)

	def reset(self):
		self.collectedPieces = []


class Board:

	def __init__(self,size):
		self.size = size
		self.grid = []
		self.resetBoard()

	def getSize(self):
		return self.size

	def getGrid(self):
		return self.grid
		
	def resetBoard(self):

		for i in range(self.size):
			currRow = []

			for j in range(self.size):

				if i == 1:
					currRow.append(PieceFactory.getPiece("pawn","black"))

				elif i == self.size - 2:
					currRow.append(PieceFactory.getPiece("pawn","white"))

			self.grid.append(currRow)



class AbstractGameProcessor(ABC):

	@abstractmethod
	def move(i,j,p,q):
		pass

# this should be singleton
class ChessGameProcessor(AbstractGameProcessor):

	__instance = None
	boardObj = None
	players = [None,None]
	count = 0

	def getInstance():
		if ChessGameProcessor.__instance == None:
			ChessGameProcessor.__instance = ChessGameProcessor()

		return ChessGameProcessor.__instance

	def registerBoard(self,boardObj):
		ChessGameProcessor.boardObj = boardObj

	def registerPlayers(self,name,color):

		color = color.lower()

		if (color == "black" and ChessGameProcessor.players[0] != None) or (color == "white" and ChessGameProcessor.players[1] != None):
			print(color,"already choosen!")
			return

		currPlayer = Player(name,color)

		if color == "black":
			ChessGameProcessor.players[0] = currPlayer

		elif color == "white":
			ChessGameProcessor.players[1] = currPlayer

		else:
			print("Invalid color selection")

	def validatePieceMove(self,i,j,p,q,piece,currPlayer):

		if isinstance(piece,Pawn):

			# checking if the move is forward
			if p = i + 1 and q = j:
				if ChessGameProcessor.boardObj.getGrid()[p][q] != None:
					return False

				else:
					return True

			# checking for diagonal moves
			elif (p = i + 1 and q = j - 1) or (p = i + 1 and q = j + 1) :

				if ChessGameProcessor.boardObj.getGrid()[p][q] == None:
					return True

				else:
					if ChessGameProcessor.boardObj.getGrid()[p][q].getColor() == currPlayer.getColor():
						return False

					else:
						return True

	def isValid(self,i,j,p,q,currPlayer):


		size = ChessGameProcessor.boardObj.getSize()

		if i < 0 or j < 0 or p < 0 or q < 0 or i >= size or j >= size or p >= size or q >= size:
			return False

		if ChessGameProcessor.boardObj == None :
			print("No board registered!")
			return

		if ChessGameProcessor.boardObj.getGrid()[i][j] == None:
			return False

		if ChessGameProcessor.boardObj.getGrid()[i][j].getColor() != currPlayer.getColor():
			return False

		if ChessGameProcessor.validatePieceMove(i,j,p,q,ChessGameProcessor.boardObj.getGrid()[i][j],currPlayer) == False:
			return False

		return True

	def move(i,j,p,q):

		if ChessGameProcessor.players[0] == None or  ChessGameProcessor.players[1] == None:
			print("Register players first")
			return

		currPlayer = self.players[self.count]

		if self.isValid(i,j,p,q,currPlayer) == True:

			piece = self.boardObj.getGrid()[i][j]
			currPlayer.addCollectedPiece(piece)
			ChessGameProcessor.boardObj.getGrid()[i][j] = None
			ChessGameProcessor.boardObj.getGrid()[p][q] = piece

			ChessGameProcessor.count = (ChessGameProcessor.count + 1) % 2

		else:
			print("Invalid move! Try again!")

	def reset(self):
		ChessGameProcessor.boardObj.reset()
		ChessGameProcessor.players = None
		ChessGameProcessor.count = 0
