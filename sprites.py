import pygame
from settings import *

# this class to take some properties from "pygame.sprite.Sprite"
class Snake(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # we will group all the sprites together, so when we use update or draw function
        # will updates all of the classes and objects at once without using for loop.
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # assign the new coordinates of the snake 
        self.x, self.y = x, y
        
        # draw the snake 
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        # set the color of the snake 
        self.image.fill(GREEN)
        
        self.rect = self.image.get_rect()


    # this function to check if the head of the snake hits its body then we need to end the game
    def body_collision(self):
        if self.x == self.game.head.x and self.y == self.game.head.y:
            return True
        return False

    def update(self):
        # the movement of the snake wil be with the titlesize (32 pixels)
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


# create a food class 
class Food(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x, self.y = x, y
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

    # check if X, Y of the head of the snake are equal to X, Y of the food part then we have a collision 
    def food_collision(self):
        if self.game.head.x == self.x and self.game.head.y == self.y:
            return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


# this class is responsible for if we press the spacebar button the game will be paused.
class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.text = text

    # show the Pause word on the screen 
    def draw(self, screen, font_size):
        font = pygame.font.SysFont("Arial", font_size)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))

# Create a button class for the main screan 
class Button:
    def __init__(self, game, colour, outline, x, y,  width, height, text):
        self.game = game
        self.colour, self.outline = colour, outline
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text
    
    # we need to draw the bottuns and put the text inside the rectangle 
    def draw(self, screen):
        # we have two rectangle (Start & Quit)
        pygame.draw.rect(screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(self.text, True, WHITE)
        draw_x = self.x + (self.width/2 - text.get_width()/2)
        draw_y = self.y + (self.height/2 - text.get_height()/2)
        screen.blit(text, (draw_x, draw_y))

    def is_over(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height