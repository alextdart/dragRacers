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
last_shift = 0
volume = 50
multiplayer = False
sp_car_choice = 0
mp_car1_choice = 0
mp_car2_choice = 0
pause = 0
gear_pct = 0

# Helper Functions


def get_shift_quality(pct):
    if pct < 45:
        return "poor"
    elif pct < 65:
        return "okay"
    elif pct < 85:
        return "good"
    elif pct < 95:
        return "perf"
    else:
        return "good"


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
    def __init__(self, car, location):
        super().__init__()

        self.car = car
        self.speed = 0

        self.location = location

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
            self.image = pygame.image.load('resources/images/sprites/car_green.png')
            self.base_speed = 15
            self.gear_ratio = 1.1
            self.gear = 0
            self.max_gear = 6
            self.nitro_pct = 100
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.location

    def upshift(self, quality, recent_shift):
        current_tick = pygame.time.get_ticks()
        if (current_tick - 100) > recent_shift:
            if self.gear < self.max_gear:
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

    def update(self):
        self.location = [self.location[0]+self.speed, self.location[1]]


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

btn_sel_sp_left = Button('resources/images/backgrounds/275x720blank.png',
                         'resources/images/backgrounds/275x720blank.png', [365, 150])
btn_sel_sp_right = Button('resources/images/backgrounds/275x720blank.png',
                          'resources/images/backgrounds/275x720blank.png', [640, 150])
btn_sel_mp_left_left = Button('resources/images/backgrounds/275x720blank.png',
                              'resources/images/backgrounds/275x720blank.png', [25, 150])
btn_sel_mp_left_right = Button('resources/images/backgrounds/275x720blank.png',
                               'resources/images/backgrounds/275x720blank.png', [300, 150])
btn_sel_mp_right_left = Button('resources/images/backgrounds/275x720blank.png',
                               'resources/images/backgrounds/275x720blank.png', [665, 150])
btn_sel_mp_right_right = Button('resources/images/backgrounds/275x720blank.png',
                                'resources/images/backgrounds/275x720blank.png', [940, 150])
btn_sel_multiplayer = Button('resources/images/buttons/btn_toggle_sp_mp.png',
                             'resources/images/buttons/btn_toggle_sp_mp_h.png', [1100, 15])
btn_sel_play_sp = Button('resources/images/buttons/btn_play.png',
                         'resources/images/buttons/btn_play_h.png', [1000, 600])
btn_sel_play_mp = Button('resources/images/buttons/btn_play.png',
                         'resources/images/buttons/btn_play_h.png', [515, 20])

# Selectors
sel_sp_cars = Selector('resources/images/selectors/sel_car1.png',
                       'resources/images/selectors/sel_car2.png',
                       'resources/images/selectors/sel_car3.png', [365, 0])

sel_mp_car1 = Selector('resources/images/selectors/sel_car1.png',
                       'resources/images/selectors/sel_car2.png',
                       'resources/images/selectors/sel_car3.png', [25, 0])
sel_mp_car2 = Selector('resources/images/selectors/sel_car1.png',
                       'resources/images/selectors/sel_car2.png',
                       'resources/images/selectors/sel_car3.png', [665, 0])

# Images
image_shift_bar = Image('resources/images/sprites/shift_bar.png', [0, 0])
image_shift_slider = Image('resources/images/sprites/shift_slider.png', [20, 675])

# Starting music (-1 makes it play forever).
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)

# Players
player = Player(0, top_pos)
mp_p1 = Player(0, top_pos)
mp_p2 = Player(0, bot_pos)

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

        if click_check(btn_sel_multiplayer, mouse, pressed, last_click):
            last_click = pygame.time.get_ticks()
            btn_sel_multiplayer.toggle()
            multiplayer = not multiplayer

        if not multiplayer:

            # Button Click Checks
            if click_check(btn_sel_play_sp, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                player = Player(sp_car_choice, top_pos)
                pause = 100
                scene = "Game"

            if click_check(btn_sel_sp_left, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                if sp_car_choice > 0:
                    sp_car_choice -= 1
                else:
                    sp_car_choice = 2
                sel_sp_cars.selection(sp_car_choice)

            if click_check(btn_sel_sp_right, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                if sp_car_choice < 2:
                    sp_car_choice += 1
                else:
                    sp_car_choice = 0
                sel_sp_cars.selection(sp_car_choice)

            # Drawing and Updating Buttons
            btn_sel_play_sp.hover(hover_check(btn_sel_play_sp, mouse))
            window.blit(btn_sel_play_sp.image, btn_sel_play_sp.rect)

            window.blit(sel_sp_cars.image, sel_sp_cars.rect)

        else:

            # Button Click Checks
            if click_check(btn_sel_play_mp, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                player1 = Player(mp_car1_choice, top_pos)
                player2 = Player(mp_car2_choice, bot_pos)
                pause = 100
                scene = "Game"

            if click_check(btn_sel_mp_left_left, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                if mp_car1_choice > 0:
                    mp_car1_choice -= 1
                else:
                    mp_car1_choice = 2
                sel_mp_car1.selection(mp_car1_choice)

            if click_check(btn_sel_mp_left_right, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                if mp_car1_choice < 2:
                    mp_car1_choice += 1
                else:
                    mp_car1_choice = 0
                sel_mp_car1.selection(mp_car1_choice)

            if click_check(btn_sel_mp_right_left, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                if mp_car2_choice > 0:
                    mp_car2_choice -= 1
                else:
                    mp_car2_choice = 2
                sel_mp_car2.selection(mp_car2_choice)

            if click_check(btn_sel_mp_right_right, mouse, pressed, last_click):
                last_click = pygame.time.get_ticks()
                if mp_car2_choice < 2:
                    mp_car2_choice += 1
                else:
                    mp_car2_choice = 0
                sel_mp_car2.selection(mp_car2_choice)

            # Drawing and Updating Buttons
            btn_sel_play_mp.hover(hover_check(btn_sel_play_mp, mouse))
            window.blit(btn_sel_play_mp.image, btn_sel_play_mp.rect)

            window.blit(sel_mp_car1.image, sel_mp_car1.rect)
            window.blit(sel_mp_car2.image, sel_mp_car2.rect)

        window.blit(btn_sel_multiplayer.image, btn_sel_multiplayer.rect)

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

        # Base Fill
        window.fill(WHITE)

        if not multiplayer:  # single player

            if pause > 1:
                pause -= 1

            elif pause == 1:

                player.upshift("good", last_shift)
                pause = 0

            if pause == 0:

                if gear_pct < 100:
                    gear_pct += 0.5
                    image_shift_slider.rect.left = (gear_pct/100)*1280
                else:
                    player.blow_up()

                # Checks which keys are pressed, makes a list.
                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE]:
                    player.upshift(get_shift_quality(gear_pct), last_shift)
                    last_shift = pygame.time.get_ticks()
                    gear_pct = 0

            font.render_to(window, (420, 430), "Gear: " + str(player.gear), BLACK)
            window.blit(image_shift_bar.image, image_shift_bar.rect)
            window.blit(image_shift_slider.image, image_shift_slider.rect)
            # window.blit(player.image, player.rect)

        else:  # multiplayer

            window.blit(player1.image, player1.rect)
            window.blit(player2.image, player2.rect)

        # Loading Static Images (Background)

        # Loading Dynamic Images (HUD)

    elif scene == "Post-Race":

        # Loading Static Images (Background).
        window.fill(WHITE)

    # Update screen, 60fps
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
