from pico2d import *
import game_world
import game_framework

Time_PER_ACTION =1
ACTION_PER_TIME =1.0/Time_PER_ACTION

class Skill_lightening:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        self.frame = 0
        self.damage = 50
        if Skill_lightening.image == None:
            Skill_lightening.image = load_image('resource/skill/skill_lightening.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * 64, 160, 64, 160, 0, 'h',
                                       self.x, self.y, 500, 500)
        #draw_rectangle(*self.get_bb())

    def update(self, x, y):
        self.frame = (self.frame + 10 * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame > 10:
            game_world.remove_object(self)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass