from math import radians

from pico2d import *
import game_world
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_ATTACK = 10

skill_lightening_width = 320
skill_lightening_height = 64
class Skill_lightening:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Skill_lightening.image == None:
            Skill_lightening.image = load_image('resource/skill/skill_lightening.png')
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, radians(90), 'h',
                                           self.x, self.y, skill_lightening_height, skill_lightening_width)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, radians(90), ' ',
                                           self.x, self.y, skill_lightening_height, skill_lightening_width)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == FRAMES_PER_ACTION_ATTACK - 1:
            game_world.remove_object(self)

    def get_bb(self):
        return (self.x - skill_lightening_width / 2, self.y - skill_lightening_height / 2,
                self.x + skill_lightening_width / 2, self.y + skill_lightening_height / 2)
        pass

    def handle_collision(self, group, other):
        pass