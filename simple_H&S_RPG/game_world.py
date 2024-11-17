# world = [] # 단일 계층 구조

# world[0] : 백그라운드 객체들 - 맨 아래에 그릴 객체들
# world[1] : 포그라운드 객체들 - 위에 그려야 할 객체들
world = [ [], [], [], [], []]

def clear_all():
    clear()
    collision_pairs.clear()

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

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return # 지우는 미션은 달성, 다른 요소는 체크할 필요가 없다

    print('에러: 존재하지 않은 객체를 지우려는 중')

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)


def objects_at_depth(depth):
    # 특정 depth의 객체 리스트 반환
    if 0 <= depth < len(world):
        return world[depth]
    else:
        print(f"에러: 잘못된 depth 접근 - {depth}")
        return []