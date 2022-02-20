from tarfile import BLOCKSIZE
from pieces import *
import os
import pygame

class Board:


    def __init__(self, screen, background) -> None:
        blackPieces = self.initBlackSide()
        whitePieces = self.initWhiteSide()
        a = [whitePieces['rooks'][0], whitePieces['pawns'][0], 0, 0, 0, 0, blackPieces['pawns'][0], blackPieces['rooks'][0]]
        b = [whitePieces['knights'][0], whitePieces['pawns'][1], 0, 0, 0, 0, blackPieces['pawns'][1], blackPieces['knights'][0]]
        c = [whitePieces['bishops'][0], whitePieces['pawns'][2], 0, 0, 0, 0, blackPieces['pawns'][2], blackPieces['bishops'][0]]
        d = [whitePieces['queen'][0], whitePieces['pawns'][3], 0, 0, 0, 0, blackPieces['pawns'][3], blackPieces['queen'][0]]
        e = [whitePieces['king'][0], whitePieces['pawns'][4], 0, 0, 0, 0, blackPieces['pawns'][4], blackPieces['king'][0]]
        f = [whitePieces['bishops'][1], whitePieces['pawns'][5], 0, 0, 0, 0, blackPieces['pawns'][5], blackPieces['bishops'][1]]
        g = [whitePieces['knights'][1], whitePieces['pawns'][6], 0, 0, 0, 0, blackPieces['pawns'][6], blackPieces['knights'][1]]
        h = [whitePieces['rooks'][1], whitePieces['pawns'][7], 0, 0, 0, 0, blackPieces['pawns'][7], blackPieces['rooks'][1]]

        self.board = [a,b,c,d,e,f,g,h]
        self.screen = screen
        self.background = background
        #self.board = [h, g, f, e, d, c, b, a]

        self.size = self.screen.get_size()
        self.width = self.size[0]
        self.height = self.size[1]
        self.BLOCKSIZE = self.width/8
        
        


    def display(self):
        print('todo')

    def initWhiteSide(self):
        bishops = []
        king = []
        knights = []
        pawns = []
        queen = []
        rooks = []

        images = self.loadImages()

        for i in range(8):
            whitePawn = Pawn.Pawn(images['white_pawn'], 0)
            pawns.append(whitePawn)

        for i in range(2):
            whiteKnight = Knight.Knight(images['white_knight'], 0)
            whiteBishop = Bishop.Bishop(images['white_bishop'], 0)
            whiteRook = Rook.Rook(images['white_rook'], 0)
            bishops.append(whiteBishop)
            knights.append(whiteKnight)
            rooks.append(whiteRook)
        
        king.append(King.King(images['white_king'], 0))
        queen.append(Queen.Queen(images['white_queen'], 0))

        allPieces = {
            'bishops':bishops,
            'king':king,
            'knights':knights,
            'pawns':pawns,
            'queen':queen,
            'rooks':rooks
        }

        return allPieces

    def initBlackSide(self):
        bishops = []
        king = []
        knights = []
        pawns = []
        queen = []
        rooks = []

        images = self.loadImages()

        for i in range(8):
            blackPawn = Pawn.Pawn(images['black_pawn'], 1)
            pawns.append(blackPawn)

        for i in range(2):
            blackKnight = Knight.Knight(images['black_knight'], 1)
            blackBishop = Bishop.Bishop(images['black_bishop'], 1)
            blackRook = Rook.Rook(images['black_rook'], 1)
            bishops.append(blackBishop)
            knights.append(blackKnight)
            rooks.append(blackRook)
        
        king.append(King.King(images['black_king'], 1))
        queen.append(Queen.Queen(images['black_queen'], 1))

        allPieces = {
            'bishops':bishops,
            'king':king,
            'knights':knights,
            'pawns':pawns,
            'queen':queen,
            'rooks':rooks
        }

        return allPieces
    
    def editBoard(self, x, y, value):
        #TODO
        # self.board[x][y]
        # print('AFTER EDIT : ', self.board[x])
        return self

    def drawSprites(self,board): #Dessine toutes les pièces de l'échiquier
        all_sprites_list = pygame.sprite.Group()
        width = self.screen.get_width()
        height = self.screen.get_height()
        BLOCKSIZE = width/8
        i = 0
        for x in range(0, width, int(width/8)):
            j = 0
            if i > 7:
                i = 0
            for y in range(0, height, int(height/8)):
                block = self.board[i][j]
                if isinstance(block, piece.Piece):
                    block.set_position(x+14, y+14)
                    all_sprites_list.add(block)

                j = j + 1
            i = i +1
        all_sprites_list.draw(self.screen)
        return all_sprites_list

    def loadImages(self):
        path = os.getcwd()


        parent = os.path.abspath(os.path.join(path, os.pardir))


        image_folder = os.path.abspath(os.path.join(path, 'static/img/'))

        black_bishop = pygame.image.load(os.path.abspath(os.path.join(image_folder,'black_bishop.png')))
        black_king = pygame.image.load(os.path.abspath(os.path.join(image_folder,'black_king.png')))
        black_knight = pygame.image.load(os.path.abspath(os.path.join(image_folder,'black_knight.png')))
        black_pawn = pygame.image.load(os.path.abspath(os.path.join(image_folder,'black_pawn.png')))
        black_queen = pygame.image.load(os.path.abspath(os.path.join(image_folder,'black_queen.png')))
        black_rook = pygame.image.load(os.path.abspath(os.path.join(image_folder,'black_rook.png')))

        white_bishop = pygame.image.load(os.path.abspath(os.path.join(image_folder,'white_bishop.png')))
        white_king = pygame.image.load(os.path.abspath(os.path.join(image_folder,'white_king.png')))
        white_knight = pygame.image.load(os.path.abspath(os.path.join(image_folder,'white_knight.png')))
        white_pawn = pygame.image.load(os.path.abspath(os.path.join(image_folder,'white_pawn.png')))
        white_queen = pygame.image.load(os.path.abspath(os.path.join(image_folder,'white_queen.png')))
        white_rook = pygame.image.load(os.path.abspath(os.path.join(image_folder,'white_rook.png')))

        allImages = {
            'black_bishop':black_bishop,
            'black_king':black_king,
            'black_knight':black_knight,
            'black_pawn':black_pawn,
            'black_queen':black_queen,
            'black_rook':black_rook,
            'white_bishop':white_bishop,
            'white_king':white_king,
            'white_knight':white_knight,
            'white_pawn':white_pawn,
            'white_queen':white_queen,
            'white_rook':white_rook,
        }

        return allImages

    
    
    
    def reDrawBoard(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, [0,0])
        all_sprites_list = self.drawSprites(self.board)
        for sprite in all_sprites_list:
            sprite.cleanShowOptionsShowed()
        return all_sprites_list
        
    def getPositionOfClick(self, pos):
        x = int(pos[0]/self.BLOCKSIZE)
        y = int(pos[1]/self.BLOCKSIZE)
        return (x, y)
        

