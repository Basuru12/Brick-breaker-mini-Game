import pygame
from pygame import mixer
import sys


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
font_size = 35 # font size

font = pygame.font.SysFont("Arial", font_size)

paddle_fx = pygame.mixer.Sound('Music/paddle_sound.MP3')
paddle_fx.set_volume(1.0)
brick_fx = pygame.mixer.Sound('Music/brick.MP3')
brick_fx.set_volume(0.7)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')
img = pygame.image.load('assets\my_paddle.png')
rect = img.get_rect()
rect.centerx = SCREEN_WIDTH/2
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
        self.img = pygame.image.load('assets\\brick.png')
        #Wself.rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.collide_bottom = False
        self.collide_side = False
        
    
    def draw(self,brick_surface ):
        pygame.Surface.blit(brick_surface,self.img, (self.x, self.y))

    def check_collision(self,brick_surface):
        global bricks_hit
        if loc_x > self.x and loc_x < self.x + 34 and loc_y > self.y and loc_y < self.y+18: 
            #print(loc_y)
            #print(self.y)
            bricks_hit += 1
            #print("collided")
            self.collide_bottom =  True
            brick_fx.play()

        else:
            self.collide = False
    
        

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
brick_list=build(10,10,100,100)



"""Draw the bricks"""
brick_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            
for brick in brick_list:
        
        brick.draw(brick_surface)


start_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 150, 200, 50)
quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50, 200, 50)
screen.fill((255,255,255))

# Draw the buttons
pygame.draw.rect(screen, (0,0,0), start_button, 2)
pygame.draw.rect(screen, (0,0,0), quit_button, 2)

# Draw the button text
start_text = font.render("Start", True, (0,0,0))
quit_text = font.render("Quit", True, (0,0,0))
screen.blit(start_text, (start_button.x + 75, start_button.y + 15))
screen.blit(quit_text, (quit_button.x + 85, quit_button.y + 15))

# Update the display
pygame.display.flip()


        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                run = True
                while (run):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    # Start the game here
                    screen.blit(brick_surface, (0, 0))
        

                    screen.blit(img, rect)
                    #screen.blit(brick_img, brick_rect)
                    loc_y=loc_y+spd*dir_y
                    loc_x=loc_x+spd*dir_x

                    """Reflects the ball from borders
                    """
                    if loc_y <rad:
                        
                        dir_y = 1
                    elif loc_y > SCREEN_HEIGHT-rad:
                        game_over = True
                        run = False
                        dir_y= -1

                    if loc_x <rad:
                        dir_x = 1
                    elif loc_x > SCREEN_WIDTH-rad:
                        dir_x= -1
                    """Collision of the ball with the bricks"""
                    for brick in brick_list:
                        brick.check_collision(brick_surface)
                        if brick.collide_bottom == True  and (loc_x < brick.x + correction and loc_x > brick.x - correction) and dir_x == 1:
                            dir_x *= -1
                            pygame.draw.rect(brick_surface ,(0,0,0),(brick.x,brick.y,34,18))
                            brick.kill()
                        elif brick.collide_bottom == True and (loc_x < (brick.x + 34 + correction) and loc_x > (brick.x + 34 - correction)) and dir_x == -1:
                            dir_x *= -1
                            pygame.draw.rect(brick_surface ,(0,0,0),(brick.x,brick.y,34,18))
                            brick.kill()
                        elif brick.collide_bottom == True   :
                        
                            dir_y *= -1
                            pygame.draw.rect(brick_surface ,(0,0,0),(brick.x,brick.y,34,18))
                            brick.kill()
                        if bricks_hit == 1 :
                            break
                    bricks_hit = 0

                    """Glitch fix paddle"""
                    current_time = pygame.time.get_ticks()
                    if current_time - collision_time < 200  and count > 0 :
                        hit_count += 1
                    else :
                        hit_count = 0
                    """Checking collision with paddle"""
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    rect.x = mouse_x - img.get_width() / 2
                    if loc_x > (mouse_x - img.get_width()/2)  and loc_x < (mouse_x + img.get_width()/2) and loc_y > SCREEN_HEIGHT - + img.get_width()/2 and hit_count == 0 :
                        count += 1
                        collision_time = pygame.time.get_ticks()
                        dir_y *= -1
                        paddle_fx.play()
                    '''Keeps the paddle from going outside the frame'''
                    if rect.x < 0:
                        rect.x = 0
                    elif rect.x > SCREEN_WIDTH - img.get_width():
                        rect.x = SCREEN_WIDTH - img.get_width()
                    
                    if loc_y == SCREEN_HEIGHT - rad:
                        

                        run = False
                        
                    pygame.draw.circle(screen ,(8,202,73),(loc_x,loc_y),rad)
                    pygame.display.flip()
                    pygame.time.Clock().tick(60)
                    if len(brick_list) == 0:
                        screen.fill((255,255,255))
                        game_win_text = font.render("You Win", True, (0,0,0))
                        screen.blit(game_win_text, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        pygame.quit()
                        sys.exit()

            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            print(game_over)
            if game_over:
                print("hi")
                screen.fill((255,255,255))
                game_over_text = font.render("Game Over", True, (0,0,0))
                screen.blit(game_over_text, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50))
                pygame.display.flip()
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()
