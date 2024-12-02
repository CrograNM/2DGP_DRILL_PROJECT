from pico2d import load_image, get_time, clear_canvas, update_canvas, get_events
import game_framework
import title_mode

def init():
    global image
    global logo_start_time

    image = load_image('resource/tuk_credit.png')
    logo_start_time = get_time()

def finish():
    global image
    del image # image는 용량이 크기 때문에 지워주도록 한다.

def update():
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw(1280//2,720//2)
    update_canvas()

def handle_events():
    events = get_events()

def pause():
    pass

def resume():
    pass