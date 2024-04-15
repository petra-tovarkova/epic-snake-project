import sys
import random
import pygame
import time
from pygame.locals import *

BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
FPS = 10

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, 'Window width must be a multiple of cell size.'
assert WINDOWHEIGHT % CELLSIZE == 0, 'Window height must be a multiple of cell size.'
NUM_CELLS_X = WINDOWWIDTH // CELLSIZE
NUM_CELLS_Y = WINDOWHEIGHT // CELLSIZE
TIME_SLEEP = 0.3

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class Board:
    def __init__(self):
        self.width = NUM_CELLS_X
        self.height = NUM_CELLS_Y
        self.snake = Snake(self.width // 2, self.height // 2)
        self.letters_to_collect = list("ICANREAD")  # Letters to collect
        self.letter_position = []
        for letter in self.letters_to_collect:
            self.add_letter(letter)
    
    def draw_board(self):
        # Draw grid
        DISPLAYSURF.fill(BGCOLOR)
        for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
            pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
            pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

        # Draw snake
        for body_part in self.snake.body:
            x = body_part[0] * CELLSIZE
            y = body_part[1] * CELLSIZE
            outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
            pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)

        # Draw letters
        for i in range(len(self.letter_position)):
            x = self.letter_position[i][0]
            y = self.letter_position[i][1]
            food_rect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
            letter = self.letter_position[i][2]
            font = pygame.font.Font(None, 36)  
            text_surface = font.render(letter, True, RED)
            text_rect = text_surface.get_rect(center=food_rect.center)
            DISPLAYSURF.blit(text_surface, text_rect)

        # Draw score
        score_surface = BASICFONT.render('Score: ' + str(len(self.snake.body) - 3), True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (WINDOWWIDTH - 120, 10)
        DISPLAYSURF.blit(score_surface, score_rect)

    def check_letter(self):
        x, y = self.snake.body[0][0], self.snake.body[0][1]
        for i, el in enumerate(self.letter_position):
            if el[0] == x and el[1] == y:
                if el[2] == self.letters_to_collect[0]:  # Check if collected letter matches the next letter in the sentence
                    self.letters_to_collect.pop(0)
                    self.snake.ate = True
                    self.letter_position.pop(i)
                    break

    def add_letter(self, letter):
        while True:
            x, y = get_random_position()
            if self.check_list(self.snake.body, x, y) or self.check_list(self.letter_position, x, y):
                continue
            else:
                self.letter_position.append((x, y, letter))
                break
            
    def check_list(self, elist, x, y):
        for el in elist:
            if el[0] == x and el[1] == y:
                return True
        return False

    def check_death(self):
        head_x = self.snake.body[0][0]
        head_y = self.snake.body[0][1]
        if self.check_list(self.snake.body[1:], head_x, head_y):
            return True
        if head_x in (-1, NUM_CELLS_X) or head_y in (-1, NUM_CELLS_Y):
            return True
        return False


class Snake:
    def __init__(self, x, y):
        self.direction = RIGHT
        self.ate = False
        self.body = []
        for i in range(3):
            self.body.append((x - i, y))

    def move(self):
        x, y = self.body[0]
        if self.direction == UP:
            new_head = (x, y - 1)
        elif self.direction == DOWN:
            new_head = (x, y + 1)
        elif self.direction == LEFT:
            new_head = (x - 1, y)
        elif self.direction == RIGHT:
            new_head = (x + 1, y)
        self.body.insert(0, new_head)
        if not self.ate:
            self.body.pop()
        else:
            self.ate = False


def get_random_position():
    return random.randint(1, NUM_CELLS_X - 2), random.randint(1, NUM_CELLS_Y - 2)
       
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    show_start_screen()
    board = Board()
    board.draw_board()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_UP and board.snake.direction != DOWN:
                    board.snake.direction = UP
                elif event.key == K_DOWN and board.snake.direction != UP:
                    board.snake.direction = DOWN
                elif event.key == K_LEFT and board.snake.direction != RIGHT:
                    board.snake.direction = LEFT
                elif event.key == K_RIGHT and board.snake.direction != LEFT:
                    board.snake.direction = RIGHT

        board.snake.move()
        board.check_letter()
        if board.check_death():
            show_game_over_screen()
            terminate()
        elif len(board.letters_to_collect) == 0:  # Check if all letters have been collected
            show_victory_screen()
            terminate()
        else:
            board.draw_board()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            time.sleep(TIME_SLEEP)


def show_start_screen():
    #Show a welcome screen at the first start of the game
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 4)

    sentence_font = pygame.font.Font('freesansbold.ttf', 30)
    sentence_surface = sentence_font.render('Collect the sentence: "I CAN READ"', True, WHITE)
    sentence_rect = sentence_surface.get_rect()
    sentence_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)
    DISPLAYSURF.blit(sentence_surface, sentence_rect)
    wait_for_key_pressed()


def show_victory_screen():
    #Show a victory screen when the player collects all letters
    victory_font = pygame.font.Font('freesansbold.ttf', 100)
    victory_surface = victory_font.render('Victory!', True, WHITE)
    victory_rect = victory_surface.get_rect()
    victory_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(victory_surface, victory_rect)
    pygame.display.update()
    wait_for_key_pressed()



def wait_for_key_pressed():
    #Wait for a player to press any key.
    msg_surface = BASICFONT.render('Press a key to play.', True, GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(msg_surface, msg_rect)
    pygame.display.update()
    pygame.time.wait(500)  # Prevent player pressing a key too soon
    was_key_pressed()  # Clear any previous key presses in the event queue
    while True:
        if was_key_pressed():
            pygame.event.get()  # Clear event queue
            return



def show_game_over_screen():
    #Show a game over screen when the player loses
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    wait_for_key_pressed()

def was_key_pressed():
    #Exit game on QUIT event, or return True if key was pressed
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return False
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return True

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()