import pico2d
import play_mode

pico2d.open_canvas()
play_mode.init()
# game loop
global delayCount
delayCount = 0

while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    pico2d.delay(0.01)
    if delayCount < 10:
        delayCount += 1
    else :
        delayCount = 0

play_mode.finish()
pico2d.close_canvas()