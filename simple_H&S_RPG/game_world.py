# world = [] # 단일 계층 구조

# world[0] : 백그라운드 객체들 - 맨 아래에 그릴 객체들
# world[1] : 포그라운드 객체들 - 위에 그려야 할 객체들
world = [ [], [] ]

def add_object(o, depth):
    world[depth].append(o)

def render():
    for layer in world:
        for o in layer:
            o.draw()

def update():
    for layer in world:
        for o in layer:
            o.update()


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return # 지우는 미션은 달성, 다른 요소는 체크할 필요가 없다

    print('에러: 존재하지 않은 객체를 지우려는 중')