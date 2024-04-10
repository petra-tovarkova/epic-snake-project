# Tady je takovy zaklad pro zacatek jestli vas jeste neco napada cokoli prepiste nebo dopiste :D
#hlavni kod

import pygame, random, sys
from pygame.locals import *

FPS = 40
WINDOWWIDTH = 960
WINDOWHEIGHT = 720

# jake barvy budeme potrebovat???
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
PINK = (255, 192, 203)
NAVYBLUE = (60, 60, 100)
LIGHTBLUE = (173, 216, 230)
LIGHTGREEN = (144, 238, 144)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    #Infinitely run the game.
    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()

def terminate():
    """Exit the program."""
    pygame.quit()
    sys.exit()
"""
def was_key_pressed():
    #Exit game on QUIT event, or return True if key was pressed.

def wait_for_key_pressed():
    #Wait for a player to press any key.

def show_start_screen():
    #Show a welcome screen at the first start of the game.

def show_game_over_screen():
    #Show a game over screen when the player loses.

def get_new_snake():
    #Set a random start point for a new snake and return its coordinates.

def get_random_location():
    #Return a random cell on the game plan.

def run_game():
    #Main game logic. Return on game over.

def draw_game_state(snake, apple):
    #Draw the contents on the screen.
    
    # Draw Grid
    # Draw Snake
    # Draw objects
    # Draw Score
    # Others

class Objects:
    #crete class for objects on the map that can be picked up

# write functions for that objects
    # Draw Apple (letter, numbers, blocks,... items to complete the level) (score)
    # Draw objects that uncover map
    # Draw objects that take a life
    # Draw objects that give a life
    # Draw objects that slow snake down
    # Draw objects that make snake deathless
    # Draw treasure (prize) 
"""
#domyslet mapu, bude se pohybovat se snakem a nebo se pohybuje podle toho jaky delas progres (oddaluje se)
    

if __name__ == '__main__':
    main() 
x="změna"
