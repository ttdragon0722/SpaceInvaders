import pygame
from .settings import *
from .ui import TV,UI,Over,BlackScreen,draw_text
from .player import Player
from .bullet import Bullet,EnemyBullet
from .obstacle import Obstacle
from .enemy import Enemy,Extra
from random import choice,randint

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.tv = TV()
        self.ui = UI()
        self.trasition = BlackScreen((255,0,0))
        self.over = Over(self.restart)
        self.player = pygame.sprite.GroupSingle()
        self.bullets_sprites = pygame.sprite.Group()
        self.enemy_bullets_sprites = pygame.sprite.Group()
        self.extra_enemy = pygame.sprite.GroupSingle()
        self.explosion_sound = pygame.mixer.Sound("SpaceInvadersData/audio/explosion.wav")
        self.explosion_sound.set_volume(0.1)
        Player((self.display_surface.get_width()/2,self.display_surface.get_height()-50),self.player,self.bullet_append)

        self.create_obstacle()
        self.create_enemy()

        self.enemy_direction = pygame.math.Vector2(1,0)
        self.down_distance = enemy_distance
        self.shot_time = 2500 + pygame.time.get_ticks()
        self.shot_cooldown = 800

        self.enemy_respawn_cooldown = 1000
        self.respawn_enemy = False
        self.end_time = 0

        self.precise_shot_cooldown =2000
        self.precise_shot_time = 3000 + pygame.time.get_ticks()

        self.close_to_shot = pygame.sprite.Group()

        self.player_life = 3
        self.score = 0
        self.player_die = False
        self.die_time = 0
        self.respawn_cooldown = 1000

        self.game_status = "playing"

        self.extra_spawn_cooldown = extra_spawn_cooldown
        self.extra_spawn_time = 0
        self.extra_spawning = False

    def restart(self):
        self.__init__()

    def create_obstacle(self):
        self.obstacle_sprites = pygame.sprite.Group()
        for amount in range(4):
            for col_index,col in enumerate(obstacle_shape):
                for row_index,row in enumerate(col):
                    
                    x = obstacle_start_pos + amount * (obstacle_spacing+block_obstacle)
                    y = self.display_surface.get_height()*3/4
                    
                    if row == "x":
                        self.obstacle_sprites.add(Obstacle((x + row_index*obstacle_size,y + col_index*obstacle_size)))

    def create_enemy(self):
        self.enemy_sprites = pygame.sprite.Group()
        for col in range(enemy_group[1]):
            for row in range(enemy_group[0]):
                x = enemy_start_x + (enemy_spacing_x * row ) 
                y = enemy_start_y + (enemy_spacing_y * col ) 
                if col == 0:
                    type = "yellow"
                elif col == 1 or col == 2:
                    type = "green"
                else:
                    type = "red"
                enemy = Enemy((x,y),type,self.enemy_bullet_append)
                self.enemy_sprites.add(enemy)

    def bullet_append(self,pos):
        self.bullets_sprites.add(Bullet(pos))

    def enemy_bullet_append(self,pos):
        self.enemy_bullets_sprites.add(EnemyBullet(pos))

    def enemy_shot(self):
        try:
            time = pygame.time.get_ticks()
            if time - self.shot_time > self.shot_cooldown:
                choice(self.enemy_sprites.sprites()).shot()
                self.shot_time = time
            if time - self.precise_shot_time > self.precise_shot_cooldown:
                try:
                    self.enemy_close_check()
                    choice(self.close_to_shot.sprites()).shot()
                    self.close_to_shot = pygame.sprite.Group()
                    self.precise_shot_time = pygame.time.get_ticks()
                except:
                    pass
        except:
            pass

    def enemy_close_check(self):
        self.close_to_shot = pygame.sprite.Group()
        enemys = self.enemy_sprites.sprites()
        player = self.player.sprite
        for enemy in enemys:
            if abs(enemy.rect.centerx - player.rect.centerx) < enemy_player_shot_distance:
                self.close_to_shot.add(enemy)

    def enemy_checker(self):
        enemys = self.enemy_sprites.sprites()
        for enemy in enemys:
            if enemy.rect.right > WIDTH:
                self.enemy_change_direction()
                self.enemy_move_down()
                break
            elif enemy.rect.left < 0:
                self.enemy_change_direction()
                self.enemy_move_down()
                break

        if  len(self.enemy_sprites) == 30:
            self.enemy_speedup(4)
        if  len(self.enemy_sprites) == 10:
            self.enemy_speedup(5)
        if  len(self.enemy_sprites) == 5:
            self.enemy_speedup(7)

    def enemy_speedup(self,amount):
        for enemy in self.enemy_sprites:
            enemy.speed = amount

    def enemy_y_check(self,enemy_group):
        for enemy in enemy_group:
            if enemy.rect.y > enemy_move_rangey[1]:
                self.down_distance *= -1
                break
            if enemy.rect.y < enemy_move_rangey[0]:
                self.down_distance *= -1
                break

    def enemy_move_down(self):
        enemys = self.enemy_sprites.sprites()
        self.enemy_y_check(enemys)
        for enemy in enemys:
            enemy.rect.y += self.down_distance

    def enemy_change_direction(self):
        enemys = self.enemy_sprites.sprites()
        for enemy in enemys:
            enemy.direction.x *= -1

    def collide(self):
        pygame.sprite.groupcollide(self.obstacle_sprites,self.enemy_bullets_sprites,True,True,collided=pygame.sprite.collide_mask)
        pygame.sprite.groupcollide(self.obstacle_sprites,self.bullets_sprites,True,True,collided=pygame.sprite.collide_mask)
        
        extra = pygame.sprite.groupcollide(self.extra_enemy,self.bullets_sprites,True,True)
        for hit in extra:
            self.explosion_sound.play()
            self.score += hit.score

        player_enemy =pygame.sprite.groupcollide(self.player,self.enemy_bullets_sprites,False,True,collided=pygame.sprite.collide_mask)
        for hit in player_enemy:
            if hit.invincible == False:
                hit.kill()
                self.player_life -= 1
                self.die_time = pygame.time.get_ticks()
                self.player_die = True

        enemy_bullet =  pygame.sprite.groupcollide(self.enemy_sprites,self.bullets_sprites,True,True,collided=pygame.sprite.collide_mask)
        for hit in enemy_bullet:
            self.explosion_sound.play()
            self.score += hit.score

    def respawn(self):
        if self.player_die :
            if self.player_life != 0:
                time = pygame.time.get_ticks()
                if time - self.die_time > self.respawn_cooldown:
                    self.die_time = 0
                    self.player_die = False
                    Player((self.display_surface.get_width()/2,self.display_surface.get_height()-50),self.player,self.bullet_append)
                    self.player.sprite.invincible = True
            else:
                global highScore
                if highScore < self.score:
                    game_data["HighScore"] = self.score
                if highScore < self.score:
                    game_data["HighScore"] = self.score
                self.game_status = "gameover"

    def extra_respawn(self):
        time = pygame.time.get_ticks()
        if time - self.extra_spawn_time > self.extra_spawn_cooldown:
            if randint(0,100) > extra_spawn_chance and not self.extra_spawning:
                self.extra_spawning = True
                self.extra_enemy.add(Extra(self.enemy_bullet_append,self.extra_delete,choice(["right","left"])))

    def extra_delete(self):
        self.extra_spawning = False

    def extra_shot(self):
        try:
            if abs(self.player.sprite.rect.centerx - self.extra_enemy.sprite.rect.centerx)< enemy_distance:
                self.extra_enemy.sprite.shot()
        except:
            pass

    def end_checker(self):
        if len(self.enemy_sprites) <= 0:
            self.end_time = pygame.time.get_ticks()
            self.respawn_enemy = True

    def enemy_respawn_timer(self):
        time = pygame.time.get_ticks()
        if time - self.end_time > self.enemy_respawn_cooldown:
            self.end_time = 0
            self.respawn_enemy = False
            self.create_enemy()

    def run(self):
        if self.game_status == "playing":
            self.player.update()
            self.bullets_sprites.update()
            self.enemy_bullets_sprites.update()
            self.enemy_sprites.update()
            self.extra_enemy.update()
            self.enemy_checker()
            self.enemy_shot()
            self.extra_shot()
            self.collide()
            self.respawn()
            self.extra_respawn()
            if self.respawn_enemy :
                self.enemy_respawn_timer()
            else:
                self.end_checker()


        self.player.draw(self.display_surface)
        self.bullets_sprites.draw(self.display_surface)
        self.enemy_bullets_sprites.draw(self.display_surface)
        self.obstacle_sprites.draw(self.display_surface)
        self.enemy_sprites.draw(self.display_surface)
        self.extra_enemy.draw(self.display_surface)
        self.ui.draw(self.score,self.player_life)
        
        if self.game_status == "gameover":
            self.trasition.update(100)
            self.over.update()
            
    