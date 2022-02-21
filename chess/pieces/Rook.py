from numpy import block
from .piece import Piece

class Rook(Piece):

    def calculateMovement(self, start, board):
        movements = set()
        for i in range(0, len(board.board)): #Mouvements horizontaux
            if i!= start[0]:
                movements.add((i, start[1]))
            for j in range(0, len(board.board[start[0]])):
                if j != start[1]:
                    movements.add((start[0], j))
        
        return movements

    def checkObstacles(self, options, board):
        """Check if there are obstacles between the pawn and the option

        Args:
            options ([(x,y)]): options (movements) which will be checked
            board (pygame.Surface): _description_

        Returns:
            ([(x,y)]): Movements which are blocked by an obstacle. 
        """
        optionsBlocked = []
        for movement in options:
            verticalPartition = self.checkIfPieceIsInTheWayVertically(movement, board)
            horizontalPartition = self.checkIfPieceIsInTheWayHorizontally(movement, board)
            if verticalPartition != [] or horizontalPartition != []:
                self.ennemyInFrontOfMe = True
                #On bloque le chemin jusqu'à l'option
                optionsBlocked.append(movement)
        return optionsBlocked
            

    def checkAfterEveryOptionForEnnemy(self, board):
        optionsToCheck = self.options["end"]

        start = self.options["start"]
        optionsToAdd = []
        for option in optionsToCheck:
            x = option[0]
            y = option[1]
            upPiece = board.board[x][y-1 if y-1 >= 0 else 0]
            downPiece = board.board[x][y+1 if y+1 < len(board.board[x]) else len(board.board[x])-1]
            leftPiece = board.board[x-1 if x-1 >=0 else 0][y]
            rightPiece = board.board[x+1 if x+1 < len(board.board) else len(board.board)-1][y]
            print('')
            if(start[0] > x):
                if(rightPiece != 0 and rightPiece.color != self.color):
                    optionsToAdd.append((x+1, y))
            elif(start[0] < x):
                if(leftPiece != 0 and leftPiece.color != self.color):
                    optionsToAdd.append((x-1, y))
            elif(start[1] > y):
                if(upPiece != 0 and upPiece.color != self.color):
                    optionsToAdd.append((x, y-1))
            elif(start[1] < y):
                if(downPiece != 0 and downPiece.color != self.color):
                    optionsToAdd.appen((x, y+1))

        for option in optionsToAdd:
            self.options["end"].add(option)

    def drawOption(self, option, board, pieceSize):
        """Draw a point for an option

        Args:
            option (x,y): The option we will point.
            board (_type_): _description_
            pieceSize (int): _description_
        """
        self.drawPoint(board.screen,(0,0,0), self.pixelizePosition(option, pieceSize))



    def calculateOptions(self, board, pos):
        pieceSize = board.screen.get_size()[0]/8                    #On récupère la taille d'une pièce via : La taille de l'écran divisé par le nombre de pièces
        x = int(pos[0]/pieceSize)                                   #Permet de récupérer l'indice du pion dans le board. Le x et y dans board.y avancent par pieceSize dans la boucle
        y = int(pos[1]/pieceSize)
        start = pos
        start = (x*pieceSize+pieceSize/2, y*pieceSize+pieceSize/2)  # x*pieceSize : permet de récupérer la case, +pieceSize/2 -> d'aller au centre de celle ci
        self.options["start"] = (int(start[0]/pieceSize), int(start[1]/pieceSize))

        #On calcule les options possibles
        movements = self.calculateMovement(board.getPositionOfClick(pos), board)
        print('movements ', movements)
        #On regarde les obstacles
        blockedMovements = self.checkObstacles(movements, board)
        print('blockedMovements : ', blockedMovements)
        #On élimine les options impossibles 
        for movement in movements:
            if movement not in blockedMovements:
                self.options["end"].add(movement)


        self.checkAfterEveryOptionForEnnemy(board)

        print('options Before Drawing', self.options)
        #On dessine les options
        for option in self.options["end"]:
            self.drawOption(option, board, pieceSize)

        # #On retire les movements ou il y a une pièce (non tuable) dans l'option
        # freeMovements = []
        # for movement in movements:
        #     if self.checkIfEnnemyInOptions(movement, board) == False:
        #         freeMovements.append(movement)
        
        

        # #On regarde si il y un ennemi tuable
        # self.optionsIfCanKill(board, (x,y))                         #On rajoute dans les options, les pièces tuables par le pion


        
