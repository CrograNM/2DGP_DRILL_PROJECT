from pico2d import load_image, get_canvas_width, get_canvas_height
from pygame.math import clamp
import server
import random

class InfiniteBackground:

    def __init__(self):
        self.image = load_image('resource/background.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.offset_x = 0
        self.offset_y = 0

        # 배경 비율 조정 계산
        self.scale_x = self.cw / self.w
        self.scale_y = self.ch / self.h
        self.scale = min(self.scale_x, self.scale_y)  # 비율 유지
        self.scaled_width = int(self.w * self.scale)
        self.scaled_height = int(self.h * self.scale)

    def draw(self):
        # 모든 사분면 그리기
        self.image.clip_draw_to_origin(
            int((self.q3l - self.offset_x) % self.w),
            int((self.q3b - self.offset_y) % self.h),
            int(self.q3w), int(self.q3h),
            0, 0,
            int(self.q3w * self.scale), int(self.q3h * self.scale)
        )

        self.image.clip_draw_to_origin(
            int((self.q2l - self.offset_x) % self.w),
            int((self.q2b - self.offset_y) % self.h),
            int(self.q2w), int(self.q2h),
            0, int(self.q3h * self.scale),
            int(self.q2w * self.scale), int(self.q2h * self.scale)
        )

        self.image.clip_draw_to_origin(
            int((self.q4l - self.offset_x) % self.w),
            int((self.q4b - self.offset_y) % self.h),
            int(self.q4w), int(self.q4h),
            int(self.q3w * self.scale), 0,
            int(self.q4w * self.scale), int(self.q4h * self.scale)
        )

        self.image.clip_draw_to_origin(
            int((self.q1l - self.offset_x) % self.w),
            int((self.q1b - self.offset_y) % self.h),
            int(self.q1w), int(self.q1h),
            int(self.q3w * self.scale), int(self.q3h * self.scale),
            int(self.q1w * self.scale), int(self.q1h * self.scale)
        )

    def update(self):
        # 사분면 계산 (비율 유지)
        scaled_cw = int(self.cw / self.scale)
        scaled_ch = int(self.ch / self.scale)

        # quadrant 3
        self.q3l = (int(server.player.x) - scaled_cw // 2) % self.w
        self.q3b = (int(server.player.y) - scaled_ch // 2) % self.h
        self.q3w = clamp(0, self.w - self.q3l, self.w)
        self.q3h = clamp(0, self.h - self.q3b, self.h)

        # quadrant 2
        self.q2l = self.q3l
        self.q2b = 0
        self.q2w = self.q3w
        self.q2h = scaled_ch - self.q3h

        # quadrant 4
        self.q4l = 0
        self.q4b = self.q3b
        self.q4w = scaled_cw - self.q3w
        self.q4h = self.q3h

        # quadrant 1
        self.q1l = 0
        self.q1b = 0
        self.q1w = self.q4w
        self.q1h = self.q2h

    def move_background(self, dx):
        self.offset_x += dx  # 배경의 X축 이동 처리

    def handle_event(self, event):
        pass
