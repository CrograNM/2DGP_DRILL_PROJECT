from pico2d import load_image, get_events, clear_canvas, update_canvas, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework
import game_world
import play_mode
# import play_boss_mode
import server
import title_mode
from pause_pannel import Pannel, Back_Button

WIDTH = 1280
HEIGHT = 720

def init():
    global pannel
    global back_button
    global font
    font =  load_font('resource/ENCR10B.TTF', 30)

    pannel = Pannel()
    game_world.add_object(pannel, 3)

    back_button = Back_Button(WIDTH//2, HEIGHT//2 - 100, 400, 100)
    game_world.add_object(back_button, 4)


def finish():
    game_world.remove_object(pannel)
    game_world.remove_object(back_button)

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    font.draw(WIDTH // 2 - 70, HEIGHT // 2 + 100, f'{server.kill_count} Kills', (255, 0, 0))
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
            if back_button.is_clicked(x, y):
                print("Back button clicked")
                game_world.clear()
                game_framework.push_mode(title_mode)

def pause():pass
def resume():pass
