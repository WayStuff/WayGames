import pygame
import os
import sys
import time
from pygame.locals import *
from app.gem_board import GemBoard

###############################################################
#
# Hidden Gem (Mine) Sweeper
#
# Rules: 
#   Click anywhere on the 10x10 board to start. As you click, you'll
#   uncover numbers, gray squares, and hidden gems. Numbers tell
#   you how many gems the box you clicked touches.  Gray boxes mean 
#   that the box touches 0 gems; find one of these, and you'll get
#   some boxes for free. Finally, gem boxes are the things to avoid;
#   hit a gem, and you lose.
#   
#   You can protect yourself from mistakes by right clicking a
#   box you suspect to hold a gem; if you right click again,
#   the protection goes away and you're free to click the box again.
#
#   Win the game by finding all 90 gem-free locations.
# 
###############################################################


def main():

    pygame.init()
    m = GemBoard()

    # Main game event loop; each loop is ~10 ms
    while True:

        mouse_clicked = False
        right_clicked = False 
        for event in pygame.event.get():
            mouse_x, mouse_y = 0, 0
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if event.button == 3:
                    right_clicked = True 

        m.score_keeper.show_score(m.DISPLAYSURF, time.time() - m.score_keeper.START)
        
        if mouse_clicked:

            if not m.is_click_on_board(mouse_x, mouse_y):
                continue

            box_x, box_y = m.convert_to_box(mouse_x, mouse_y)

            # If right click occurs, draw a safety image or remove it depending on box's state
            if right_clicked and (box_x, box_y) not in m.displayed_boxes_xy:
                m.update_right_click_status(box_x, box_y)
                pygame.display.update()

            if not right_clicked and (box_x, box_y) not in m.right_clicked_boxes_xy:
                if (box_x, box_y) in m.displayed_boxes_xy:
                    continue

                m.fill_users_boxes(box_x, box_y)

                # User lost
                if m.gem_was_hit:
                    m.player_lost_screen()
                    pygame.time.delay(500)

                    if m.play_again():
                        pygame.init()
                        m = GemBoard()

                # User won
                if len(m.displayed_boxes_xy) == (m.NSQUARE_X * m.NSQUARE_Y - m.N_GEMS):
                    for i in range(m.NSQUARE_X):
                        for j in range(m.NSQUARE_Y):
                            m.display_box(i, j)

                    pygame.display.update()

                    end = time.time()
                    players_name = m.score_keeper.get_players_name(m.DISPLAYSURF, suffix_text="You win! ")
                    m.score_keeper.show_high_scores(m.DISPLAYSURF, players_name, end - m.score_keeper.START)

                    if m.play_again():
                        pygame.init()
                        m = GemBoard()


if __name__ == '__main__':
    main()
