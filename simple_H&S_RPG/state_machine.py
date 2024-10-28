#이벤트 체크 함수를 정의
#상태 이벤트 e = (종류, 실제값) 튜플로 정의
from sdl2 import SDL_KEYDOWN, SDLK_SPACE


def space_down(e): # e가 spaceDown인지 판단? True/False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e): # e가 timeOut인지 판단?
    return e[0] == 'TIME_OUT' # 상태가 변하지 않으면 이 '종류 문자열'을 자세히 검사하기...


class StateMachine:
    def __init__(self, obj):
        self.obj = obj # 어떤 객체를 위한 상태머신인지 알려줌. obj = boy.self
        self.event_q = [] # 상태 이벤트를 보관할 큐 리스트
        pass

    def start(self, state):
        self.cur_state = state # 시작 상태를 받아서, 현재 상태로 만듬
        pass

    def update(self):
        self.cur_state.do(self.obj) # 최초엔 idle, idle의 do를 진행한다.
        #do가 끝난 후에 혹시 event가 있는지 확인
        if self.event_q: # list는 멤버가 존재하면 True다. (파이썬 문법)
            e = self.event_q.pop(0) # list의 맨 앞에서 꺼낸다. (큐 자료구조)
            # 이 시점에 우리에게 주어진 정보 : event, cur_state -> 이벤트를 적용해 다음 '상태'로 변환
            # 현재 상태와 현재 발생한 이벤트에 따라서 다음 상태를 결정하는 방법 : '상태 변환 테이블'을 이용
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e): # 내가 원하는 이벤트가 발생했다
                    self.cur_state.exit(self.obj)
                    self.cur_state = next_state
                    self.cur_state.enter(self.obj)
        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e): # e : 튜플로 받아온 event 파라미터.
        self.event_q.append(e)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

