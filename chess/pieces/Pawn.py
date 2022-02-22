import secrets
from tkinter import Toplevel
from .piece import Piece

#Peut avancer de 2 cases devant lui au premier tour, sinon 1 case devant lui uniquement.
class Pawn(Piece):

    def __init__(self, image, color):
        super().__init__(image, color)
        self.first_round = True
        self.ennemyInFrontOfMe = False

    def move(self):
        self.first_round = False
        self.options["end"] = set()


    
    def optionsIfCanKill(self, board, pos):
        """Return options (position of ennemy) if the pawn can kill an ennemy.

        Args:
            pos (x,y): The current position of the pawn
            board (pygame.surface): The current board of the game
        """
        x = pos[0]
        y = pos[1]
        if self.color == 0:
            topRightPos = (x+1 if x+1<=7 else 7, y+1 if y+1 <=7 else 7)
            topLeftPos = (x-1 if x-1 >=0 else 0, y+1 if y+1 <=7 else 7)
            topLeft = board.board[topLeftPos[0]][topLeftPos[1]]
            topRight = board.board[topRightPos[0]][topRightPos[1]]
            if(topLeft!=0):
                if(topLeft.color != self.color):
                    self.options["end"].add(topLeftPos)
            if(topRight!=0):
                if(topRight.color != self.color):
                    self.options["end"].add(topRightPos)
        else:
            topLeftPos = (x+1 if x+1 <= 7 else 7,y-1 if y-1 >=0 else 0)
            topRightPos = (x-1 if x-1 >=0 else 0, y-1 if y-1 >=0 else 0)
            topLeft = board.board[topLeftPos[0]][topLeftPos[1]]
            topRight = board.board[topRightPos[0]][topRightPos[1]]
            if(topLeft!=0):
                if(topLeft.color != self.color):
                    self.options["end"].add(topLeftPos)
            if(topRight!=0):
                if(topRight.color != self.color):
                    self.options["end"].add(topRightPos)
            


    def calculateMovement(self,start,pieceSize):
        """Calculate all possible movements (except killing)

        Args:
            start (x,y): Position of the pawn
            pieceSize (_type_): Size of a piece in our board. Esthetic.

        Returns:
            [(x,y)]: An array of options for movements
        """
        movements = []
        if(self.first_round):
            if(self.color==0):
                end = (start[0], start[1]+pieceSize)
                secondEnd = (start[0], start[1]+pieceSize*2)
            else:
                end = (start[0], start[1]-pieceSize)
                secondEnd = (start[0], start[1]-pieceSize*2)
            firstOption = (int(end[0]/pieceSize), int(end[1]/pieceSize))
            secondOption = (int(secondEnd[0]/pieceSize), int(secondEnd[1]/pieceSize))
            movements.append(firstOption)
            movements.append(secondOption)
        else:
            if(self.color==0):
                end = (start[0], start[1]+pieceSize)
            else:
                end = (start[0], start[1]-pieceSize)
            firstOption = (int(end[0]/pieceSize), int(end[1]/pieceSize))
            movements.append(firstOption)
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
            partition = self.checkIfEnnemyIsInTheWayVertically(movement, board)
            if partition != []:
                self.ennemyInFrontOfMe = True
                if(self.color==0):
                    optionsBlocked.append((movement[0], movement[1]-1)) ##On bloque le chemin jusqu'à l'option
                    optionsBlocked.append(movement)
                else:
                    optionsBlocked.append((movement[0], movement[1]+1))
                    optionsBlocked.append(movement)
        return optionsBlocked

    def drawOption(self, option, board, pieceSize):
        """Draw an arrow for an option

        Args:
            option (x,y): The option we will point with the arrow
            board (_type_): _description_
            pieceSize (int): _description_
        """
        start = self.options["start"]
        start = self.pixelizePosition(start, pieceSize)
        self.drawArrow(board.screen,(0,0,0), start, self.pixelizePosition(option, pieceSize))

    def calculateOptions(self, board, pos): #TODO : à terme, empêcher de libérer le roi.
        """Calculate all options for the pawn
        Args:
            board (pygame.surface): The current board of the game
            pos (x,y): The position in PIXELS
        """
        pieceSize = board.screen.get_size()[0]/8                    #On récupère la taille d'une pièce via : La taille de l'écran divisé par le nombre de pièces
        x = int(pos[0]/pieceSize)                                   #Permet de récupérer l'indice du pion dans le board. Le x et y dans board.y avancent par pieceSize dans la boucle
        y = int(pos[1]/pieceSize)
        start = pos
        start = (x*pieceSize+pieceSize/2, y*pieceSize+pieceSize/2)  # x*pieceSize : permet de récupérer la case, +pieceSize/2 -> d'aller au centre de celle ci
        self.options["start"] = (int(start[0]/pieceSize), int(start[1]/pieceSize))
        
        
        #On calcule les options possibles
        movements = self.calculateMovement(start, pieceSize)

        #On retire les movements ou il y a une pièce (non tuable) dans l'option
        freeMovements = []
        for movement in movements:
            if self.checkIfEnnemyInOptions(movement, board) == False:
                freeMovements.append(movement)
        
        #On regarde les obstacles
        blockedMovements = self.checkObstacles(freeMovements, board)
        #On élimine les options impossibles 
        for movement in freeMovements:
            if movement not in blockedMovements:
                self.options["end"].add(movement)

        #On regarde si il y un ennemi tuable
        self.optionsIfCanKill(board, (x,y))                         #On rajoute dans les options, les pièces tuables par le pion


        print('options before draw : ', self.options["end"])
        #On dessine les options
        for option in self.options["end"]:
            self.drawOption(option, board, pieceSize)



    # def calculateOptionsBis(self, board, pos):
    #     """Calculate all options for the pawn :
    #     - First round, he can move forward 2 rows
    #     - Other rounds, only 1 row
    #     - He can kill ennemy on his top left and top right

    #     Args:
    #         board (pygame.surface): The current board of the game
    #         pos (x,y): The position in PIXELS
    #     """
    #     pieceSize = pieceSize
    #     x = int(pos[0]/pieceSize) #Permet de récupérer l'indice du pion dans le board. Le x et y dans board.y avancent par pieceSize dans la boucle
    #     y = int(pos[1]/pieceSize)
    #     start = pos
    #     start = (x*pieceSize+pieceSize/2, y*pieceSize+pieceSize/2) # x*pieceSize : permet de récupérer la case, +pieceSize/2 -> d'aller au centre de celle ci
    #     self.options["start"] = (int(start[0]/pieceSize), int(start[1]/pieceSize))
    #     self.optionsIfCanKill(board, (x,y))

    #     if(len(self.options["end"]) != 0):
    #         for option in self.options["end"]:
    #             self.drawArrow(board.screen,(0,0,0), start, self.pixelizePosition(option, pieceSize/2))

    #     if self.first_round:
    #         if self.color == 0:
    #             end = (start[0], start[1]+pieceSize)
    #             secondEnd = (start[0], start[1]+pieceSize*2)

    #             options = []

    #             firstOption = (int(end[0]/pieceSize), int(end[1]/pieceSize))
    #             secondOption = (int(secondEnd[0]/pieceSize), int(secondEnd[1]/pieceSize))

    #             options.append(firstOption)
    #             options.append(secondOption)
    #             for option in options:
    #                 partition = self.checkIfEnnemyIsInTheWay(option, board)
    #                 if partition != []:
    #                     self.ennemyInFrontOfMe = True
    #                 if not(self.checkIfEnnemyInOptions(option, board)) and not self.ennemyInFrontOfMe:
    #                     self.drawArrow(board.screen,(0,0,0), start, self.pixelizePosition(option, pieceSize/2))
                

    #             self.options["end"].add(firstOption)
    #             self.options["end"].add(secondOption)


    #             #  secondEnd)
    #             # self.drawArrow(board.screen,(50,50,50), start, end)

                
    #         else:
    #             end = (start[0], start[1]-pieceSize)
    #             secondEnd = (start[0], start[1]-pieceSize*2)
    #             # self.drawArrow(board.screen,(0,0,0), start, secondEnd)
    #             # self.drawArrow(board.screen,(50,50,50), start, end)

    #             options = []

    #             firstOption = (int(end[0]/pieceSize), int(end[1]/pieceSize))
    #             secondOption = (int(secondEnd[0]/pieceSize), int(secondEnd[1]/pieceSize))

    #             options.append(firstOption)
    #             options.append(secondOption)
    #             for option in options:
    #                 partition = self.checkIfEnnemyIsInTheWay(option, board)
    #                 if partition != []:
    #                     self.ennemyInFrontOfMe = True
    #                 if not(self.checkIfEnnemyInOptions(option, board)) and not(self.ennemyInFrontOfMe):
    #                     self.drawArrow(board.screen,(0,0,0), start, self.pixelizePosition(option, pieceSize/2))

                
    #             self.options["end"].add(firstOption)
    #             self.options["end"].add(secondOption)
    #     else:
    #         if self.color == 0:
    #             end = (start[0], start[1]+pieceSize)
                
    #             # self.drawArrow(board.screen,(50,50,50), start, end)

    #             options = []

    #             firstOption = (int(end[0]/pieceSize), int(end[1]/pieceSize))

    #             options.append(firstOption)
    #             for option in options:
    #                 partition = self.checkIfEnnemyIsInTheWay(option, board)
    #                 if partition != []:
    #                     self.ennemyInFrontOfMe = True
    #                 if self.checkIfEnnemyInOptions(option, board) == False and self.ennemyInFrontOfMe==False:
    #                     self.drawArrow(board.screen,(0,0,0), start, self.pixelizePosition(option, pieceSize/2))

    #             self.options["end"].add(firstOption)
    #         else:
    #             end = (start[0], start[1]-pieceSize)
    #             # self.drawArrow(board.screen,(50,50,50), start, end)
                
    #             options = []

    #             firstOption = (int(end[0]/pieceSize), int(end[1]/pieceSize))

    #             options.append(firstOption)
    #             for option in options:
    #                 partition = self.checkIfEnnemyIsInTheWay(option, board)
    #                 if partition != []:
    #                     self.ennemyInFrontOfMe = True
    #                 if not(self.checkIfEnnemyInOptions(option, board)) and not(self.ennemyInFrontOfMe):
    #                     self.drawArrow(board.screen,(0,0,0), start, self.pixelizePosition(option,pieceSize/2))

    #             self.options["end"].add(firstOption)
        

                