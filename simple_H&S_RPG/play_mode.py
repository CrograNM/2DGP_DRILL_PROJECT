from pico2d import *
import game_world
import game_framework

import server
from player import Player
from ground import Ground
from monster import Monster
import title_mode
import pause_mode

from background import Background

# Game object class here
# class 드래그 후 우클릭 -> 리팩터링(이동)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(pause_mode)
            # game_framework.change_mode(title_mode)
        else:
            server.player.handle_event(event)

def init():
    # ground = Ground()
    # game_world.add_object(ground, 0)  # 백그라운드 깊이에 그린다 (뒤)

    server.background = Background()
    game_world.add_object(server.background, 0)

    server.player = Player()
    game_world.add_object(server.player, 1)  # 포그라운드 깊이에 그린다 (앞)

    monster = Monster(server.player)
    game_world.add_object(monster, 1)  # 포그라운드 깊이에 그린다 (앞)

    #충돌 체크
    game_world.add_collision_pair('player:monster', server.player, monster)
    # for monster in monsters:
    #     game_world.add_collision_pair('player:monster', player, monster)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()
    delay(0.01)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass