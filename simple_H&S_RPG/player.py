from pico2d import *
from state_machine import *
import game_framework
import game_world
from skill import *
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
SWORD_ATTACK_B_ACTION_PER_TIME = ACTION_PER_TIME * 2
BOW_ATTACK_ACTION_PER_TIME = ACTION_PER_TIME * 2
FRAMES_PER_ACTION_IDLE = 4
FRAMES_PER_ACTION_RUN = 6
FRAMES_PER_ACTION_ATTACK = 6
FRAMES_PER_ACTION_JUMP = 8
FRAMES_PER_ACTION_HURT = 4

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
        player.current_state = 'Jump'
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
        player.current_state = 'Jump'
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

class Attack_Sword_I:
    @staticmethod
    def enter(player, e):
        player.current_state = 'Attack'
        if server.skill_1_using == False:
            player.frame = 0
            player.dir = player.face_dir
            if server.weapon_ABC == 'A':
                player.skill_1(1)
            else:
                player.skill_Sword_B(1)
            server.skill_1_using = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):

        if server.weapon_ABC == 'A':
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_ACTION_PER_TIME * game_framework.frame_time)
            player.x += player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        else :
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_B_ACTION_PER_TIME * game_framework.frame_time)
        # dx = player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        # player.move(dx)

        if int(player.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            player.state_machine.add_event(('TIME_OUT', 0))
            server.skill_1_using = False
            pass

    @staticmethod
    def draw(player):
        if server.weapon_ABC == 'A':
            if player.face_dir == 1:
                player.image_SquatAttack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                      0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
            else:
                player.image_SquatAttack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                      0, 'h', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            if player.face_dir == 1:
                player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                      0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
            else:
                player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                      0, 'h', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

class Attack_Sword_R:
    @staticmethod
    def enter(player, e):
        player.current_state = 'Attack'
        if server.skill_1_using == False:
            player.frame = 0
            player.dir = player.face_dir
            if server.weapon_ABC == 'A':
                player.skill_1(1)
            else:
                player.skill_Sword_B(1)
            server.skill_1_using = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):

        if server.weapon_ABC == 'A':
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_ACTION_PER_TIME * game_framework.frame_time)
            player.x += player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        else:
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_B_ACTION_PER_TIME * game_framework.frame_time)
        # dx = player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        # player.move(dx)

        if int(player.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            player.state_machine.add_event(('TIME_OUT', 0))
            server.skill_1_using = False
            pass

    @staticmethod
    def draw(player):
        if server.weapon_ABC == 'A':
            if player.face_dir == 1:
                player.image_SquatAttack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                      0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
            else:
                player.image_SquatAttack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                      0, 'h', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            if player.face_dir == 1:
                player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                        0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
            else:
                player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                        0, 'h', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

class Attack_Bow:
    @staticmethod
    def enter(player, e):
        player.current_state = 'Attack'
        player.frame = 0
        player.dir = player.face_dir

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
            if server.weapon_ABC == 'A':
                player.skill_2(1)
            elif server.weapon_ABC == 'B':
                player.skill_Bow_B(1)
            elif server.weapon_ABC == 'C':
                player.skill_Bow_C(1)
            pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                    0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            player.image_Attack.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                    0, 'h', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

class Hurt:
    @staticmethod
    def enter(player, e):
        player.current_state = 'Hurt'
        player.frame = 0
        player.dir = player.face_dir

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_HURT * ACTION_PER_TIME * game_framework.frame_time)
        player.x -= player.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        # dx = player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        # player.move(dx)

        if int(player.frame) == FRAMES_PER_ACTION_HURT - 1:
            #player.hp -= 10
            player.state_machine.add_event(('TIME_OUT', 0))
            pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Hurt.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                    0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            player.image_Hurt.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
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
        self.dmg = 10
        self.invulnerable = False  # 무적 상태 여부
        self.invulnerable_start_time = 0  # 무적 상태 시작 시간

        # UI 리소스
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.ui_hp = load_image('resource/ui/HP.png')

        self.image_Idle = load_image('resource/player/sword_Idle.png')
        self.image_Run = load_image('resource/player/sword_Run.png')
        self.image_Attack = load_image('resource/player/sword_Attack.png')
        self.image_SquatAttack = load_image('resource/player/sword_SquatAttack.png')
        self.image_Jump = load_image('resource/player/sword_Jump.png')
        self.image_Hurt = load_image('resource/player/sword_Hurt.png')
        if server.weapon == 'Bow':
            self.image_Idle = load_image('resource/player/bow_Idle.png')
            self.image_Run = load_image('resource/player/bow_Run.png')
            self.image_Attack = load_image('resource/player/bow_Attack.png')
            self.image_Jump = load_image('resource/player/bow_Jump.png')
            self.image_Hurt = load_image('resource/player/bow_Hurt.png')

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
                           ctrl_down : Attack_Sword_I, hurt_start:Hurt}, #ctrl_down : Idle
                    Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                          alt_down: Jump_run,
                          ctrl_down : Attack_Sword_R, hurt_start:Hurt},
                    Jump: {right_down: Jump_run, left_down: Jump_run, jump_end: Idle, hurt_start:Hurt},
                    Jump_run: {right_up: Jump, left_up: Jump, jump_end: Run, hurt_start:Hurt},
                    Attack_Sword_I: {time_out: Idle,
                                        right_down : Attack_Sword_R, left_down : Attack_Sword_R},
                    Attack_Sword_R: {time_out: Run,
                                        right_up : Attack_Sword_I, left_up : Attack_Sword_I},
                    Hurt: {time_out: Idle}
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
                    Attack_Bow: {time_out: Idle},
                    Hurt: {time_out: Idle}
                }
            )

    def take_damage(self, damage):
        #플레이어가 피해를 입었을 때 호출
        if not self.invulnerable:  # 무적 상태가 아니면 피해 적용
            self.hp -= damage
            self.invulnerable = True  # 무적 상태로 전환
            self.invulnerable_start_time = get_time()

    def update(self):
        current_time = get_time()

        # 무적 상태 해제 체크
        if self.invulnerable and current_time - self.invulnerable_start_time > 2:
            self.invulnerable = False

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
        if self.invulnerable:
            return False  # 무적 상태라면 충돌 처리하지 않음

        if self.current_state == 'Idle' or 'Run' or 'Jump':
            if group == 'player:monster':
                self.take_damage(10)
                self.state_machine.add_event(('HURT_START', 0))
        pass

    def skill_1(self, num):
        skill_1 = Skill_lightening(self.x + self.dir*180, self.y - 10, self.dir)
        game_world.add_collision_pair('monster:skill_1', None, skill_1)
        game_world.add_collision_pair('boss:skill_1', None, skill_1)
        game_world.add_object(skill_1, 1)

    def skill_Sword_B(self, num):
        skill_Sword_B = Skill_sword_B(self.x + self.dir*150, self.y + 100, self.dir)
        game_world.add_collision_pair('monster:skill_1', None, skill_Sword_B)
        game_world.add_collision_pair('boss:skill_1', None, skill_Sword_B)
        game_world.add_object(skill_Sword_B, 1)

    def skill_2(self, num):
        skill_2 = Skill_bow(self.x + self.dir*20, self.y - 20, self.dir)
        game_world.add_collision_pair('monster:skill_1', None, skill_2) # 추후 충돌체크 그룹 변경 : 무기별 차이 두기
        game_world.add_collision_pair('boss:skill_1', None, skill_2)
        game_world.add_object(skill_2, 1)

    def skill_Bow_B(self, num):
        skill_Bow_B = Skill_bow_B(self.x + self.dir*20, self.y - 20, self.dir)
        game_world.add_collision_pair('monster:skill_1', None, skill_Bow_B) # 추후 충돌체크 그룹 변경 : 무기별 차이 두기
        game_world.add_collision_pair('boss:skill_1', None, skill_Bow_B)
        game_world.add_object(skill_Bow_B, 1)

    def skill_Bow_C(self, num):
        skill_Bow_C = Skill_bow_C(self.x + self.dir*180, self.y - 10, self.dir)
        game_world.add_collision_pair('monster:skill_1', None, skill_Bow_C) # 추후 충돌체크 그룹 변경 : 무기별 차이 두기
        game_world.add_collision_pair('boss:skill_1', None, skill_Bow_C)
        game_world.add_object(skill_Bow_C, 1)