import pygame
import sys
import os
import math
from pygame.locals import *

# Create Game Window
pygame.init()
pygame.display.set_caption('Crônicas de Marrcos')
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60
TILE_SIZE = 50 ##redefinir quando fizer o level

#define player action variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
shoot = False

#load images
bullet_img = pygame.image.load('Images/player/ammo/0.png').convert_alpha()
hearth_img = pygame.image.load('Images/items/hearth.png').convert_alpha()
coin_img = pygame.image.load('Images/items/coin.png').convert_alpha()
shield_img = pygame.image.load('Images/items/shield.png').convert_alpha()
coin_img = pygame.transform.scale_by(coin_img, 2)
hearth_img = pygame.transform.scale_by(hearth_img, 0.03)
shield_img = pygame.transform.scale_by(shield_img, 0.1)
item_boxes = {'Health': hearth_img, 'Shield': shield_img, 'Coin': coin_img}

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (128, 128, 128)
blue = (30, 144, 255)

#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, health):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.shoot_cooldown = 0
        self.health = health
        self.max_health = self.health
        self.speed = speed
        self.direction = 1
        self.wallet = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #load all images fdor the players
        animation_types = ['idle', 'run', 'attack', 'death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            # count number of files in folder
            num_of_frames = len(os.listdir(f'Images/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # calculate the direction towards the target position
            direction_x = mouse_x - self.rect.centerx
            direction_y = mouse_y - self.rect.centery
            distance = max(abs(direction_x), abs(direction_y))
            if distance != 0:
                direction_x /= distance
                direction_y /= distance
            else:
                direction_x = 0
                direction_y = 0

            # adjust the initial position of the bullet
            bullet_offset_x = direction_x * 50  # adjust the offset as needed
            bullet_offset_y = direction_y * 70  # adjust the offset as needed

            bullet = Bullet(self.rect.centerx + bullet_offset_x, self.rect.centery + bullet_offset_y, mouse_x, mouse_y)
            bullet_group.add(bullet)


    def update_action(self,new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, red, self.rect, 1)

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Shield":
                player.health += 50
            elif self.item_type == "Coin":
                player.wallet += 5
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, black, (self.x-2, self.y-2, 154, 24))
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
        if self.health > self.max_health:
            pygame.draw.rect(screen, black, (self.x + 152, self.y - 2, (150 * ratio)-150, 24))
            pygame.draw.rect(screen, blue, (self.x + 150, self.y, (150 * ratio)-150, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 15
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # calculate the direction towards the target position
        direction_x = target_x - x
        direction_y = target_y - y
        distance = max(abs(direction_x), abs(direction_y))
        if distance != 0:
            self.direction_x = direction_x / distance
            self.direction_y = direction_y / distance
        else:
            self.direction_x = 0
            self.direction_y = 0

        # calculate the angle of rotation
        self.angle = math.degrees(math.atan2(-self.direction_y, self.direction_x))

        # rotate the image
        self.image = pygame.transform.rotate(self.image, self.angle)

        # adjust the rect center based on the rotation
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        # move bullet
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width or self.rect.bottom < 0 or self.rect.top > screen_height:
            self.kill()

        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 20
                print(f'Vida do imigo: {enemy.health}')
                self.kill()




#create sprite groups
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()


#temp - testing items
item_box = ItemBox('Coin', 100, 300)
item_box_group.add(item_box)
item_box = ItemBox('Shield', 400, 500)
item_box_group.add(item_box)
item_box = ItemBox('Health', 200, 500)
item_box_group.add(item_box)
item_box = ItemBox('Coin', 300, 300)
item_box_group.add(item_box)

player = Player('player', 200, 200, 1, 3, 100)
health_bar = HealthBar(85, 13, player.health, player.health)

enemy = Player('enemy', 400, 200, 1, 3, 60)



def play():
    global moving_right, moving_left, moving_up, moving_down, shoot
    pygame.display.set_caption('Crônicas de Marrcos')
    can_shoot = True



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
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and can_shoot:
                    shoot = True
                    can_shoot = False


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
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    shoot = False
                    can_shoot = True


        #update player actions
        if player.alive:
            #shoot bullets
            if shoot:
                player.shoot()
            if moving_left or moving_up or moving_right or moving_down:
                player.update_action(1) #1: run
            else:
                player.update_action(0) #0: idle

        player.move(moving_left, moving_up, moving_right, moving_down)
        # update and draw groups
        screen.fill(gray)

        # show player status
        draw_text(f"Coins:{player.wallet}", font, black, 10, 35)
        draw_text("Health:", font, black, 10, 15)
        for x in range(player.health):
            screen.blit
        health_bar.draw(player.health)
        bullet_group.update()
        bullet_group.draw(screen)
        item_box_group.update()
        item_box_group.draw(screen)
        player.update()
        player.draw()
        enemy.update()
        enemy.draw()
        pygame.display.flip()



play()
