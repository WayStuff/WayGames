import sys
import pygame
from pygame.locals import *
import base.color as c


class BaseBoard: 
    
    def __init__(self):
        """Base class implementation for games using boards
        """
        self.BOARD_WIDTH = 800
        self.BOARD_HEIGHT = 600
        self.START_X = 130
        self.START_Y = 50 
        self.DISPLAYSURF = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT), 0, 32)
        self.FONT = pygame.font.Font("freesansbold.ttf", 24) 
        # TODO: make separate score class
        self.SCORE_FILE = "../app/scores.csv" 
        self.SCORE_BOARD_X = 100
        self.SCORE_BOARD_Y = 60
        self.N_TOP_SCORES = 10
        self.SCORE_SORT_ASC = False 

    def init_board(self):
        raise NotImplementedError

    def player_lost_screen(self):
    
        DISPLAY = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT), 0, 32)
        DISPLAY.fill(c.BLACK)
    
        text = self.FONT.render("You lost! Sad blob.", True, c.WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = DISPLAY.get_rect().centerx
        text_rect.centery = DISPLAY.get_rect().centery - self.BOARD_HEIGHT / 4
    
        DISPLAY.blit(text, text_rect)
        pygame.display.update()

    def play_again(self):
        """Ask user if they want to play again
           Return (bool): True is yes; no will exit game 
        """
        text = self.FONT.render(f"Play again? (y/n)", True, c.WHITE)
        self.DISPLAYSURF.blit(text, (self.SCORE_BOARD_X, self.BOARD_HEIGHT * 0.8))
        pygame.display.update()
 
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                   (event.type == KEYUP and event.key == K_ESCAPE) or \
                   (event.type == pygame.KEYDOWN and event.key == pygame.K_n):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    return True
