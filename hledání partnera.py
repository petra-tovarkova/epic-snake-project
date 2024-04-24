import sys, random, pygame
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 16
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
PINK = (255,192,203)
BLUE =(173,216,230)
DIRECTION = ["left","right","up","down"]
CLOCK_PARTNER = 0
YELLOW =(255,255,0)
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

    pygame.time.wait(500)  
    was_key_pressed()  
    while True:
        if was_key_pressed():
            pygame.event.get()  
            return


def show_start_screen():
    subtitle_font = pygame.font.Font('freesansbold.ttf', 15)
    subtitle_surface = subtitle_font.render('Touch your pink soulmate to get a point,win by getting 20 points ', True, GRAY)
    subtitle_rect = subtitle_surface.get_rect()
    subtitle_rect.center = (WINDOWWIDTH/2-220, WINDOWHEIGHT / 2+55)



    
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('EPIC Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(subtitle_surface,subtitle_rect.center)
    DISPLAYSURF.blit(title_surface, title_rect)
    wait_for_key_pressed()


def show_game_over_screen():
    """Show a game over screen when the player loses."""
    game_over_font = pygame.font.Font('freesansbold.ttf', 120)
    game_surface = game_over_font.render('YOU´RE ', True, RED)
    over_surface = game_over_font.render('UNLOVED', True, RED)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    keep_up_font = pygame.font.Font('freesansbold.ttf', 20)
    keep_up_surface = keep_up_font.render('don´t worry, you´ll find your soulmate eventually ', True,WHITE)
    
    keep_up_rect = keep_up_surface.get_rect()
    keep_up_rect.midtop = (WINDOWWIDTH / 2, 300)
    

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    DISPLAYSURF.blit(keep_up_surface,keep_up_rect )
    
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
    head_x = random.randint(4,(NUM_CELLS_X//5))  #(5, NUM_CELLS_X - 8)  # Don't go too close the edge
    head_y = random.randint(4,(NUM_CELLS_Y//5))#(5, NUM_CELLS_Y - 8)  # Don't go too close the edge
    snake = [(head_x, head_y), (head_x - 1, head_y), (head_x - 2, head_y)]
    direction = random.choice(DIRECTION)
    return (snake, direction)


def random_snake_direction(direction_partner,clock):
    clock_partner = clock
    calm_frames=8
    if  clock_partner>=calm_frames:
        if direction_partner == 'up':
            clock_partner = 0
            return [random.choice(["left","right","up",]),clock_partner]
            
        elif direction_partner == 'down':
            clock_partner = 0
            return [random.choice(["left","right","down",]),clock_partner]
            
        elif direction_partner == 'left':
            clock_partner = 0
            return [random.choice(["left","up","down",]),clock_partner]
            
        elif direction_partner == 'right':
            clock_partner = 0
            return [random.choice(["right","up","down",]),clock_partner]
    clock_partner+=1
    return (direction_partner,clock_partner)

def get_new_partner():
    head_x = random.randint(18, NUM_CELLS_X - 6)  
    head_y = random.randint(12, NUM_CELLS_Y - 6)  
    snake = [(head_x, head_y), (head_x - 1, head_y), (head_x - 2, head_y)]
    direction = random.choice(DIRECTION)
    return (snake, direction)

def get_random_location():
    """Return a random cell on the game plan."""
    return (random.randint(0, NUM_CELLS_X - 1), random.randint(0, NUM_CELLS_Y - 1))


def run_game():
    """Main game logic. Return on game over."""
    snake, direction = get_new_snake()
    partner, direction_partner = get_new_partner()
    clock=0
    score=0
    while True:
        
        head_x_partner = partner[0][0]
        head_y_partner = partner[0][1]
        clock = random_snake_direction(direction_partner,clock)[1]
        direction_partner = random_snake_direction(direction_partner,clock)[0]
        if head_x_partner == (3 or 2 or 1): #and direction_partner == 'left':
            direction_partner = random.choice(['up','down'])
        if head_y_partner == (3 or 2 or 1): #and direction_partner == 'down':
            direction_partner = random.choice(['left','right'])
        if head_x_partner == (NUM_CELLS_X-3 or NUM_CELLS_X-2 or NUM_CELLS_X-1):# and direction_partner == 'right':
            direction_partner = random.choice(['up','down'])
        if head_y_partner == (NUM_CELLS_Y-3 or NUM_CELLS_Y-2 or NUM_CELLS_Y-1): #and direction_partner =='down':
            direction_partner = random.choice(['left','right'])
        if head_x_partner ==(3 or 2 or 1) and direction_partner == ('up'or 'down'):
            direction_partner = "right"
        if head_y_partner == (3 or 2 or 1) and direction_partner == ('left'or'right'):
            direction_partner = "down"
        if head_x_partner == (NUM_CELLS_X-3 or NUM_CELLS_X-2 or NUM_CELLS_X-1) and direction_partner == ('up'or'down'):
            direction_partner = "left"
        if head_y_partner == (NUM_CELLS_Y-3 or NUM_CELLS_Y-2 or NUM_CELLS_Y-1) and direction_partner ==('left'or'right'):
            direction_partner = "up"
            

        del partner[-1]
        if direction_partner == 'up':
                new_head_partner = (head_x_partner, head_y_partner - 1)
        elif direction_partner == 'down':
                new_head_partner = (head_x_partner, head_y_partner + 1)
        elif direction_partner == 'left':
                new_head_partner = (head_x_partner - 1, head_y_partner)
        elif direction_partner == 'right':
            new_head_partner = (head_x_partner + 1, head_y_partner)
        partner.insert(0, new_head_partner)

        
        
        #direction_partner = random_snake_direction(direction_partner,clock)[0]
       #----
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
       
      
        head_x, head_y = snake[0][0], snake[0][1]
        if head_x in (-1, NUM_CELLS_X) or head_y in (-1, NUM_CELLS_Y):
            return  # Game over, snake hit the edge
        #for (body_x, body_y) in snake[1:]:
            #if body_x == head_x and body_y == head_y:
               # return  # Game over, snake hit itself
            
        # contact detector
        body1_x_partner,body1_y_partner = partner[1][0],partner[1][1]
        body2_x_partner,body2_y_partner = partner[2][0],partner[2][1]
        if head_x == head_x_partner and head_y == head_y_partner:
            score+=1
        if body1_x_partner == head_x and body1_y_partner == head_y:
            score+=1
        if body2_x_partner == head_x and body2_y_partner == head_y:
            score+=1
        if score>=20:
            good_job()
            


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


       

        
        draw_game_state(snake,partner,score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_game_state(snake, partner,score):
    """Draw the contents on the screen."""
    score=score
    #last_cell_x,last_cell_y=partner[2][0],partner[2][1]
    # Draw grid
    DISPLAYSURF.fill(BGCOLOR)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

    # Draw snake
    for body_part in snake:
        x = body_part[0] * CELLSIZE
        y = body_part[1] * CELLSIZE
        outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
        pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)
    #DRAW partner
    for cell in partner :
        x = cell[0] * CELLSIZE
        y = cell[1] * CELLSIZE
        part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,PINK , part_rect)
    
    #last_x = last_cell_x * CELLSIZE
    #last_y = last_cell_y * CELLSIZE
    #part_rect = pygame.Rect(last_x, last_y, CELLSIZE, CELLSIZE)
    #pygame.draw.rect(DISPLAYSURF, BLUE , part_rect)  
    

    # Draw score
    score_surface = BASICFONT.render('Score: ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(score_surface, score_rect)


if __name__ == '__main__':
    main()
