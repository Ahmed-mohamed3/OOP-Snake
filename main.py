import pygame
from settings import *
from sprites import *
import random

# the class wgich will gonna hold our game loop and most of the settings 
class Game:
    def __init__(self):
        # start pygame
        pygame.init()
        # define the screen, and give it width and height 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # set the title of the screen 
        pygame.display.set_caption(TITLE)
        # this will be the frame rate (depend on the speed of the snake )
        self.clock = pygame.time.Clock()
        # initiate the direction of the snake is to the right
        self.orientation = 0
        # to pause the game
        self.paused = False
        
        self.playing = True
        self.score = 0
        self.high_score = self.get_high_score()

    # every time you start the game or click start buttom it is gonna to call this function and start up from the begining 
    def new(self):
        # create the sprite groups 
        self.all_sprites = pygame.sprite.Group()
        # create the head of the snake 
        self.head = Snake(self, 5, 5)
        # create a list to increase the body of the snake 
        # when the snake eats one fruit, a new part will append to the list.
        self.snake_parts = []
        self.snake_parts.append(Snake(self, 4, 5))
        self.snake_parts.append(Snake(self, 3, 5))

        # create the init food part
        self.food = Food(self, 20, 5)


    # check if the coordinates of the new food part equal to the coordinates of the snake,
    # then we will change the coordinates of the new food part and look for another position.
    def is_body_part(self):
        # check the coords against the body of the snake
        x = random.randint(0, GRIDWIDTH - 1)
        y = random.randint(0, GRIDHEIGHT - 1)
        for body in self.snake_parts:
            if x == body.x and y == body.y:
                x, y = self.is_body_part()
        return x, y

    # this function to keep the game looping so keep the snake moving and eating the food and all of that 
    def run(self):
        # game loop - set self.playing to False to end the game
        self.playing = True
        
        # while variable "playing" == True 
        # every loop == one frame of the game 
        while self.playing:
            self.clock.tick(SPEED)
            # check for rvents (if we have any mouse movements or any buttom press )
            self.events()
            # update every thing 
            self.update()
            # drow the screen again 
            self.draw()

    # to quit the game when click on the quit buttom    
    def quit(self):
        pygame.quit()
        quit(0)
        
    # will carry all the updates 
    def update(self):
        # Check if the game is Unpaused
        if not self.paused:
            
            # check if the snake eats the food
            if self.food.food_collision():
                # check coords of food part != coords of snake body
                x, y = self.is_body_part()
                self.food.x = x
                self.food.y = y
                # we need to increase the body parts 
                self.snake_parts.append(Snake(self, self.snake_parts[-1].x, self.snake_parts[-1].y))
                self.score += 1

            # update all sprites
            self.all_sprites.update()

            # track and move the body parts
            x, y = self.head.x, self.head.y
            # create a looping to loop through the list of body parts 
            for body in self.snake_parts:
                temp_x, temp_y = body.x, body.y
                body.x, body.y = x, y
                x, y = temp_x, temp_y
            
            # update the orientation value to set the direction of the snake depends on which key we pressed.
            # 0 --> right 
            if self.orientation == 0:
                self.head.x += 1
            # 1 --> Up
            elif self.orientation == 1:
                self.head.y -= 1
            # 2 --> Left
            elif self.orientation == 2:
                self.head.x -= 1
            # 3 --> Down
            elif self.orientation == 3:
                self.head.y += 1

            # check for body collision
            for body in self.snake_parts:
                if body.body_collision():
                    self.playing = False

            # send snake to other side of the screen
            # if the snake go to the right side i come back to the left side 
            if self.head.x > GRIDWIDTH - 1:
                self.head.x = 0
            # if the snake go to the left side i come back to the right side 
            elif self.head.x < 0:
                self.head.x = GRIDWIDTH
            # if the snake go to the up side i come back to the down side 
            elif self.head.y > GRIDHEIGHT - 1:
                self.head.y = 0
            # if the snake go to the down side i come back to the up side 
            elif self.head.y < 0:
                self.head.y = GRIDHEIGHT
    
    # draw the grids on the screen 
    def draw_grid(self):
        # loop to drow 32 horizontal lines, every 32 pixels we will draw one line  
        for row in range(0, WIDTH, TILESIZE):    
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, HEIGHT))
            
        # loop to drow 32 vitical lines, every 32 pixels we will draw one line 
        for col in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (WIDTH, col))

    def draw(self):
        # clear the screan before updatethe snake movment
        self.screen.fill(BGCOLOUR)
        # to draw the sprites group (all of the snake) 
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        if self.paused:
            UIElement(10, 10, "PAUSED").draw(self.screen, 100)
        # we need to flip the screen every time we call draw function 
        pygame.display.flip()

    # catch all events
    def events(self):
        # loop through the events 
        for event in pygame.event.get():
            
            # if we pressing the X button and want to close the game 
            if event.type == pygame.QUIT:
                self.quit()
            # check if we press eny key on the keyboard
            if event.type == pygame.KEYDOWN:
                if not self.paused:
                    # we press up arrow key or W key 
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        # check if the orientation is not the opposit, to avoid killing my self.
                        if not self.orientation == 3:
                            self.orientation = 1
                    # we press down arrow key or S key 
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        # check if the orientation is not the opposit, to avoid killing my self.
                        if not self.orientation == 1:
                            self.orientation = 3
                    # we press right arrow key or D key 
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        # check if the orientation is not the opposit, to avoid killing my self.
                        if not self.orientation == 0:
                            self.orientation = 2
                    # we press left arrow key or A key 
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        # check if the orientation is not the opposit, to avoid killing my self.
                        if not self.orientation == 2:
                            self.orientation = 0
                # pause the game if we press spacebar button
                if event.key == pygame.K_SPACE:
                    # we are invert every time (play <-> pause)
                    self.paused = not self.paused

    def get_high_score(self):
        with open("high_score.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self):
        with open("high_score.txt", "w") as file:
            if self.score > self.high_score:
                file.write(str(self.score))
            else:
                file.write(str(self.high_score))

    def main_screen(self):
        self.save_score()
        self.screen.fill(BGCOLOUR)
        if not self.playing:
            UIElement(8, 7, "GAME OVER!").draw(self.screen, 100)
            UIElement(14, 13, f"Score: {self.score}").draw(self.screen, 30)
        else:
            UIElement(8, 7, "SNAKE GAME").draw(self.screen, 100)

        UIElement(13, 11, f"High Score: {self.high_score if self.high_score > self.score else self.score}").draw(self.screen, 30)

        # buttons
        self.start_button = Button(self, BGCOLOUR, WHITE, WIDTH / 2 - (150/2), 470, 150, 50, "START")
        self.quit_button = Button(self, BGCOLOUR, WHITE, WIDTH / 2 - (150/2), 545, 150, 50, "QUIT")
        # to wait in the screen untill an action
        self.wait()

    def wait(self):
        waiting = True
        while waiting:
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                # to avoid gliching and not responding page 
                if event.type == pygame.QUIT:
                    self.quit()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    if self.start_button.is_over(mouse_x, mouse_y):
                        self.start_button.colour = LIGHTGREY
                    else:
                        self.start_button.colour = BGCOLOUR
                    if self.quit_button.is_over(mouse_x, mouse_y):
                        self.quit_button.colour = LIGHTGREY
                    else:
                        self.quit_button.colour = BGCOLOUR
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_over(mouse_x, mouse_y):
                        waiting = False
                    if self.quit_button.is_over(mouse_x, mouse_y):
                        self.quit()


game = Game()
while True:
    game.main_screen()
    game.new()
    game.run()