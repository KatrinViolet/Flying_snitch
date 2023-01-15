import pygame
import random

pygame.init()
pygame.mixer.init()


class Players:
    def __init__(self, win):
        self.win = win

        self.snitch_list = []
        img = pygame.image.load(f'snitch1.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        img = pygame.image.load(f'snitch2.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        img = pygame.image.load(f'snitch5.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        img = pygame.image.load(f'snitch2.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        img = pygame.image.load(f'snitch1.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        img = pygame.image.load(f'snitch3.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        img = pygame.image.load(f'snitch4.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        img = pygame.image.load(f'snitch3.png')
        img = pygame.transform.scale(img, (50, 32.5))
        self.snitch_list.append(img)
        self.index = 0
        self.image = self.snitch_list[self.index]
        # rectangle around the character
        self.rect = self.image.get_rect()
        self.rect.x = 140
        self.rect.y = int(display_height) // 2
        # information about jumps
        self.counter = 0
        self.vel = 0
        self.jumped = True
        self.alive = True
        self.theta = 0
        self.mid_pos = display_height // 2
        self.flap_pos = 0
        self.flap_inc = 1

    def update(self):
        # GRAVITY
        self.vel += 0.75
        # speed adjustment
        if self.vel >= 8:
            self.vel = 8
        # ground collision check
        if self.rect.bottom <= display_height:
            self.rect.y += int(self.vel)
        # if the hero is alive
        if self.alive:

            # JUMP
            # check if the mouse is pressed to jump
            if pygame.mouse.get_pressed()[0] == 1 and not self.jumped:
                wing_s.play()
                self.jumped = True
                self.vel = -9
            if pygame.mouse.get_pressed()[0] == 0:
                self.jumped = False

            self.flap_counter()

            self.image = pygame.transform.rotate(self.snitch_list[self.index], self.vel * -2)
        else:
            # ground collision check
            if self.rect.bottom <= display_height:
                self.theta -= 2
            self.image = pygame.transform.rotate(self.snitch_list[self.index], self.theta)

        self.win.blit(self.image, self.rect)

    def flap_counter(self):
        # ANIMATION
        self.counter += 1
        # zeroing the jump counter
        if self.counter > 5:
            self.counter = 0
            self.index += 1
        # reset jump groups counter
        if self.index >= 3:
            self.index = 0

    def draw_flap(self):
        # jump animation
        self.flap_counter()
        if self.flap_pos <= -10 or self.flap_pos > 10:
            self.flap_inc *= -1
        self.flap_pos += self.flap_inc
        self.rect.y += self.flap_inc
        self.rect.x = 130
        self.image = self.snitch_list[self.index]
        self.win.blit(self.image, self.rect)

    def reset(self):
        self.index = 0
        self.image = self.snitch_list[self.index]
        # rectangle around the character
        self.rect = self.image.get_rect()
        self.rect.x = 140
        self.rect.y = int(display_height) // 2
        # information about jumps
        self.counter = 0
        self.vel = 0
        self.jumped = False
        self.alive = True
        self.theta = 0
        self.mid_pos = display_height // 2
        self.flap_pos = 0
        self.flap_inc = 1

    def y_coord(self):
        m = self.rect.y
        return m


class Base:
    def __init__(self, win, image):
        self.win = win
        self.image1 = image
        # creating 2 platforms
        self.image2 = self.image1
        # infinite track
        self.rect1 = self.image1.get_rect()
        self.rect1.x = 0
        self.rect1.y = int(display_height) + 25
        self.rect2 = self.image2.get_rect()
        self.rect2.x = WIDTH
        self.rect2.y = int(display_height) + 25

    def update(self, speed):
        # infinite track links movement
        self.rect1.x -= speed * 0.5
        self.rect2.x -= speed * 0.5
        if self.rect1.right <= 0:
            self.rect1.x = WIDTH
        if self.rect2.right <= 0:
            self.rect2.x = WIDTH

        self.win.blit(self.image1, self.rect1)
        self.win.blit(self.image2, self.rect2)

    def new_game(self, image):
        self.image1 = image
        # creating 2 platforms
        self.image2 = self.image1


# Ring class
class Ring(pygame.sprite.Sprite):
    def __init__(self, window, ring_image, y_pos, flip_position, gap):
        super(Ring, self).__init__()

        self.win = window
        self.image = ring_image
        self.rect = self.image.get_rect()
        # half distance between the rings
        x_pos = WIDTH

        if flip_position:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x_pos, y_pos - gap)
        else:
            self.rect.topleft = (x_pos, y_pos + gap)

    def update(self, speed):
        self.rect.x -= speed
        # removal of unnecessary rings
        if self.rect.right < 0:
            self.kill()
        self.win.blit(self.image, self.rect)


class Score:
    def __init__(self, x, y, win):
        # creating a list with numbers
        self.score_list = []
        for score in range(10):
            score_img = pygame.image.load(f'Score/{score}.png')
            self.score_list.append(score_img)
            self.x = x
            self.y = y

        self.win = win

    def update(self, score):
        # counting display
        score = str(score)
        for index, num in enumerate(score):
            self.image = self.score_list[int(num)]
            self.rect = self.image.get_rect()
            self.rect.topleft = self.x - 15 * len(score) + 30 * index, self.y
            self.win.blit(self.image, self.rect)


class Button:
    def __init__(self, value, color, x_pos, y_pos, button_width, button_height, window, text=''):
        self.value = value
        self.color = color
        self.x = x_pos
        self.y = y_pos
        self.width = button_width
        self.height = button_height
        self.text = text
        self.win = window
        self.font = pygame.font.SysFont(None, 24)

    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height), 0)
        text = self.font.render(self.text, True, BLACK)
        self.win.blit(text,
                      (self.x + (self.width / 2 - text.get_width() / 2),
                       self.y + (self.height / 2 - text.get_height() / 2)))

    def mouse_is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def check_mouse(self) -> bool:
        if pygame.mouse.get_pressed()[0] == 1:
            if self.mouse_is_over(pygame.mouse.get_pos()):
                print(f"{self.text} is clicked")
                return True
        return False


class DistanceSelector:
    def __init__(self, window, default_distance=1):
        self.win = window
        self.current_distance = 65
        self.font = pygame.font.SysFont(None, 32)

        self.buttons = []

        self.y_pos = 100
        x_pos = 350
        button_width = 32
        button_height = 32

        for b in range(5):
            v = 2 * (35 + 10 * (b + 1))
            self.buttons.append(
                Button(v, WHITE, x_pos, self.y_pos, button_width, button_height, window, f"{v}"))
            x_pos += button_width + 20

    def draw_caption(self):
        distance_info = f"Distance: {self.current_distance * 2}"

        img = self.font.render(distance_info, True, BLACK)
        rect = img.get_rect()
        rect.y += self.y_pos
        self.win.blit(img, (200, rect.y + 5))

    def draw(self):
        self.draw_caption()
        for button in self.buttons:
            button.draw()

    def check_mouse(self) -> bool:
        for button in self.buttons:
            if button.check_mouse():
                self.current_distance = button.value // 2
                return True
        return False

    def set_distance(self):
        return int(self.current_distance)


class ScoreSaver:
    def __init__(self, path_to_file: str, window):
        self.win = window
        self.best_score = 0
        self.you_best_score = 0
        self.path_to_file = path_to_file

        self.font = pygame.font.SysFont(None, 24)

        # попытка чтения из файла
        try:
            with open(self.path_to_file) as f:
                line = f.readline()
                self.best_score = int(line)
        except:
            print(f"Error read from {path_to_file}")

    # update scrore with new value
    def update_score(self, new_score: int):
        self.best_score = max(self.best_score, new_score)
        self.you_best_score = max(self.you_best_score, new_score)

    # save best score to file
    def save(self):
        # open to write text
        with open(self.path_to_file, "w+") as f:
            f.write(str(self.best_score))

    # draw score info as text
    def draw_score(self):
        score_info = f"best = {self.best_score}, you = {self.you_best_score}"

        img = self.font.render(score_info, True, BLACK)
        self.win.blit(img, (20, 15))


# TIME
fps = 30
clock = pygame.time.Clock()
# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 90, 80)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# DISPLAY
HEIGHT = 400
WIDTH = 800
SCREEN = WIDTH, HEIGHT
screen = pygame.display.set_mode(SCREEN)
# point of death of the hero from the fall
display_height = 0.80 * HEIGHT
info = pygame.display.Info()
width = info.current_w
height = info.current_h
if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
# SOUNDS
# sound of death
die_s = pygame.mixer.Sound('Sounds/die.wav')
# impact sound
hit_s = pygame.mixer.Sound('Sounds/hit.wav')
# the sound of the ring passing
point_s = pygame.mixer.Sound('Sounds/point.wav')
# jump sound
wing_s = pygame.mixer.Sound('Sounds/wing.wav')
# victory sound
win_s = pygame.mixer.Sound('Sounds/win.wav')
# BACKGROUND
pygame.display.set_caption("Quiddich")
screen.fill(pygame.Color('BLACK'))
# brick width
w = 90
# brick height
h = 45
# number of bricks in a row
m = 1200 // (w + 2) + 1
# number of brick rows
n = 800 // (h + 2) + 1
y = 0
# brick painting
for i in range(n):
    if i % 2 == 0:
        x = 0
    else:
        x = -w // 2
    for j in range(m):
        pygame.draw.rect(screen, RED, (x, y, w, h))
        x += w + 2
    y += h + 2
logo = pygame.image.load('logo.png')
logo = pygame.transform.scale(logo, (WIDTH // 2, HEIGHT // 2))
# seconds to sky
i = 20
while i != 0:
    l_g = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    i -= 1
    screen.blit(logo, l_g)
    clock.tick(fps)
    pygame.display.update()
clock.tick(fps)
pygame.display.flip()
# SKY
sky_choice = random.choice(['1', '2', ''])
sky = pygame.image.load(f'sky{sky_choice}.png')
sky = pygame.transform.scale(sky, (WIDTH * 1.25, HEIGHT * 1.25))
# sky movement
x = -1000
while x <= -100:
    gm_r = sky.get_rect(center=(x, 150))
    x += 40
    screen.blit(sky, gm_r)
    clock.tick(fps)
    pygame.display.update()
# START BUTTON
start_button = pygame.image.load('start_button.png')
start_button = pygame.transform.scale(start_button, (400, 100))
s_b = start_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(start_button, s_b)
pygame.display.update()
# FINISH
gameover_note = pygame.image.load('gameover.png')
# OBJECTS
base_choice = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', ''])
image = pygame.image.load(f'base{base_choice}.png')
base = Base(win, image)
score_img = Score(WIDTH // 2, 50, win)
player = Players(win)
hand = pygame.image.load('hand.png')
hand = pygame.transform.scale(hand, (100, 75))
scoreSaver = ScoreSaver("best.txt", win)
distanceSelector = DistanceSelector(win, 2)
ring_group = pygame.sprite.Group()
# WORK
base_height = display_height
speed = 0
game_started = False
game_over = False
restart = False
score = 0
start_screen = True
ring_choice = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', ''])
ring_img = pygame.image.load(f'ring{ring_choice}.png')

ring_pass = False
ring_frequency = 1600
running = True
last_ring = pygame.time.get_ticks()
while running:
    bg = sky
    win.blit(bg, (0, 0))

    if start_screen:
        speed = 0
        win.blit(start_button, (200, 150))
        distanceSelector.draw()

    else:
        # if the game goes on
        win.blit(hand, (-20, player.y_coord() - 20))
        if game_started and not game_over:
            player.draw_flap()
            base.update(speed)

            next_ring = pygame.time.get_ticks()
            # when it's time to add rings
            if next_ring - last_ring >= ring_frequency:
                y = display_height // 2
                ring_pos = random.choice(range(-100, 100, 4))
                height = y + ring_pos
                # glue the top and bottom
                top = Ring(win, ring_img, height, True, distanceSelector.current_distance)
                bottom = Ring(win, ring_img, height, False, distanceSelector.current_distance)
                ring_group.add(top)
                ring_group.add(bottom)
                last_ring = next_ring

        # update everything
        ring_group.update(speed)
        base.update(speed)
        player.update()
        score_img.update(score)
        scoreSaver.draw_score()

        # collision with the rings
        if pygame.sprite.spritecollide(player, ring_group, False) or player.rect.top <= 0:
            game_started = False
            if player.alive:
                hit_s.play()
                die_s.play()
            player.alive = False
            player.theta = player.vel * -2

        # falling to the ground
        if player.rect.bottom >= display_height:
            speed = 0
            game_over = True

        # ring passing
        if len(ring_group) > 0:
            p = ring_group.sprites()[0]

            if player.rect.right > p.rect.left and player.rect.right < p.rect.right and not ring_pass and player.alive:
                ring_pass = True

            if ring_pass:
                if player.rect.left > p.rect.right:
                    ring_pass = False
                    score += 1
                    point_s.play()
                    # update score
                    scoreSaver.update_score(score)

    # finish the game
    if not player.alive:
        win.blit(gameover_note, (150, 125))

    # reactions to player actions
    for e in pygame.event.get():
        # window is closed
        if e.type == pygame.QUIT:
            running = False
        # pressed a button on the keyboard
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE or \
                    e.key == pygame.K_q:
                running = False
        # check only if is start screen
        if start_screen and distanceSelector.check_mouse():
            continue
        # mouse button pressed
        if e.type == pygame.MOUSEBUTTONDOWN:
            if start_screen:
                # SKY IMAGE CHOICE
                sky_choice = random.choice(['1', '2', '3', ''])
                sky = pygame.image.load(f'sky{sky_choice}.png')
                sky = pygame.transform.scale(sky, (WIDTH * 1.25, HEIGHT * 1.25))
                # RING IMAGE CHOICE
                ring_choice = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', ''])
                ring_img = pygame.image.load(f'ring{ring_choice}.png')
                # BASE IMAGE CHOICE
                base_choice = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', ''])
                image = pygame.image.load(f'base{base_choice}.png')
                base.new_game(image)
                # game started
                game_started = True
                speed = 2
                start_screen = False
                game_over = False
                last_ring = pygame.time.get_ticks() - ring_frequency
                next_ring = 0
                ring_group.empty()

                speed = 4
                score = 0

            if game_over:
                # back to startscreen
                start_screen = True
                player = Players(win)
                ring_img = pygame.image.load('ring.png')
                bg = sky

    clock.tick(fps)
    pygame.display.update()
# game is over -> save score
scoreSaver.save()
pygame.quit()
