from pico2d import *
from state_machine import *
import game_framework
import game_world
from skill import Skill_lightening, Skill_bow
import server

WIDTH = 1280
HEIGHT = 720

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ATTACK_SPEED_PPS = RUN_SPEED_PPS * 10

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
SWORD_ATTACK_ACTION_PER_TIME = ACTION_PER_TIME * 5
BOW_ATTACK_ACTION_PER_TIME = ACTION_PER_TIME * 2
FRAMES_PER_ACTION_IDLE = 4
FRAMES_PER_ACTION_RUN = 6
FRAMES_PER_ACTION_ATTACK = 6
FRAMES_PER_ACTION_JUMP = 8

PLAYER_SIZE = 42
sx, sy = 0 , 0

# 전역 변수 추가
pause_time = 0
paused_duration = 0

on_ground = 103
gravity_set = 15

class Idle:
    @staticmethod
    def enter(player, e):
        player.current_state = 'Idle'
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
        if player.y == on_ground:
            player.gravity = 0
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
        player.current_state = 'Run'
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
        if player.y == on_ground:
            player.gravity = 0

        player.frame = (player.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_RUN
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        # dx = player.dir * RUN_SPEED_PPS * game_framework.frame_time  # 이동 거리 계산
        # player.move(dx)  # 수정된 move 메서드 호출

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Run.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                 0, '', player.x + 5, player.y, PLAYER_SIZE*2, PLAYER_SIZE*2)
        else:
            player.image_Run.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                 0, 'h', player.x - 5, player.y, PLAYER_SIZE*2, PLAYER_SIZE*2)

class Jump_run:
    @staticmethod
    def enter(player, e):
        if right_down(e):
            player.face_dir = 1
            player.dir = 1
        elif left_down(e):
            player.face_dir = -1
            player.dir = -1
        if alt_down(e):
            player.gravity = gravity_set
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_JUMP
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.gravity -= 1
        if player.y <= on_ground:
            player.gravity = 0
            player.y = on_ground
            player.state_machine.add_event(('JUMP_END', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Jump.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                 0, '', player.x + 5, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            player.image_Jump.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                 0, 'h', player.x - 5, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

class Jump:
    @staticmethod
    def enter(player, e):
        if right_down(e):
            player.face_dir = 1
        elif left_down(e):
            player.face_dir = -1
        if alt_down(e):
            player.gravity = gravity_set
        player.dir = 0
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_JUMP
        player.gravity -= 1
        if player.y <= on_ground:
            player.gravity = 0
            player.y = on_ground
            player.state_machine.add_event(('JUMP_END', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Jump.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                  0, '', player.x + 5, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            player.image_Jump.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                  0, 'h', player.x - 5, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

class Attack_Sword:
    @staticmethod
    def enter(player, e):
        player.current_state = 'Attack'
        player.frame = 0
        player.dir = player.face_dir
        player.skill_1(1)

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):

        player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_ACTION_PER_TIME * game_framework.frame_time)
        player.x += player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        # dx = player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        # player.move(dx)

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

Attack_Sword_I = Attack_Sword
Attack_Sword_R = Attack_Sword

class Attack_Bow:
    @staticmethod
    def enter(player, e):
        player.current_state = 'Attack'
        player.frame = 0
        player.dir = player.face_dir
        # player.skill_1(1)

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):

        player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * BOW_ATTACK_ACTION_PER_TIME * game_framework.frame_time)
        # player.x += player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        # dx = player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        # player.move(dx)

        if int(player.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            player.state_machine.add_event(('TIME_OUT', 0))
            player.skill_2(1)
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
        self.weapon = server.weapon
        self.x, self.y = 200, 103
        self.gravity = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.current_state = None

        self.hp_max = 100
        self.hp = 100

        # UI 리소스
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.ui_hp = load_image('resource/ui/HP.png')

        self.image_Idle = load_image('resource/player/sword_Idle.png')
        self.image_Run = load_image('resource/player/sword_Run.png')
        self.image_Attack = load_image('resource/player/sword_SquatAttack.png')
        self.image_Jump = load_image('resource/player/sword_Jump.png')
        if server.weapon == 'Bow':
            self.image_Idle = load_image('resource/player/bow_Idle.png')
            self.image_Run = load_image('resource/player/bow_Run.png')
            self.image_Attack = load_image('resource/player/bow_Attack.png')
            self.image_Jump = load_image('resource/player/bow_Jump.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {  # 상태 변환 테이블 : 더블 Dict로 구현
                Idle: { }
            }
        )
        if server.weapon == 'Sword':
            self.state_machine.set_transitions(
                {   #상태 변환 테이블 : 더블 Dict로 구현
                    Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                           alt_down : Jump,
                           ctrl_down : Attack_Sword_I}, #ctrl_down : Idle
                    Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                          alt_down: Jump_run,
                          ctrl_down : Attack_Sword_R},
                    Jump: {right_down: Jump_run, left_down: Jump_run, jump_end: Idle},
                    Jump_run: {right_up: Jump, left_up: Jump, jump_end: Run},
                    Attack_Sword_I: {time_out: Idle,
                                        right_up : Attack_Sword_R, left_up : Attack_Sword_R,
                                        right_down : Attack_Sword_R, left_down : Attack_Sword_R},
                    Attack_Sword_R: {time_out: Run,
                                       right_up : Attack_Sword_I, left_up : Attack_Sword_I,
                                       right_down : Attack_Sword_I, left_down : Attack_Sword_I}
                }
            )
        elif server.weapon == 'Bow':
            self.state_machine.set_transitions(
                {  # 상태 변환 테이블 : 더블 Dict로 구현
                    Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                           alt_down: Jump,
                           ctrl_down: Attack_Bow, ctrl_up: Attack_Bow},  # ctrl_down : Idle
                    Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                          alt_down: Jump_run,
                          ctrl_down: Attack_Bow, ctrl_up: Attack_Bow},
                    Jump: {right_down: Jump_run, left_down: Jump_run, jump_end: Idle},
                    Jump_run: {right_up: Jump, left_up: Jump, jump_end: Run},
                    Attack_Bow: {time_out: Idle}
                }
            )

    def update(self):
        self.y += self.gravity

        self.state_machine.update()
        self.time = get_time()
        # 캐릭터 이동 거리 제한
        if self.x < 10:
            self.x = 10
        elif self.x > 1280 - 10:
            self.x = 1270

        # 카메라 비활성화
        # self.x = clamp(10.0, self.x, server.background.w - 10.0)
        # self.y = clamp(20.0, self.y, server.background.h - 10.0)

    def handle_event(self, event):
        #if self.current_state != 'Attack':
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

        #UI
        #HP
        self.ui_hp.draw(100, HEIGHT - 50, 200, 100)
        self.font.draw(100 + 10, HEIGHT - 17, f'HP: {self.hp}', (255, 0, 0))
        #TIME
        self.font.draw(WIDTH - 100, HEIGHT - 17, f'time: {server.time}', (0, 0, 255))
        #KILL
        self.font.draw(WIDTH - 100, HEIGHT - 35, f'kill: {server.kill_count}', (255, 0, 0))

        # 카메라 비활성화
        # global sx          
        # global sy
        # sx = self.x - server.background.window_left
        # sy = self.y - server.background.window_bottom
        # draw_rectangle(sx - 10, sy - 10, sx + 10, sy + 10)

    def get_bb(self):
        if self.current_state != 'Attack':
            return self.x - PLAYER_SIZE*0.7, self.y - PLAYER_SIZE, self.x + PLAYER_SIZE*0.7, self.y + PLAYER_SIZE*0.5
        else:
            return 0, 0, 0, 0

    def handle_collision(self, group, other):
        # fill here
        if group == 'player:monster_attack':
            self.hp -= 10
        pass

    def skill_1(self, num):
        skill_1 = Skill_lightening(self.x + self.dir*180, self.y - 10, self.dir)
        # game_world.add_collision_pair('zombie:ball', None, ball)
        game_world.add_collision_pair('monster:skill_1', None, skill_1)
        game_world.add_collision_pair('boss:skill_1', None, skill_1)
        game_world.add_object(skill_1, 1)

    def skill_2(self, num):
        skill_2 = Skill_bow(self.x + self.dir*20, self.y - 20, self.dir)
        # game_world.add_collision_pair('zombie:ball', None, ball)
        game_world.add_collision_pair('monster:skill_1', None, skill_2) # 추후 충돌체크 그룹 변경 : 무기별 차이 두기
        game_world.add_collision_pair('boss:skill_1', None, skill_2)
        game_world.add_object(skill_2, 1)