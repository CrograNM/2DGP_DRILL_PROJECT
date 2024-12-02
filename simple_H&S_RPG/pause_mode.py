from pico2d import get_events, clear_canvas, update_canvas, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework
import game_world
import title_mode
from pause_pannel import Pannel, Back_Button, Resume_Button
import server

WIDTH = 1280
HEIGHT = 720

def init():
    global pannel
    global back_button
    global resume_button
    global Button_sound, start_Button_sound

    Button_sound = load_wav('resource/sounds/button_click.wav')
    Button_sound.set_volume(128)
    start_Button_sound = load_wav('resource/sounds/button_start.wav')
    start_Button_sound.set_volume(32)

    pannel = Pannel()
    game_world.add_object(pannel, 3)

    resume_button = Resume_Button(WIDTH//2, HEIGHT//2 + 80, 400, 100)
    game_world.add_object(resume_button, 4)

    back_button = Back_Button(WIDTH//2, HEIGHT//2 - 100, 400, 100)
    game_world.add_object(back_button, 4)


def finish():
    game_world.remove_object(pannel)
    game_world.remove_object(resume_button)
    game_world.remove_object(back_button)

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    global Button_sound, start_Button_sound
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            Button_sound.play()
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, (HEIGHT - event.y)  # Pico2D에서 y축 방향 보정
            if resume_button.is_clicked(x, y):
                Button_sound.play()
                print("Resume button clicked")
                game_framework.pop_mode()
            elif back_button.is_clicked(x, y):
                start_Button_sound.play()
                server.weapon = 'Sword'
                server.weapon_ABC = 'A'
                print("Back button clicked")
                game_world.clear()
                game_framework.push_mode(title_mode)

def pause():pass
def resume():pass
