"""
Tic-tac-toe OOD

1. Requirement gathering and use cases:
    
    1. Ask the user for the names of the two players
    2. Print the grid after initializing
    3. The user will make a move by entering the cell position.
    4. Player 1 is X and player 2 is O
    5. Valid move:
        put the piece on the cell
        print the board after the move
        Empty or non occupied move
    6. Invalid move
        print 'Invalid Move'
        the same player plays again in the next move

    7. Ending the game
        Either a player wins or match ties
        No moves to be accepted after this    


2. Identifying the entities and services:
    
    Entities
        1. User -> name, symbol
        2. Board -> n * n grid

    Services
        1. GameManager -> play(), findWinner(), validateMove()

3. Design ex: can something be singleton? Can we use factory pattern somewhere?

4. Refine
"""

from abc import ABC, abstractmethod

class User:

    def __init__(self,name):
        self.name = name

    def getName(self):
        return self.name


class Board:

    def __init__(self,size):
        self.size = size
        self.mat = []
        self.initializeMat()

    def initializeMat(self):

        self.mat = []

        for x in range(self.size):
            currRow = []
            for y in range(self.size):
                currRow.append(-1)
            self.mat.append(currRow)

    def getMat(self):
        return self.mat

    def getSize(self):
        return self.size

class AbstractGameManager(ABC):

    @abstractmethod
    def registerPlayer(self,number,name):
        pass

    @abstractmethod
    def printBoard(self,board):
        pass

    @abstractmethod
    def validateMove(self,i,j,board):
        pass

    @abstractmethod
    def findWinner(self,board):
        pass

    @abstractmethod
    def play(self,i,j,board):
        pass

# This class should be singleton
class GameManager(AbstractGameManager):

    flag = 0
    player1 = None
    player2 = None
    __instance = None

    def getInstance():
        if GameManager.__instance == None:
            GameManager.__instance = GameManager()

        return GameManager.__instance

    def __init__(self):
        if GameManager.__instance != None:
            raise Exception("Object already exists! Use getInstance method!")

    def registerPlayer(self,number,name):
        if number == 1:
            GameManager.player1 = User(name)

        elif number == 2:
            GameManager.player2 = User(name)

        else:
            print("Invalid input")


    def makeMove(self,i,j,board):
        
        if GameManager.flag % 2 == 0:
            sym = 'X'

        else:
            sym = 'O'

        board.getMat()[i][j] = sym
        GameManager.flag += 1

    def validateMove(self,i,j,board):

        if i < 0 or j < 0 or i >= len(board.mat) or j >= len(board.mat[0]) or  board.getMat()[i][j] != -1:
            return False

        return True

    def printBoard(self,board):

        for i in range(board.getSize()):
            currRow = []
            for j in range(board.getSize()):
                currRow.append(str(board.getMat()[i][j]))
            print(" ".join(currRow))
        print("----------------------------------")


    def findWinner(self,board):

        """
        Things to check
        1. All the rows
        2. All the cols
        3. Both the diagonals
        """

        allOccupied = True

        for i in range(len(board.getMat())):
            currRow = ""
            for j in range(len(board.getMat()[0])):
                currRow += str(board.getMat()[i][j])

                if board.getMat()[i][j] == -1:
                    allOccupied = False

            if currRow == 3*'X':
                return True,'X'

            elif currRow == 3*'O':
                return True,'O'


        for j in range(len(board.getMat()[0])):
            currCol = []
            for i in range(len(board.getMat())):

                currCol += str(board.getMat()[i][j])

            if currCol == 3*'X':
                return True,'X'

            elif currCol == 3*'O':
                return True,'O'

        if allOccupied == True:
            True,None

        # checking the principle diagonal
        index = 0
        principleDia = ""
        while index < board.getSize():
            principleDia += str(board.getMat()[index][index])
            index += 1

        if principleDia == 3*'X':
            return True,'X'

        elif principleDia == 3*'O':
            return True,'O'

        # checking the other dia
        i = 0
        j = board.getSize() - 1
        otherDia = ""

        while i < board.getSize() and j >= 0:

            otherDia += str(board.getMat()[i][j])
            i += 1
            j -= 1


        if otherDia == 3*'X':
            return True,'X'

        elif otherDia == 3*'O':
            return True,'O'

        return False,None

    def play(self,i,j,board):

        if GameManager.player1 == None or GameManager.player2 == None:
            print("Register players before playing!")
            return

        isValid = self.validateMove(i,j,board)

        if isValid == False:
            print("Invalid move!")
            return

        self.makeMove(i,j,board)
        self.printBoard(board)
        winnerFound,sym = self.findWinner(board)

        if winnerFound == True:

            if sym == None:
                print("It was a tie")

            elif sym == 'X':
                print(GameManager.player1.getName(),"won the match!")

            else:
                print(GameManager.player2.getName(),"won the match!")

            GameManager.flag = 0
            board.initializeMat()
            GameManager.player1 = None
            GameManager.player2 = None
            return


board = Board(3)
gameManager = GameManager()
gameManager.registerPlayer(1,"Shubham")
gameManager.registerPlayer(2,"Shikha")
gameManager.play(0,0,board)
gameManager.play(1,0,board)
gameManager.play(1,1,board)
gameManager.play(2,0,board)
gameManager.play(2,2,board)
gameManager.play(0,2,board)

# gameManager.registerPlayer(1,"Bart")
# gameManager.registerPlayer(2,"Homer")
# gameManager.play(0,0,board)
# gameManager.play(1,0,board)
# gameManager.play(0,1,board)
# gameManager.play(2,0,board)
# gameManager.play(0,2,board)
# gameManager.play(0,2,board)

# print(board.getMat())
