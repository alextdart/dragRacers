import pygame
import pygame.freetype
# import random

pygame.init()

# Setting up window
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Alex Dart's Drag Racers")

# Globals
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
top_pos = [10, 220]
bot_pos = [10, 420]
done = False
font = pygame.freetype.Font('resources/fonts/joystix monospace.ttf', 60)

# Setting starting variables.
scene = "Title"
controllable = False
last_click = 0
volume = 50

# Helper Functions


def hover_check(b, mouse_pos):
    if b.rect.left < mouse_pos[0] < b.rect.right and b.rect.top < mouse_pos[1] < b.rect.bottom:
        return True
    else:
        return False


def click_check(b, mouse_pos, mouse_btns, recent_click_time):
    current_tick = pygame.time.get_ticks()
    if b.rect.left < mouse_pos[0] < b.rect.right and b.rect.top < mouse_pos[1] < b.rect.bottom:
        if mouse_btns[0] == 1 and ((current_tick - 100) > recent_click_time):
            button_sound.play()
            return True
    else:
        return False

# Creating Classes


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Button(pygame.sprite.Sprite):
    def __init__(self, image_file, image_hover, location):
        pygame.sprite.Sprite.__init__(self)
        self.toggled = False
        self.image_file = pygame.image.load(image_file)
        self.image_hover = pygame.image.load(image_hover)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
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


class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


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
button_sound = pygame.mixer.Sound('resources/sounds/button.wav')

# Backgrounds
bg_title = Background('resources/images/backgrounds/bg_title.png', [0, 0])

# Buttons
btn_title_start = Button('resources/images/buttons/btn_play.png',
                         'resources/images/buttons/btn_play_h.png', [340, 600])
btn_title_opt = Button('resources/images/buttons/btn_title_opt.png',
                       'resources/images/buttons/btn_title_opt_h.png', [670, 600])

btn_opt_back = Button('resources/images/buttons/btn_opt_back.png',
                      'resources/images/buttons/btn_opt_back_h.png', [30, 30])
btn_opt_vol_up = Button('resources/images/buttons/btn_opt_plus.png',
                        'resources/images/buttons/btn_opt_plus_h.png', [320, 400])
btn_opt_vol_dwn = Button('resources/images/buttons/btn_opt_minus.png',
                         'resources/images/buttons/btn_opt_minus_h.png', [860, 400])

# Images
# image_title = Image('resources/images/image_title.png', [0, 0])

# Starting music (-1 makes it play forever).
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    # Gets the state of the mouse and it's location that will be all throughout the program.
    pressed = pygame.mouse.get_pressed(3)
    mouse = pygame.mouse.get_pos()

    if scene == "Title":

        # Button Click Checks
        if click_check(btn_title_start, mouse, pressed, last_click):
            last_click = pygame.time.get_ticks()
            scene = "Selection"

        if click_check(btn_title_opt, mouse, pressed, last_click):
            last_click = pygame.time.get_ticks()
            scene = "Options"

        # Loading Static Images
        window.blit(bg_title.image, bg_title.rect)

        # Loading Dynamic Images
        btn_title_start.hover(hover_check(btn_title_start, mouse))
        btn_title_opt.hover(hover_check(btn_title_opt, mouse))
        window.blit(btn_title_start.image, btn_title_start.rect)
        window.blit(btn_title_opt.image, btn_title_opt.rect)

    elif scene == "Selection":

        # Base Fill
        window.fill(WHITE)

    elif scene == "Options":

        # Base Fill
        window.fill(WHITE)

        # Loading Static Images and Text
        font.render_to(window, (440, 50), "Options:", BLACK)

        # Button Click Checks
        if click_check(btn_opt_back, mouse, pressed, last_click):
            last_click = pygame.time.get_ticks()
            scene = "Title"

        if click_check(btn_opt_vol_up, mouse, pressed, last_click) and volume < 100:
            last_click = pygame.time.get_ticks()
            volume += 5
            pygame.mixer.music.set_volume(volume / 100)

        if click_check(btn_opt_vol_dwn, mouse, pressed, last_click) and volume > 0:
            last_click = pygame.time.get_ticks()
            volume -= 5
            pygame.mixer.music.set_volume(volume / 100)

        # Loading Dynamic Images
        vol_text = font.render("Vol: "+str(volume)+"%", BLACK)
        font.render_to(window, (420, 430), "Vol: "+str(volume)+"%", BLACK)

        # Drawing and Updating Buttons
        btn_opt_back.hover(hover_check(btn_opt_back, mouse))
        window.blit(btn_opt_back.image, btn_opt_back.rect)
        btn_opt_vol_up.hover(hover_check(btn_opt_vol_up, mouse))
        window.blit(btn_opt_vol_up.image, btn_opt_vol_up.rect)
        btn_opt_vol_dwn.hover(hover_check(btn_opt_vol_dwn, mouse))
        window.blit(btn_opt_vol_dwn.image, btn_opt_vol_dwn.rect)

    elif scene == "Game":

        # Loading Static Images (Background).
        window.blit(bg_title.image, bg_title.rect)

        # Loading Dynamic Images (Health).

    elif scene == "Post-Race":

        # Loading Static Images (Background).
        window.fill(WHITE)

    # Update screen, 60fps
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
