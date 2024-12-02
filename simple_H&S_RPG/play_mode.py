from pico2d import *
import game_world
import game_framework
import time
import server

from player import Player
from background import Background
from monster import Monster
from boss import Boss

import pause_mode
import result_mode

BOSS_APPEAR_TIME = 10   # 1초 : 테스트용, 나중에 30초, 60초 등으로 설정
MAX_MOB_COUNT = 10   # 최대 10마리까지만 스폰

# 전역 변수 추가
pause_time = 0
paused_duration = 0

server.spawn_boss_count = 0
def spawn_boss():
    boss = Boss(server.player)
    game_world.add_object(boss, 1)  # 포그라운드 깊이에 추가
    game_world.add_collision_pair('player:boss', server.player, boss)
    game_world.add_collision_pair('player:boss_skill', server.player, None)
    game_world.add_collision_pair('player:boss_skill_!!!', server.player, None) #강한 공격
    game_world.add_collision_pair('boss:skill_1', boss, None)

last_spawn_time = 0
def spawn_monster():
    global last_spawn_time

    # 0.2초마다 몬스터 스폰
    current_time = time.time()
    if current_time - last_spawn_time >= 0.2:
        # 현재 몬스터 개수 확인
        monsters = [obj for obj in game_world.objects_at_depth(1) if isinstance(obj, Monster)]
        if len(monsters) < MAX_MOB_COUNT:
            new_monster = Monster(server.player)
            game_world.add_object(new_monster, 1)  # 포그라운드 깊이에 추가
            game_world.add_collision_pair('player:monster', server.player, new_monster)
            game_world.add_collision_pair('player:monster_attack', server.player, None)
            game_world.add_collision_pair('monster:skill_1', new_monster, None)
        last_spawn_time = current_time

def handle_events():
    events = get_events()
    global Button_sound
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            Button_sound.play()
            game_framework.push_mode(pause_mode)
            # game_framework.change_mode(title_mode)
        else:
            server.player.handle_event(event)

def init():
    global mode
    mode = 'monster'

    global Button_sound
    Button_sound = load_wav('resource/sounds/button_click.wav')

    server.background = Background()
    game_world.add_object(server.background, 0)

    server.player = Player()
    game_world.add_object(server.player, 1)  # 포그라운드 깊이에 그린다 (앞)

def finish():
    global pause_time, paused_duration
    pause_time = 0
    paused_duration = 0
    server.time = 0
    server.kill_count = 0
    game_world.clear()

def update():
    global mode
    if mode == 'monster':
        spawn_monster()
        server.time = get_adjusted_time()
    if server.time > BOSS_APPEAR_TIME:
        mode = 'boss'
        if server.spawn_boss_count == 0:
            spawn_boss()
            server.spawn_boss_count += 1
    if server.boss_dead == True:
        game_framework.push_mode(result_mode)
    elif server.player_dead == True:
        game_framework.push_mode(result_mode)
    game_world.update()
    game_world.handle_collisions()
    delay(0.01)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    global pause_time
    pause_time = current_time()  # 일시정지 시점 저장
    pass

def resume():
    global pause_time, paused_duration
    if pause_time != 0:
        paused_duration += current_time() - pause_time  # 누적 일시정지 시간 계산
        pause_time = 0
    pass

# 시간을 보정하여 반환하는 함수
def get_adjusted_time():
    return current_time() - paused_duration

def current_time():
    return get_time() - server.start_time