from abc import ABCMeta, abstractmethod
from os import path, listdir
from os.path import isfile, join
import numpy as np
import sys
import random
import pygame
from base.board import BaseBoard
from base.score_keeper import ScoreKeeper
import base.color as c

class GemBoard(BaseBoard):

    def __init__(self):
        BaseBoard.__init__(self)
        # Set some mine/gem game-specific constants
        self.BOX_SIZE = 50
        self.BOX_WIDTH = self.BOX_SIZE * 0.75
        self.BOX_HEIGHT = self.BOX_SIZE * 0.75
        self.NSQUARE_X = 10
        self.NSQUARE_Y = 10
        self.START_X = (self.BOARD_WIDTH  - self.NSQUARE_X * self.BOX_SIZE) / 2
        self.START_Y = (self.BOARD_HEIGHT - self.NSQUARE_Y * self.BOX_SIZE) / 2
        self.N_GEMS = 10 
        self.GEM_FPATH = '../images/furniture/'
        # Initialize some vars for tracking info throughout the game
        self.gem_locations = []
        self.board_values = [[0 for x in range(self.NSQUARE_Y)] for x in range(self.NSQUARE_X)]
        self.gem_was_hit = False
        self.displayed_boxes_xy = []
        self.right_clicked_boxes_xy = []
        self.gem_images = []
        # self.gem_img = pygame.image.load('../images/furniture/gnome.png')
        # self.gem_img = pygame.transform.scale(self.gem_img, (int(self.BOX_WIDTH), int(self.BOX_HEIGHT)))
        self.safety_img = pygame.image.load('../images/camel.png')
        self.safety_img = pygame.transform.scale(self.safety_img, (int(self.BOX_WIDTH), int(self.BOX_HEIGHT)))
        self.init_board()

        self.score_keeper = ScoreKeeper()
        self.score_keeper.SCORE_FILE = 'scores/gem_scores.csv'
        self.score_keeper.SCORE_SORT_ASC = True

    @abstractmethod
    def init_board(self):
        """Randomly place gems, calculates box values, and draw initial white board tiles
        """
        # Randomly assign gems to x-y board coordinates
        while len(self.gem_locations) < self.N_GEMS:
            r = random.randint(0, self.NSQUARE_X * self.NSQUARE_Y - 1)
            x_box = r % self.NSQUARE_X
            y_box = int(r / self.NSQUARE_X)

            if (x_box, y_box) not in self.gem_locations:
                self.gem_locations.append((x_box, y_box))

        # Calculate the number of gems each square touches
        for i in range(0, self.NSQUARE_X):
            for j in range(0, self.NSQUARE_Y):
                if (i, j) in self.gem_locations:
                    self.board_values[i][j] = 999
                    continue
                for ii in range(i - 1, i + 2):
                    for jj in range(j - 1, j + 2):
                        if (ii, jj) in self.gem_locations:
                            self.board_values[i][j] += 1

        # Draw box tiles
        for i in range(self.NSQUARE_X):
            for j in range(self.NSQUARE_Y):
                self.display_box(i, j, reset_board=True)

        pygame.display.update()

        self.pick_hidden_gems()

    def pick_hidden_gems(self):   
        """Randomly select N hidden gems for hidin
        """
        gem_files = [f for f in listdir(self.GEM_FPATH) if isfile(join(self.GEM_FPATH, f))]

        for i in range(self.N_GEMS):
            image_i = np.random.randint(0, len(gem_files))
            gem_img = pygame.image.load(self.GEM_FPATH + f'{gem_files[image_i]}')
            gem_img = pygame.transform.scale(gem_img, (int(self.BOX_WIDTH), int(self.BOX_HEIGHT)))
            self.gem_images.append(gem_img)

    def display_box(self, box_x, box_y, reset_board=False):
        """Display the box at the supplied coordinates 
           box_x (int): i'th box in x-space (i.e. 0 - 9 on a 10x10 board)
           box_y (int): j'th box in y-space (i.e. 0 - 9 on a 10x10 board)
        """
        left_x, upper_y = self.get_upper_left_corner(box_x, box_y)
        rendered = self.FONT.render(str(self.board_values[box_x][box_y]), True, c.RED)

        if reset_board:
            pygame.draw.rect(self.DISPLAYSURF, c.WHITE, (left_x, upper_y, self.BOX_WIDTH, self.BOX_HEIGHT))
        elif self.board_values[box_x][box_y] == 999:
            self.gem_was_hit = True
            loc_i = self.gem_locations.index((box_x, box_y))
            self.DISPLAYSURF.blit(self.gem_images[loc_i], (left_x, upper_y, self.BOX_WIDTH, self.BOX_HEIGHT))
        elif self.board_values[box_x][box_y] > 0:
            pygame.draw.rect(self.DISPLAYSURF, c.WHITE, (left_x, upper_y, self.BOX_WIDTH, self.BOX_HEIGHT))
            self.DISPLAYSURF.blit(rendered, (left_x + 10, upper_y + 4, self.BOX_WIDTH, self.BOX_HEIGHT))
            pygame.draw.rect(self.DISPLAYSURF, c.BLUE, (left_x, upper_y, self.BOX_WIDTH, self.BOX_HEIGHT), 3)
        elif self.board_values[box_x][box_y] == 0:
            pygame.draw.rect(self.DISPLAYSURF, c.GRAY, (left_x, upper_y, self.BOX_WIDTH, self.BOX_HEIGHT))

    def get_upper_left_corner(self, box_x, box_y):
        """Get the upper left corner of the clicked-box; this is useful for plotting
           box_x (int): i'th box in x-space (i.e. 0 - 9 on a 10x10 board)
           box_y (int): j'th box in y-space (i.e. 0 - 9 on a 10x10 board)
           Return (tuple): upper left x, y coordinates of the clicked box 
        """
        left_x =  self.START_X + box_x * self.BOX_SIZE
        upper_y =  self.START_Y + box_y * self.BOX_SIZE
        return (left_x, upper_y)

    def get_indices_to_display(self, box_x, box_y):
        """Based on the position of the user's click, find the box indices we'll need to fill
           box_x (int): i'th box in x-space clicked by the user
           box_y (int): j'th box in y-space clicked by the user
           Return (list of tuples): Coordinates that need to be filled in for the user's board
        """
        indices_queue = [(box_x, box_y)]
        indices_to_display = []
       
        while len(indices_queue):
            box_x_ii, box_y_jj = indices_queue.pop()

            for ii in range(box_x_ii - 1, box_x_ii + 2):
                for jj in range(box_y_jj - 1, box_y_jj + 2):
                    # If the position is off board, a gem, or already in our indices, continue
                    if (ii < 0 or ii >= self.NSQUARE_X or jj < 0 or jj >= self.NSQUARE_Y) or \
                        (self.board_values[ii][jj] == 999) or ((ii, jj) in indices_to_display):
                        continue

                    # We only want to fill squares surrounding empties, so only add 0 squares to the queues
                    if self.board_values[ii][jj] is 0:
                        indices_queue.append((ii, jj))

                    indices_to_display.append((ii, jj))

        return indices_to_display

    def fill_users_boxes(self, box_x, box_y):
        """Based on the position the user clicks, fill in the necessary spaces
           box_x (int): i'th box in x-space clicked by the user
           box_y (int): j'th box in y-space clicked by the user
           Return the number of filled boxes, so we can determine when user wins
        """
        # If the user clicked a 0-space, fill in surrounding boxes also
        if self.board_values[box_x][box_y] == 0:
            indices_to_display = self.get_indices_to_display(box_x, box_y)

            for ii, jj in indices_to_display:
                if (ii, jj) not in self.displayed_boxes_xy:
                    self.display_box(ii, jj)
                    self.displayed_boxes_xy.append((ii, jj))
        else:
            self.display_box(box_x, box_y)
            self.displayed_boxes_xy.append((box_x, box_y))

        pygame.display.update()

    def is_click_on_board(self, mouse_x, mouse_y):
        """Check if box coordinates are on the board
           mouse_x (int): x board location of mouse click
           mouse_y (int): y board location of mouse click
           Return (bool): Was the click on the gem squares board? If so, True
        """
        return (mouse_x >= self.START_X) and \
               (mouse_y >= self.START_Y) and \
               (mouse_x < self.START_X + self.NSQUARE_X * self.BOX_SIZE - (self.BOX_SIZE - self.BOX_WIDTH)) and \
               (mouse_y < self.START_Y + self.NSQUARE_Y * self.BOX_SIZE - (self.BOX_SIZE - self.BOX_HEIGHT))
   
    def convert_to_box(self, mouse_x, mouse_y):
        """Convert mouse coordinates to iterative board box-values (e.g. 0-9 on a 10x10 square board)
           mouse_x (int): x board location of mouse click
           mouse_y (int): y board location of mouse click
           Return (tuple): Box number on board that corresponds to mouse click
        """
        box_x = int((mouse_x - self.START_X) / self.BOX_SIZE)
        box_y = int((mouse_y - self.START_Y) / self.BOX_SIZE)
        return (box_x, box_y)

    def update_right_click_status(self, box_x, box_y):
        """Update the right click status on the box-- add safey flag if no flag already, else remove it 
           box_x (int): x board location of mouse click
           box_y (int): y board location of mouse click
        """
        left_x, upper_y = self.get_upper_left_corner(box_x, box_y)

        if (box_x, box_y) not in self.right_clicked_boxes_xy:
            self.DISPLAYSURF.blit(self.safety_img, (left_x, upper_y, self.BOX_WIDTH, self.BOX_HEIGHT))
            self.right_clicked_boxes_xy.append((box_x, box_y))
        else:
            pygame.draw.rect(self.DISPLAYSURF, c.WHITE, (left_x, upper_y, self.BOX_WIDTH, self.BOX_HEIGHT))
            self.right_clicked_boxes_xy.remove((box_x, box_y))
