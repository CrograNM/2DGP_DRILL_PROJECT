from pico2d import load_image, get_time

from player import Player
from state_machine import mob_close
from state_machine import StateMachine

class Run:
    @staticmethod
    def enter(mob, e):
        mob.face_dir = -1
        mob.dir = -1
        mob.frame = 0
        pass

    @staticmethod
    def exit(mob, e):
        pass

    @staticmethod
    def do(mob):
        if mob.delayCount < 5:
            mob.delayCount += 1
        else:
            mob.delayCount = 0
            mob.frame = (mob.frame + 1) % 12

            # player.x 위치를 추적하여 mob.dir 설정
            if mob.player.x > mob.x:
                mob.dir = 1  # player가 오른쪽에 있을 때
                mob.face_dir = 1
            elif mob.player.x < mob.x:
                mob.dir = -1  # player가 왼쪽에 있을 때
                mob.face_dir = -1

            mob.x += mob.dir * 3

            # 충분히 거리가 가까워지면 공격 모션을 진행
            if mob.player.x - 50 < mob.x < mob.player.x + 50:
                mob.state_machine.add_event(('MOB_CLOSE', 0))

        pass

    @staticmethod
    def draw(mob):
        if mob.face_dir == -1:
            mob.image_Run.clip_composite_draw(mob.frame * 72, 0, 72, 48, 0, '', mob.x - 20, mob.y, 144, 96)
        else:
            mob.image_Run.clip_composite_draw(mob.frame * 72, 0, 72, 48, 0, 'h', mob.x + 20, mob.y, 144, 96)
        pass

class Attack:
    @staticmethod
    def enter(mob, e):
        mob.frame = 0
        pass

    @staticmethod
    def exit(mob, e):
        pass

    @staticmethod
    def do(mob):
        if mob.delayCount < 5:
            mob.delayCount += 1
        else:
            mob.delayCount = 0
            mob.frame = (mob.frame + 1) % 8

    @staticmethod
    def draw(mob):
        if mob.face_dir == -1:
            mob.image_Attack.clip_composite_draw(mob.frame * 72, 0, 72, 48, 0, '', mob.x - 20, mob.y, 144, 96)
        else:
            mob.image_Attack.clip_composite_draw(mob.frame * 72, 0, 72, 48, 0, 'h', mob.x + 20, mob.y, 144, 96)
        pass

class Monster:
    def __init__(self, player):
        self.x, self.y = 600, 90
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 0
        self.image_Run = load_image('monster_Run.png')
        self.image_Attack = load_image('monster_Attack.png')

        self.player = player  # player 참조

        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            {
                Run: {mob_close : Attack},
                Attack: {}
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
