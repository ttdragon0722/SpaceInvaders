import pygame
from .settings import obstacle_color,obstacle_size

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((obstacle_size,obstacle_size))
        self.image.fill(obstacle_color)
        self.rect = self.image.get_rect(topleft =  pos)