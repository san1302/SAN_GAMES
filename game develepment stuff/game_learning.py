# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 00:12:13 2018

@author: Sanchit
"""
#########LIBRARIES USED ###############
import pygame
import time
import random
import os


display_width = 800
display_height = 600
game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder,"img")
player_img = pygame.image.load(os.path.join(image_folder, "playerShip1_red.png"))
enemy_img = pygame.image.load(os.path.join( image_folder, "meteorBrown_med1.png"))
bullet_img = pygame.image.load(os.path.join(image_folder, "laserRed01.png"))

###########COLORS######################
black = (0,0,0)
white = (255,255,255)
darkblue = (0,0,160)
green = (0,255,0)
red = (255,0,0)
yellow = (255,255,0)
#######################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(60,50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (display_width/2,display_height - self.rect.height)
        self.rect.centerx = display_width/2
        self.speedx = 0


    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_LEFT]:
            self.speedx = -8        
        self.rect.x += self.speedx
        if self.rect.left > display_width:
            self.rect.right = display_width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx , self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(display_width-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(1,3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > display_height + 15:
            self.rect.x = random.randrange(0, display_width-self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(1, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
       self.rect.y += self.speedy
       if self.rect.bottom < 0:
         self.kill()


pygame.init()
pygame.mixer.init()
############DISPLAY####################

gamedisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Just game')
clock = pygame.time.Clock()
background = pygame.image.load(os.path.join(image_folder, "Space Background.png"))
background_rect = background.get_rect()
#######################################
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
enemys = pygame.sprite.Group()
for i in range(8):
    e = Enemy()
    enemys.add(e)
    all_sprites.add(e)
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(60)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                  player.shoot()
          

    # Update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemys,bullets,True,True)
    for hit in hits:
        e = Enemy()
        all_sprites.add(e)
        enemys.add(e)
    hits = pygame.sprite.spritecollide(player,enemys,False)
    if hits:
        running = False

    
    # Draw / render
    gamedisplay.fill(black)
    gamedisplay.blit(background,background_rect)
    all_sprites.draw(gamedisplay)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()



