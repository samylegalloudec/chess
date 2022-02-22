from .piece import Piece

class Knight(Piece):
    def move(self):
        print('todo')

    def calculateMovement(self, start, board):
        movements = set()
        print('start : ,' ,start)
        x = start[0]
        y = start[1]
        movements.add((x-2, y-1))
        movements.add((x-2, y+1))
        movements.add((x-1, y-2))
        movements.add((x-1,y+2))
        movements.add((x+1, y-2))
        movements.add((x+1,y+2))
        movements.add((x+2, y-1))
        movements.add((x+2, y+1))
        return movements
        #Mouvements de gauche à droite : (x-2, y-1), (x-2, y+1) -> (x-1, y-2), (x-1,y+2) -> (x+1, y-2), (x+1,y+2) > (x+2, y-1), (x+2, y+1)

    def checkIfAllyInOptions(self, options, board):
        blockedMovements = []
        for option in options:
            targettedPiece=board.board[option[0]][option[1]]
            if(targettedPiece != 0 and self.color==targettedPiece.color):
                blockedMovements.append(option)

        return blockedMovements

    def drawOption(self, option, board, pieceSize):
        """Draw a point for an option

        Args:
            option (x,y): The option we will point.
            board (_type_): _description_
            pieceSize (int): _description_
        """
        self.drawPoint(board.screen,(30,30,30), self.pixelizePosition(option, pieceSize))

    def calculateOptions(self, board, pos):
        print('todo')

        pieceSize = board.screen.get_size()[0]/8                    #On récupère la taille d'une pièce via : La taille de l'écran divisé par le nombre de pièces
        x = int(pos[0]/pieceSize)                                   #Permet de récupérer l'indice du pion dans le board. Le x et y dans board.y avancent par pieceSize dans la boucle
        y = int(pos[1]/pieceSize)
        start = pos
        start = (x*pieceSize+pieceSize/2, y*pieceSize+pieceSize/2)  # x*pieceSize : permet de récupérer la case, +pieceSize/2 -> d'aller au centre de celle ci
        self.options["start"] = (int(start[0]/pieceSize), int(start[1]/pieceSize))

        #Calculer les options possibles
        movements = self.calculateMovement(board.getPositionOfClick(start), board)
        #Retirer celles qui ne sont pas sur le plateau
        outOfMapMovements = self.checkIfMovementsAreOutOfMap(movements)

        allowedMovements = []
        for movement in movements:
            if movement not in outOfMapMovements:
                allowedMovements.append(movement)
        #Retirer celles ou il y a des pions ALLIES
        blockedByAlliesMovements = self.checkIfAllyInOptions(allowedMovements, board)
        
        #Draw
        for option in allowedMovements:
            if option not in blockedByAlliesMovements:
                self.options["end"].add(option)
                self.drawOption(option, board, self.BLOCKSIZE)
        
