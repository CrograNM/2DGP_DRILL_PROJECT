import pico2d
import game_framework
import play_mode as start_mode

pico2d.open_canvas(1280, 720)
game_framework.run(start_mode)
pico2d.close_canvas()