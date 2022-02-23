from shutil import move
from .piece import Piece

class Bishop(Piece):
    def move(self):
        print('todo')


    def calculateMovement(self, start, board):
        movements = []
        blockedBySomethingBottomRight = False
        blockedBySomethingBottomLeft = False
        firstCaseToCheck = start[1]+1 if start[1]+1 <=7 else 7
        for i in range(firstCaseToCheck, 7):
            bottomRightPosition = (start[0]+i, i)
            bottomLeftPosition = (start[0]-i, i)
            if bottomRightPosition[0] <= 7:
                if board.getPieceAtPosition(bottomRightPosition) == 0 and blockedBySomethingBottomRight==False:
                    movements.append(((start[0]+i, i)))
                elif board.getPieceAtPosition(bottomRightPosition) !=0 and blockedBySomethingBottomRight==False :
                    if board.getPieceAtPosition(bottomRightPosition).color != self.color:
                        movements.append(bottomRightPosition)
                        blockedBySomethingBottomRight=True
                    else:
                        blockedBySomethingBottomRight=True
                    

            if bottomLeftPosition[0] >= 0:
                if board.getPieceAtPosition(bottomLeftPosition) == 0 and blockedBySomethingBottomLeft==False:
                    movements.append(bottomLeftPosition)
                elif board.getPieceAtPosition(bottomLeftPosition) !=0 and blockedBySomethingBottomLeft==False :
                    if board.getPieceAtPosition(bottomLeftPosition).color != self.color:
                        movements.append(bottomLeftPosition)
                        blockedBySomethingBottomLeft=True
                    else:
                        blockedBySomethingBottomLeft=True

        blockedBySomethingTopRight = False
        blockedBySomethingTopLeft = False
        for i in range(1, start[1]-1):
            topRightPosition = (start[0]+i, start[1]-i)
            topLeftPosition = (start[0]-i, start[1]-i)
            if topRightPosition[0] <= 7:
                if board.getPieceAtPosition(topRightPosition) == 0 and blockedBySomethingTopRight==False:
                    movements.append(topRightPosition)
                elif board.getPieceAtPosition(topRightPosition) !=0 and blockedBySomethingTopRight==False :
                    if board.getPieceAtPosition(topRightPosition).color != self.color:
                        movements.append(topRightPosition)
                        blockedBySomethingTopRight=True
                    else:
                        blockedBySomethingTopRight=True
            
            if topLeftPosition[0] >= 0:
                if board.getPieceAtPosition(topLeftPosition) == 0 and blockedBySomethingTopLeft==False:
                    movements.append(topLeftPosition)
                elif board.getPieceAtPosition(topLeftPosition) !=0 and blockedBySomethingTopLeft==False :
                    if board.getPieceAtPosition(topLeftPosition).color != self.color:
                        movements.append(topLeftPosition)
                        blockedBySomethingTopLeft=True
                    else:
                        blockedBySomethingTopLeft=True
        
        return movements

    def drawOption(self, option, board, pieceSize):
        """Draw a point for an option

        Args:
            option (x,y): The option we will point.
            board (_type_): _description_
            pieceSize (int): _description_
        """
        self.drawPoint(board.screen,(30,30,30), self.pixelizePosition(option, pieceSize))

    def calculateOptions(self, board, pos):
        pieceSize = board.screen.get_size()[0]/8                    #On récupère la taille d'une pièce via : La taille de l'écran divisé par le nombre de pièces
        x = int(pos[0]/pieceSize)                                   #Permet de récupérer l'indice du pion dans le board. Le x et y dans board.y avancent par pieceSize dans la boucle
        y = int(pos[1]/pieceSize)
        start = pos
        start = (x*pieceSize+pieceSize/2, y*pieceSize+pieceSize/2)  # x*pieceSize : permet de récupérer la case, +pieceSize/2 -> d'aller au centre de celle ci
        self.options["start"] = (int(start[0]/pieceSize), int(start[1]/pieceSize))

        #Calculer les options possibles
        movements = self.calculateMovement(board.getPositionOfClick(start), board)

        for movement in movements:
            self.options["end"].add(movement)
            self.drawOption(movement, board, self.BLOCKSIZE)
