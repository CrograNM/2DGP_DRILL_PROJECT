from pico2d import *
from state_machine import *
import game_framework
import game_world
from skill import Skill_lightening

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ATTACK_SPEED_PPS = RUN_SPEED_PPS * 20

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 4
FRAMES_PER_ACTION_RUN = 6
FRAMES_PER_ACTION_ATTACK = 6

PLAYER_SIZE = 42

class Idle:
    @staticmethod
    def enter(player, e):
        player.dir = 0
        if start_event(e):
            player.face_dir = -1
        elif right_down(e) or left_up(e):
            player.face_dir = -1
        elif left_down(e) or right_up(e):
            player.face_dir = 1

        player.frame = 0
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
            player.image_Idle.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                  0, '', player.x, player.y, PLAYER_SIZE*2, PLAYER_SIZE*2)
        else:
            player.image_Idle.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                  0, 'h', player.x, player.y, PLAYER_SIZE*2, PLAYER_SIZE*2)

class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):
            player.result_dir = 1
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.result_dir = -1
            player.dir = -1
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
            player.image_Run.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                 0, '', player.x + 5, player.y, PLAYER_SIZE*2, PLAYER_SIZE*2)
        else:
            player.image_Run.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                 0, 'h', player.x - 5, player.y, PLAYER_SIZE*2, PLAYER_SIZE*2)

class Attack:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.dir = player.face_dir
        player.skill(1)

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.x += player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * (ACTION_PER_TIME * 5)* game_framework.frame_time)

        if int(player.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            player.state_machine.add_event(('TIME_OUT', 0))
            pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                  0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                  0, 'h', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

class Player:
    def __init__(self):
        self.x, self.y = 200, 90
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        #self.action = 0
        self.image_Idle = load_image('resource/player/character_Idle.png')
        self.image_Run = load_image('resource/player/character_Run.png')
        self.image_Attack = load_image('resource/player/character_SquatAttack.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {   #상태 변환 테이블 : 더블 Dict로 구현
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                       ctrl_down : Attack, ctrl_up : Attack}, #ctrl_down : Idle
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                      ctrl_down : Attack, ctrl_up : Attack},
                Attack: {time_out: Idle}
            }
        )
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.hp = 100

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(10, 580, f'(HP: {self.hp})', (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - PLAYER_SIZE*0.7, self.y - PLAYER_SIZE, self.x + PLAYER_SIZE*0.7, self.y + PLAYER_SIZE*0.5

    def handle_collision(self, group, other):
        # fill here
        if group == 'player:monster':
            self.hp -= 10
        pass

    def skill(self, num):
        skill_1 = Skill_lightening(self.x, self.y)
        # game_world.add_collision_pair('zombie:ball', None, ball)
        game_world.add_object(skill_1, 1)