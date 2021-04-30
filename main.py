import pygame
import pygame.freetype
import random

pygame.init()

# Setting up window
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Alex Dart's Drag Racers")

# Globals
white = (255, 255, 255)
clock = pygame.time.Clock()
top_pos = [10, 220]
bot_pos = [10, 420]
done = False

# Creating Classes


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


""" The button class """


class Button(pygame.sprite.Sprite):
    def __init__(self, image_file, image_hover, location):
        pygame.sprite.Sprite.__init__(self)
        self.toggled = False
        self.image_file = pygame.image.load(image_file)
        self.image_hover = pygame.image.load(image_hover)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    # Adds hovering functionality to buttons
    def hover(self, mouseover):
        if mouseover:
            self.image = self.image_hover
        else:
            self.image = self.image_file

    # Adds toggle functionality to buttons
    def toggle(self):
        if not self.toggled:
            self.image = self.image_hover
            self.toggled = True
        else:
            self.image = self.image_file
            self.toggled = False

    def reset(self):
        self.toggled = False
        self.image = self.image_file


""" Selectors are like buttons with 3 different options. """


class Selector(pygame.sprite.Sprite):
    def __init__(self, image0, image1, image2, location):
        pygame.sprite.Sprite.__init__(self)
        self.image0 = pygame.image.load(image0)
        self.image1 = pygame.image.load(image1)
        self.image2 = pygame.image.load(image2)
        self.image = pygame.image.load(image0)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def selection(self, value):
        if value == 0:
            self.image = self.image0
        elif value == 1:
            self.image = self.image1
        else:
            self.image = self.image2


""" Images are just like backgrounds. Really, I didn't need to separate them. """


class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


""" The player """


class Player(pygame.sprite.Sprite):
    def __init__(self, car):
        super().__init__()

        self.car = car
        self.speed = 0
        self.location = (0, 0)

        if self.car == 0:
            self.image = pygame.image.load('resources/images/sprites/car_red.png')
            self.base_speed = 10
            self.gear_ratio = 1.25
            self.gear = 0
            self.max_gear = 6
            self.nitro_pct = 100
        elif self.car == 1:
            self.image = pygame.image.load('resources/images/sprites/car_purple.png')
            self.base_speed = 12.5
            self.gear_ratio = 1.5
            self.gear = 0
            self.max_gear = 6
            self.nitro_pct = 100
        else:
            self.image = pygame.image.load('resources/images/sprites/car_red.png')
            self.base_speed = 15
            self.gear_ratio = 1.1
            self.gear = 0
            self.max_gear = 6
            self.nitro_pct = 100
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.location

    def upshift(self, quality):
        if self.gear > self.max_gear:
            if self.gear == 0:
                self.gear = 1
                self.speed = self.base_speed
            else:
                self.gear += 1
                if quality == "poor":
                    self.speed = self.speed * (self.gear_ratio * 0.2)
                elif quality == "okay":
                    self.speed = self.speed * (self.gear_ratio * 0.7)
                elif quality == "good":
                    self.speed = self.speed * (self.gear_ratio * 1)
                elif quality == "perf":
                    self.speed = self.speed * (self.gear_ratio * 1.3)


""" The com class is almost identical to the player class, except with slight random variations based on the difficulty
selected by the user. It also has the fire and update methods, for the same reason as the players. One difference is
that it doesn't have a direction indicator, as it can only be on the right side. """

"""
class Opponent(pygame.sprite.Sprite):
    def __init__(self, diffvalue, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/players/com_ship.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.health = 100
        self.lastshot = pygame.time.get_ticks()
        if diffvalue == 0:
            self.movespeed = 3
            self.velocity = random.randint(8, 18)
            self.firerate = random.randint(600, 900)
            self.damage = random.randint(3, 12)
        elif diffvalue == 1:
            self.movespeed = 6
            self.velocity = random.randint(15, 30)
            self.firerate = random.randint(300, 700)
            self.damage = random.randint(9, 21)
        else:
            self.movespeed = 8
            self.velocity = random.randint(25, 50)
            self.firerate = random.randint(100, 500)
            self.damage = random.randint(15, 30)

    def fire(self):
        time = pygame.time.get_ticks()
        if time - self.lastshot >= self.firerate:
            self.lastshot = time
            bullets.append(Bullet('resources/images/image_laser.png', -1, player,
                                  self.velocity, self.damage, [self.rect.left + 40, self.rect.top + 40]))
            shot.play()

    def update(self):
        if self.health <= 0:
            self.image = pygame.image.load('resources/images/image_ship_exploded.png')
"""

""" Creating Objects """

# Sounds
music = pygame.mixer.music.load('resources/sounds/music.mp3')
button = pygame.mixer.Sound('resources/sounds/button.wav')

# Backgrounds
bg_title = Background('resources/images/backgrounds/bg_title.png', [0, 0])

# Buttons
button_start = Button('resources/images/buttons/button_play.png',
                      'resources/images/buttons/button_play_hover.png', [340, 600])
button_options = Button('resources/images/buttons/button_options.png',
                        'resources/images/buttons/button_options_hover.png', [670, 600])

# Images
# image_title = Image('resources/images/image_title.png', [0, 0])

# Setting starting variables.
scene = "Title"
controllable = False

# Starting music (-1 makes it play forever).
pygame.mixer.music.play(-1)

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    # Gets the state of the mouse and it's location that will be all throughout the program.
    pressed = pygame.mouse.get_pressed(3)
    mouse = pygame.mouse.get_pos()

    if scene == "Title":

        # Checking for Start Button Hover
        if 340 < mouse[0] < 610 and 600 < mouse[1] < 700:
            hovering_play = True
            if pressed[0] == 1:
                scene = "Selection"
                button.play()
        else:
            hovering_play = False

        # Checking for Options Button Hover
        if 670 < mouse[0] < 920 and 600 < mouse[1] < 700:
            hovering_options = True
            if pressed[0] == 1:
                scene = "Options"
                button.play()
        else:
            hovering_options = False

        # Loading Static Images
        window.blit(bg_title.image, bg_title.rect)

        # Loading Dynamic Images
        button_start.hover(hovering_play)
        button_options.hover(hovering_options)
        window.blit(button_start.image, button_start.rect)
        window.blit(button_options.image, button_options.rect)

    elif scene == "Selection":

        # Base Fill
        window.fill(white)

    elif scene == "Options":

        # Base Fill
        window.fill(white)

    elif scene == "Game":

        # Loading Static Images (Background).
        window.blit(bg_title.image, bg_title.rect)

        # Loading Dynamic Images (Health).

    elif scene == "Post-Race":

        # Loading Static Images (Background).
        window.fill(white)

    # Update screen, 60fps
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
