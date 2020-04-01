import sys
from os import path, listdir
from os.path import isfile, join
import pygame
from pygame.locals import *
import base.color as c
import pandas as pd
import time


class ScoreKeeper:

    def __init__(self):
        """Class for book keeping scores
        """
        self.FONT = pygame.font.Font("freesansbold.ttf", 24)
        self.SCORE_FILE = "../app/scores.csv"
        self.SCORE_BOARD_X = 100
        self.SCORE_BOARD_Y = 60
        self.SCORE_POS_X = 70
        self.SCORE_POS_Y = 60
        self.N_TOP_SCORES = 10
        self.SCORE_SORT_ASC = False
        self.START = time.time()

    def show_score(self, display, score):
        """Keep track of players score on board as the game proceeds
           display (pygame.display): Current board where game is displayed
           score (int): Player's current score
        """
        text = self.FONT.render(f'Score: {int(score)}', True, c.WHITE, c.BLACK)
        text_rect = text.get_rect()
        text_rect.centerx = self.SCORE_POS_X
        text_rect.centery = self.SCORE_POS_Y
        display.blit(text, text_rect)
        pygame.display.update()

    def get_players_name(self, display, suffix_text=""):
        """Get players name...this is real janky. Probably can improve this
           display (pygame.display): Current board where game is displayed
           suffix_text (str): Extra text in front of request for player's name
           Return: player (str): player's name
        """
        player = ""
        text = self.FONT.render(f"{suffix_text} Enter your name: {player}", True, c.WHITE)
        display.blit(text, (self.SCORE_BOARD_X * 2, self.SCORE_BOARD_Y / 3))
        pygame.display.update()

        char_keys = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h,
                     pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p,
                     pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
                     pygame.K_y, pygame.K_z
                     ]
        keep_going = True

        while keep_going:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in char_keys:
                        player += str(chr(event.key))
                    if event.key == pygame.K_BACKSPACE:
                        text = self.FONT.render(f"{suffix_text} Enter your name: {player}", True, c.BLACK)
                        display.blit(text, (self.SCORE_BOARD_X * 2, self.SCORE_BOARD_Y / 3))
                        player = player[:-1]
                    # TODO: Remove constant
                    if event.key == pygame.K_RETURN or len(player) > 15:
                        keep_going = False

                    text = self.FONT.render(f"{suffix_text} Enter your name: {player}", True, c.WHITE)
                    display.blit(text, (self.SCORE_BOARD_X * 2, self.SCORE_BOARD_Y / 3))
                pygame.display.update()

        return player

    def update_high_scores(self, player, score):
        """Update high scores in the game's score file
           player (str): name
           score (int): player's score
        """
        if path.exists(self.SCORE_FILE):
           f = pd.read_csv(self.SCORE_FILE)
           df = pd.DataFrame(f)
           df = df.append({"player": player, "score": score}, ignore_index=True)
        else:
           df = pd.DataFrame(data={"player": player, "score": score}, index=[0])

        df_write = df.sort_values(by=["score"], ascending=self.SCORE_SORT_ASC).head(self.N_TOP_SCORES).reset_index(drop=True)
        df_write = df_write[["player", "score"]]
        df_write.to_csv(self.SCORE_FILE, index=False)

        return df_write

    def show_high_scores(self, display, player, score):
        """Display high scores
           display (pygame.display): Current board where game is displayed
           player (str): name
           score (int): player's score
        """
        df = self.update_high_scores(player, score)
        display.fill(c.BLACK)

        text = self.FONT.render(f"High Scores", True, c.WHITE, c.BLACK)
        display.blit(text, (self.SCORE_BOARD_X, 50))

        for i in range(df.shape[0]):
           n_dots = "." * (20 -len(df["player"][i]))
           text = self.FONT.render(f"{df['player'][i]} {n_dots} {int(df['score'][i])}", True, c.WHITE)
           display.blit(text, (self.SCORE_BOARD_X, i * 30 + 120))

        pygame.display.update()
