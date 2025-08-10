import pygame
from pygame import mixer
import sys
import os

# ---------- paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset(*parts):
    return os.path.join(BASE_DIR, *parts)

# ---------- init ----------
mixer.init()
pygame.init()

game_over = False
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
spd = 3
dir_y = -1
dir_x = -1
loc_y = SCREEN_HEIGHT - 100
loc_x = SCREEN_WIDTH - 100
rad = 5
font_size = 35  # font size

font = pygame.font.SysFont("Arial", font_size)

# === UPDATED PATHS ===
paddle_fx = pygame.mixer.Sound(asset("paddle_sound.MP3"))  # file is in same folder
paddle_fx.set_volume(1.0)
brick_fx = pygame.mixer.Sound(asset("brick.MP3"))          # was "Music/brick.MP3"
brick_fx.set_volume(0.7)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# was assets/my_paddle.png
img = pygame.image.load(asset("my_paddle.png")).convert_alpha()
rect = img.get_rect()
rect.centerx = SCREEN_WIDTH / 2
rect.centery = SCREEN_HEIGHT - img.get_height() - 20

count = 0
hit_count = 0
collision_time = 0
bricks_hit = 0
correction = 5
space = 0
Start_game = False


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # was assets/brick.png
        self.img = pygame.image.load(asset("brick.png")).convert_alpha()
        self.x = x
        self.y = y
        self.collide_bottom = False
        self.collide_side = False

    def draw(self, brick_surface):
        pygame.Surface.blit(brick_surface, self.img, (self.x, self.y))

    def check_collision(self, brick_surface):
        global bricks_hit
        self.collide_bottom = False  # reset each frame
        if (self.x < loc_x < self.x + 34) and (self.y < loc_y < self.y + 18):
            bricks_hit += 1
            self.collide_bottom = True
            brick_fx.play()


def build(rows, cols, x, y):
    bricks = pygame.sprite.Group()
    reset = x
    for i in range(cols):
        y += 20 + space
        x = reset
        for j in range(rows):
            x += 50 + space
            brick = Brick(x, y)
            bricks.add(brick)
    return bricks


brick_list = build(10, 10, 100, 100)

# Draw the bricks once into a surface
brick_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
for brick in brick_list:
    brick.draw(brick_surface)

start_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 150, 200, 50)
quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50, 200, 50)
screen.fill((255, 255, 255))

# Draw the buttons
pygame.draw.rect(screen, (0, 0, 0), start_button, 2)
pygame.draw.rect(screen, (0, 0, 0), quit_button, 2)

# Draw the button text
start_text = font.render("Start", True, (0, 0, 0))
quit_text = font.render("Quit", True, (0, 0, 0))
screen.blit(start_text, (start_button.x + 75, start_button.y + 15))
screen.blit(quit_text, (quit_button.x + 85, quit_button.y + 15))

# Update the display
pygame.display.flip()

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                run = True
                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    # draw background & bricks
                    screen.blit(brick_surface, (0, 0))

                    # paddle
                    screen.blit(img, rect)

                    # move ball
                    loc_y = loc_y + spd * dir_y
                    loc_x = loc_x + spd * dir_x

                    # reflect off borders
                    if loc_y < rad:
                        dir_y = 1
                    elif loc_y > SCREEN_HEIGHT - rad:
                        game_over = True
                        run = False
                        dir_y = -1

                    if loc_x < rad:
                        dir_x = 1
                    elif loc_x > SCREEN_WIDTH - rad:
                        dir_x = -1

                    # brick collisions
                    for brick in brick_list:
                        brick.check_collision(brick_surface)
                        if brick.collide_bottom and (brick.x - correction < loc_x < brick.x + correction) and dir_x == 1:
                            dir_x *= -1
                            pygame.draw.rect(brick_surface, (0, 0, 0), (brick.x, brick.y, 34, 18))
                            brick.kill()
                        elif brick.collide_bottom and (brick.x + 34 - correction < loc_x < brick.x + 34 + correction) and dir_x == -1:
                            dir_x *= -1
                            pygame.draw.rect(brick_surface, (0, 0, 0), (brick.x, brick.y, 34, 18))
                            brick.kill()
                        elif brick.collide_bottom:
                            dir_y *= -1
                            pygame.draw.rect(brick_surface, (0, 0, 0), (brick.x, brick.y, 34, 18))
                            brick.kill()

                        if bricks_hit == 1:
                            break
                    bricks_hit = 0

                    # simple paddle glitch fix using a short cooldown
                    current_time = pygame.time.get_ticks()
                    if current_time - collision_time < 200 and count > 0:
                        hit_count += 1
                    else:
                        hit_count = 0

                    # paddle follows mouse
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    rect.x = mouse_x - img.get_width() / 2

                    # paddle collision (fixed y check)
                    if (mouse_x - img.get_width() / 2 < loc_x < mouse_x + img.get_width() / 2) and (
                        loc_y > rect.top
                    ) and hit_count == 0:
                        count += 1
                        collision_time = pygame.time.get_ticks()
                        dir_y *= -1
                        paddle_fx.play()

                    # keep paddle inside screen
                    if rect.x < 0:
                        rect.x = 0
                    elif rect.x > SCREEN_WIDTH - img.get_width():
                        rect.x = SCREEN_WIDTH - img.get_width()

                    # draw ball
                    pygame.draw.circle(screen, (8, 202, 73), (loc_x, loc_y), rad)

                    pygame.display.flip()
                    pygame.time.Clock().tick(60)

                    if len(brick_list) == 0:
                        screen.fill((255, 255, 255))
                        game_win_text = font.render("You Win", True, (0, 0, 0))
                        screen.blit(game_win_text, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        pygame.quit()
                        sys.exit()

            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

         
