import sys, random, pygame
from pygame.locals import *

FPS = 8
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 10
assert WINDOWWIDTH % CELLSIZE == 0, 'Window width must be a multiple of cell size.'
assert WINDOWHEIGHT % CELLSIZE == 0, 'Window height must be a multiple of cell size.'
NUM_CELLS_X = WINDOWWIDTH // CELLSIZE
NUM_CELLS_Y = WINDOWHEIGHT // CELLSIZE

BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
YELLOW=(255,255,0)
GREY = (128,128,128)
def main():
    """Infinitely run the game."""
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def terminate():
    """Exit the program."""
    pygame.quit()
    sys.exit()


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
    game_surface = game_over_font.render('Game', True, RED)
    over_surface = game_over_font.render('Over', True, RED)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    wait_for_key_pressed()
def good_job():
    good_job_font = pygame.font.Font('freesansbold.ttf', 200)
    good_surface = good_job_font.render('GOOD', True, YELLOW)
    job_surface = good_job_font.render('JOB', True, YELLOW)
    good_rect = good_surface.get_rect()
    job_rect = job_surface.get_rect()
    good_rect.midtop = (WINDOWWIDTH / 2, 10)
    job_rect.midtop = (WINDOWWIDTH / 2, good_rect.height + 10 + 25)

    DISPLAYSURF.blit(good_surface, good_rect)
    DISPLAYSURF.blit(job_surface, job_rect)
    wait_for_key_pressed()

def get_new_snake():
    """Set a random start point for a new snake and return its coordinates."""
    head_x =(2)  # Don't go too close the edge
    head_y =(2)  # Don't go too close the edge
    snake = [(head_x, head_y), (head_x - 1, head_y), (head_x - 2, head_y)]
    direction = 'right'
    return (snake, direction)


def wall_position_x():
    x=0
    coordinants = (0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,4,4,4,4,5,5,5,5,5,
                   5,5,5,5,4,3,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,9,10,11,12,9,9,10,11,12,13,
                   14,15,16,10,10,10,10,10,10,10,10,10,10,11,12,13,14,15,16,17,18,19,20,11,12,13,11,12,13,14,
                   15,16,17,11,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,
                   37,38,39,40,41,42,43,10,12,13,14,13,13,13,13,13,13,13,13,13,13,13,14,14,14,14,14,15,16,17,18,
                   19,20,21,14,14,14,14,14,14,14,14,14,14,14,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,59,60,61,
                   62,63,15,15,15,15,15,15,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,23,24,25,26,27,30,
                   31,32,33,37,38,39,40,41,42,43,44,45,48,49,50,51,52,53,54,55,56,57,58,5916,16,16,16,16,16,16,16,15,14,
                   46,46,46,46,46,46,46,46,46,46,46,46,46,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,
                   59,59,20,21,22,23,24,25,26,27,28,29,30,31,32,33,17,17,17,17,17,17,17,17,18,18,18,18,18,18,19,19,19,19,19,19,19,19,19,19,
                   19,19,19,19,19,20,20,20,20,20,20,20,20,20,20,20,
                   21,21,21,21,21,21,21,21,21,21,22,23,23,23,23,23,23,23,23,23,23,50,50,50,50,50,50,50,50,59,59,59,59,59,59,59,59,51,52,53,
                   54,55,56,57,58,51,52,53,54,55,56,57,58,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,24,24,24,24,24,24,24,24,24,24,
                   24,24,24,24,24,24,24,46,46,46,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,56,56,56,56,56,57,58,50,50,50,50,50,50,50,
                   50,50,47,48,49,50,51,52,53,56,57,58,52,53,54,55,56,57,58,54,55,56,57,58,48,49,50,51,52,48,48,48,48,49,50,51,46,46,46,46,45,
                   45,45,45,45,40,41,42,43,44,44,43,43,43,43,43,43,41,42,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,39,39,39,39,39
                   ,39,32,33,34,35,36,37,38,38,38,37,37,36,35,35,35,34,34,34,34,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,
                   33,33,33,33,32,32,32,32,32,31,31,31,31,31,31,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,29,29,28,28,28,28,
                   28,28,28,28,27,27,27,27,27,27,27,27,27,27,26,26,26,26,26,26,26,26,25,25,25)
    for i in coordinants:
        x = x+1
    
    return coordinants

    
def wall_position_y():
    x = 0
    coordinants = (5,6,7,8,9,10,11,12,13,14,15,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,15,26,
                   33,45,5,16,26,33,45,5,17,26,33,39,40,41,33,45,0,1,2,5,26,33,38,45,2,5,6,7,8,9,10,11,21,22,23,
                   24,25,26,33,34,35,36,37,45,12,21,45,13,14,15,16,21,45,21,21,21,21,21,21,21,33,34,35,36,37,38,39,40,41,42,
                   2,2,2,2,2,2,2,2,2,2,26,26,26,33,33,33,33,33,33,33,42,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,
                   45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,42,42,42,5,6,7,11,12,13,17,38,39,40,42,0,1,5,13,17,17,
                   17,17,17,17,17,17,25,29,30,31,32,36,37,40,42,43,44,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,
                   45,45,45,45,45,5,13,26,29,36,40,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,2,2,2,2,2,2,2,2,2,
                   2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,5,13,22,23,29,36,40,24,25,17,18,19,20,21,22,23,24,25,26,27,28,29,4,5,
                   6,7,8,9,10,13,14,15,16,17,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,3,40,21,21,21,21,21,21,21,21,21,21
                   ,21,21,21,21,5,13,27,28,29,32,36,40,5,13,26,32,37,40,5,6,7,8,9,10,11,12,13,25,32,38,40,41,42,13,22,23,24,28,29,30,
                   31,32,39,40,
                   13,14,15,16,32,33,34,35,36,40,13,3,4,5,6,7,8,9,10,11,21,20,21,22,23,24,25,26,27,20,21,22,23,24,25,26,27,20,20,20,20,
                   20,20,20,20,27,27,27,27,27,27,27,27,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,20,25,26,27,28,29,30,35,36,
                   37,38,39,40,41,42,43,44,30,31,32,33,33,33,33,33,33,33,33,33,33,33,33,33,36,36,36,36,38,39,40,41,42,40,40,34,35,36,37,38
                   ,39,40,41,42,17,17,17,17,17,17,17,17,17,17,13,13,13,13,13,13,13,8,8,8,8,8,5,5,5,5,5,6,7,8,9,10,11,12,11,12,13,14,6,7,
                   8,11,14,11,11,11,11,11,14,14,15,16,17,18,19,19,19,6,7,8,9,10,11,12,13,14,19,20,21,22,23,24,25,5,26,33,34,35,36,33,33,33,
                   33,33,33,33,4,27,3,28,29,12,26,30,38,12,27,30,34,3,7,8,9,10,11,12,15,16,17,18,19,20,26,30,34,35,36,37,41,
                   42,43,44,7,15,25,29,41,7,15,24,28,32,41,3,4,5,6,7,10,11,12,13,14,15,16,17,24,28,29,30,31,41,24,41,34,35,36,37,38,39,
                   40,41,5,6,7,8,9,10,11,12,13,33,13,14,15,16,17,18,24,32,19,24,31,)
    for i in coordinants:
        x = x+1
    
    return coordinants


def get_random_location():
    """Return a random cell on the game plan."""
    return (random.randint(0, NUM_CELLS_X - 1), random.randint(0, NUM_CELLS_Y - 1))


def run_game():
    """Main game logic. Return on game over."""
    snake, direction = get_new_snake()
    apple = (60,44)
    while True:  # Main game loop
        for event in pygame.event.get():  # Event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a) and direction != 'right':
                    direction = 'left'
                elif event.key in (K_RIGHT, K_d) and direction != 'left':
                    direction = 'right'
                elif event.key in (K_UP, K_w) and direction != 'down':
                    direction = 'up'
                elif event.key in (K_DOWN, K_s) and direction != 'up':
                    direction = 'down'
                elif event.key == K_ESCAPE:
                    terminate()
        clock=0            
        wall_x = wall_position_x()
        wall_y = wall_position_y()
        head_x, head_y = snake[0][0], snake[0][1]
        if head_x in (-1, NUM_CELLS_X) or head_y in (-1, NUM_CELLS_Y):
            return  # Game over, snake hit the edge
        for (body_x, body_y) in snake[1:]:
            if body_x == head_x and body_y == head_y:
                return  # Game over, snake hit itself
        for i in wall_x:
            if i == head_x and wall_y[clock] == head_y:
                return
            clock = clock+1
            

        if head_x == apple[0] and head_y == apple[1]:  # Apple was eaten
            good_job()
        else:  # Simulate movement by removing the snake's tail
            del snake[-1]

        # Add a new segment in the direction the snake is moving
        if direction == 'up':
            new_head = (head_x, head_y - 1)
        elif direction == 'down':
            new_head = (head_x, head_y + 1)
        elif direction == 'left':
            new_head = (head_x - 1, head_y)
        elif direction == 'right':
            new_head = (head_x + 1, head_y)
        snake.insert(0, new_head)

        draw_game_state(snake, apple)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_game_state(snake, apple):
    """Draw the contents on the screen."""

    
    DISPLAYSURF.fill(BGCOLOR)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

        
    
    wall_y_help = wall_position_y()
    clock=0
    for i in wall_position_x():
        wall_x = i*CELLSIZE
        wall_y = wall_y_help[clock]*CELLSIZE
        clock=clock+1
        wall_rect = pygame.Rect(wall_x,wall_y, CELLSIZE, CELLSIZE)   
        pygame.draw.rect(DISPLAYSURF,WHITE, wall_rect)

    
    
    for body_part in snake:
        x = body_part[0] * CELLSIZE
        y = body_part[1] * CELLSIZE
        outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
        pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)

    
    x = apple[0] * CELLSIZE
    y = apple[1] * CELLSIZE
    apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, YELLOW, apple_rect)
   # x_mid = apple[0] * CELLSIZE
   # y_mid = apple[1] * CELLSIZE
   # apple_rect_mid = pygame.Rect(x_mid, y_mid, CELLSIZE-5, CELLSIZE-5)
   # pygame.draw.rect(DISPLAYSURF, GREY, apple_rect_mid)

    
    # Draw score
    #score_surface = BASICFONT.render('Score: ' + str(len(snake) - 3), True, WHITE)
    #score_rect = score_surface.get_rect()
   # score_rect.topleft = (WINDOWWIDTH - 120, 10)
    #DISPLAYSURF.blit(score_surface, score_rect)


if __name__ == '__main__':
    main()
