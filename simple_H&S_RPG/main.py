import pico2d
import game_framework
import logo_mode as start_mode

pico2d.open_canvas()
game_framework.run(start_mode)
pico2d.close_canvas()