import sys, random, pygame, time
from pygame.locals import *

BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
DARKYELLOW = (139, 128, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BROWN = (150, 75, 0)
FPS = 10

TIME_LIMIT = 120

TEXT_COLOR = WHITE
#ELEMENT_SIZE = 10

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
        self.chest = Chest()
        self.start_time = time.time()
        self.elapsed_time = 0
        self.coin_position = []
        for i in range(6):
            self.add_coin()
    
    def draw_board(self):
        # Draw grid
        DISPLAYSURF.fill(BGCOLOR)
        for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
            pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
            pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

        # Draw snake
        for body_part in self.snake.body[:3]:  # First three body parts
            x = body_part[0] * CELLSIZE
            y = body_part[1] * CELLSIZE
            outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
            pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)

        for body_part in self.snake.body[3:]:  # Rest of the body parts
            x = body_part[0] * CELLSIZE
            y = body_part[1] * CELLSIZE
            outer_part_ellipse = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            inner_part_ellipse = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.ellipse(DISPLAYSURF, DARKYELLOW, outer_part_ellipse)
            pygame.draw.ellipse(DISPLAYSURF, YELLOW, inner_part_ellipse)

        # Draw coin
        for i in range(len(self.coin_position)):
            x = self.coin_position[i][0]
            y = self.coin_position[i][1]
            coin_rect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
            pygame.draw.ellipse(DISPLAYSURF, YELLOW, coin_rect)

        # Draw coins score
        score_surface = BASICFONT.render('Coins: ' + str(len(self.snake.body) - 3), True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (WINDOWWIDTH - 120, 10)
        DISPLAYSURF.blit(score_surface, score_rect)
        
        # Draw time left
        time_left = TIME_LIMIT  - round(self.elapsed_time, 2)
        #time_surface = BASICFONT.render('Time left: ' + str(time_left), True, WHITE)
        time_surface = BASICFONT.render('Time left: {:.2f}'.format(time_left), True, WHITE)
        time_rect = time_surface.get_rect()
        time_rect.topleft = (10, 10)
        DISPLAYSURF.blit(time_surface, time_rect)
    
        #Draw chest
        text = "0"
        if self.check_chest():
            text = str(int(text) + len(self.snake.body) - 3) 
        self.chest.draw(str(self.chest.coins))


    def check_coin(self):
        x, y = self.snake.body[0][0], self.snake.body[0][1]
        for el in self.coin_position:
            if el[0] == x and el[1] == y:
                self.snake.ate = True
                self.coin_position.remove(el)
                self.add_coin()
                return
            
    def add_coin(self):
        while True:
            x, y = get_random_position()
            if self.check_list(self.snake.body, x, y) or self.check_list(self.coin_position, x, y):
                continue
            else:
                self.coin_position.append((x, y))
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

    def check_victory(self):
        chest_x, chest_y = self.chest.position
        snake_head_x, snake_head_y = self.snake.body[0]

        if (chest_x <= snake_head_x < chest_x + 2) and (chest_y <= snake_head_y < chest_y + 2) and (self.chest.coins >= 20):
            self.chest.opened = True
            return True
        self.elapsed_time = time.time() - self.start_time
        if self.elapsed_time >= TIME_LIMIT:
            return True
        return False

    def check_chest(self):
        chest_x, chest_y = self.chest.position
        snake_head_x, snake_head_y = self.snake.body[0]

        if (chest_x <= snake_head_x < chest_x + 2) and (chest_y <= snake_head_y < chest_y + 2):
            self.chest.coins += len(self.snake.body) -3
            for i in range (len(self.snake.body) - 3):
                self.snake.body.pop()   
            return True
        
        
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


class Chest:
    def __init__(self):
        self.position = (8, 10)  # Fixed position for the chest
        self.opened = False
        self.coins = 0

    def draw(self, text):
        imp = pygame.image.load(".\\chest_40.png").convert()
        x, y = self.position
        DISPLAYSURF.blit(imp, (x * CELLSIZE, y * CELLSIZE))
        SMALL_FONT = pygame.font.Font('freesansbold.ttf', 20)
        text_surf = SMALL_FONT.render(text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect()
        text_rect.center = ((x + 1) * CELLSIZE, (y + 1) * CELLSIZE)
        DISPLAYSURF.blit(text_surf, text_rect)


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
        board.check_coin()
        board.check_chest()
        if board.check_victory():
            if board.chest.opened:
                show_victory_screen()
            else:
                show_game_over_screen()
            terminate()
        if board.check_death():
            show_game_over_screen()
            terminate()       
        board.draw_board()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        time.sleep(TIME_SLEEP)

def wait_for_key_pressed():
    """Wait for a player to press any key."""
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

def show_start_screen():
    """Show a welcome screen at the first start of the game."""
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)
    wait_for_key_pressed()

def show_game_over_screen():
    """Show a game over screen when the player loses."""
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
    victory_font = pygame.font.Font('freesansbold.ttf', 100)
    victory_surface = victory_font.render('Victory!', True, WHITE)
    victory_rect = victory_surface.get_rect()
    victory_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(victory_surface, victory_rect)
    pygame.display.update()
    wait_for_key_pressed()

def was_key_pressed():
    """Exit game on QUIT event, or return True if key was pressed."""
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
