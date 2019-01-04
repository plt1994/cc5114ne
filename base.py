import math
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Ball(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, surface: pygame.Surface):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([10, 10])

        # Color the ball
        self.image.fill(WHITE)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Speed in pixels per cycle
        self.speed = 0

        # Floating point representation of where the ball is
        self.x = 350
        self.y = 250

        # Direction of ball in degrees
        self.direction = 0

        # Height and width of the ball
        self.width = 10
        self.height = 10

        # Set the initial ball speed and position
        self.players = []
        self.font = pygame.font.Font(None, 36)
        self.font2 = pygame.font.Font(None, 80)


        self.surface = surface

        self.p1 = 0
        self.p1bounce = 0
        self.p2 = 0
        self.p2bounce = 0

        self.reset()





    def linkPlayers(self, list:list):
        for i in list:
            self.players.append(i)

    def reset(self):
        pygame.time.wait(500)
        self.p2bounce, self.p1bounce = 0, 0
        self.x = 350
        self.y = 250
        self.speed = 8.0
        for p in self.players:
            p.reset()

        # Direction of ball (in degrees)
        self.direction = random.randrange(45, 135)

        # Flip a 'coin'
        if random.randrange(2) == 0:
            # Reverse ball direction, let the other guy get it first
            self.direction += 180

    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce(self):
        self.direction += 180 - 2 * self.direction
        self.direction%=360

    # Update the position of the ball
    def update(self):
        #score
        scoreprint = "Player 1: " + str(self.p1)
        textp1 = self.font.render(scoreprint, 1, WHITE)
        textpos1 = (0, 0)
        self.surface.blit(textp1, textpos1)

        scoreprint = "CPU: " + str(self.p2)
        text = self.font.render(scoreprint, 1, WHITE)
        textpos = (600, 0)
        self.surface.blit(text, textpos)

        #bounces
        scoreprintbouncep1 = str(self.p1bounce)
        textbouncep1 = self.font.render(scoreprintbouncep1, 1, WHITE)
        textbouncepos1 = (0, 30)
        self.surface.blit(textbouncep1, textbouncepos1)

        scoreprintbouncep2 = str(self.p2bounce)
        textbouncep2 = self.font.render(scoreprintbouncep2, 1, WHITE)
        textbouncepos2 = (600, 30)
        self.surface.blit(textbouncep2, textbouncepos2)

        self.rect.centerx = self.x
        self.rect.centery = self.y
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        if self.speed>12.0:
            self.speed=12

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        if self.x < 0:
            self.p2+=1
            self.reset()

        if self.x > 700:
            self.p1+=1
            self.reset()

        # Move the image to where our x and y are

        # Do we bounce off the left of the screen?
        if self.y>500:
            self.bounce()
            self.y = 495
        if self.y<0:
            self.bounce()
            self.y = 5

        # Do we bounce of the right side of the screen?

    def draw(self):
        self.surface.blit(self.image, self.rect)


    def bouncep1(self):
        self.speed+=0.1
        self.direction = random.randint(45,135)
        self.p1bounce+=1

    def bouncep2(self):
        self.speed += 0.1
        self.direction = 180+ random.randint(45, 135)
        self.p2bounce+=1


# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, xpos, ypos):
        # Call the parent's constructor
        super().__init__()

        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.height,self.width])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = xpos
        self.rect.centery = ypos

        self.surface = None

        self.up = False
        self.down = False

    def set_surface(self, surface:pygame.Surface):
        self.surface = surface

    def cpumove(self, ball:Ball):
        if ball.rect.top< self.rect.top and ball.rect.x>400:
            self.moveup()
        if ball.rect.bottom > self.rect.bottom and ball.rect.x>400:
            self.movedown()


    def draw(self):
        self.surface.blit(self.image, self.rect)

    # Update the player
    def update(self):
        if self.up:
            self.moveup()
        if self.down:
            self.movedown()

    def moveup(self):
        self.move(-10)

    def movedown(self):
        self.move(10)

    def move(self, param): #####checkear esto
        self.rect.centery += param
        if self.rect.bottom>500 or self.rect.top<0:
            self.rect.centery -= param

    def reset(self):
        self.rect.centery = 250


def start():

    # Define some colors
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (700, 500)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    #players creation
    p1 = Player(10,250)
    cpu = Player(675, 250)
    p1.set_surface(screen)
    cpu.set_surface(screen)
    ball = Ball(screen)
    list = [p1, cpu]
    ball.linkPlayers(list)


    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        data = [ball.direction, ball.x, ball.y, ball.speed, p1.rect.y]
        score = [ball.p1, ball.p1bounce, ball.p2, ball.p2bounce]
        print(data, score)

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # --- Game logic should go here
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p1.up = True
                    p1.down = False
                if event.key == pygame.K_DOWN:
                    p1.down = True
                    p1.up = False
                if event.key == pygame.K_a:
                    ball.reset()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    p1.up = False
                if event.key == pygame.K_DOWN:
                    p1.down = False

        if p1.rect.colliderect(ball.rect):
            ball.bouncep1()
            ball.x = p1.rect.right+5

        if cpu.rect.colliderect(ball.rect):
            ball.bouncep2()
            ball.x = cpu.rect.left - 5


        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
        p1.draw()
        cpu.draw()
        ball.draw()
        ball.update()
        p1.update()
        cpu.cpumove(ball)

        # --- Drawing code should go here

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        #when we finish a game
        if ball.p1bounce == 5:
            done = True

    screen.fill(WHITE)
    pygame.display.flip()
    textp1 = ball.font2.render('GAME OVER', 1, BLACK)
    textpos1 = (200, 300)
    screen.blit(textp1, textpos1)
    pygame.display.flip()
    pygame.time.wait(2000)
    # Close the window and quit.
    pygame.quit()

start()