from pico2d import *
import game_world
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_ATTACK = 10

class Skill_lightening:
    image = None

    def __init__(self, x = 400, y = 300):
        self.frame = 0
        self.damage = 50
        if Skill_lightening.image == None:
            Skill_lightening.image = load_image('resource/skill/skill_lightening.png')
        self.x, self.y, = x, y

    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * 64, 160, 64, 160, 0, 'h',
                                       self.x, self.y, 500, 500)
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            game_world.remove_object(self)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass