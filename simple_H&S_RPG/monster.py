from random import randint
from pico2d import *

import server
from player import Player
from state_machine import mob_close, mob_attack_end, time_out, hurt_start
from state_machine import StateMachine
import game_framework
import game_world
from skill import Monster_Attack

# Monster Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Monster Action Speed
TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_RUN = 12
FRAMES_PER_ACTION_ATTACK = 9
FRAMES_PER_ACTION_HIT = 5

MONSTER_SIZE = 48  #72
# sx, sy = 0 , 0
WIDTH = 1280
HEIGHT = 720

class Run:
    @staticmethod
    def enter(mob, e):
        mob.current_state = 'Run'
        if mob.player.x > mob.x:
            mob.dir = 1  # player가 오른쪽에 있을 때
            mob.face_dir = 1
        elif mob.player.x < mob.x:
            mob.dir = -1  # player가 왼쪽에 있을 때
            mob.face_dir = -1
        mob.frame = 0
        pass

    @staticmethod
    def exit(mob, e):
        pass

    @staticmethod
    def do(mob):
        mob.frame = (mob.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_RUN
        mob.ax = mob.x

        # 충분히 거리가 가까워지면 공격 모션을 진행
        if mob.player.x - 80 < mob.x < mob.player.x + 80:
            mob.state_machine.add_event(('MOB_CLOSE', 0))
        else:
            # player.x 위치를 추적하여 mob.dir 설정
            if mob.player.x > mob.x:
                mob.dir = 1  # player가 오른쪽에 있을 때
                mob.face_dir = 1
            elif mob.player.x < mob.x:
                mob.dir = -1  # player가 왼쪽에 있을 때
                mob.face_dir = -1

            mob.x += mob.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(mob):
        if mob.face_dir == -1:
            mob.images['Run'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, '', mob.x - 20, mob.y, 144, 96)
        else:
            mob.images['Run'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, 'h', mob.x + 20, mob.y, 144, 96)
        pass

class Attack:
    @staticmethod
    def enter(mob, e):
        mob.current_state = 'Attack'
        mob.frame = 0
        mob.attack_count = 0
        pass

    @staticmethod
    def exit(mob, e):
        pass

    @staticmethod
    def do(mob):
        mob.frame = mob.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * game_framework.frame_time
        if int(mob.frame) >= (FRAMES_PER_ACTION_ATTACK - 1) / 2:
            mob.ax = mob.x + (mob.face_dir * (FRAMES_PER_ACTION_ATTACK - 1) / 2 * 12) - (mob.face_dir * int(mob.frame)%4 * 12)
        else :
            mob.ax = mob.x + (mob.face_dir * int(mob.frame) * 12)
        if int(mob.frame) == 4 and mob.attack_count == 0:
            mob.atk_sound.play()
            mob.monster_attack(1)
            mob.attack_count += 1
        if int(mob.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            mob.state_machine.add_event(('MOB_ATTACK_END', 0))
            #mob.monster_attack(1)

    @staticmethod
    def draw(mob):
        if mob.face_dir == -1:
            mob.images['Attack'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, '', mob.x - 20, mob.y, 144, 96)
        else:
            mob.images['Attack'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, 'h', mob.x + 20, mob.y, 144, 96)

class Hit:
    @staticmethod
    def enter(mob, e):
        mob.current_state = 'Hit'
        mob.frame = 0
        pass

    @staticmethod
    def exit(mob, e):
        pass

    @staticmethod
    def do(mob):
        mob.frame = mob.frame + FRAMES_PER_ACTION_HIT * ACTION_PER_TIME * game_framework.frame_time
        if int(mob.frame) == FRAMES_PER_ACTION_HIT - 1:
            mob.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(mob):
        if mob.face_dir == -1:
            mob.images['Hit'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, '', mob.x - 20, mob.y, 144, 96)
        else:
            mob.images['Hit'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, 'h', mob.x + 20, mob.y, 144, 96)

animation_names = ['Run', 'Attack', 'Hit']

class Monster:
    images = None
    atk_sound = None
    hit_sound_sword = None
    hit_sound_bow = None

    def load_images(self):
        if Monster.images == None:
            Monster.images = {}
            for name in animation_names:
                Monster.images[name] = load_image("resource/monster/monster_"+ name + ".png")
                # Monster.images['Attack'] = load_image('monster_Attack.png')

    def __init__(self, player):
        if not Monster.atk_sound:
            Monster.atk_sound = load_wav('resource/sounds/mob_slap.wav')
            Monster.atk_sound.set_volume(16)

            Monster.hit_sound_sword = load_wav('resource/sounds/hit_sword.wav')
            Monster.hit_sound_sword.set_volume(16)

            Monster.hit_sound_bow = load_wav('resource/sounds/hit_arrow.wav')
            Monster.hit_sound_bow.set_volume(16)

        self.x, self.y = WIDTH//2 + randint(WIDTH//4,WIDTH//2), 108
        self.ax, self.ay = self.x, self.y - 20
        self.load_images()
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 0

        self.hp_max = 100
        self.hp = self.hp_max
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.current_state = None

        self.player = player  # player 참조

        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            {
                Run: {mob_close : Attack, hurt_start:Hit},
                Attack: {mob_attack_end : Run, hurt_start:Hit},
                Hit: {time_out : Run}
            }
        )
        self.hit_by_skills = {} #스킬 객체를 키로, 충돌 상태를 값으로 저장

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        if self.hp != self.hp_max:
            if self.face_dir == -1:
                self.font.draw(self.x - 7, self.y - 62, f'{self.hp}', (255, 0, 0))
            else:
                self.font.draw(self.x - 13, self.y - 62, f'{self.hp}', (255, 0, 0))

    def get_bb(self):
        if self.current_state == 'Run' or 'Hit':
            return self.x - MONSTER_SIZE*0.7, self.y - MONSTER_SIZE, self.x + MONSTER_SIZE*0.7, self.y + MONSTER_SIZE*0.5
        elif self.current_state == 'Attack':
            # 애니메이션에 따라 크기, 위치 변경이 필요함
            return self.ax - 5, self.ay - 5, self.ax + 5, self.ay + 5

    def handle_collision(self, group, other):
        if self.current_state == 'Run' or 'Attack':
            if group == 'monster:skill_1':
                if other not in self.hit_by_skills or not self.hit_by_skills[other]:
                    self.hp -= self.player.dmg
                    self.hit_by_skills[other] = True  # 충돌 상태 업데이트
                    self.state_machine.add_event(('HURT_START', 0))
                    if server.weapon == 'Sword':
                        Monster.hit_sound_sword.play()
                        pass
                    else:
                        Monster.hit_sound_bow.play()
                        pass
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.kill_count += 1

    def monster_attack(self, num):
        monster_attack = Monster_Attack(self.x + self.dir * 87, self.y - 20, self.dir)
        game_world.add_collision_pair('player:monster_attack', None, monster_attack)
        game_world.add_object(monster_attack, 1)