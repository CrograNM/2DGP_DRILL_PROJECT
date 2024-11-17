from pico2d import *
import game_world
import game_framework
import time
import server
from player import Player
from ground import Ground
from monster import Monster
import title_mode
import pause_mode

from background import Background

# Game object class here
# class 드래그 후 우클릭 -> 리팩터링(이동)

last_spawn_time = 0
def spawn_monster():
    global last_spawn_time

    # 0.2초마다 몬스터 스폰
    current_time = time.time()
    if current_time - last_spawn_time >= 0.2:
        # 현재 몬스터 개수 확인
        monsters = [obj for obj in game_world.objects_at_depth(1) if isinstance(obj, Monster)]
        if len(monsters) < 10:  # 최대 10마리까지만 스폰
            new_monster = Monster(server.player)
            game_world.add_object(new_monster, 1)  # 포그라운드 깊이에 추가
            game_world.add_collision_pair('player:monster', server.player, new_monster)
            game_world.add_collision_pair('monster:skill_1', new_monster, None)
        last_spawn_time = current_time

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
    server.background = Background()
    game_world.add_object(server.background, 0)

    server.player = Player()
    game_world.add_object(server.player, 1)  # 포그라운드 깊이에 그린다 (앞)

def finish():
    game_world.clear()

def update():
    spawn_monster()
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