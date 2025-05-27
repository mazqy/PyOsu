import pygame as pg
import time
import sys
import os
import ctypes
from config.settings import get_setting, save_setting
from menu.beatmap_menu import show_beatmaps_menu

def game():

    ctypes.windll.user32.SetProcessDPIAware()

    volume = get_setting('Audio', 'Volume', cast=float)
    hitsound_volume = get_setting('Audio', 'HitsoundVolume', cast=float)
    dim = get_setting('Game', 'Dim', cast=float)
    play_area_dim = get_setting('Game', 'PlayAreaDim', cast=float)
    skin_name = get_setting('General', 'Skin')
    cursor_size = get_setting('General', 'CursorSize',cast=float)
    FPS = get_setting('Screen', 'FPS', cast=int)
    WIDTH = get_setting('Screen', 'Width', cast=int)
    HEIGHT = get_setting('Screen', 'Height', cast=int)
    fullscreen = get_setting('Screen', 'Fullscreen', cast=bool)

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
    overlay.fill((0, 0, 0, play_area_dim))

    osu_path = os.path.join(f"C:/Users/{os.getlogin()}/AppData/Local/osu!")
    osu_path_songs = os.path.join(osu_path + "/Songs")
    osu_path_skins = os.path.join(osu_path + "/Skins")
    osu_info_path, osu_map_path = show_beatmaps_menu(osu_path_songs)

    circles = []
    combo_colors = []
    has_combo_colors = False
    has_background = False

    with open(osu_info_path, encoding='utf-8') as f:
        hitobjects_section = False
        combo_colors = []
        color_index = 0
        combo_num = 1
        for line in f:
            if hitobjects_section:
                line = line.strip()
                if not line:
                    continue
                par = line.split(',')
                
                if int(par[3]) == 2:
                    has_combo_colors = True
                    if color_index >= len(combo_colors) - 1:
                        color_index = 0
                    else:
                        color_index += 1

                color = combo_colors[color_index] if combo_colors else (255, 255, 255)

                circles.append([
                    int(par[0]) * scale_x + offset_x,
                    int(par[1]) * scale_y + offset_y,
                    float(par[2]),
                    int(par[3]),
                    color
                ])
                
            if line.startswith("AudioFilename:"):
                map_song = line.split(":", 1)[1].strip()
                print("AudioFilename:", map_song)
            if line.startswith("CircleSize:"):
                CS = float(line.split(":", 1)[1].strip())
                print("CircleSize:", str(CS))
            if line.startswith("ApproachRate:"):
                AR = float(line.split(":", 1)[1].strip())
                print("ApproachRate:", str(AR))
            if line.startswith("OverallDifficulty:"):
                OD = float(line.split(":", 1)[1].strip())
                print("OverallDifficulty:", str(OD))
            if line.startswith('0,0,"'):
                has_background = True
                bg_file_name = line.split('"')[1]
                print("BG file:", bg_file_name)
            if line.startswith(f"Combo{combo_num} :"):
                colors = [int(color.strip()) for color in line.split(":")[1].split(",")]
                combo_colors.append((colors[0], colors[1], colors[2]))
                combo_num += 1
            if line.startswith("[HitObjects]"):
                hitobjects_section = True

    print("Combo colors:", combo_colors)
    audio_file = os.path.join(osu_map_path, map_song)

    r = (54.4 - (4.48 * CS))*scale_y
    d = int(r*2)

    if AR < 5:
        preempt = 1200 + 600 * (5 - AR) / 5
        fade_in = 800 + 400 * (5 - AR) / 5
    elif AR > 5:
        preempt = 1200 - 750 * (AR - 5) / 5
        fade_in = 800 - 500 * (AR - 5) / 5
    else:
        preempt = 1200
        fade_in = 800

    hit300_window = 80-6*OD
    hit100_window = 140-8*OD
    hit50_window = 200-10*OD

    mouse_pos_history = []
    angle = 0
    circles_on_scene = []

    pg.init()
    pg.mixer.init()

    font = pg.font.SysFont("Arial", 24)
    
    if fullscreen:
        screen = pg.display.set_mode((WIDTH, HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF | pg.FULLSCREEN)

        
    else:
        screen = pg.display.set_mode((WIDTH, HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)

    print("Fullscreen:", fullscreen)

    pg.display.set_caption("PyOsu!")
    icon = pg.image.load("Data/osu_logo.png")
    pg.display.set_icon(icon)

    approach_circle = pg.image.load(osu_path_skins + f"/{skin_name}/approachcircle.png").convert_alpha()

    cursor = pg.image.load(osu_path_skins + f"/{skin_name}/cursor.png").convert_alpha()
    #cursor_middle = pg.image.load(osu_path_skins + "/cursormiddle.png").convert_alpha()
    #cursor_middle = pg.transform.smoothscale(cursor_middle, (cursor_middle.get_size()[0] * cursor_size,cursor_middle.get_size()[1] * cursor_size))
    cursor_trail = pg.image.load(osu_path_skins + f"/{skin_name}/cursortrail.png").convert_alpha()
    cursor = pg.transform.smoothscale(cursor, (cursor.get_size()[0] * cursor_size,cursor.get_size()[1] * cursor_size))
    cursor_trail = pg.transform.smoothscale(cursor_trail, (cursor_trail.get_size()[0] * cursor_size,cursor_trail.get_size()[1] * cursor_size))

    circle_sprite = pg.image.load(osu_path_skins + f"/{skin_name}/hitcircle.png").convert_alpha()

    def colorize_white_image(image, new_color):
        tinted_image = image.copy()
        color_surface = pg.Surface(image.get_size()).convert_alpha()
        color_surface.fill(new_color)
        tinted_image.blit(color_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        return tinted_image
    
    approach_circle = pg.transform.smoothscale(approach_circle, (d, d))

    circle_sprite = pg.transform.smoothscale(circle_sprite, (d, d))
    circle_overlay = pg.image.load(osu_path_skins + f"/{skin_name}/hitcircleoverlay.png")
    circle_overlay = pg.transform.smoothscale(circle_overlay, (d, d))
    number1 = pg.image.load(osu_path_skins + f"/{skin_name}/default-2.png")
    number1 = pg.transform.smoothscale(number1, (number1.get_size()[0]*0.8, number1.get_size()[1]*0.8))

    if has_background:
        bg_path = os.path.join(osu_map_path, bg_file_name)
        background = pg.image.load(bg_path).convert_alpha()
        background.set_alpha(dim)

        original_bg_width, original_bg_height = background.get_size()

        new_bg_height = int(original_bg_height * (WIDTH / original_bg_width))

        background = pg.transform.smoothscale(background, (WIDTH, new_bg_height))

    running = True
    clock = pg.time.Clock()
    prev_time = time.time()
    pg.mouse.set_visible(False)

    hitsound = pg.mixer.Sound(osu_path_skins + f"/{skin_name}/normal-hitclap2.wav")
    hitsound.set_volume(hitsound_volume)

    pg.mixer.music.load(audio_file)
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(0)

    color_index = 0
    trail_interval = 1000 / 60
    last_trail_time = 0

    while running:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False              
                    
        curr_time = pg.mixer.music.get_pos()
        delta_time = (curr_time - prev_time) / 1000.0
        prev_time = curr_time
        
        if not pg.mixer.music.get_busy():
            print("Trak finished")
            
            running = False

        screen.fill((0, 0, 0))
        if has_background:
            screen.blit(background, background.get_rect(center=(WIDTH//2, HEIGHT//2)))
        screen.blit(overlay, (offset_x, offset_y))
        
        if len(circles) > 0 and curr_time >= circles[0][2] - preempt:
            circles_on_scene.append([circles[0], curr_time])
            circles.pop(0)

        for circle_data in reversed(circles_on_scene):

            circle, appear_time = circle_data
            x, y, hit_time, note_type, color = circle

            circle_sprite_colored = colorize_white_image(circle_sprite, color)
            approach_circle_colored = colorize_white_image(approach_circle, color)

            time_since_appeared = (curr_time - appear_time)

            if time_since_appeared < fade_in:
                alpha = float((time_since_appeared / fade_in) * 255)
                alpha = max(0, min(255, alpha))
            else:
                alpha = 255

            temp_circle = circle_sprite_colored.copy()
            temp_approach_circle = approach_circle_colored.copy()

            #temp_number = number1.copy()

            temp_circle.set_alpha(alpha)
            temp_approach_circle.set_alpha(alpha)
            #temp_number.set_alpha(alpha)
            

            scale_factor = max(1, 4 - 3 * (time_since_appeared / preempt))

            scaled_size = float(d * scale_factor)
            temp_approach_scaled = pg.transform.smoothscale(temp_approach_circle, (scaled_size, scaled_size))

            screen.blit(temp_approach_scaled, temp_approach_scaled.get_rect(center=(x, y)))

            screen.blit(temp_circle, temp_circle.get_rect(center=(x, y)))
            temp_overlay = circle_overlay.copy()
            temp_overlay.set_alpha(alpha)
            screen.blit(temp_overlay, temp_overlay.get_rect(center=(x, y)))

            #screen.blit(temp_number, temp_number.get_rect(center=(x, y)))

        if len(circles_on_scene) > 0 and curr_time >= circles_on_scene[0][0][2]:
                hitsound.play()
                circles_on_scene.pop(0)

        mouse_pos = pg.mouse.get_pos()

        if curr_time - last_trail_time >= trail_interval:
            mouse_pos_history.append([mouse_pos, curr_time])
            last_trail_time = curr_time

        mouse_pos_history = [pos for pos in mouse_pos_history if curr_time - pos[1] <= 100]


        for x in mouse_pos_history[:]:
            if x[1] >= curr_time - 100:
                screen.blit(cursor_trail, (x[0][0] - cursor_trail.get_size()[0]//2, x[0][1] - cursor_trail.get_size()[0]//2))
            else:
                mouse_pos_history.remove(x)

        rotated_cursor = pg.transform.rotate(cursor, angle)
        rotated_rect = rotated_cursor.get_rect(center=mouse_pos)
        screen.blit(rotated_cursor, rotated_rect.topleft)
        #screen.blit(cursor_middle, cursor_middle.get_rect(center=mouse_pos))

        angle -= 0.5

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        info_quit = font.render('Press "q" to exit', True, (255, 255, 255))
        screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
        screen.blit(info_quit,  (WIDTH - info_quit.get_width() - 10, 40))

        pg.display.flip()

        clock.tick(FPS)

    pg.quit()