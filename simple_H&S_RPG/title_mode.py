from pico2d import get_events, clear_canvas, update_canvas, draw_rectangle, get_time, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework
import game_world
import play_mode
import server
from title_pannel import *

WIDTH = 1280
HEIGHT = 720

server.weapon = 'Sword'
server.weapon_ABC = 'A'

def draw_thick_rectangle(x1, y1, x2, y2, thickness):
    for i in range(thickness):
        draw_rectangle(x1 - i, y1 - i, x2 + i, y2 + i)

def init():
    server.time = 0
    server.weapon = 'Sword'
    server.weapon_ABC = 'A'

    global background
    global panel_sword, panel_bow
    global start_button
    global sword_button, sword_A, sword_B
    global bow_button, bow_A, bow_B, bow_C
    global Button_sound, start_Button_sound
    global sword_choose, bow_choose

    sword_choose = 'A'
    bow_choose = 'A'

    Button_sound = load_wav('resource/sounds/button_click.wav')
    Button_sound.set_volume(128)
    start_Button_sound = load_wav('resource/sounds/button_start.wav')
    start_Button_sound.set_volume(32)

    panel_sword = Pannel(400, HEIGHT - 150, 400, 200)
    panel_bow = Pannel(400, HEIGHT - 300, 400, 200)

    sword_A = Sword_A(100 + 175, HEIGHT - 150, 100, 100)
    sword_B = Sword_B(100 + 175 + 125, HEIGHT - 150, 100, 100)
    bow_A = Bow_A(100 + 175, HEIGHT - 300, 100, 100)
    bow_B = Bow_B(100 + 175 + 125, HEIGHT - 300, 100, 100)
    bow_C = Bow_C(100 + 175 + 125 + 125, HEIGHT - 300, 100, 100)

    #====================================================================
    background = Background()
    game_world.add_object(background, 3)

    start_button = Start_Button(WIDTH - 200, 100, 300, 100)
    game_world.add_object(start_button, 4)

    sword_button = Sword_Button(100, HEIGHT - 150, 100, 100)
    game_world.add_object(sword_button, 4)

    bow_button = Bow_Button(100, HEIGHT - 300, 100, 100)
    game_world.add_object(bow_button, 4)

def finish():
    game_world.remove_object(background)
    game_world.remove_object(start_button)
    game_world.remove_object(sword_button)
    game_world.remove_object(bow_button)

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    if server.weapon == 'Sword':
        draw_thick_rectangle(sword_button.x - 50, sword_button.y - 50,
                       sword_button.x + 50, sword_button.y + 50, 3)
        panel_sword.draw()
        sword_A.draw()
        sword_B.draw()
        if sword_choose == 'A':
            draw_thick_rectangle(sword_A.x - 50, sword_A.y - 50,
                                 sword_A.x + 50, sword_A.y + 50, 3)
        else:
            draw_thick_rectangle(sword_B.x - 50, sword_B.y - 50,
                                 sword_B.x + 50, sword_B.y + 50, 3)
    elif server.weapon == 'Bow' :
        draw_thick_rectangle(bow_button.x - 50, bow_button.y - 50,
                       bow_button.x + 50, bow_button.y + 50, 3)
        panel_bow.draw()
        bow_A.draw()
        bow_B.draw()
        bow_C.draw()
        if bow_choose == 'A':
            draw_thick_rectangle(bow_A.x - 50, bow_A.y - 50,
                                 bow_A.x + 50, bow_A.y + 50, 3)
        elif bow_choose == 'B':
            draw_thick_rectangle(bow_B.x - 50, bow_B.y - 50,
                                 bow_B.x + 50, bow_B.y + 50, 3)
        else:
            draw_thick_rectangle(bow_C.x - 50, bow_C.y - 50,
                                 bow_C.x + 50, bow_C.y + 50, 3)
    update_canvas()

def handle_events():
    events = get_events()
    global sword_choose, bow_choose
    global Button_sound, start_Button_sound
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, (HEIGHT - event.y)  # Pico2D에서 y축 방향 보정
            if server.weapon == 'Sword':
                if sword_A.is_clicked(x, y):
                    Button_sound.play()
                    sword_choose = 'A'
                    server.weapon_ABC = 'A'
                elif sword_B.is_clicked(x, y):
                    Button_sound.play()
                    sword_choose = 'B'
                    server.weapon_ABC = 'B'
            elif server.weapon == 'Bow':
                if bow_A.is_clicked(x, y):
                    Button_sound.play()
                    bow_choose = 'A'
                    server.weapon_ABC = 'A'
                elif bow_B.is_clicked(x, y):
                    Button_sound.play()
                    bow_choose = 'B'
                    server.weapon_ABC = 'B'
                elif bow_C.is_clicked(x, y):
                    Button_sound.play()
                    bow_choose = 'C'
                    server.weapon_ABC = 'C'

            if start_button.is_clicked(x, y):
                start_Button_sound.play()
                print("Start button clicked")
                server.kill_count = 0
                server.spawn_boss_count = 0
                server.start_time = get_time()
                server.boss_dead = False
                server.player_dead = False
                server.skill_1_using = False
                game_world.clear_all()
                game_framework.change_mode(play_mode)
            else :
                if sword_button.is_clicked(x, y):
                    Button_sound.play()
                    print("Sword button clicked")
                    server.weapon = 'Sword'
                elif bow_button.is_clicked(x, y):
                    Button_sound.play()
                    print("Bow button clicked")
                    server.weapon = 'Bow'

def pause():pass
def resume():pass
