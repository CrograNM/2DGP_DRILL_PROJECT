from pico2d import *
import server

class Background:
    def __init__(self):
        self.image = load_image('resource/background_3840_2.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.window_left = clamp(0, int(server.player.x) - self.cw // 4 * 3, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.player.y) - self.ch // 2, self.h - self.ch - 1)

        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        pass

    def handle_event(self, event):
        pass
