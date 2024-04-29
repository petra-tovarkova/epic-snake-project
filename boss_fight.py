#final boss fight level 
# \(°e°)/ aaaaaaaaaaaaaaaa
import sys
import random
import pygame
import time
from pygame.locals import *

FPS = 45
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
NUM_CELLS_X = WINDOWWIDTH // CELLSIZE
NUM_CELLS_Y = WINDOWHEIGHT // CELLSIZE
TIME_SLEEP = 0.24 

BGCOLOR = (0, 0, 0)
PURPLE = (128, 0, 128)
DARKPURPLE = (72, 0, 72)
WHITE = (255, 255, 255)
DARKGRAY = (128, 128, 128)
BLACK = (0, 0, 0)
DARKRED = (139, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

FULL_LIFE = pygame.image.load("heart.png")
EMPTY_LIFE = pygame.image.load("eheart.png")
FULL_LIFE = pygame.transform.scale2x(FULL_LIFE)
EMPTY_LIFE = pygame.transform.scale2x(EMPTY_LIFE)



class Board:
    def __init__(self):
        self.width = NUM_CELLS_X
        self.height = NUM_CELLS_Y
        self.snake = Snake(self.width // 2, self.height // 2, 3)
        self.boss = Boss(0, NUM_CELLS_Y // 2 - 4, 3, (3,8))
        self.danger_zones = [(x, 0) for x in range(NUM_CELLS_X)] + [(x, NUM_CELLS_Y - 1) for x in range(NUM_CELLS_X)]
        self.zizaly = []
        self.respawn_zizala()
    
    
    def draw_board(self):
        # Draw grid
        DISPLAYSURF.fill(BGCOLOR)
        for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
            pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
            pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))
 
        # Draw danger zones
        danger_rect_top = pygame.Rect(0, 0, WINDOWWIDTH, CELLSIZE * 4)
        danger_rect_bottom = pygame.Rect(0, WINDOWHEIGHT - CELLSIZE * 4, WINDOWWIDTH, CELLSIZE * 4)
        pygame.draw.rect(DISPLAYSURF, RED, danger_rect_top, 4)
        pygame.draw.rect(DISPLAYSURF, RED, danger_rect_bottom, 4)
    


        # Draw worms
        for zizala in self.zizaly:
            for part in zizala.position:
                outer_part_rect = pygame.Rect(part[0], part[1], CELLSIZE, CELLSIZE)
                inner_part_rect = pygame.Rect(part[0] + 4, part[1] + 4, CELLSIZE - 8, CELLSIZE - 8)
                if zizala.deadly:
                    pygame.draw.rect(DISPLAYSURF, DARKRED, outer_part_rect)
                    pygame.draw.rect(DISPLAYSURF, RED, inner_part_rect)
                else:
                    pygame.draw.rect(DISPLAYSURF, DARKGRAY, outer_part_rect)
                    pygame.draw.rect(DISPLAYSURF, GRAY, inner_part_rect)


         # Draw snake
        for body_part in self.snake.body:
            x = body_part[0] * CELLSIZE
            y = body_part[1] * CELLSIZE
            outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
            pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)



        # Draw boss
        boss_x, boss_y = self.boss.position
        for i in range(self.boss.size[0]):
            for j in range(self.boss.size[1]):
                outer_part_rect_boss = (boss_x * CELLSIZE + i * CELLSIZE, boss_y * CELLSIZE + j * CELLSIZE, CELLSIZE, CELLSIZE)
                inner_part_rect_boss = (boss_x * CELLSIZE + 4 + i * CELLSIZE, boss_y * CELLSIZE + 4 + j * CELLSIZE, CELLSIZE - 8, CELLSIZE - 8)
                pygame.draw.rect(DISPLAYSURF, DARKPURPLE,outer_part_rect_boss)
                pygame.draw.rect(DISPLAYSURF, PURPLE, inner_part_rect_boss)

        #očka
        pygame.draw.rect(DISPLAYSURF, WHITE, (boss_x * CELLSIZE + CELLSIZE // 4 + CELLSIZE, boss_y * CELLSIZE + CELLSIZE // 4 + self.boss.size[0] * CELLSIZE * 2, CELLSIZE // 2, CELLSIZE // 2))
        pygame.draw.rect(DISPLAYSURF, BLACK, (boss_x * CELLSIZE + CELLSIZE // 4 + CELLSIZE // 8 + CELLSIZE, boss_y * CELLSIZE + CELLSIZE // 4 + CELLSIZE // 8 + self.boss.size[0] * CELLSIZE * 2, CELLSIZE // 4, CELLSIZE // 4))

        pygame.draw.rect(DISPLAYSURF, WHITE, (boss_x * CELLSIZE + CELLSIZE // 4 + CELLSIZE, boss_y * CELLSIZE + CELLSIZE // 4 + CELLSIZE, CELLSIZE // 2, CELLSIZE // 2))
        pygame.draw.rect(DISPLAYSURF, BLACK, (boss_x * CELLSIZE + CELLSIZE // 4 + CELLSIZE // 8 + CELLSIZE, boss_y * CELLSIZE + CELLSIZE // 4 + CELLSIZE // 8 + CELLSIZE, CELLSIZE // 4, CELLSIZE // 4))


        max_lives_boss = 3
        for live in range(max_lives_boss):
            DISPLAYSURF.blit(EMPTY_LIFE, (20 + live * EMPTY_LIFE.get_width(), 20))
        for live in range(self.boss.lives):
            DISPLAYSURF.blit(FULL_LIFE, (20 + live * FULL_LIFE.get_width(), 20))

        max_lives_snake = 3
        for live in range(max_lives_snake):
            DISPLAYSURF.blit(EMPTY_LIFE, (640 - max_lives_snake * EMPTY_LIFE.get_width() - 20 + live * EMPTY_LIFE.get_width(), 20))
        for live in range(self.snake.lives):
            DISPLAYSURF.blit(FULL_LIFE, (640 - max_lives_snake * EMPTY_LIFE.get_width() - 20 + live * FULL_LIFE.get_width(), 20))

    
    def check_collision(self):
        # zde zkonttrolovat vsechny kolize ktere se mohou stat.
        # v hlavni smycce se podle returnu provede nejaka nasledujici akce
        head_x, head_y = self.snake.get_head_position()
        for zizala in self.zizaly:
            zizala_head_x, zizala_head_y = zizala.get_head_position()
            if zizala.die:
                continue
            for part in self.snake.body:
                if zizala_head_x == part[0] and zizala_head_y == part[1]:
                    if zizala.deadly:
                        self.snake.lives -= 1
                        if self.snake.lives == 0:
                            return "snake_dead"
                        else:
                            return "snake_hit"
                    else:
                        zizala.die = True
                        zizala.lives = 0
                        self.boss.lives -= 1
                        if self.boss.lives == 0:
                            return "boss_dead"
                        else:
                            return "boss_hit"
    
            for part in zizala.position:
                if part[1] == head_x and part[1] == head_y:
                    self.snake.lives -= 1
                    if self.snake.lives == 0:
                        return "snake_dead"
                    else:
                        return "snake_hit"
            if zizala.position[0][0] > 640:
                zizala.die = True
                zizala.lives = 0
                self.respawn_zizala(1)
        
        for zizala in range(len(self.zizaly)):
            if len(self.zizaly) == 0:
                break
            try:
                if self.zizaly[zizala].lives == 0:
                    self.zizaly.pop(zizala)
            except:
                continue

        # Check if snake collided with danger zones or edges
        head_x, head_y = self.snake.get_head_position()
        if (head_x, head_y) in self.danger_zones or head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            self.snake.lives -= 1
            if self.snake.lives == 0:
                return "snake_dead"
            else:
                return "snake_hit"
            
            
        # Check if boss collided with danger block
        # jeste pridat zmensování displaye po tom co snae ztratí život

    def reset(self):
        self.zizaly = []
        self.snake.body[0] = self.snake.reset
        self.respawn_zizala()


    def respawn_zizala(self, count = None):
        if count == None:
            count = random.randint(2, 10)
        for zizala in range(count):
            self.zizaly.append(Worm(random.randint(-750, 0) // CELLSIZE, random.randint(0, 480) // CELLSIZE, 1, random.randint(2, 4), bool(random.randint(0, 1))))


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

class Boss:
    def __init__(self, x, y, lives, size):
        self.position = (x, y)
        self.lives = lives
        self.size = size

    
class Worm:
    def __init__(self, x, y, lives, size, deadly):
        self.direction = RIGHT
        self.size = size
        self.lives = lives
        self.position = [(x * CELLSIZE - i * CELLSIZE, y * CELLSIZE) for i in range(size)]
        self.die = False
        self.deadly = deadly
        
    def get_head_position(self):
        x = self.position[0][0] // CELLSIZE
        y = self.position[0][1] // CELLSIZE
        return (x, y)
    
    def worm_move(self):
        x, y = self.position[0]
        if self.direction == RIGHT:
            new_worm_head = (x + CELLSIZE, y)
        self.position.insert(0, new_worm_head)
        self.position.pop()


class Snake:
    def __init__(self, x, y, lives):
        self.direction = RIGHT
        self.lives = lives
        self.ate = False
        self.reset = (x, y)
        self.body = []
        for i in range(5):
            self.body.append((x - i, y))


    def get_head_position(self):
        return self.body[0]
    

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

# vyuziti na generovanni nahodnych bloku kterych se had nemuze dotknout ?? 
def get_random_position():
    return random.randint(1, NUM_CELLS_X - 2), random.randint(1, NUM_CELLS_Y - 2)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Epic Snake!')

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
        for zizala in board.zizaly:
            zizala.worm_move()
        collision_result = board.check_collision()
        if collision_result == "snake_dead":
            pygame.mixer.music.load("game_over.mp3")
            pygame.mixer.music.play()
            show_game_over_screen()
            terminate()
        elif collision_result == "boss_hit":
            pygame.mixer.music.load("good.mp3")
            pygame.mixer.music.play()
            board.respawn_zizala(1)
        elif collision_result == "snake_hit":
            pygame.mixer.music.load("bad.mp3")
            pygame.mixer.music.play()
            board.reset()
        elif collision_result == "boss_dead":
            pygame.mixer.music.load("victory.mp3")
            pygame.mixer.music.play()
            show_victory_screen()
            terminate()
        time.sleep(TIME_SLEEP)  


        board.draw_board()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


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
            pygame.event.get()  
            return
        

def was_key_pressed():
    """Exit game on QUIT event, or return True if key was pressed."""
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
            return True
    return False


def show_start_screen():
    #Show a welcome screen at the first start of the game
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Boss Fight!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 3)

    sentence_font = pygame.font.Font('freesansbold.ttf', 30)
    sentence_surface = sentence_font.render('Fight with worms and kill the boss!', True, WHITE)
    sentence_rect = sentence_surface.get_rect()
    sentence_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 1.7)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)
    DISPLAYSURF.blit(sentence_surface, sentence_rect)
    wait_for_key_pressed()


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


def show_victory_screen():
   #Show a victory screen when the player kill the boss
    victory_font = pygame.font.Font('freesansbold.ttf', 100)
    victory_surface = victory_font.render('Victory!', True, WHITE)
    victory_rect = victory_surface.get_rect()
    victory_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 100)

    sentence_font = pygame.font.Font('freesansbold.ttf', 30)
    sentence_surface = sentence_font.render('Congratulejshinnnn!', True, WHITE)
    sentence_rect = sentence_surface.get_rect()
    sentence_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 1.7)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(victory_surface, victory_rect)
    DISPLAYSURF.blit(sentence_surface, sentence_rect)
    pygame.display.update()
    wait_for_key_pressed()


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()