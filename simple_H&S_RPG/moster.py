from pico2d import load_image, get_time

from state_machine import time_out, space_down, right_down, right_up, left_down, left_up, start_event
from state_machine import StateMachine

class Run:
    @staticmethod
    def enter(mob, e):
        pass

    @staticmethod
    def exit(mob, e):
        pass

    @staticmethod
    def do(mob):
        pass

    @staticmethod
    def draw(mob):
        pass

class Monster:
    def __init__(self):
        self.x, self.y = 400, 90
        self.delayCount = 0
        self.frame = 0
        self.dir = 0
        self.action = 0
        self.image_Run = load_image('monster_Run.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            {   #상태 변환 테이블 : 더블 Dict로 구현
                Run: {}
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
