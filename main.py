import pygame as pg
import time
import sys
import configparser

config = configparser.ConfigParser()
config.read('osuData.cfg')

volume = config.getfloat('Audio', 'Volume')
dim = config.getint('Game', 'Dim')
skin_name = config.get('General', 'Skin')
cursor_size = config.getfloat('General', 'CursorSize')
FPS = config.getint('Screen', 'FPS')
WIDTH = config.getint('Screen', 'Width')
HEIGHT = config.getint('Screen', 'Height')

target_aspect = 4 / 3
if WIDTH / HEIGHT > target_aspect:
    game_height = HEIGHT*0.8
    game_width = int(game_height * target_aspect)
else:
    game_width = WIDTH*0.8
    game_height = int(game_width / target_aspect)

offset_x = (WIDTH - game_width) / 2
offset_y = (HEIGHT - game_height) / 2

scale_x = game_width / 512
scale_y = game_height / 384


overlay = pg.Surface((game_width, game_height), pg.SRCALPHA)
overlay.fill((0, 0, 0, 70))

pg.init()
pg.mixer.init()

pg.mixer.music.load("Songs/3/audio.mp3")

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Osu!")

icon = pg.image.load("Data/osu_logo.png")
pg.display.set_icon(icon)
background = pg.image.load("Songs/3/katamari2.png").convert_alpha()
background.set_alpha(dim)

original_bg_width, original_bg_height = background.get_size()

new_bg_width = int(original_bg_width * (HEIGHT / original_bg_height))

background = pg.transform.smoothscale(background, (new_bg_width, HEIGHT))

approach_circle = pg.image.load(f"Skins/{skin_name}/approachcircle.png").convert_alpha()
approach_circle.set_alpha(255)

cursor = pg.image.load(f"Skins/{skin_name}/cursor.png").convert_alpha()
#cursor_middle = pg.image.load(f"Skins/{skin_name}/cursormiddle.png").convert_alpha()
#cursor_middle = pg.transform.smoothscale(cursor_middle, (cursor_middle.get_size()[0] * cursor_size,cursor_middle.get_size()[1] * cursor_size))
cursor_trail = pg.image.load(f"Skins/{skin_name}/cursortrail.png").convert_alpha()
cursor = pg.transform.smoothscale(cursor, (cursor.get_size()[0] * cursor_size,cursor.get_size()[1] * cursor_size))
cursor_trail = pg.transform.smoothscale(cursor_trail, (cursor_trail.get_size()[0] * cursor_size,cursor_trail.get_size()[1] * cursor_size))

circle_sprite = pg.image.load(f"Skins/{skin_name}/hitcircle.png").convert_alpha()

def colorize_white_image(image, new_color):
    tinted_image = image.copy()
    color_surface = pg.Surface(image.get_size()).convert_alpha()
    color_surface.fill(new_color)
    tinted_image.blit(color_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    return tinted_image


CS = 4
r = (54.4 - (4.48 * CS))*scale_y
d = int(r*2)

AR = 9.3

if AR < 5:
    preempt = 1200 + 600 * (5 - AR) / 5
    fade_in = 800 + 400 * (5 - AR) / 5
elif AR == 5:
    preempt = 1200
    fade_in = 800
elif AR > 5:
    preempt = 1200 - 750 * (AR - 5) / 5
    fade_in = 800 - 500 * (AR - 5) / 5

OD = 8.5

hit300_window = 80-6*OD
hit100_window = 140-8*OD
hit50_window = 200-10*OD


circle_sprite = colorize_white_image(circle_sprite, (255, 0, 0))
approach_circle = colorize_white_image(approach_circle, (255, 0, 0))
approach_circle = pg.transform.smoothscale(approach_circle, (d, d))

circle_sprite = pg.transform.smoothscale(circle_sprite, (d, d))
circle_overlay = pg.image.load(f"Skins/{skin_name}/hitcircleoverlay.png")
circle_overlay = pg.transform.smoothscale(circle_overlay, (d, d))
number1 = pg.image.load(f"Skins/{skin_name}/default-2.png")
number1 = pg.transform.smoothscale(number1, (number1.get_size()[0]*0.8, number1.get_size()[1]*0.8))

running = True
clock = pg.time.Clock()
prev_time = time.time()
circle_prev_time = prev_time
pg.mouse.set_visible(False)

mouse_pos_history = []
angle = 0
circles = []
circles_on_scene = []

with open('Songs/3/1.txt', 'r') as file:
    for row in file:
        par = row.split(',')
        circles.append([
    int(par[0]) * scale_x + offset_x,
    int(par[1]) * scale_y + offset_y,
    float(par[2])
])

pg.mixer.music.play(-1)
pg.mixer.music.set_volume(volume)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            sys.exit()
    screen.fill((0, 0, 0))
    screen.blit(background, background.get_rect(center=(WIDTH//2, HEIGHT//2)))
    screen.blit(overlay, (offset_x, offset_y))
    curr_time = (time.time() - prev_time)

    if len(circles) > 0 and curr_time*1000 >= circles[0][2] - preempt:
        circles_on_scene.append([circles[0], curr_time])
        circles.pop(0)


    for circle_data in circles_on_scene:
        circle, appear_time = circle_data
        x, y, hit_time = circle

        time_since_appeared = (curr_time - appear_time) * 1000

        if time_since_appeared < fade_in:
            alpha = int((time_since_appeared / fade_in) * 255)
            alpha = max(0, min(255, alpha))
        else:
            alpha = 255

        temp_circle = circle_sprite.copy()
        temp_overlay = circle_overlay.copy()
        temp_number = number1.copy()
        temp_approach_circle = approach_circle.copy()

        temp_circle.set_alpha(alpha)
        temp_overlay.set_alpha(alpha)
        temp_number.set_alpha(alpha)
        temp_approach_circle.set_alpha(alpha)
        

        scale_factor = max(1, 4 - 3 * (time_since_appeared / preempt))

        scaled_size = int(d * scale_factor)
        temp_approach_scaled = pg.transform.smoothscale(temp_approach_circle, (scaled_size, scaled_size))

        screen.blit(temp_approach_scaled, temp_approach_scaled.get_rect(center=(x, y)))

        screen.blit(temp_circle, temp_circle.get_rect(center=(x, y)))
        screen.blit(temp_overlay, temp_overlay.get_rect(center=(x, y)))
        screen.blit(temp_number, temp_number.get_rect(center=(x, y)))


    if len(circles_on_scene) > 0 and curr_time*1000 >= circles_on_scene[0][0][2] + hit50_window:
            circles_on_scene.pop(0)

    mouse_pos = pg.mouse.get_pos()
    mouse_pos_history.append([mouse_pos, curr_time])

    for x in mouse_pos_history[:]:
        if x[1] >= curr_time - 0.1:
            screen.blit(cursor_trail, (x[0][0] - cursor_trail.get_size()[0]//2, x[0][1] - cursor_trail.get_size()[0]//2))
        else:
            mouse_pos_history.remove(x)

    rotated_cursor = pg.transform.rotate(cursor, angle)
    rotated_rect = rotated_cursor.get_rect(center=mouse_pos)
    screen.blit(rotated_cursor, rotated_rect.topleft)
    #screen.blit(cursor_middle, cursor_middle.get_rect(center=mouse_pos))

    angle -= 0.5
    pg.display.flip()

    fps = int(clock.get_fps())
    pg.display.set_caption(f"Osu! FPS: {fps}")

    clock.tick(FPS)

pg.quit()