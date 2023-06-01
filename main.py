import pygame
import sys
from pygame.locals import *

# Create Game Window
pygame.init()
pygame.display.set_caption('Menu')
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60

#define player action variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (128, 128, 128)


class Archer(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'Images/{self.char_type}/archer.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_up, moving_right, moving_down):
        #reset movement variables
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if moving_up:
            dy = -self.speed
        if moving_down:
            dy = self.speed

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Archer('player',200, 200, 0.1, 3)
enemy = Archer('enemy',400, 200, 0.1, 3)



def play():
    global moving_right, moving_left, moving_up, moving_down
    pygame.display.set_caption('Crônicas de Marrcos')
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # keyboard presses
            if event.type == KEYDOWN:
                if event.key == K_a:
                    moving_left = True
                if event.key == K_d:
                    moving_right = True
                if event.key == K_w:
                    moving_up = True
                if event.key == K_s:
                    moving_down = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # keyboard button released
            if event.type == KEYUP:
                if event.key == K_a:
                    moving_left = False
                if event.key == K_d:
                    moving_right = False
                if event.key == K_w:
                    moving_up = False
                if event.key == K_s:
                    moving_down = False
        player.move(moving_left, moving_up, moving_right, moving_down)
        screen.fill(gray)
        player.draw()
        enemy.draw()
        pygame.display.flip()


play()
