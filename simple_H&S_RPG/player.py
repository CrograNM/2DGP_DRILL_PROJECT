from state_machine import *
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
FRAMES_PER_ACTION_DEATH = 8

PLAYER_SIZE = 42
sx, sy = 0 , 0

# 전역 변수 추가
pause_time = 0
paused_duration = 0

on_ground = 103
gravity_set = 15

IDLE_STATE = 0
RUN_STATE = 1
JUMP_STATE = 2
ATTACK_STATE = 3
HURT_STATE = 4
DEATH_STATE = 5

class Idle:
    @staticmethod
    def enter(player, e):
        player.current_state = IDLE_STATE
        player.dir = 0
        if start_event(e):
            player.face_dir = -1
        elif right_down(e) or left_up(e):
            player.face_dir = -1
        elif left_down(e) or right_up(e):
            player.face_dir = 1
        player.frame = 0

    @staticmethod
    def exit(player, e):
        player.frame = 0
        pass

    @staticmethod
    def do(player):
        if player.y == on_ground:
            player.gravity = 0
        elif player.y < on_ground:
            player.gravity = 0
            player.y = on_ground
        player.frame = (player.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_IDLE

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
        player.current_state = RUN_STATE
        player.dir = player.face_dir
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1

    @staticmethod
    def exit(player, e):
        player.frame = 0
        #player.stop_sound()
        pass

    @staticmethod
    def do(player):
        if player.y == on_ground:
            player.gravity = 0
        elif player.y < on_ground:
            player.gravity = 0
            player.y = on_ground
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

class Jump_run:
    @staticmethod
    def enter(player, e):
        if player.current_state != JUMP_STATE:
            player.jump_sound.play()
        player.current_state = JUMP_STATE
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
        if player.current_state != JUMP_STATE:
            player.jump_sound.play()
        player.current_state = JUMP_STATE
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
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1
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
        player.attacking = True
        player.current_state = ATTACK_STATE
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
        player.attacking = False
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1
        pass

    @staticmethod
    def do(player):

        if server.weapon_ABC == 'A':
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_ACTION_PER_TIME * game_framework.frame_time)
            player.x += player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        else :
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_B_ACTION_PER_TIME * game_framework.frame_time)

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
        player.attacking = True
        player.current_state = ATTACK_STATE
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
        player.attacking = False
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1
        pass

    @staticmethod
    def do(player):
        if server.weapon_ABC == 'A':
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_ACTION_PER_TIME * game_framework.frame_time)
            player.x += player.dir * ATTACK_SPEED_PPS * game_framework.frame_time
        else:
            player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * SWORD_ATTACK_B_ACTION_PER_TIME * game_framework.frame_time)

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

class Attack_Bow_I:
    @staticmethod
    def enter(player, e):
        player.attacking = True
        player.current_state = ATTACK_STATE
        player.dir = player.face_dir

    @staticmethod
    def exit(player, e):
        player.attacking = False
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1
        pass

    @staticmethod
    def do(player):

        player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * BOW_ATTACK_ACTION_PER_TIME * game_framework.frame_time)

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

class Attack_Bow_R:
    @staticmethod
    def enter(player, e):
        player.attacking = True
        player.current_state = ATTACK_STATE
        player.dir = player.face_dir

    @staticmethod
    def exit(player, e):
        player.attacking = False
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_ATTACK * BOW_ATTACK_ACTION_PER_TIME * game_framework.frame_time)
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
        player.current_state = HURT_STATE
        player.dir = player.face_dir

    @staticmethod
    def exit(player, e):
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1
        pass

    @staticmethod
    def do(player):
        player.gravity -= 1
        if player.y == on_ground:
            player.gravity = 0
        elif player.y < on_ground:
            player.gravity = 0
            player.y = on_ground

        player.frame = (player.frame + FRAMES_PER_ACTION_HURT * ACTION_PER_TIME * game_framework.frame_time)
        player.x -= player.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        if int(player.frame) == FRAMES_PER_ACTION_HURT - 1:
            #player.hp -= 10
            if player.hp <= 0:
                player.state_machine.add_event(('DEATH_START', 0))
            else:
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

class Hurt_run:
    @staticmethod
    def enter(player, e):
        player.current_state = HURT_STATE
        player.dir = player.face_dir

    @staticmethod
    def exit(player, e):
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1
        pass

    @staticmethod
    def do(player):
        player.gravity -= 1
        if player.y == on_ground:
            player.gravity = 0
        elif player.y < on_ground:
            player.gravity = 0
            player.y = on_ground

        player.frame = (player.frame + FRAMES_PER_ACTION_HURT * ACTION_PER_TIME * game_framework.frame_time)
        player.x -= player.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        if int(player.frame) == FRAMES_PER_ACTION_HURT - 1:
            #player.hp -= 10
            if player.hp <= 0:
                player.state_machine.add_event(('DEATH_START', 0))
            else:
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

class Death:
    @staticmethod
    def enter(player, e):
        player.current_state = DEATH_STATE
        player.frame = 0
        player.dir = player.face_dir

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if player.y <= on_ground:
            player.gravity = 0
            player.y = on_ground

        player.frame = (player.frame + FRAMES_PER_ACTION_DEATH * ACTION_PER_TIME * game_framework.frame_time)
        if int(player.frame) >= FRAMES_PER_ACTION_DEATH - 1:
            player.frame = FRAMES_PER_ACTION_DEATH - 1
            server.player_dead = True
            #player.state_machine.add_event(('TIME_OUT', 0))
            pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Death.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                    0, '', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
        else:
            player.image_Death.clip_composite_draw(int(player.frame) * PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE,
                                                    0, 'h', player.x, player.y, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

class Player:
    def __init__(self):
        self.weapon = server.weapon
        self.x, self.y = 200, 103
        self.gravity = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.current_state = IDLE_STATE

        self.hp_max = 100
        self.hp = 10000
        self.dmg = 50
        self.invulnerable = False  # 무적 상태 여부
        self.invulnerable_start_time = 0  # 무적 상태 시작 시간
        self.attacking = False

        # 리소스
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.ui_hp = load_image('resource/ui/HP.png')
        self.hit_sound = load_wav('resource/sounds/hit_arrow.wav')
        self.hit_sound.set_volume(32)
        self.jump_sound = load_wav('resource/sounds/action_jump.wav')
        self.jump_sound.set_volume(128)

        self.image_Idle = load_image('resource/player/sword_Idle.png')
        self.image_Run = load_image('resource/player/sword_Run.png')
        self.image_Attack = load_image('resource/player/sword_Attack.png')
        self.image_SquatAttack = load_image('resource/player/sword_SquatAttack.png')
        self.image_Jump = load_image('resource/player/sword_Jump.png')
        self.image_Hurt = load_image('resource/player/sword_Hurt.png')
        self.image_Death = load_image('resource/player/sword_Death.png')
        if server.weapon == 'Bow':
            self.image_Idle = load_image('resource/player/bow_Idle.png')
            self.image_Run = load_image('resource/player/bow_Run.png')
            self.image_Attack = load_image('resource/player/bow_Attack.png')
            self.image_Jump = load_image('resource/player/bow_Jump.png')
            self.image_Hurt = load_image('resource/player/bow_Hurt.png')
            self.image_Death = load_image('resource/player/bow_Death.png')

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
                           ctrl_down : Attack_Sword_I,
                           hurt_start:Hurt},
                    Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                          alt_down: Jump_run,
                          ctrl_down : Attack_Sword_R,
                          hurt_start:Hurt_run},
                    Jump: {right_down: Jump_run, left_down: Jump_run, right_up: Jump_run, left_up: Jump_run,
                           jump_end: Idle,
                           hurt_start:Hurt},
                    Jump_run: {right_up: Jump, left_up: Jump, right_down: Jump, left_down: Jump,
                               jump_end: Run,
                               hurt_start:Hurt_run},
                    Attack_Sword_I: {time_out: Idle,
                                        right_down : Attack_Sword_R, left_down : Attack_Sword_R,
                                        right_up: Attack_Sword_R, left_up: Attack_Sword_R },
                    Attack_Sword_R: {time_out: Run,
                                        right_up : Attack_Sword_I, left_up : Attack_Sword_I,
                                        right_down: Attack_Sword_I, left_down: Attack_Sword_I},
                    Hurt: {right_down: Hurt_run, left_down: Hurt_run, right_up: Hurt_run, left_up: Hurt_run,
                            time_out: Idle, death_start : Death},
                    Hurt_run: {right_up: Hurt, left_up: Hurt, right_down: Hurt, left_down: Hurt,
                            time_out: Run, death_start: Death},
                    Death: {}
                }
            )
        elif server.weapon == 'Bow':
            self.state_machine.set_transitions(
                {  # 상태 변환 테이블 : 더블 Dict로 구현
                    Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                           alt_down: Jump,
                           ctrl_down: Attack_Bow_I, ctrl_up: Attack_Bow_I,
                           hurt_start:Hurt},  # ctrl_down : Idle
                    Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                          alt_down: Jump_run,
                          ctrl_down: Attack_Bow_R, ctrl_up: Attack_Bow_R,
                          hurt_start:Hurt_run},
                    Jump: {right_down: Jump_run, left_down: Jump_run, right_up: Jump_run, left_up: Jump_run,
                           jump_end: Idle,
                           hurt_start: Hurt},
                    Jump_run: {right_up: Jump, left_up: Jump, right_down: Jump, left_down: Jump,
                               jump_end: Run,
                               hurt_start: Hurt_run},
                    Attack_Bow_I: {time_out: Idle,
                                     right_down: Attack_Bow_R, left_down: Attack_Bow_R,
                                     right_up: Attack_Bow_R, left_up: Attack_Bow_R},
                    Attack_Bow_R: {time_out: Run,
                                     right_up: Attack_Bow_I, left_up: Attack_Bow_I,
                                     right_down: Attack_Bow_I, left_down: Attack_Bow_I},
                    Hurt: {right_down: Hurt_run, left_down: Hurt_run, right_up: Hurt_run, left_up: Hurt_run,
                           time_out: Idle, death_start: Death},
                    Hurt_run: {right_up: Hurt, left_up: Hurt, right_down: Hurt, left_down: Hurt,
                               time_out: Run, death_start: Death},
                    Death: {}
                }
            )
        self.hit_by_skills = {}  # 스킬 객체를 키로, 충돌 상태를 값으로 저장

    def take_damage(self, damage):
        #플레이어가 피해를 입었을 때 호출
        if not self.invulnerable:  # 무적 상태가 아니면 피해 적용
            self.hit_sound.play()
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

    def handle_event(self, event):
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

    def get_bb(self):
        if self.current_state != 'Attack':
            return self.x - PLAYER_SIZE*0.7, self.y - PLAYER_SIZE, self.x + PLAYER_SIZE*0.7, self.y + PLAYER_SIZE*0.5
        else:
            return 0, 0, 0, 0

    def handle_collision(self, group, other):
        if self.invulnerable:
            return False  # 무적 상태라면 충돌 처리하지 않음
        if self.attacking:
            return False
        if group == 'player:monster':
            if other not in self.hit_by_skills or not self.hit_by_skills[other]:
                self.hit_by_skills[other] = True
                self.take_damage(10)
                self.frame = 0
                self.state_machine.add_event(('HURT_START', 0))
        elif group == 'player:monster_attack':
            if other not in self.hit_by_skills or not self.hit_by_skills[other]:
                self.hit_by_skills[other] = True
                self.take_damage(10)
                self.frame = 0
                self.state_machine.add_event(('HURT_START', 0))
        elif group == 'player:boss':
            self.take_damage(10)
            self.frame = 0
            self.state_machine.add_event(('HURT_START', 0))
        elif group == 'player:boss_skill':
            if other not in self.hit_by_skills or not self.hit_by_skills[other]:
                self.hit_by_skills[other] = True
                self.take_damage(20)
                self.frame = 0
                self.state_machine.add_event(('HURT_START', 0))
        elif group == 'player:boss_skill_!!!':
            if other not in self.hit_by_skills or not self.hit_by_skills[other]:
                self.hit_by_skills[other] = True
                self.take_damage(50)
                self.frame = 0
                self.state_machine.add_event(('HURT_START', 0))

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