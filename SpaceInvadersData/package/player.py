import pygame
from .settings import SCREEN_OUT
from math import sin
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,bullet_append):
        super().__init__(groups)

        #function
        self.bullet_append = bullet_append

        #setup
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('SpaceInvadersData/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect( midbottom = pos)

        self.spawn_time = pygame.time.get_ticks()
        self.invincible = False
        self.invincible_time = 1000

        #movement
        self.speed = 5
        self.direction = pygame.math.Vector2((0,0))

        #shot
        self.can_shot = True
        self.shot_time = 0
        self.shot_cooldown = 400

        self.shot_music = pygame.mixer.Sound("SpaceInvadersData/audio/laser.wav")
        self.shot_music.set_volume(0.1)

    def input(self):
        keys = pygame.key.get_pressed()

            #left
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        #right
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.can_shot:
            self.shot_music.play()
            self.can_shot = False
            self.shot_time = pygame.time.get_ticks()
            self.bullet_append(self.rect.midtop)

    def invincicble_check(self):
        if self.invincible:
            value = sin(pygame.time.get_ticks())
            if value >= 0:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

    def invincible_cooldown(self):
        if self.invincible:
            if pygame.time.get_ticks() - self.spawn_time > self.invincible_time:
                self.invincible = False

    def cooldown(self):
        if pygame.time.get_ticks() - self.shot_time > self.shot_cooldown:
            self.can_shot = True
            self.shot_time = 0

    def out(self):
        if self.rect.centerx < SCREEN_OUT:
            self.rect.centerx = SCREEN_OUT
        if self.rect.centerx > self.display_surface.get_width()-SCREEN_OUT:
            self.rect.centerx = self.display_surface.get_width()-SCREEN_OUT

    def update(self):
        self.cooldown()
        self.input()
        self.out()
        self.rect.x += self.direction.x * self.speed

        self.invincicble_check()
        self.invincible_cooldown()