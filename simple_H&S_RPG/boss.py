from random import randint
from pico2d import *

import server
from player import Player
from state_machine import mob_close, mob_attack_end
from state_machine import StateMachine
import game_framework
import game_world

# Monster Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Monster Action Speed
TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 4
FRAMES_PER_ACTION_ATTACK = 4

MONSTER_SIZE = 100
# sx, sy = 0 , 0
WIDTH = 1280
HEIGHT = 720

class Idle:
    @staticmethod
    def enter(mob, e):
        mob.current_state = 'Idle'
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
        mob.delayCount += 1
        mob.frame = (mob.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_IDLE

        # 충분히 거리가 가까워지면 공격 모션을 진행
        if mob.delayCount > 300:
            mob.delayCount = 0
            mob.state_machine.add_event(('MOB_CLOSE', 0))

    @staticmethod
    def draw(mob):
        if mob.face_dir == -1:
            mob.images['Idle'].clip_composite_draw(int(mob.frame) * 67, 0, 67, 50, 0, 'h', mob.x, mob.y, 67 * 4, 50 * 4)
        else:
            mob.images['Idle'].clip_composite_draw(int(mob.frame) * 67, 0, 67, 50, 0, '', mob.x, mob.y, 67 * 4, 50 * 4)

        pass

class Attack:
    @staticmethod
    def enter(mob, e):
        mob.current_state = 'Attack'
        mob.frame = 0
        pass

    @staticmethod
    def exit(mob, e):
        pass

    @staticmethod
    def do(mob):
        mob.frame = mob.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * game_framework.frame_time
        if int(mob.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            mob.state_machine.add_event(('MOB_ATTACK_END', 0))


    @staticmethod
    def draw(mob):
        if mob.face_dir == -1:
            mob.images['Attack'].clip_composite_draw(int(mob.frame) * 110, 0, 110, 50, 0, 'h', mob.x - 60, mob.y, 110 * 4, 50 * 4)
        else:
            mob.images['Attack'].clip_composite_draw(int(mob.frame) * 110, 0, 110, 50, 0, ' ', mob.x - 60, mob.y, 110 * 4, 50 * 4)


animation_names = ['Idle', 'Attack']
# 100, 86, frames = 4

class Boss:
    images = None

    def load_images(self):
        if Boss.images == None:
            Boss.images = {}
            for name in animation_names:
                Boss.images[name] = load_image("resource/boss/" + name + ".png")
                # Monster.images['Attack'] = load_image('monster_Attack.png')

    def __init__(self, player):
        self.x, self.y = WIDTH//2 + 450, 158
        self.ax, self.ay = self.x, self.y - 20
        self.load_images()
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = -1
        self.action = 0
        self.hp = 100

        self.font = load_font('resource/ENCR10B.TTF', 16)
        # self.image_Run = load_image('monster_Run.png')
        # self.image_Attack = load_image('monster_Attack.png')
        self.current_state = None

        self.player = player  # player 참조

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {mob_close : Attack},
                Attack: {mob_attack_end : Idle}
                # ,Attack: {}, Hit: {}
            }
        )
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 15, self.y + 100, f'{self.hp}', (255, 0, 0))
        draw_rectangle(*self.get_bb())
        #draw_rectangle(self.ax - 5, self.ay - 5, self.ax + 5, self.ay + 5)

    def get_bb(self):
        return self.x - MONSTER_SIZE*0.7, self.y - MONSTER_SIZE, self.x + MONSTER_SIZE*0.7, self.y + MONSTER_SIZE*0.5

    def handle_collision(self, group, other):
        # fill here
        if group == 'boss:skill_1':
            game_world.remove_object(self)
            # server.kill_count += 1
            server.boss_dead = True
        pass