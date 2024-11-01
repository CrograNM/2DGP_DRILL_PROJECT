from pico2d import load_image, get_time

from state_machine import time_out, space_down, right_down, right_up, left_down, left_up, start_event
from state_machine import StateMachine

class Idle:
    @staticmethod
    # ^^^ : 데코레이트(장식한다, 꾸민다) : 함수의 기능을 조금 바꾼다
    # 클래스 내 함수에 self 파라미터를 안넣는다?
    # ^^^ 스태틱메소드 함수로 간주한다. -> 멤버함수x, 클래스 안에 들어있는 객체와 관계없는 그냥 함수로 간주
    # 왜 클래스 안에서 함수를 선언하는가? 이 Idle클래스는 객체를 찍어내기위한 클래스가 아니라, '그룹화'를 위한 클래스
    # 따라서, 이 클래스의 이름으로 함수들을 묶어주는것
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
        # 현재 시각을 저장(idle이 시작된 시점)
        player.start_time = get_time()
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player): # boy는 상태에 해당하는 객체를 의미하는 파라미터일 뿐이다. boy자체가 아님
        if player.delayCount < 5:
            player.delayCount += 1
        else:
            player.delayCount = 0
            player.frame = (player.frame + 1) % 4
        if get_time() - player.start_time > 3:
            player.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(player):
        # player.image.clip_draw(player.frame * 42, player.action * 42, 42, 42, player.x, player.y, 84, 84)
        if player.face_dir == 1:
            player.image_Idle.clip_composite_draw(player.frame * 42, 0, 42, 42, 0, '', player.x, player.y, 84, 84)
        else:
            player.image_Idle.clip_composite_draw(player.frame * 42, 0, 42, 42, 0, 'h', player.x, player.y, 84, 84)
    # entry, exit, do, draw -> 4가지 정보로 상태state를 표현
    # Idle이란 클래스는 그저 4개의 함수로 이루어져 있는 '상태'이다.

class Sleep:
    @staticmethod
    def enter(player, e):
        if start_event(e):
            player.face_dir = -1
            player.action = 0
        player.frame = 0
        player.delayCount = 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if player.delayCount < 5:
            player.delayCount += 1
        else:
            player.delayCount = 0
            player.frame = (player.frame + 1) % 4
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Idle.clip_composite_draw(player.frame * 42, 0, 42, 42,
                                                  3.141592 / 2,  # 파이/2 = 90도 회전
                                                  '',  # 상하좌우 반전하지 않는다 : ''.   반전 시 : 'v', 'h'
                                                  player.x - 60, player.y - 20, 84, 84)
        else:
            player.image_Idle.clip_composite_draw(player.frame * 42, 0, 42, 42,
                                                  -3.141592 / 2, 'h', player.x + 60, player.y - 20, 84, 84)

class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir, player.action = 1, 0
            player.face_dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir, player.action = -1, 0
            player.face_dir = -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        #player.frame = (player.frame + 1) % 6
        if player.delayCount < 5:
            player.delayCount += 1
        else:
            player.delayCount = 0
            player.frame = (player.frame + 1) % 6
        player.x += player.dir * 3

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_Run.clip_composite_draw(player.frame * 42, 0, 42, 42, 0, '', player.x, player.y, 84, 84)
        else:
            player.image_Run.clip_composite_draw(player.frame * 42, 0, 42, 42, 0, 'h', player.x, player.y, 84, 84)

class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.action = 0
        self.image_Idle = load_image('character_Idle.png')
        self.image_Run = load_image('character_Run.png')
        self.state_machine = StateMachine(self) # 소년 객체의 state machine 생성, self 인자로 생성자의 파라미터들도 스테이트 머신에 넘겨준다.
        self.state_machine.start(Sleep) # 초기 상태가 idle, 스테이트 머신이 최초에 idle을 처리하게된다.
        self.state_machine.set_transitions(
            {   #상태 변환 테이블 : 더블 Dict로 구현
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )
    def update(self):
        self.state_machine.update() # 스테이트 머신이 업데이트를 담당하게 된다.
        #self.frame = (self.frame + 1) % 8 # 이제 이건 필요가 없음

    def handle_event(self, event):
        #소년이 날리는 입력 이벤트들을 스테이트 머신이 리스트에 차곡차곡 저장할 수 있게 해야한다.
        # event : 입력 이벤트 - key, mouse 등
        # 우리가 state machine에 전달해야하는 것은 튜플 ('종류',실제값)
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
