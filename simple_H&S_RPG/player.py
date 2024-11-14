from pico2d import load_image, get_time, load_font

from state_machine import time_out, space_down, right_down, right_up, left_down, left_up, start_event
from state_machine import StateMachine
import game_framework

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 4
FRAMES_PER_ACTION_RUN = 6

class Idle:
    @staticmethod
    def enter(player, e):
        if start_event(e):
            player.action = 0
            player.face_dir = -1
        elif right_down(e) or left_up(e):
            player.action = 0
            player.face_dir = -1
        elif left_down(e) or right_up(e):
            player.action = 0
            player.face_dir = 1

        player.frame = 0
        player.delayCount = 0
        player.start_time = get_time()

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_IDLE
        # if get_time() - player.start_time > 3:
        #     player.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Idle.clip_composite_draw(int(player.frame) * 42, 0, 42, 42, 0, '', player.x, player.y, 84, 84)
        else:
            player.image_Idle.clip_composite_draw(int(player.frame) * 42, 0, 42, 42, 0, 'h', player.x, player.y, 84, 84)

class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):  
            player.dir, player.action = 1, 0
            player.face_dir = 1
        elif left_down(e) or right_up(e): 
            player.dir, player.action = -1, 0
            player.face_dir = -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_RUN
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Run.clip_composite_draw(int(player.frame) * 42, 0, 42, 42, 0, '', player.x + 5, player.y, 84, 84)
        else:
            player.image_Run.clip_composite_draw(int(player.frame) * 42, 0, 42, 42, 0, 'h', player.x - 5, player.y, 84, 84)

class Player:
    def __init__(self):
        self.x, self.y = 200, 90
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 0
        self.image_Idle = load_image('character_Idle.png')
        self.image_Run = load_image('character_Run.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {   #상태 변환 테이블 : 더블 Dict로 구현
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}
            }
        )
        self.font = load_font('ENCR10B.TTF', 16)
        self.hp = 100
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'(HP: {self.hp})', (255, 0, 0))