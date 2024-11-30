from math import radians

from pico2d import *
import game_world
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

LIGHTENING_FRAMES_PER_ACTION = 10
ARROW_FRAMES_PER_ACTION = 6

skill_lightening_width = 320
skill_lightening_height = 64

skill_bow_width = 48
skill_bow_height = 48
arrow_velocity = 10

# sx, sy = 0 , 0
class Skill_lightening:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Skill_lightening.image == None:
            Skill_lightening.image = load_image('resource/skill/skill_lightening_2.png')
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
        self.frame = (self.frame + LIGHTENING_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == LIGHTENING_FRAMES_PER_ACTION - 1:
            game_world.remove_object(self)

    def get_bb(self):
        if int(self.frame) == 2:
            return (self.x - skill_lightening_width / 2, self.y - skill_lightening_height / 2,
                    self.x + skill_lightening_width / 2, self.y + skill_lightening_height / 2)
        else :
            return 0,0,0,0


    def handle_collision(self, group, other):
        pass

class Skill_bow:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Skill_bow.image == None:
            Skill_bow.image = load_image('resource/skill/skill_bow_48_48.png') #frame = 6
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, 0, 'h',
                                           self.x, self.y, skill_bow_width, skill_bow_height)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, 0, ' ',
                                           self.x, self.y, skill_bow_width, skill_bow_height)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.dir * arrow_velocity
        self.frame = (self.frame + ARROW_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == ARROW_FRAMES_PER_ACTION - 1:
            game_world.remove_object(self)

    def get_bb(self):
        return (self.x - skill_bow_width / 2, self.y - 10,
                    self.x + skill_bow_width / 2, self.y + 10)

    def handle_collision(self, group, other):
        pass

class Skill_bow_B:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Skill_bow_B.image == None:
            Skill_bow_B.image = load_image('resource/skill/skill_bow_48_48.png') #frame = 6
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, 0, 'h',
                                           self.x, self.y, skill_bow_width, skill_bow_height)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, 0, ' ',
                                           self.x, self.y, skill_bow_width, skill_bow_height)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.dir * arrow_velocity
        self.frame = (self.frame + ARROW_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == ARROW_FRAMES_PER_ACTION - 1:
            game_world.remove_object(self)

    def get_bb(self):
        return (self.x - skill_bow_width / 2, self.y - 10,
                    self.x + skill_bow_width / 2, self.y + 10)

    def handle_collision(self, group, other):
        if group == 'monster:skill_bow_B':
            game_world.remove_object(self)
            skill = Skill_bow(self.x, self.y)
            # game_world.add_collision_pair('zombie:ball', None, ball)
            game_world.add_collision_pair('monster:skill_bow_B_explode', None, skill)  # 추후 충돌체크 그룹 변경 : 무기별 차이 두기
            game_world.add_collision_pair('boss:skill_bow_B_explode', None, skill)
            game_world.add_object(skill, 1)
        pass

skill_bow_explode_width = 48
skill_bow_explode_height = 48
BOW_EXPLODE_FRAMES_PER_ACTION = 8
class Skill_bow_B_explode:
    image = None
    # 48 * 48, 8frame
    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Skill_bow_B_explode.image == None:
            Skill_bow_B_explode.image = load_image('resource/skill/bow_B_explode.png')
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 48, 0 * 48, 48, 48, radians(90), 'h',
                                           self.x, self.y, skill_bow_explode_width, skill_bow_explode_height)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 48, 0 * 48, 48, 48, radians(90), ' ',
                                           self.x, self.y, skill_bow_explode_width, skill_bow_explode_height)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + BOW_EXPLODE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == BOW_EXPLODE_FRAMES_PER_ACTION - 1:
            game_world.remove_object(self)

    def get_bb(self):
        if int(self.frame) == 4:
            return (self.x - skill_bow_explode_width / 2, self.y - skill_bow_explode_height / 2,
                    self.x + skill_bow_explode_width / 2, self.y + skill_bow_explode_height / 2)
        else :
            return 0,0,0,0


    def handle_collision(self, group, other):
        pass