# June 17th, 2022
# Gurvir Randhawa :]

''' BACKGROUND STORY '''
    # A fabled samurai who calls himself Echo is on a quest to find the Lost Temple Of Sound...
    # ...a Treble Quest...

''' CONTROLS '''

    # WASD - Move
    # F - Sound Wave        (Break Crystals)
    # Q - Wave Ride         (W To Dismount)
    # E - Sound Barrier     (No Dmg)

    # G - Dev Mode
        # R                 (Place Green Gems)
        # V                 (Save Level)
        # Left Click        (Choose & Place Blocks)
        # Right Click       (Break Blocks)
        # Middle Click      (Move Camera)

''' ENJOY '''

# importing modules
import pygame as py
import pickle
import random
import json
import math
import time
py.init()

# setting up pygame
py.mixer.init(44100)
# system values
width, height = 1280,720
screen = py.display.set_mode((width, height), py.RESIZABLE)
screen_width = screen.get_width()
screen_height = screen.get_height()
FPS = 60
Running = True
clock = py.time.Clock()

#main menu stuff
main_menu_background = py.image.load("assets/GM Treble Quest V2.png").convert()
parallax1 = py.image.load("assets/parallax_sky1.png").convert()
parallax1 = py.transform.scale(parallax1, (parallax1.get_width() * 8, parallax1.get_height() * 8))

parallax2 = py.image.load("assets/parallax_sky2.png").convert_alpha()
parallax2 = py.transform.scale(parallax2, (parallax2.get_width() * 8, parallax2.get_height() * 8))

parallax3 = py.image.load("assets/parallax_sky3.png").convert_alpha()
parallax3 = py.transform.scale(parallax3, (parallax3.get_width() * 8, parallax3.get_height() * 8))
def base_text(text,size,color):
    base_font = py.font.Font("assets/Halogen.otf", size)
    return base_font.render(text,True,color)

main_menu_start_text = base_text("Press Enter To Play", 50, (255, 255, 255))
main_menu_start_text_timer = 100
def main_menu():
    global main_menu_start_text_timer
    screen.blit(main_menu_background, (0, 0))
    main_menu_start_text_timer -= 1
    if main_menu_start_text_timer < 1:
        main_menu_start_text_timer = 100
    if main_menu_start_text_timer > 50:
        screen.blit(main_menu_start_text, (1280/2 - main_menu_start_text.get_width()/2, 630))

# using .json files to save our progress
def load(path):
    return pickle.load(open(path,"rb"))

# hovering with button
def button_hover(x,y,width,height):
    a = mouse_position()
    if a[0] > x and a[0] < x + width and a[1] > y and a[1] < y + height:
        return True
    else:
        return False

# collisions
def movementM(rect,movement,tiles): #change=[5,2]
    collision_type = {"TOP": False, "BOTTOM": False, "RIGHT": False, "LEFT": False, "TYPE": ""}
    rect.x -= movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.left = tile[1].right
            collision_type["RIGHT"] = True
            collision_type["TYPE"] = tile
        elif movement[0] < 0:
            rect.right = tile[1].left
            collision_type["LEFT"] = True
            collision_type["TYPE"] = tile


    rect.y -= movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.top = tile[1].bottom
            collision_type["BOTTOM"] = True
            collision_type["TYPE"] = tile
        elif movement[1] < 0:

            rect.bottom = tile[1].top
            collision_type["TOP"] = True
            collision_type["TYPE"] = tile
    return rect, collision_type

# adding all of the colliding tiles to a list
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if not tile[0] == "spike-left" and not tile[0] == "spike-up" and not tile[0] == "spike-right" and not tile[0] == "spike-down" and not tile[0] == "gem":
            if rect.colliderect(tile[1]):
                hit_list.append(tile)
    return hit_list

def mouse_position():
    was = py.mouse.get_pos()
    return was

# mouse clicks
def mouse_leftclick():
    a = py.mouse.get_pressed()[0]
    return a

def mouse_middleclick():
    a = py.mouse.get_pressed()[1]
    return a

def mouse_rightclick():
    a = py.mouse.get_pressed()[2]
    return a

def mouse_was():
    was = py.mouse.get_rel()
    return was

def save(data,path):
    pickle.dump(data, open(path,"wb"))

def tile_check(x,y,tile_size):
	a = x % tile_size
	x = x - a
	a = y % tile_size
	y = y - a
	return x, y

def tile_in_tile_FORXY(position,type,tiles):
    c = 0
    for tile in tiles:
        if position[0] == tile[1].x and position[1] == tile[1].y and tile[0] == type:
            break
        else:
            c += 1
        if c == len(tiles):
            return True

def transparent_rect(width,height,color,transparent_level):
    s = py.Surface((width,height))
    s.set_alpha(transparent_level)
    s.fill(color)
    return s

def button_click(x,y,width,height):
    a = mouse_position()
    if a[0] > x and a[0] < x + width and a[1] > y and a[1] < y + height:
        if mouse_leftclick():
            return True
    else:
        return False

#player stuff#
player = py.image.load("assets/p_sprite.png").convert_alpha()
player_rect = py.Rect((0,0,55,104))
cameraXY = [0,0]
move_down = False
move_up = False
move_left = False
move_right = False
player_y_momentum = 0
game_state = "main menu"
player_animation_timer = 0
player_animation_timer_max = 10
player_animation_state = 0
player_animation = "idle-right"
player_direction = "right"
jumping = False
placing_type = "grass"


# loading all of the images for animations and converting to alpha
player_animations = {
    "run-right":[
    py.image.load("player/run/character_sprite1.png").convert_alpha(),
    py.image.load("player/run/character_sprite2.png").convert_alpha(),
    py.image.load("player/run/character_sprite3.png").convert_alpha(),
    py.image.load("player/run/character_sprite4.png").convert_alpha(),
    py.image.load("player/run/character_sprite5.png").convert_alpha(),
    py.image.load("player/run/character_sprite6.png").convert_alpha(),
    ],
    "run-left":[
    py.transform.flip(py.image.load("player/run/character_sprite1.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/run/character_sprite2.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/run/character_sprite3.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/run/character_sprite4.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/run/character_sprite5.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/run/character_sprite6.png").convert_alpha(), (1),(0)),
    ],
    "idle-right":[
    py.image.load("player/idle/p_sprite1.png").convert_alpha(),
    py.image.load("player/idle/p_sprite2.png").convert_alpha(),
    py.image.load("player/idle/p_sprite3.png").convert_alpha(),
    py.image.load("player/idle/p_sprite4.png").convert_alpha(),
    ],
    "idle-left":[
    py.transform.flip(py.image.load("player/idle/p_sprite1.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/idle/p_sprite2.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/idle/p_sprite3.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/idle/p_sprite4.png").convert_alpha(), (1),(0)),
    ],
    "jump-right":[
    py.image.load("player/jump/p_sprite_jump1.png").convert_alpha(),
    py.image.load("player/jump/p_sprite_jump2.png").convert_alpha(),
    py.image.load("player/jump/p_sprite_jump3.png").convert_alpha(),
    py.image.load("player/jump/p_sprite_jump4.png").convert_alpha(),
    py.image.load("player/jump/p_sprite_jump5.png").convert_alpha(),
    py.image.load("player/jump/p_sprite_jump6.png").convert_alpha(),
    py.image.load("player/jump/p_sprite_jump7.png").convert_alpha(),
    py.image.load("player/jump/p_sprite_jump8.png").convert_alpha(),
    ],
    "jump-left":[
    py.transform.flip(py.image.load("player/jump/p_sprite_jump1.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/jump/p_sprite_jump2.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/jump/p_sprite_jump3.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/jump/p_sprite_jump4.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/jump/p_sprite_jump5.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/jump/p_sprite_jump6.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/jump/p_sprite_jump7.png").convert_alpha(), (1),(0)),
    py.transform.flip(py.image.load("player/jump/p_sprite_jump8.png").convert_alpha(), (1),(0)),
    ],
    "wave-right":[
    py.image.load("player/wave/wave3_no_bg1.png").convert_alpha(),
    py.image.load("player/wave/wave3_no_bg2.png").convert_alpha(),
    py.image.load("player/wave/wave3_no_bg3.png").convert_alpha(),
    py.image.load("player/wave/wave3_no_bg4.png").convert_alpha(),
    py.image.load("player/wave/wave3_no_bg5.png").convert_alpha(),
    py.image.load("player/wave/wave3_no_bg6.png").convert_alpha(),
    py.image.load("player/wave/wave3_no_bg7.png").convert_alpha(),
    py.image.load("player/wave/wave3_no_bg8.png").convert_alpha(),
    ],
    "wave-left":[
    py.transform.flip(py.image.load("player/wave/wave3_no_bg1.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave/wave3_no_bg2.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave/wave3_no_bg3.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave/wave3_no_bg4.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave/wave3_no_bg5.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave/wave3_no_bg6.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave/wave3_no_bg7.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave/wave3_no_bg8.png").convert_alpha(),(1),(0)),
    ],
    "sound-barrier-right":[
    py.image.load("player/sound barrier/p_sprite_sound_barrier1.png").convert_alpha(),
    py.image.load("player/sound barrier/p_sprite_sound_barrier2.png").convert_alpha(),
    py.image.load("player/sound barrier/p_sprite_sound_barrier3.png").convert_alpha(),
    py.image.load("player/sound barrier/p_sprite_sound_barrier4.png").convert_alpha(),
    py.image.load("player/sound barrier/p_sprite_sound_barrier5.png").convert_alpha(),
    py.image.load("player/sound barrier/p_sprite_sound_barrier6.png").convert_alpha(),
    ],
    "sound-barrier-left":[
    py.transform.flip(py.image.load("player/sound barrier/p_sprite_sound_barrier1.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/sound barrier/p_sprite_sound_barrier2.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/sound barrier/p_sprite_sound_barrier3.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/sound barrier/p_sprite_sound_barrier4.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/sound barrier/p_sprite_sound_barrier5.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/sound barrier/p_sprite_sound_barrier6.png").convert_alpha(),(1),(0)),
    ],
    "wave-surfing-right":[
    py.image.load("player/wave surf/p_sprite_wave_rider1.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider2.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider3.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider4.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider5.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider7.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider8.png").convert_alpha(),
    ],
    "wave-surfing-left":[
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider1.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider2.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider3.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider4.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider5.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider7.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider8.png").convert_alpha(),(1),(0)),
    ],
    "wave-surfing-going-right":[
    py.image.load("player/wave surf/p_sprite_wave_rider11.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider12.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider13.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider14.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider15.png").convert_alpha(),
    py.image.load("player/wave surf/p_sprite_wave_rider17.png").convert_alpha(),
    ],
    "wave-surfing-going-left":[
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider11.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider12.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider13.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider14.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider15.png").convert_alpha(),(1),(0)),
    py.transform.flip(py.image.load("player/wave surf/p_sprite_wave_rider17.png").convert_alpha(),(1),(0)),
    ],
}

sound_barriering = False
#script stuff#
screen_shake = 0
dev_mode = False

# loading data variable
data = load("level.json")
level = data[0]
gems = data[1]
dev_camera_position = [0,0]
def check_gui(pos):

    if button_hover(0,0,300,720):
        return False
    else:
        return True


# dictionary to hold our tiles
tiles = {
"grass-left":py.image.load("tiles/grass_side_left.png").convert_alpha(),
"grass":py.image.load("tiles/grass_terrain.png").convert_alpha(),
"grass-right":py.image.load("tiles/grass_side_right.png").convert_alpha(),

"rock-left":py.image.load("tiles/rock_left.png").convert_alpha(),
"grass-full":py.image.load("tiles/blank_terrain.png").convert_alpha(),
"rock-right":py.image.load("tiles/rock_right.png").convert_alpha(),

"rock-left-corner":py.image.load("tiles/rock_left_corner.png").convert_alpha(),
"rock-middle":py.image.load("tiles/rock_middle.png").convert_alpha(),
"rock-right-corner":py.image.load("tiles/rock_right_corner.png").convert_alpha(),

"grass-rock-left":py.image.load("tiles/floating_rock_left.png").convert_alpha(),
"grass-rock-middle":py.image.load("tiles/floating_rock_middle.png").convert_alpha(),
"grass-rock-right":py.image.load("tiles/floating_rock_right.png").convert_alpha(),

"note":py.transform.scale(py.image.load("tiles/breakable_block1.png").convert_alpha(), (64,64)),
"jump-pad1":py.transform.scale(py.image.load("tiles/jump_up1.png").convert_alpha(), (64,64)),
"jump-pad2":py.transform.scale(py.image.load("tiles/jump_up2.png").convert_alpha(), (64,64)),
"jump-pad3":py.transform.scale(py.image.load("tiles/jump_up3.png").convert_alpha(), (64,64)),

"grass-corner-left":py.image.load("tiles/grass_corner_left.png").convert_alpha(),
"grass-corner-right":py.image.load("tiles/grass_corner_right.png").convert_alpha(),
"grass_rock_full":py.image.load("tiles/grass_rock_full.png").convert_alpha(),

"spike-up":py.image.load("spikes/spikes_up/spikes_up3.png").convert_alpha(),
"spike-down":py.image.load("spikes/shooting_spikes_down/shooting_spikes_down3.png").convert_alpha(),
"spike-left":py.image.load("spikes/shooting_spikes_right/shooting_spikes_right3.png").convert_alpha(),
"spike-right":py.image.load("spikes/shooting_spikes_left/shooting_spikes_left3.png").convert_alpha(),

}
spikes = []
gem_tiles = [py.transform.scale(py.image.load("gem/gem1.png").convert_alpha(), (64,64)), py.transform.scale(py.image.load("gem/gem2.png").convert_alpha(), (64,64)), py.transform.scale(py.image.load("gem/gem3.png").convert_alpha(), (64,64)), py.transform.scale(py.image.load("gem/gem4.png").convert_alpha(), (64,64))]
last_gemXY = [0,0]

# tiles for the spikes
spike_tiles = {
"spike-up":[
py.image.load("spikes/spikes_up/spikes_up1.png").convert_alpha(),
py.image.load("spikes/spikes_up/spikes_up2.png").convert_alpha(),
py.image.load("spikes/spikes_up/spikes_up3.png").convert_alpha(),
py.image.load("spikes/spikes_up/spikes_up4.png").convert_alpha(),
py.image.load("spikes/spikes_up/spikes_up5.png").convert_alpha(),
py.image.load("spikes/spikes_up/spikes_up6.png").convert_alpha(),
],
"spike-left":[
py.image.load("spikes/shooting_spikes_right/shooting_spikes_right1.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_right/shooting_spikes_right2.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_right/shooting_spikes_right3.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_right/shooting_spikes_right4.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_right/shooting_spikes_right5.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_right/shooting_spikes_right6.png").convert_alpha(),
],
"spike-down":[
py.image.load("spikes/shooting_spikes_down/shooting_spikes_down1.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_down/shooting_spikes_down2.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_down/shooting_spikes_down3.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_down/shooting_spikes_down4.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_down/shooting_spikes_down5.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_down/shooting_spikes_down6.png").convert_alpha(),
],
"spike-right":[
py.image.load("spikes/shooting_spikes_left/shooting_spikes_left1.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_left/shooting_spikes_left2.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_left/shooting_spikes_left3.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_left/shooting_spikes_left4.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_left/shooting_spikes_left5.png").convert_alpha(),
py.image.load("spikes/shooting_spikes_left/shooting_spikes_left6.png").convert_alpha(),
],
"spike-bullet-down":py.image.load("spikes/spike_travel_down.png").convert_alpha(),
"spike-bullet-right":py.image.load("spikes/spike_travel_right.png").convert_alpha(),
"spike-bullet-left":py.transform.flip(py.image.load("spikes/spike_travel_right.png").convert_alpha(),(1),(0)),
"spike-bullet-up":py.transform.flip(py.image.load("spikes/spike_travel_down.png").convert_alpha(),(1),(0)),
}

portal = py.Rect((-64,-256,128,128))

particles = []

waves = []

sound_effect = py.mixer.Channel(5)

# setting up the parallax (moving backgrounds)
parallax3_X = 0
parallax2_X = 0
parallax1_X = 0
parallax1_Y = 0

# making crystals breakable with projectile
def crystals():
    c = 0
    for i in level:
        if i[0] == "note":
            return True
        if c == len(level):
            return False
        c += 1

# checking collision
def check_note_hit(rect):
    c = 0
    for i in level:
        if i[1].colliderect(rect) and not i[0] == "spike-left" and not i[0] == "spike-up" and not i[0] == "spike-right" and not i[0] == "spike-down":
            return i
        else:
            c += 1
        if c == len(level):
            return False
            break

t1 = 0
t0 = 0
ground_hit = 0

spike_timer = 0
spike_state = 0
spike_shooting_state = False
spike_wait = random.randint(100,300)

into_wave_surf = False
wave_surfing = False
wave_surfing_direction = "left"
wave_shots = 800
placing_style = "tile"
player_dead_timer = 0
player_dead_timer_state = False


def base_text(text,size,color):
    base_font = py.font.Font("assets/Halogen.otf", size)
    return base_font.render(text,True,color)

gems_timer = 0
gems_state = 0
gems_amount = 0
while Running:
    screen.fill((59,75,91))
    #screen_width = screen.get_width()
    #screen_height = screen.get_height()
    #for main menu#
    if game_state == "main menu":
        main_menu()
    # for game
    if game_state == "game":

        # ask if we are in game mode
        if not dev_mode:
            # handles the camera and offset
            cameraXY[0] -= int((((player_rect.x + cameraXY[0] + 30) - screen_width/2 + 12)/20))
            cameraXY[1] -= int((((player_rect.y + cameraXY[1] + 42) - screen_height/2 + 24)/20))

            # screen shake
            if screen_shake:
                screen_shake -= 1
                cameraXY[0] -= random.randint(0,8) - 4
                cameraXY[1] -= random.randint(0,8) - 4

            # offset calculations
            screen.blit(parallax1, (-1000 + cameraXY[0] * 0.2, -700 + cameraXY[1] * 0.2))
            screen.blit(parallax2, (-parallax2_X - 1050 + cameraXY[0] * 1.2, -600 + cameraXY[1] * 1.2))
            screen.blit(parallax2, (-parallax2_X - parallax2.get_width() -1050 + cameraXY[0] * 1.2, -600 + cameraXY[1] * 1.2))
            screen.blit(parallax2, (-parallax2_X + parallax2.get_width() -1050 + cameraXY[0] * 1.2, -600 + cameraXY[1] * 1.2))
            if -parallax2_X - 1050 + cameraXY[0] * 1.2 > screen.get_width():
                parallax2_X += parallax2.get_width()
            if -parallax2_X - 1050 + cameraXY[0] * 1.2 < 0 - parallax2.get_width():
                parallax2_X -= parallax2.get_width()


            screen.blit(parallax3, (-parallax3_X - 1150 + cameraXY[0] * 1.4, -500 + cameraXY[1] * 1.4))
            screen.blit(parallax3, (-parallax3_X - parallax3.get_width() - 1150 + cameraXY[0] * 1.4, -500 + cameraXY[1] * 1.4))
            screen.blit(parallax3, (-parallax3_X + parallax3.get_width() - 1150 + cameraXY[0] * 1.4, -500 + cameraXY[1] * 1.4))
            if -parallax3_X - 1150 + cameraXY[0] * 1.4 > screen.get_width():
                parallax3_X += parallax3.get_width()
            if -parallax3_X - 1150 + cameraXY[0] * 1.4 < 0 - parallax3.get_width():
                parallax3_X -= parallax3.get_width()

            py.draw.rect(screen, (193, 221, 251), (0, 500 + cameraXY[1] * 1.4, screen.get_width(), 10000))


            # player animation handler
            player_animation_timer += 1
            if player_animation_timer > player_animation_timer_max:
                player_animation_timer = 0
                player_animation_state += 1
                if player_animation_state > len(player_animations[player_animation]) - 1:
                    player_animation_state = 0
                    if player_animation == "wave-surfing-" + player_direction:
                        into_wave_surf = False
                        wave_surfing = True
                        player_animation_state = 0
                        jumping = False


# what to do when player is not dead
            if not player_dead_timer_state:
                if player_animation == "idle-right" or player_animation == "idle-left":
                    screen.blit(player_animations[player_animation][player_animation_state], (player_rect.x + cameraXY[0] - 13, player_rect.y + cameraXY[1] + 10))
                elif player_animation == "wave-surfing-right" or player_animation == "wave-surfing-left" or player_animation == "wave-surfing-going-left" or player_animation == "wave-surfing-going-right":
                    screen.blit(player_animations[player_animation][player_animation_state], (player_rect.x + cameraXY[0] - 13, player_rect.y + cameraXY[1] - 20))
                else:
                    screen.blit(player_animations[player_animation][player_animation_state], (player_rect.x + cameraXY[0] - 13, player_rect.y + cameraXY[1]))
            else:
                player_dead_timer += 1
                if player_dead_timer > 100:
                    player_dead_timer = 0
                    player_dead_timer_state = False
                    # spawning player to last crystal
                    player_rect = py.Rect((last_gemXY[0], last_gemXY[1], 55, 104))
                    cameraXY = [0, 0]

            if player_rect.y > 2000:
                player_dead_timer_state = True

            # player movement and power up movement (wave rider)
            movement = [0,0]

            if move_right and not sound_barriering and not wave_surfing and not player_dead_timer_state:
                movement[0] -= 5
                player_animation = "run-right"
                player_direction = "right"
            elif move_left and not sound_barriering and not wave_surfing and not player_dead_timer_state:
                movement[0] += 5
                player_animation = "run-left"
                player_direction = "left"
            elif move_up and not sound_barriering and not wave_surfing and not player_dead_timer_state:
                movement[1] += 5
                player_animation = "run-right"
            elif move_down and not sound_barriering and not wave_surfing and not player_dead_timer_state:
                movement[1] -= 15

            else:
                player_animation = "idle-" + player_direction
            if jumping:
                player_animation = "jump-" + player_direction
            if sound_barriering:
                player_animation = "sound-barrier-" + player_direction
            if into_wave_surf:
                player_animation = "wave-surfing-" + player_direction
            if wave_surfing:
                player_animation = "wave-surfing-going-" + player_direction
                if wave_surfing_direction == "left":
                    movement[0] += 7
                else:
                    movement[0] -= 7

            # gravity for jumping
            movement[1] -= player_y_momentum
            if not wave_surfing:
                player_y_momentum += 0.4
            else:
                player_y_momentum = 0

            player_rect, collisions = movementM(player_rect, movement, level)
            if collisions["BOTTOM"]:
                player_y_momentum = 0
                screen_shake = 5

            if collisions["BOTTOM"]:
                if collisions["TYPE"][0] == "jump-pad1":
                    player_y_momentum += 19

            if collisions["TOP"]:
                if jumping:
                    player_animation_state = 0
                    screen_shake = 5
                    ground_hit = 0
                    jumping = False
                player_y_momentum = 0

# jump pads
                if collisions["TYPE"][0] == "jump-pad1" or collisions["TYPE"][0] == "jump-pad2" or collisions["TYPE"][0] == "jump-pad3":
                    if not jumping:
                        player_animation_state = 0
                        player_animation_timer_max = 8
                        player_y_momentum -= 19
                        jumping = True

            # world rendering
            spike_timer += 1
            if spike_shooting_state:
                if spike_timer > 5:
                    spike_wait = random.randint(100, 300)
                    spike_timer = 0
                    spike_state += 1
                    if spike_state > 5:
                        spike_state = 0
                    if spike_state == 2:
                        spike_shooting_state = False
                        spike_timer = 0
            else:
                if spike_timer>spike_wait:
                    spike_timer = 0
                    spike_shooting_state = True
                    spike_state = 3

            for i in level:
                surface = tiles[i[0]]
                type = i[0]
                x = i[1].x + cameraXY[0]
                y = i[1].y + cameraXY[1]
                if x > 0 - surface.get_width() and y > 0 - surface.get_height() and x < screen.get_width() and y < screen.get_height():
                    if not "spike" in type:
                        screen.blit(surface, (x, y))

                    else:
                        if spike_shooting_state:
                            screen.blit(spike_tiles[type][spike_state], (x, y))
                            if spike_state == 1 and spike_timer == 0:
                                spikes.append((py.Rect((x - cameraXY[0] + 16, y - cameraXY[1] + 16, 32, 32)), type))
                        else:
                            screen.blit(spike_tiles[type][3], (x, y))

# adding the spikes and checking if it collides with player, if using sound barrier, player won"t die (shield)
            c = 0
            for i in spikes:
                rect =  i[0]
                type = i[1]
                if type == "spike-left":
                    rect.x -= 10
                    screen.blit(spike_tiles["spike-bullet-right"], (rect.x + cameraXY[0], rect.y + cameraXY[1]))
                if type == "spike-right":
                    rect.x += 10
                    screen.blit(spike_tiles["spike-bullet-left"], (rect.x + cameraXY[0], rect.y + cameraXY[1]))
                if type == "spike-up":
                    rect.y -= 10
                    screen.blit(spike_tiles["spike-bullet-up"], (rect.x + cameraXY[0], rect.y + cameraXY[1]))
                if type == "spike-down":
                    rect.y += 10
                    screen.blit(spike_tiles["spike-bullet-down"], (rect.x + cameraXY[0], rect.y + cameraXY[1]))
                spikes[c] = (rect, type)
                retu = check_note_hit(rect)
                if rect.colliderect(player_rect):
                    if not sound_barriering:
                        player_dead_timer_state = True
                    spikes.remove((rect,type))
                if retu:
                    spikes.remove((rect,type))
                c += 1

            gems_timer += 1
            if gems_timer > 10:
                gems_timer = 0
                gems_state += 1
                if gems_state > 3:
                    gems_state = 0

            for i in gems:
                screen.blit(gem_tiles[gems_state], (i.x + cameraXY[0], i.y + cameraXY[1]))
                if i.colliderect(player_rect):
                    gems.remove(i)
                    gems_amount += 1
                    last_gemXY = [i.x, i.y]

            screen.blit(gem_tiles[0], (15,15))
            screen.blit( base_text("x " + str(gems_amount), 34, (255, 255, 255)), (90, 25))

            c = 0
            # wave need to die after leaving screen
            for i in waves:
                timer = i[2]
                state = i[3]
                if i[0].x + cameraXY[0] - 20 > 0 - player_animations["wave-" + i[1]][state].get_width() and i[0].y + cameraXY[1] > 0 - player_animations["wave-" + i[1]][state].get_height() and i[0].x + cameraXY[0] - 20 < screen.get_width() and i[0].y + cameraXY[1] < screen.get_height():
                    screen.blit(player_animations["wave-" + i[1]][state], (i[0].x + cameraXY[0] - 20, i[0].y + cameraXY[1]))
                timer += 1
                if timer > 4:
                    state += 1
                    timer = 0
                    if state > 7:
                        state = 0
                if i[1] == "right":
                    new_rect = py.Rect((i[0].x + 10, i[0].y, 50, 10))
                    waves[c] = (new_rect, i[1], timer,state)
                else:
                    new_rect = py.Rect((i[0].x - 10, i[0].y, 50, 10))
                    waves[c] = (new_rect, i[1], timer, state)
                retu = check_note_hit(new_rect)
                if new_rect.colliderect(player_rect) and sound_barriering:
                    if i[1] == "right":
                        new_dir = "left"
                    else:
                        new_dir = "right"
                    waves[c] = (new_rect, new_dir, timer, state)
                if retu:
                    if retu[0] == "note":
                        try:
                            while retu in level:
                                level.remove(retu)
                            waves.remove((new_rect, i[1], timer, state))
                            screen_shake = 5
                        except:
                            pass
                        break
                    else:
                        if  retu[0] == "bounce-block":

                            if i[1] == "right":
                                new_dir = "left"
                            else:
                                new_dir = "right"
                            waves[c] = (new_rect, new_dir, timer, state)
                        else:
                            waves.remove((new_rect, i[1], timer, state))
                c += 1


        else:
            for i in gems:
                screen.blit(gem_tiles[0], (i.x + cameraXY[0], i.y + cameraXY[1]))
                if mouse_rightclick() and button_hover(i.x + cameraXY[0], i.y + cameraXY[1], 64, 64):
                    gems.remove(i)

            #camera#
            cameraXY[0] -= int((((dev_camera_position[0] + cameraXY[0] + 30) - screen_width/2 + 12)/5))
            cameraXY[1] -= int((((dev_camera_position[1] + cameraXY[1] + 42) - screen_height/2 + 24)/5))
            #player render#
            screen.blit(player_animations["idle-right"][0], (player_rect.x + cameraXY[0], player_rect.y + cameraXY[1] + 10))
            #placing tile#
            mouse_movement =  mouse_was()

# mouse clikcs and dev mode controls

            if  mouse_middleclick():
                dev_camera_position = [dev_camera_position[0] - mouse_movement[0], dev_camera_position[1] - mouse_movement[1]]
            mxy = mouse_position()
            if mouse_leftclick() and check_gui(mxy):
                newXY = tile_check(mxy[0] - cameraXY[0], mxy[1] - cameraXY[1], 64)
                if tile_in_tile_FORXY(newXY, placing_type, level):
                    level.append((placing_type, py.Rect((newXY[0], newXY[1], 64, 64))))
                    print(newXY)

            # world render
            for i in level:
                screen.blit(tiles[i[0]], (i[1].x + cameraXY[0], i[1].y + cameraXY[1]))
                if mouse_rightclick() and button_hover(i[1].x + cameraXY[0], i[1].y + cameraXY[1], 64, 64):
                    level.remove(i)


            # tile picker (g)
            screen.blit(transparent_rect(300, 720, (0, 0, 0), 150), (0, 0))
            x = 0
            y = 0
            for i in tiles:
                screen.blit(tiles[i], (35 + x, 15 + y))
                if button_click(35 + x, 15 + y, 64, 64):
                    placing_type = i
                x += tiles[i].get_width() + 15
                if x > 200:
                    x = 0
                    y += tiles[i].get_height() + 15

# game loop and key input presses
    for event in py.event.get():
        if event.type == py.QUIT:
            Running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                Running = False
            if event.key == py.K_RETURN:
                game_state = "game"
            if event.key == py.K_d:
                move_right = True
                player_animation_state = 0
                player_animation_timer_max = 10
            if event.key == py.K_a:
                move_left = True
                player_animation_state = 0
                player_animation_timer_max = 10
            if event.key == py.K_r:
                mxy = mouse_position()
                newXY = tile_check(mxy[0] - cameraXY[0], mxy[1] - cameraXY[1], 64)
                gems.append((py.Rect((newXY[0], newXY[1], 64, 64))))

                wave_surfing = False
            if event.key == py.K_e:
                sound_barriering = True
                player_animation_state = 0
            if event.key == py.K_w or event.key == py.K_SPACE and not player_dead_timer_state:
                into_wave_surf = False
                wave_surfing = False
                player_animation_state = 0
                if not jumping and not sound_barriering:
                    player_animation_state = 0
                    player_animation_timer_max = 8
                    player_y_momentum = -14
                    jumping = True

            if event.key == py.K_q:
                into_wave_surf = True
                player_animation_state = 0
                player_animation_timer_max = 5
                wave_surfing_direction = player_direction

            if event.key == py.K_g:
                if dev_mode:
                    dev_mode = False
                else:
                    if not dev_mode:
                        dev_camera_position = [player_rect.x, player_rect.y]
                        dev_mode = True

            if event.key == py.K_v:
                save((level, gems),"level.json")
            if event.key == py.K_f:
                if not sound_barriering and wave_shots > 0 and not player_dead_timer_state:
                    wave_shots -= 1
                    waves.append((py.Rect((player_rect.x, player_rect.y + 50, 96, 48)), player_direction, 0, 0))

# what happens when key is not pressed (no movement basically)
        if event.type == py.KEYUP:
            if event.key == py.K_e:
                sound_barriering = False
                player_animation_state = 0
            if event.key == py.K_d:
                move_right = False
                player_animation_state = 0
            if event.key == py.K_a:
                move_left = False
                player_animation_state = 0
            if event.key == py.K_w:
                move_up = False
                player_animation_state = 0


    py.display.update()
    clock.tick(74)

    # displaying the FPS
    py.display.set_caption("FPS:" + str(clock.get_fps()))

py.quit()
