from tarfile import BLOCKSIZE
from turtle import pos
import pygame
import math
from variables import WIDTH, HEIGHT

size = WIDTH, HEIGHT


#from main import screen
class Piece(pygame.sprite.Sprite):
    def __init__(self, image, color):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.w = WIDTH/8
        self.rect.h = HEIGHT/8
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
        self.alive = True


    def set_position(self, x, y):
        self.rect.x =  x
        self.rect.y =  y

    def showOptions(self, board, pos):
        if(self.optionsShowed==False):
            self.calculateOptions(board, pos)
            self.optionsShowed = True
        else:
            self.optionsShowed = False

    def getOptions(self):
        return self.options

    def get_position(self):
        return(int(self.rect.x/self.BLOCKSIZE), int(self.rect.y/self.BLOCKSIZE))

    def movePiece(self, board, oldPos, newPos):
        
        currentPiece = board.board[oldPos[0]][oldPos[1]]
        targettedPiece = board.board[newPos[0]][newPos[1]]
        #Si il y a un ennemi
        if(self.checkIfEnnemyInOptions(newPos, board)==True):
            del  board.board[newPos[0]][newPos[1]]
            board.board[newPos[0]].insert(newPos[1], currentPiece)
            #board.board[newPos[0]][newPos[1]] = currentPiece
            board.board[oldPos[0]][oldPos[1]] = 0
            targettedPiece.alive = False
            targettedPiece.kill()
            board.all_sprites.remove(targettedPiece)
            del targettedPiece
        #Si il n'y a pas d'ennemi
        else:
            board.board[oldPos[0]][oldPos[1]] = targettedPiece
            board.board[newPos[0]][newPos[1]] = currentPiece
        
        board.reDrawBoard()
        self.move()

    def checkIfMovementsAreOutOfMap(self, events):
        outOfMapMovements = []
        for event in events:
            if(event[0]<0 or event[0]>7 or event[1]<0 or event[1]>7):
                outOfMapMovements.append(event)
        return outOfMapMovements
    
    def clickOnMySelf(self, board, event):
        """Does the action when the user clicks on the piece. It shows the possible options, or it hides it.

        Args:
            board (_type_): _description_
            event (_type_): _description_
        """
        if(self.optionsShowed==False and self.alive==True):
            self.showOptions(board, event.pos)
        else:
            self.hideOptions(board)
    
    def clickElseWhere(self, event, board):
        """Does the action when we click on something else than the piece itself.

        Args:
            event (_type_): _description_
            board (_type_): _description_
        """
        clickPosition = board.getPositionOfClick(event.pos)
        options = self.options["end"]
        if(self.optionsShowed==True):
            if(clickPosition in options):
                self.movePiece(board, self.options['start'], clickPosition)
            else:
                self.hideOptions(board)

    def update(self, event_list, board):
        for event in event_list:
            #We get the click event on the board.
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPosition = event.pos
                #1er cas : on clique sur la pièce elle même
                if(self.rect.collidepoint(event.pos)):
                    self.clickOnMySelf(board, event)
                #2e cas : on clique ailleurs que sur la case elle même
                else:
                    #Options showing :
                        #On clique sur une option => On se déplace
                        #On clique sur du vide => On cache les options
                    #Options hidden : 
                         #Il ne se passe rien
                    self.clickElseWhere(event, board)

    def swapPositions(self, list, pos1, pos2):     
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list

    def checkIfPieceIsInTheWayHorizontally(self, option, board):
        position = self.options["start"]
        x = position[0]
        y = position[1]
        partition = []
        for i in range(x+1, option[0]+1):
            if(board.board[i][y]!=0):
                partition.append(board.board[i][y])
        for i in range(option[0], x):
            if(board.board[i][y]!=0):
                partition.append(board.board[i][y])
        return partition
        
    def checkIfPieceIsInTheWayVertically(self, option, board):
        position = self.options["start"]
        x = position[0]
        y = position[1]
        partition = []
        partition = board.board[x][y+1:option[1]+1]
        for element in partition:
            if element!=0:
                return partition

        partition = board.board[x][option[1]:y]  
        for element in partition:
            if element != 0:
                return partition
        return []

    
    def checkIfEnnemyIsInTheWayVertically(self, option, board):
        """Check if an ennemy is between the piece and the option chose VERTICALLY

        Args:
            position (x,y): The position of the piece
            option (x,y): The position of the option
            board (pygame.Surface): The current board of the game
            
        """
        position = self.options["start"]
        x = position[0]
        y = position[1]
        if(self.color==0):
            partition = board.board[x][y+1:option[1]]
            ennemyPresent = False
            for element in partition:
                if element != 0:
                    ennemyPresent = True
            if ennemyPresent:
                return partition
        else:
            partition = board.board[x][option[1]:y]
            ennemyPresent = False
            for element in partition:
                if element != 0:
                    ennemyPresent = True
            if ennemyPresent:
                return partition
        
        return []
            
    def checkAroundMeForEnnemy(self, board):
        position = self.options["start"]
        x = position[0]
        y = position[1]
        upPiece = board.board[x][y-1 if y-1 >= 0 else 0]
        downPiece = board.board[x][y+1 if y+1 < len(board.board[x]) else len(board.board[x])-1]
        leftPiece = board.board[x-1 if x-1 >=0 else 0][y]
        rightPiece = board.board[x+1 if x+1 < len(board.board) else len(board.board)-1][y]

        if(upPiece != 0):
            if(upPiece.color !=self.color):
                self.options["end"].add((x, y-1))

        if(downPiece != 0):
            if(downPiece.color !=self.color):
                self.options["end"].add((x, y+1))

        if(leftPiece != 0):
            if(leftPiece.color !=self.color):
                self.options["end"].add((x-1, y))

        if(rightPiece != 0):
            if(rightPiece.color !=self.color):
                self.options["end"].add((x+1, y))


    def partitionList(self,alist, indices):
        return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

    def drawArrow(self,screen, colour, start, end):
        pygame.draw.line(screen,colour,start,end,10)
        rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(screen, colour, ((end[0]+20*math.sin(math.radians(rotation)), end[1]+20*math.cos(math.radians(rotation))), (end[0]+20*math.sin(math.radians(rotation-120)), end[1]+20*math.cos(math.radians(rotation-120))), (end[0]+20*math.sin(math.radians(rotation+120)), end[1]+20*math.cos(math.radians(rotation+120)))))


    def hideOptions(self, board):
        board.reDrawBoard()
        self.optionsShowed = False
        self.options['start'] = ()
        self.options["end"] = set()

    def checkIfEnnemyInOptions(self, option, board):
        if(board.board[option[0]][option[1]]!=0):
            return True
        else:
            return False
    
    def drawPoint(self,screen, colour, option):
        x = option[0]
        y = option[1]
        pygame.draw.ellipse(screen, colour, (x-self.BLOCKSIZE/4, y-self.BLOCKSIZE/4, self.BLOCKSIZE/2, self.BLOCKSIZE/2))


    def move(self):
        self.options["end"] = set()

    def cleanShowOptionsShowed(self):
        self.optionsShowed = False

    def killPiece(self):
        print("todo")

    def die(self):
        print("todo")

    def display(self):
        print("todo")

    def pixelizePosition(self, pos,pieceSize): 
        return (pos[0]*pieceSize+pieceSize/2, pos[1]*pieceSize+pieceSize/2)
    
    # def unPixelizePosition(self, pos, pieceSize):
    #     return (pos[0]/pieceSize-pieceSize/2, pos[1]/pieceSize-pieceSize/2)

    # def updateBis(self, event_list, board):
    #     for event in event_list:
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if self.rect.collidepoint(event.pos): 
    #                 if(self.optionsShowed==False):
    #                     self.showOptions(board, event.pos)
    #                 elif(self.optionsShowed==True):
    #                     self.hideOptions(board)
                        
    #             else:
    #                 if(self.optionsShowed==True):
    #                     #get where it got clicked
    #                     (x,y) = board.getPositionOfClick(event.pos)
    #                     (oldX, oldY) = self.get_position()
    #                     (boardX, boardY) = (x, y)
    #                     #on check si on peut se déplacer
    #                     if((x,y) in self.options["end"]):
    #                         print('rentre dedans')
    #                         if(x==oldX):
    #                             board.board[x] = self.swapPositions(board.board[x], oldY,y)
    #                         else:
    #                             if(self.checkIfEnnemyInOptions((x,y), board) == True):
    #                                 print('killing ennemy')
    #                                 oldElem = board.board[oldX][oldY]
    #                                 newElem = board.board[x][y]
    #                                 del newElem
    #                                 board.board[oldX][oldY] = 0
    #                                 board.board[x][y] = oldElem
    #                             else:
    #                                 print('moving to another case')
    #                                 oldElem = board.board[oldX][oldY]
    #                                 newElem = board.board[x][y]
    #                                 board.board[oldX][oldY] = newElem
    #                                 board.board[x][y] = oldElem
    #                         self.move()
    #                     else:
    #                         self.options["end"] = set()

                        
    #                     board.reDrawBoard()