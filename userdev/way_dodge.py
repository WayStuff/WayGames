from os import path, listdir
from os.path import isfile, join
import sys
import random
import time
import pandas as pd
import numpy as np
import pygame
from pygame.locals import *

# Game: WayDrop
# Rules: Move the feral camel (fiercest of all march maddness mammals) left and right
# to avoid the falling furnitures.

# TODO: GENERAL REFACTOR NEEDED
# TODO: Move all board values+functions to a board class; reuse score keeper
# Board configs
# NOTE: 0, 0 is in the upper left hand corner
BOARD_WIDTH   = 1000
BOARD_HEIGHT  = 800
SCORE_BOARD_X = 100
SCORE_BOARD_Y = 60
SCORE_FONT_SIZE = 30
SCORE_BASE = 5
WALL_WIDTH = 20

# Player configs
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 120
MAX_PLAYER_SPEED = 20 
PLAYER_ABS_ACCEL = 4

# Falling furniture configs
FALLING_WIDTH = PLAYER_WIDTH
FALLING_HEIGHT = PLAYER_HEIGHT
START_FALL_VELOCITY = 10

# Player boundaries
LEFT_WALL = WALL_WIDTH
RIGHT_WALL = BOARD_WIDTH - WALL_WIDTH
GROUND_Y = int(BOARD_HEIGHT * 0.8)

# Colors (R, G, B)
BLACK  = (  0,    0,    0)
GRAY   = (100,  100,  100)
WHITE  = (255,  255,  255)
RED    = (255,    0,    0)
GREEN  = (  0,  255,    0)
BLUE   = (  0,    0,  255)
ORANGE = (255,  128,    0)
PURPLE = (255,    0,  255)
YELLOW = (255,  255,    0)
RANDO  = (100,  200,  209)

COLORS = [RED, GREEN, BLUE, ORANGE, PURPLE, RANDO]
# Path to the falling furniture pngs
FURN_FPATH = '../images/furniture/'
FURN_FILES = [f for f in listdir(FURN_FPATH) if isfile(join(FURN_FPATH, f))]
N_PER_VELOCITY = 6

def not_main():

    # Initialize game and board
    global DISPLAYSURF
    pygame.init()
    pygame.font.init()
    DISPLAYSURF = pygame.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT),0,32)
    DISPLAYSURF.fill(BLACK)
    pygame.display.set_caption('Can you WayDodge all the things?')

    # Initialize x position, velocity, and acceleration for all pieces in the game
    # Start things at the bottom middle of the screen
    x_player = int(BOARD_WIDTH / 2)
    v_player = 0
    a_player = 0
    local_score = 0
    player_img = pygame.image.load('../images/camel.png')
    player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

    # Start with just 1 falling thing 
    x_falling = random.randrange(0, BOARD_WIDTH - FALLING_WIDTH)
    y_falling = 0
    v_falling = START_FALL_VELOCITY 
    n_fallen_at_this_vel = 0
    n_falling_things = 1

    image_i = np.random.randint(0, len(FURN_FILES))
    falling_img = pygame.image.load(FURN_FPATH + f'{FURN_FILES[image_i]}')
    falling_img = pygame.transform.scale(falling_img, (FALLING_WIDTH, FALLING_HEIGHT))

    # Main game event loop; each loop is ~10 ms
    while True:
        mouse_clicked = False
        for event in pygame.event.get():
             if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                 pygame.quit()
                 sys.exit()
             elif event.type == MOUSEMOTION:
                 mouseX, mouseY = event.pos
             elif event.type == MOUSEBUTTONUP:
                 mouseX, mouseY = event.pos
                 mouse_clicked = True
             # TODO: Fix sticky keys
             elif event.type == pygame.KEYDOWN:
                 # If key is held down, accelerate the player
                 if event.key == pygame.K_LEFT:
                     a_player = -1 * PLAYER_ABS_ACCEL
                 elif event.key == pygame.K_RIGHT:
                     a_player = 1 * PLAYER_ABS_ACCEL
             elif event.type == pygame.KEYUP:
                 if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                     a_player = 0
                     v_player = 0

        # Draw over the player's old spot in prep for new position
        pygame.draw.rect(DISPLAYSURF, BLACK, (x_player, GROUND_Y, PLAYER_WIDTH, PLAYER_HEIGHT))

        ################################################################################
        # Calculate new position and velocity for the player
        # x = x0 + v * dt; v = v0 + a * dt; dt = 1 pygame event
        #
        # Apply these constraints:
        # 1. new velocity < MAX_PLAYER_SPEED
        # 2. new position is within the game's walls
        ################################################################################
        v_player += a_player
        v_player = v_player if abs(v_player) < MAX_PLAYER_SPEED else v_player / abs(v_player) * MAX_PLAYER_SPEED

        x_player += v_player
        x_player = x_player if x_player >= LEFT_WALL else LEFT_WALL
        x_player = x_player if x_player <= RIGHT_WALL - PLAYER_WIDTH else RIGHT_WALL - PLAYER_WIDTH

        DISPLAYSURF.blit(player_img, (x_player, GROUND_Y, PLAYER_WIDTH, PLAYER_HEIGHT))
        pygame.display.update()

        ################################################################################
        # Calculate new position for the attacker
        ################################################################################
        pygame.draw.rect(DISPLAYSURF, BLACK, (x_falling, y_falling, FALLING_WIDTH, FALLING_HEIGHT))

        y_falling += v_falling

        ################################################################################
        # Check if the falling furniture
        # 1. Hit the player: end game and update high scores
        # 2. Is still in the air: draw new position
        # 3. Hit the ground: generate new piece(s) and update velocity if necessary
        ################################################################################
        if (y_falling >= GROUND_Y - PLAYER_HEIGHT) and check_overlap(x_player, x_falling):
           player_lost_screen()
           players_name = get_players_name()
           # display_score = int(SCORE_BASE * round(float(local_score) / 10 / SCORE_BASE))
           show_high_scores(players_name, display_score)
        elif y_falling < GROUND_Y: 
            DISPLAYSURF.blit(falling_img, (x_falling, y_falling, FALLING_WIDTH, FALLING_HEIGHT))
        else:
            n_fallen_at_this_vel += 1

            if n_fallen_at_this_vel == N_PER_VELOCITY:
                v_falling += 0.5

            # for i in range(n_falling_things):
            x_falling = random.randrange(LEFT_WALL, RIGHT_WALL - FALLING_WIDTH)
            y_falling = random.randrange(-10, 0)
            image_i = np.random.randint(0, len(FURN_FILES))
            falling_img = pygame.image.load(FURN_FPATH + f'{FURN_FILES[image_i]}')
            falling_img = pygame.transform.scale(falling_img, (FALLING_WIDTH, FALLING_HEIGHT))

        ################################################################################
        # Update and display score
        # Increment by 5's in this janky way; prob a better way to do this
        ################################################################################
        local_score += 1

        if local_score % 10 == 0:
            display_score = int(SCORE_BASE * round(float(local_score) / 10 / SCORE_BASE))
            text, text_rect = show_score(display_score)
            DISPLAYSURF.blit(text, text_rect)


def check_overlap(x_player, x_falling):
    # Check the x overlap for falling pieces
    if (x_falling >= x_player and x_falling <= x_player + PLAYER_WIDTH) or \
       (x_falling + FALLING_WIDTH >= x_player and x_falling + FALLING_WIDTH <= x_player + PLAYER_WIDTH):
       return 1
    else:
        return 0

def show_score(score, base=5):

       print(score)
       font = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)
       text = font.render(f'Score: {score}', True, WHITE, BLACK)
       text_rect = text.get_rect()
       text_rect.centerx = SCORE_BOARD_X
       text_rect.centery = SCORE_BOARD_Y

       return text, text_rect

def player_lost_screen():

    # TODO: Figure out why SysFont (vs Font) causes the system to hang. Issue in sysfont.py
    font = pygame.font.Font('freesansbold.ttf', 26)
    DISPLAY = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT),0,32)
    DISPLAY.fill(BLACK)

    text = font.render('You\'ve been struck. Sad blob. ', True, WHITE, RED)
    text_rect = text.get_rect()
    text_rect.centerx = DISPLAY.get_rect().centerx
    text_rect.centery = DISPLAY.get_rect().centery - BOARD_HEIGHT/2 * 0.5

    DISPLAY.blit(text, text_rect)
    pygame.display.update()
    # pygame.time.wait(3000)

def get_players_name():
    player = ""
    font = pygame.font.Font('freesansbold.ttf', 24)
    text = font.render(f"Enter your name: {player}", True, WHITE)
    DISPLAYSURF.blit(text, (SCORE_BOARD_X, 250))
    pygame.display.update()

    # Now get player's name
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
                    player = player[:-1]
                if event.key == pygame.K_RETURN or len(player) > 10:
                    keep_going = False

            text = font.render(f"Enter your name: {player}", True, WHITE)
            DISPLAYSURF.blit(text, (SCORE_BOARD_X, 250))
            pygame.display.update()

    return player

def update_high_scores(player, score):

    if path.exists("scores.csv"):
       print('Exists!' )
       f = pd.read_csv("scores.csv")
       df = pd.DataFrame(f)
       df = df.append({'player': player, 'score': score}, ignore_index=True)
    else:
       df = pd.DataFrame(data={'player': player, 'score': score}, index=[0])

    df_write = df.sort_values(by=['score'], ascending=False).head(5).reset_index(drop=True)
    df_write = df_write[['player', 'score']]
    df_write.to_csv("scores.csv", index=False)

    return df_write

def show_high_scores(player, score):

    df = update_high_scores(player, score)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        font = pygame.font.Font('freesansbold.ttf', 24)
        DISPLAY = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT), 0, 32)
        DISPLAY.fill(BLACK)

        text = font.render(f"High Scores", True, WHITE, BLACK)
        DISPLAY.blit(text, (SCORE_BOARD_X, 50))

        for i in range(df.shape[0]):
           n_dots = '.' * (20 -len(df['player'][i]))
           text = font.render(f"{df['player'][i]} {n_dots} {int(df['score'][i])}", True, WHITE)
           DISPLAYSURF.blit(text, (SCORE_BOARD_X, i * 50 + 100))

        pygame.display.update()

if __name__=='__main__':
    not_main()
