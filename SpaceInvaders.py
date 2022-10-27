import pygame 
from sys import exit
from SpaceInvadersData.package.settings import *
from SpaceInvadersData.package.level import Level
from SpaceInvadersData.package.ui import MainScreen,TV

class Game:
    def __init__(self) -> None:

        #setup
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Space Invaders","hahaha")
        pygame.display.set_icon(pygame.image.load('SpaceInvadersData/graphics/red.png'))

        self.status = "ready"
        self.text_load = False

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.main_screen = MainScreen(self.start_text_load)
        self.tv = TV()

        pygame.mixer.music.load("SpaceInvadersData/audio/music.wav")
        pygame.mixer.music.set_volume(0.1)

    def start_text_load(self):
        self.text_load = True

    def run(self):
        pygame.mixer.music.play(-1)
        while True:
            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    store_score()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP :
                    if event.key == pygame.K_SPACE and self.text_load:
                        time = pygame.time.get_ticks()
                        self.level.precise_shot_time += time
                        self.status = "playing"

            self.screen.fill(BACKGROUND_COLOR)
            #element update
            match self.status:
                case "ready":
                    self.main_screen.update()
                case "playing":
                    self.level.run()

            self.tv.run()

            #element display update
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()        
    game.run()