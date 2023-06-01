import pygame
import sys
from pygame.locals import *

# Create Game Window
pygame.init()
pygame.display.set_caption('Crônicas de Marrcos')
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


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'Images/{self.char_type}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'Images/{self.char_type}/run/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
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

    def update_animation(self):
        #update animation
        animation_cooldown = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self,new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Player('player',200, 200, 1, 3)
enemy = Player('enemy',400, 200, 1, 3)



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
        #update player actions
        if player.alive:
            if moving_left or moving_up or moving_right or moving_down:
                player.update_action(1) #1: run
            else:
                player.update_action(0)
        player.move(moving_left, moving_up, moving_right, moving_down)
        screen.fill(gray)
        player.update_animation()
        player.draw()
        enemy.draw()
        pygame.display.flip()


play()
