from pico2d import *

from player import Player
from ground import Ground


# Game object class here
# class 드래그 후 우클릭 -> 리팩터링(이동)


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)


def reset_world():
    global running

    global ground
    global player
    #global team
    global world

    running = True
    world = []

    ground = Ground()
    world.append(ground)

    player = Player()
    world.append(player)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()
# game loop
global delayCount
delayCount = 0

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
    if delayCount < 10:
        delayCount += 1
    else :
        delayCount = 0
# finalization code
close_canvas()
