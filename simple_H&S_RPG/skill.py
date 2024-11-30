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

skill_sword_B_width = 300
skill_sword_B_height = 300
SWORD_B_FRAMES_PER_ACTION = 6
SWORD_ATTACK_B_ACTION_PER_TIME = ACTION_PER_TIME * 2
class Skill_sword_B:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Skill_sword_B.image == None:
            Skill_sword_B.image = load_image('resource/skill/sword_B_2.png')
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 100, 0 * 100, 100, 100, 0, '',
                                           self.x, self.y, skill_sword_B_width, skill_sword_B_height)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 100, 0 * 100, 100, 100, 0, 'h',
                                           self.x, self.y, skill_sword_B_width, skill_sword_B_height)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + SWORD_B_FRAMES_PER_ACTION * SWORD_ATTACK_B_ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == SWORD_B_FRAMES_PER_ACTION - 1:
            game_world.remove_object(self)

    def get_bb(self):
        if int(self.frame) == 2:
            return (self.x - skill_sword_B_width / 2, self.y - skill_sword_B_height / 2,
                    self.x + skill_sword_B_width / 2, self.y + skill_sword_B_height / 2)
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
        if group == 'monster:skill_1' or 'boss:skill_1':
            skill = Skill_bow_B_explode(self.x, self.y)
            # game_world.add_collision_pair('zombie:ball', None, ball)
            game_world.add_collision_pair('monster:skill_1', None, skill)  # 추후 충돌체크 그룹 변경 : 무기별 차이 두기
            game_world.add_collision_pair('boss:skill_1', None, skill)
            game_world.add_object(skill, 1)
            game_world.remove_object(self)
        pass

skill_bow_explode_width = 100
skill_bow_explode_height = 100
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
        if int(self.frame) != 10:
            return (self.x - skill_bow_explode_width / 2, self.y - skill_bow_explode_height / 2,
                    self.x + skill_bow_explode_width / 2, self.y + skill_bow_explode_height / 2)
        else :
            return 0,0,0,0


    def handle_collision(self, group, other):
        pass

skill_bow_C_width = 320
skill_bow_C_height = 72
BOW_C_FRAMES_PER_ACTION = 8
class Skill_bow_C:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Skill_bow_C.image == None:
            Skill_bow_C.image = load_image('resource/skill/bow_C.png')
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        # 72 * 72, 8
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 72, 0 * 72, 72, 72, 0, '',
                                           self.x, self.y, skill_bow_C_width, skill_bow_C_height)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 72, 0 * 72, 72, 72, 0, 'h',
                                           self.x, self.y, skill_bow_C_width, skill_bow_C_height)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + BOW_C_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == BOW_C_FRAMES_PER_ACTION - 1:
            game_world.remove_object(self)

    def get_bb(self):
        if int(self.frame) >= 2:
            return (self.x - skill_bow_C_width / 2, self.y - skill_bow_C_height / 2,
                    self.x + skill_bow_C_width / 2, self.y + skill_bow_C_height / 2)
        else :
            return 0,0,0,0


    def handle_collision(self, group, other):
        pass

#boss
class Boss_1:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        self.count = 0
        if Boss_1.image == None:
            Boss_1.image = load_image('resource/skill/boss_1.png')
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, 0, '',
                                           self.x, self.y, skill_lightening_height, skill_lightening_width)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 64, 0 * 160, 64, 160, 0, 'h',
                                           self.x, self.y, skill_lightening_height, skill_lightening_width)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + LIGHTENING_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == LIGHTENING_FRAMES_PER_ACTION - 1:
            self.frame = 0
            self.count += 1
            self.x += self.dir * 80
            if self.count >= 3:
                game_world.remove_object(self)

    def get_bb(self):
        if int(self.frame) == 2:
            return (self.x - skill_lightening_height / 2, self.y - skill_lightening_width / 2,
                    self.x + skill_lightening_height / 2, self.y + skill_lightening_width / 2)
        else :
            return 0,0,0,0


    def handle_collision(self, group, other):
        pass
class Boss_2:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.frame = 0
        self.damage = 50
        if Boss_2.image == None:
            Boss_2.image = load_image('resource/skill/sword_B_3.png')
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 100, 0 * 100, 100, 100, 0, '',
                                           self.x, self.y, skill_sword_B_width, skill_sword_B_height)
            draw_rectangle(*self.get_bb())
        else :
            self.image.clip_composite_draw(int(self.frame) * 100, 0 * 100, 100, 100, 0, 'h',
                                           self.x, self.y, skill_sword_B_width, skill_sword_B_height)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + SWORD_B_FRAMES_PER_ACTION * SWORD_ATTACK_B_ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == SWORD_B_FRAMES_PER_ACTION - 1:
            game_world.remove_object(self)

    def get_bb(self):
        if int(self.frame) == 2:
            return (self.x - skill_sword_B_width / 2, self.y - skill_sword_B_height / 2,
                    self.x + skill_sword_B_width / 2, self.y + skill_sword_B_height / 2)
        else :
            return 0,0,0,0


    def handle_collision(self, group, other):
        pass