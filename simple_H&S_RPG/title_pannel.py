from pico2d import load_image

WIDTH = 1280
HEIGHT = 720

class Background:
    def __init__(self):
        self.image = load_image('resource/title_mode/background.png')

    def draw(self):
        self.image.draw(WIDTH//2, HEIGHT//2)

    def update(self):
        pass

class Pannel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = load_image('resource/pause_mode/pause.png')

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

# Button 클래스 수정
class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_clicked(self, mx, my):
        return (self.x - self.width//2 <= mx <= self.x + self.width//2
                and self.y - self.height//2 <= my <= self.y + self.height//2)

class Start_Button(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = load_image('resource/title_mode/start_button_300_100.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class Sword_Button(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = load_image('resource/title_mode/sword_button_100_100_2.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class Sword_A(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = load_image('resource/title_mode/sword_A.png')

    def draw(self):
        self.image.draw(self.x, self.y)


class Bow_Button(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = load_image('resource/title_mode/bow_button_100_100_2.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class Bow_A(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = load_image('resource/title_mode/bow_A.png')

    def draw(self):
        self.image.draw(self.x, self.y)