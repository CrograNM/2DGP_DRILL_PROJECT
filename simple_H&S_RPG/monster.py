from pico2d import *

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
FRAMES_PER_ACTION_RUN = 12
FRAMES_PER_ACTION_ATTACK = 9

MONSTER_SIZE = 48
sx, sy = 0 , 0

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
            mob.images['Attack'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, '', mob.x - 20, mob.y, 144, 96)
        else:
            mob.images['Attack'].clip_composite_draw(int(mob.frame) * 72, 0, 72, 48, 0, 'h', mob.x + 20, mob.y, 144, 96)


animation_names = ['Run', 'Attack']

class Monster:
    images = None

    def load_images(self):
        if Monster.images == None:
            Monster.images = {}
            for name in animation_names:
                Monster.images[name] = load_image("resource/monster/monster_"+ name + ".png")
                # Monster.images['Attack'] = load_image('monster_Attack.png')

    def __init__(self, player):
        self.x, self.y = 600, 108
        self.load_images()
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 0
        # self.image_Run = load_image('monster_Run.png')
        # self.image_Attack = load_image('monster_Attack.png')
        self.current_state = None

        self.player = player  # player 참조

        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            {
                Run: {mob_close : Attack},
                Attack: {mob_attack_end : Run}
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
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.current_state == 'Run':
            return self.x - MONSTER_SIZE*0.7, self.y - MONSTER_SIZE, self.x + MONSTER_SIZE*0.7, self.y + MONSTER_SIZE*0.5
        elif self.current_state == 'Attack':
            # 애니메이션에 따라 크기, 위치 변경이 필요함
            return self.x - MONSTER_SIZE * 1.8, self.y - MONSTER_SIZE, self.x + MONSTER_SIZE * 1.8, self.y + MONSTER_SIZE * 0.5

    def handle_collision(self, group, other):
        # fill here
        # if group == 'zombie:ball':
        #     self.size -= 100
        #     self.y = self.size / 2 + 50
        #     if self.size <= 0:
        #         game_world.remove_object(self)
        pass