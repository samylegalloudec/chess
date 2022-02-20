from .piece import Piece

class Rook(Piece):

    def move():
        print('todo')

    def showOptions(self, board, pos):
        self.calculateOptions(board, pos)

    def calculateOptions(self, board, pos):
        x = int(pos[0]/150) #Permet de récupérer l'indice du pion dans le board. Le x et y dans board.y avancent par 150 dans la boucle
        y = int(pos[1]/150)
        print(pos)
