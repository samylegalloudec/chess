from inspect import isclass
import sys, pygame
#from chess.pieces.piece import Piece
from tarfile import BLOCKSIZE
from board import Board
from pieces import piece
pygame.init()

#Variables taille, couleurs...
size = width, height = 1200, 1200
speed = [2, 2]
black = 0, 0, 0
my_color = 0,0,255
BLOCKSIZE = int(width/8)

#Variables pygame
screen = pygame.display.set_mode(size)
background = pygame.image.load('static/img/Chessboard480.png')
background = pygame.transform.scale(background, (width, height))
board = Board(screen, background)





def drawGrid():
    print('drawing !')
    for x in range(0, width, int(width/8)):
        print('x: ', x)
        for y in range(0, height, int(height/8)):
            print('y: ',y)
            rect = pygame.Rect(x, y, BLOCKSIZE,BLOCKSIZE)
            pygame.draw.rect(screen, my_color, rect)

def drawChessGrid():
    print('drawing !')
    for x in range(0, len(board.board), BLOCKSIZE):
        print('x: ', x)
        col = board.board[x]
        for y in range(0, len(col), BLOCKSIZE):
            print('y: ',y)
            pygame.draw.rect(screen, my_color, pygame.Rect(x+BLOCKSIZE,y+BLOCKSIZE,BLOCKSIZE,BLOCKSIZE), width=0)




screen.fill(black)
screen.blit(background, [0,0])
all_sprites_list = board.drawSprites(board)
clickPos = (0, 0)
while 1:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN : clickPos = pygame.mouse.get_pos()

        # for sprite in all_sprites_list:
        #     if sprite.rect.collidepoint(clickPos): 
        #         print('yay',clickPos)
                
            

    
    
    all_sprites_list.update(event_list, board)
    pygame.display.update()
    




