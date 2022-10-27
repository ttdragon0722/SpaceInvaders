import pygame
from .settings import FONT,FONT_COLOR,FONT_SIZE,WIDTH,HEIGHT,game_data,highScore
from math import sin
from random import randint

def draw_text(surf,text,size,x,y,color,bold=False):
    font=pygame.font.Font(FONT,size)
    if bold == True:
        font.set_bold(bold)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect(topleft = (x,y))
    surf.blit(text_surface,text_rect)
    return text_rect

class TV:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.tv = pygame.image.load('SpaceInvadersData/graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(WIDTH,HEIGHT))
        self.tv.set_alpha(50)
    def run(self):
        self.display_surface.blit(self.tv,(0,0))

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.player = pygame.image.load('SpaceInvadersData/graphics/player.png').convert_alpha()

    def life_minus(self):
        if sin(pygame.time.get_ticks()) > 0:
            alpha =  255
        else:
            alpha = 0
        self.player.set_alpha(alpha)


    def player_life(self,life):
        for amount in range(life,0,-1):
            self.display_surface.blit(self.player,(WIDTH-(amount*(self.player.get_width()+10)),10))

    def draw(self,score,life):
        draw_text(self.display_surface,f"SCORE:{score}",FONT_SIZE,10,-10,FONT_COLOR,False)
        if highScore != 0:
            draw_text(self.display_surface,f"HIGH SCORE:{highScore}",12,10,20,FONT_COLOR,False)
        else:
            draw_text(self.display_surface,f"HIGH SCORE:{highScore}",12,10,20,FONT_COLOR,False)
        self.player_life(life)

class Button:
    def __init__(self,pos,func):
        self.display = pygame.display.get_surface()
        self.image = pygame.image.load('SpaceInvadersData\graphics/restart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(128,128))
        self.rect = self.image.get_rect(center = pos)
        self.time_offset = False
        self.func = func

    def update(self):
        self.display.blit(self.image,self.rect)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.func()

        return True

class TextAnimation:
    def __init__(self,text,size,x,y,color,bold,anime = True,time_offset = False,time = None,speed = 50):
        self.display = pygame.display.get_surface()
        self.text = text
        self.index = 0
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.bold = bold

        self.text_speed = speed
        self.next_time = 0

        self.anime = anime

        self.time_offset = time_offset
        if self.time_offset:
            self.time = time
            self.time_start = None
            self.time_get = False

    def draw_text(self,surf,text,size,x,y,color,bold=False):
            font=pygame.font.Font(FONT,size)
            if bold == True:
                font.set_bold(bold)
            text_surface=font.render(text,True,color)
            text_rect=text_surface.get_rect(center = (x,y))
            surf.blit(text_surface,text_rect)
            return text_rect

    def update(self):
        self.draw_text(self.display,self.text[0:self.index],self.size,self.x,self.y,self.color,self.bold)

        if self.index >= len(self.text):
            return True
        else:
            time = pygame.time.get_ticks()
            if time - self.next_time > self.text_speed:
                self.text_speed = randint(self.text_speed-10,self.text_speed+10)
                self.next_time = time
                self.index += 1 
            return False

class PictureBilt:
    def __init__(self,pic_name,pos):
        self.display = pygame.display.get_surface()
        self.image = pygame.image.load(f'SpaceInvadersData/graphics/{pic_name}.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.time_offset = False

    def update(self):
        self.display.blit(self.image,self.rect)
        return True

class FlickerText:
    def __init__(self,text,size,x,y,bold,text_load):
        self.time_offset = 0
        self.display = pygame.display.get_surface()
        self.text = text
        self.index = 0
        self.size = size
        self.x = x
        self.y = y
        self.bold = bold

        self.status = "dark"

        self.stay = False

        #store time
        self.change_time = 0

        #cooldown
        self.stay_time = 500
        self.flicker_time = 200

        self.light = (255,170,51)
        self.dark = (255,255,255)
        self.color = self.dark

        self.text_load_func = text_load

    def color_change_timmer(self):
        
        time = pygame.time.get_ticks()
        if self.stay:
            if time - self.change_time > self.stay_time:
                self.change_time = time
                self.stay = False
        else:
            if time - self.change_time > self.flicker_time:
                if self.status == "dark":
                    self.status = "light"
                    self.color = self.light
                else:
                    self.status = "dark"
                    self.color = self.dark
                self.stay = True
                self.change_time = time
        

    def update(self):
        self.text_load_func()
        draw_text(self.display,self.text,self.size,self.x,self.y,self.color,True)
        self.color_change_timmer()

class BlackScreen:
    def __init__(self,color):
        self.display = pygame.display.get_surface()
        self.image = self.display.copy()
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (0,0))
        self.alpha =0
        self.image.set_alpha(self.alpha)

        self.fade_time = 0
        self.fade_cooldown = 50
        self.fade_in = False
        self.fade_out = False

    def fade_in_fade_out(self,obj_spawn,start_game):
        self.image.set_alpha(self.alpha)
        time = pygame.time.get_ticks()
        if not self.fade_in:
            if time - self.fade_time > self.fade_cooldown:
                self.fade_time = time
                self.alpha += 10
                if self.alpha >= 255:
                    self.alpha = 255
                    self.fade_in = True
                    start_game()
        elif not self.fade_out:
            if time - self.fade_time > self.fade_cooldown:
                self.fade_time = time
                self.alpha -= 10
                if self.alpha <= 0:
                    self.alpha = 0
                    self.fade_in = True
                    obj_spawn()
                    return True

    def fade_in_anime(self,to_alpha):
        time = pygame.time.get_ticks()
        if not self.fade_in:
            if time - self.fade_time > self.fade_cooldown:
                self.image.set_alpha(self.alpha)
                self.fade_time = time
                self.alpha += 2
                if self.alpha >= to_alpha:
                    self.alpha = to_alpha
                    self.fade_in = True

    def update(self,to_alpha):
        self.display.blit(self.image,self.rect)
        self.fade_in_anime(to_alpha)

class MainScreen:
    def __init__(self,text_load):
        self.diplay_surface = pygame.display.get_surface()
        self.text = [
            TextAnimation("SPACE INVADERS",25,WIDTH/2,100,"#FFAA33",True),
            TextAnimation("Instructions:".upper(),20,WIDTH/2,180,(255,255,255),True,time_offset=True,time=1000),
            TextAnimation("Press A D or LEFT RIGHT to move.".upper(),18,WIDTH/2,235,(255,255,255),False),
            TextAnimation("SPACE to shot.".upper(),18,WIDTH/2,270,(255,255,255),False),
            TextAnimation("Your goal is to move around don't get shoot.".upper(),18,WIDTH/2,305,(255,255,255),False),
            TextAnimation("Good Luck!!".upper(),20,WIDTH/2,340,(255,255,255),False,False),

            TextAnimation("SCORE ADVANCE TABLE:",20,WIDTH/2,445,(255,255,255),True,True,True,1000),
            PictureBilt("extra",(210,500)),
            TextAnimation("= ? mistery points",20,WIDTH/2+35,500,(255,255,255),True,True),
            PictureBilt("yellow",(210,550)),
            TextAnimation("= 30 points       ",20,WIDTH/2,550,(255,255,255),True,True),
            PictureBilt("green",(210,600)),
            TextAnimation("= 20 points       ",20,WIDTH/2,600,(255,255,255),True,True),
            PictureBilt("red",(210,650)),
            TextAnimation("= 10 points       ",20,WIDTH/2,650,(255,255,255),True,True),
            FlickerText("TAP SPACE TO START THE GAME",20,120,700,True,text_load)
        ]

    def update(self):
        for obj in self.text:
            if obj.time_offset:
                if not obj.time_get:
                    obj.time_get = True
                    time = pygame.time.get_ticks()
                    obj.time_start = time + obj.time
                    
                if obj.time_start < pygame.time.get_ticks():
                    if not obj.update() :
                        obj.time_offset = False
                        break
                break
            else:
                if not obj.update() :
                    break

class Over:
    def __init__(self,restart):
        self.diplay_surface = pygame.display.get_surface()
        self.text = [
            TextAnimation("GAME OVER",50,WIDTH/2,200,(255,255,255),True,speed=500),
            Button((WIDTH/2,HEIGHT/2),restart)
        ]

    def update(self):
        for obj in self.text:
            if obj.time_offset:
                if not obj.time_get:
                    obj.time_get = True
                    time = pygame.time.get_ticks()
                    obj.time_start = time + obj.time
                    
                if obj.time_start < pygame.time.get_ticks():
                    if not obj.update() :
                        obj.time_offset = False
                        break
                break
            else:
                if not obj.update() :
                    break
