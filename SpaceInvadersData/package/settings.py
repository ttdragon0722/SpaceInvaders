from json import load,dump

def store_score():
    with open("SpaceInvadersData/package/game_data.json","w") as f:
        dump(game_data,f)

with open("SpaceInvadersData/package/game_data.json","r") as f:
    game_data = load(f)
    highScore = game_data["HighScore"]
highScore = game_data["HighScore"]

WIDTH = 800
HEIGHT = 800
FPS = 60

SCREEN_OUT = 50

BULLET_SIZE = (3,30)
PLAYER_BULLET_COLOR = (255,255,255)

BACKGROUND_COLOR = (24,24,24) 
FONT_COLOR = (255,255,255)
FONT = "SpaceInvadersData/font/Pixeled.ttf"
FONT_SIZE = 18

obstacle_spacing = 133

obstacle_color = "#F14F50"
obstacle_size = 6
obstacle_shape = [
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx']
block_obstacle = len(obstacle_shape[-1])*6

obstacle_spacing = (HEIGHT-4*block_obstacle)//5
obstacle_start_pos = obstacle_spacing


#enemy 40x32
enemy_player_shot_distance = 20
enemy_speed = 3
enemy_distance = 5

enemy_group = (8,6)
enemy_spacing_x = 60
enemy_spacing_y = 40

enemy_group_width = enemy_group[0]*40 + ((enemy_group[0]-1)*(enemy_spacing_x-40))
enemy_group_height = enemy_group[1]*32 + ((enemy_group[1]-1)*(enemy_spacing_y-32))


enemy_start_x = (WIDTH-enemy_group_width)/2
enemy_start_y = (HEIGHT-enemy_group_height)/2

extra_enemy_y = 150
extra_speed = 5
extra_spawn_cooldown = 5000
extra_spawn_chance = 80

enemy_move_rangey = 210,500

