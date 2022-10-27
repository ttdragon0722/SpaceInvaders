import pygame
from .settings import PLAYER_BULLET_COLOR,BULLET_SIZE,HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        #setup
        self.image = pygame.Surface(BULLET_SIZE)
        self.image.fill(PLAYER_BULLET_COLOR)
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)

        #move
        self.speed = 10
        self.direction = pygame.math.Vector2((0,-1))

    def out(self):
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

    def update(self):
        self.rect.y += self.direction.y * self.speed
        self.out()

class EnemyBullet(Bullet):
    def __init__(self, pos):
        super().__init__(pos)
        self.rect = self.image.get_rect(midtop = pos)
        self.direction = pygame.math.Vector2((0,1))

    def out(self):
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

    def update(self):
        self.rect.y += self.direction.y * self.speed
        self.out()
        