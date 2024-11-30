from pico2d import load_image, get_events, clear_canvas, update_canvas, draw_rectangle, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework
import game_world
import play_mode
import server
from title_pannel import *

WIDTH = 1280
HEIGHT = 720

server.weapon = 'Sword'

def draw_thick_rectangle(x1, y1, x2, y2, thickness):
    for i in range(thickness):
        draw_rectangle(x1 - i, y1 - i, x2 + i, y2 + i)

def init():
    server.time = 0

    global background
    global start_button
    global sword_button
    global bow_button

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
    elif server.weapon == 'Bow' :
        draw_thick_rectangle(bow_button.x - 50, bow_button.y - 50,
                       bow_button.x + 50, bow_button.y + 50, 3)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, (HEIGHT - event.y)  # Pico2D에서 y축 방향 보정
            if start_button.is_clicked(x, y):
                print("Start button clicked")
                server.kill_count = 0
                server.spawn_boss_count = 0
                server.start_time = get_time()
                server.boss_dead = False
                server.skill_1_using = False
                game_world.clear_all()
                game_framework.change_mode(play_mode)
            else :
                if sword_button.is_clicked(x, y):
                    print("Sword button clicked")
                    server.weapon = 'Sword'
                elif bow_button.is_clicked(x, y):
                    print("Bow button clicked")
                    server.weapon = 'Bow'

def pause():pass
def resume():pass
