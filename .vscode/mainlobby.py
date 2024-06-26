import pygame
import subprocess
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKRED = (139, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game Main Lobby")

# Define button class
class Button:
    def __init__(self, x, y, width, height, text, action, color = BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render(self.text, True, self.color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def clicked(self):
        self.action()

# Define action functions for each button
def start_level_1():
    subprocess.run(["python", "snake.py"])

def start_level_2():
    subprocess.run(["python", "level_s_pismenkami.py"])

def start_level_3():
    subprocess.run(["python", "snake_coins.py"])

def start_level_4():
    subprocess.run(["python", "hledání partnera.py"])

def start_level_5():
    subprocess.run(["python", "epic_snake_maze.py"]) 

def start_level_6():
    subprocess.run(["python", "boss_fight.py"]) 
    
#add boss fight

# Create buttons
level1_button = Button(300, 150, 200, 50, "Level 1", start_level_1)
level2_button = Button(300, 225, 200, 50, "Level 2", start_level_2)
level3_button = Button(300, 300, 200, 50, "Level 3", start_level_3)
level4_button = Button(300, 375, 200, 50, "Level 4", start_level_4)
level5_button = Button(300, 450, 200, 50, "Level 5", start_level_5)
level6_button = Button(300, 525, 200, 50, "Level 6", start_level_6, DARKRED)


#Show a welcome screen at the first start of the game
title_font = pygame.font.Font('freesansbold.ttf', 75)
title_surface = title_font.render('Epic snake game!', True, DARKGREEN)
title_rect = title_surface.get_rect()
title_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 7)


def main():
    while True:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level1_button.rect.collidepoint(mouse_pos):
                    level1_button.clicked()
                elif level2_button.rect.collidepoint(mouse_pos):
                    level2_button.clicked()
                elif level3_button.rect.collidepoint(mouse_pos):
                    level3_button.clicked()
                elif level4_button.rect.collidepoint(mouse_pos):
                    level4_button.clicked()
                elif level5_button.rect.collidepoint(mouse_pos):
                    level5_button.clicked()
                elif level6_button.rect.collidepoint(mouse_pos):
                    level6_button.clicked()

        screen.blit(title_surface, title_rect)
    

        # Draw buttons
        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)
        level4_button.draw(screen)
        level5_button.draw(screen)
        level6_button.draw(screen)

        pygame.display.flip()

if __name__ == '__main__':
    main()


# chybí postupne odemykaní levelu
# zmenit propojeni levelu v main lobby
