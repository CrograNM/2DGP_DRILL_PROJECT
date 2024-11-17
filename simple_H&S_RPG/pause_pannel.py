from pico2d import load_image

WIDTH = 1280
HEIGHT = 720

class Pannel:
    def __init__(self):
        self.image = load_image('resource/pause_mode/pause.png')

    def draw(self):
        self.image.draw(WIDTH//2, HEIGHT//2, WIDTH//4 * 3, HEIGHT//4 * 3)

    def update(self):
        pass

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


class Resume_Button(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = load_image('resource/pause_mode/resume_button_400_100.png')

    def draw(self):
        self.image.draw(self.x, self.y)


class Back_Button(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = load_image('resource/pause_mode/back_button_400_100.png')

    def draw(self):
        self.image.draw(self.x, self.y)

