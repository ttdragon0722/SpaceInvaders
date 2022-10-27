import pygame
from .settings import enemy_speed,extra_enemy_y,WIDTH,extra_speed
from random import choice,randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,type,bullet_append):
        """
        type = extra ,green,player,red,yellow
        """
        super().__init__()
        if type == "green":
            self.score = 300
        elif type == "red":
            self.score = 100
        else:
            self.score = 500
        self.image = pygame.image.load(f'SpaceInvadersData/graphics/{type}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2((1,0))
        self.speed = enemy_speed

        self.cooldown = 100
        self.movetime = 0  

        self.bullet_append = bullet_append

        self.shot_music = pygame.mixer.Sound("SpaceInvadersData/audio/laser.wav")
        self.shot_music.set_volume(0.1)

    def shot(self):
        self.shot_music.play()
        self.bullet_append(self.rect.midbottom)

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

class Extra(pygame.sprite.Sprite):
    def __init__(self,bullet_append,func_delete,direction="right"):
        super().__init__()
        self.image = pygame.image.load('SpaceInvadersData/graphics/extra.png').convert_alpha()
        if direction == "right":
            pos = (-100,extra_enemy_y)
            self.direction = pygame.math.Vector2((1,0))
        else:
            pos = (WIDTH+100,extra_enemy_y)
            self.direction = pygame.math.Vector2((-1,0))
        self.rect = self.image.get_rect(center = pos)
        self.speed = extra_speed
        self.score = choice([100,150,300])
        self.delete = func_delete
        self.skill = False
        self.skill_time = 0
        self.skill_cooldown = 1000

        self.shot_music = pygame.mixer.Sound("SpaceInvadersData/audio/laser.wav")
        self.shot_music.set_volume(0.1)

        self.bullet_append = bullet_append

    def out(self):
        if self.rect.x > WIDTH+200 or self.rect.x < -200:
            self.delete()
            self.kill()

    def shot(self):
        self.shot_music.play()
        if not self.skill:
            random = randint(0,100)
            if random > 50:
                self.bullet_append(self.rect.midbottom)
            else:
                self.shot_music.play()
                self.shot_music.play()
                self.normal_dir = self.direction
                self.skill_time = pygame.time.get_ticks()
                self.skill = True

    def use_skill(self):
        time = pygame.time.get_ticks()
        if time - self.skill_time > self.skill_cooldown:
            self.direction = self.normal_dir
            self.skill = False
        else:
            self.direction = pygame.math.Vector2((0,0))
            self.bullet_append(self.rect.midbottom)


    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.out()
        if self.skill :
            self.use_skill()