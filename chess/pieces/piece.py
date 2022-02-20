from tarfile import BLOCKSIZE
from turtle import pos
import pygame
import math

size = width, height = 1200, 1200

#from main import screen
class Piece(pygame.sprite.Sprite):
    def __init__(self, image, color):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.color = color #0 = white, 1 = black
        self.optionsShowed = False
        # self.rect.x = position.x
        # self.rect.y = position.y
        self.screen = pygame.display.set_mode(size) #Todo : Rendre ça + beau
        self.size = self.screen.get_size()
        self.width = self.size[0]
        self.height = self.size[1]
        self.BLOCKSIZE = self.width/8
        self.options = {
            "start":(),
            "end":set()
        }

    def update_position(self, x, y):
        print('updating piece to x: ', x, ' y:', y)
        self.rect.x = self.rect.x + x
        self.rect.y = self.rect.y + y

    def set_position(self, x, y):
        #print('setting piece to x: ', x, ' y:', y)
        self.rect.x =  x
        self.rect.y =  y

    def getOptions(self):
        return self.options

    def get_position(self):
        return(int(self.rect.x/self.BLOCKSIZE), int(self.rect.y/self.BLOCKSIZE))

    def update(self, event_list, board):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos): 
                    if(self.optionsShowed==False):
                        self.showOptions(board, event.pos)
                    elif(self.optionsShowed==True):
                        self.hideOptions(board)
                        self.options["end"] = set()
                else:
                    if(self.optionsShowed==True):
                        #get where it got clicked
                        (x,y) = board.getPositionOfClick(event.pos)
                        (oldX, oldY) = self.get_position()
                        (boardX, boardY) = (x, y)
                        print(boardX, boardY)
                        #on check si on peut se déplacer
                        print("x, y", x, y)
                        if((x,y) in self.options["end"]):
                            if(x==oldX):
                                board.board[x] = self.swapPositions(board.board[x], oldY,y)
                            else:
                                oldElem = board.board[oldX][oldY]
                                newElem = board.board[x][y]
                                board.board[oldX][oldY] = newElem
                                board.board[x][y] = oldElem
                            self.move()
                        else:
                            self.options["end"] = set()

                        
                        board.reDrawBoard()

    def swapPositions(self, list, pos1, pos2):     
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list
    
    def checkIfEnnemyIsInTheWay(self, option, board):
        """Check if an ennemy is between the piece and the option chose

        Args:
            position (x,y): The position of the piece
            option (x,y): The position of the option
            board (pygame.Surface): The current board of the game
            
        """
        position = self.options["start"]
        x = position[0]
        y = position[1]
        print('self.options', self.options)
        if(self.color==0):
            print('y+1 : ', y+1)
            print('option[1]', option[1])
            partition = board.board[x][y+1:option[1]]
            ennemyPresent = False
            for element in partition:
                if element != 0:
                    ennemyPresent = True
            if ennemyPresent:
                return partition
        else:
            print('option[1]+1 : ', option[1]+1)
            print('y ' , y)
            partition = board.board[x][option[1]:y]
            ennemyPresent = False
            for element in partition:
                if element != 0:
                    ennemyPresent = True
            if ennemyPresent:
                return partition
        
        return []
            

    def partitionList(self,alist, indices):
        return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

    def drawArrow(self,screen, colour, start, end):
        pygame.draw.line(screen,colour,start,end,10)
        rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(screen, colour, ((end[0]+20*math.sin(math.radians(rotation)), end[1]+20*math.cos(math.radians(rotation))), (end[0]+20*math.sin(math.radians(rotation-120)), end[1]+20*math.cos(math.radians(rotation-120))), (end[0]+20*math.sin(math.radians(rotation+120)), end[1]+20*math.cos(math.radians(rotation+120)))))

    def showOptions(self, board):
        print('showing options')

    def hideOptions(self, board):
        board.reDrawBoard()
        self.optionsShowed = False

    def checkIfEnnemyInOptions(self, option, board):
        print('checking ennemies')
        print("option : ", option[0])
        print("board : ", board.board[0])
        
        if(board.board[option[0]][option[1]]!=0):
            print('there is an ennemy !')
            return True
        else:
            return False

    def move(self):
        print("todo")

    def cleanShowOptionsShowed(self):
        self.optionsShowed = False

    def kill(self):
        print("todo")

    def die(self):
        print("todo")

    def display(self):
        print("todo")

    def pixelizePosition(self, pos,pieceSize):
        return (pos[0]*150+pieceSize, pos[1]*150+pieceSize)
    
    def unPixelizePosition(self, pos, pieceSize):
        return (pos[0]/150+pieceSize, pos[1]/150+pieceSize)