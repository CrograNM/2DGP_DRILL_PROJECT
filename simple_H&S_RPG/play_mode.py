from pico2d import *

from player import Player
from ground import Ground
from monster import Monster
import game_world
import game_framework
import title_mode

# Game object class here
# class 드래그 후 우클릭 -> 리팩터링(이동)


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)

def init():
    global running

    global ground
    global player
    global monster
    #global team

    running = True

    ground = Ground()
    game_world.add_object(ground, 0)  # 백그라운드 깊이에 그린다 (뒤)

    player = Player()
    game_world.add_object(player, 1)  # 포그라운드 깊이에 그린다 (앞)

    monster = Monster(player)
    game_world.add_object(monster, 1)  # 포그라운드 깊이에 그린다 (앞)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    delay(0.01)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass