import sys, pygame
from board import Board
from variables import WIDTH, HEIGHT
pygame.init()

#Variables taille, couleurs...
size = WIDTH, HEIGHT
speed = [2, 2]
black = 0, 0, 0
my_color = 0,0,255
BLOCKSIZE = int(WIDTH/8)

#Variables pygame
screen = pygame.display.set_mode(size)
background = pygame.image.load('static/img/Chessboard480.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
board = Board(screen, background)


#TODO : Quand on tue une pièce, elle showOptions avant de mourir, ce qui fait le bug des flèches.

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
    




