from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.config import Config
from random import randint
import os

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'fullscreen', 'auto')


class GameScreen(Widget):
    player = ObjectProperty(None)
    ud_rocket = ObjectProperty(None)
    lr_rocket = ObjectProperty(None)
    sideboard = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

    def update(self, dt):
        self.player.move()
        self.ud_rocket.move()
        self.lr_rocket.move()
        if self.player.collide_widget(self.ud_rocket) or self.player.collide_widget(self.lr_rocket):
            self.sideboard.hits += 1


class Player(Widget):
    wannabe = [625, 625]
    vector = Vector(0, 0)

    def on_touch_move(self, touch):
        if touch.pos[0] < 1500 and touch.pos[1] < 1500:
            self.wannabe = touch.pos

    def on_touch_down(self, touch):
        if touch.pos[0] < 1500 and touch.pos[1] < 1500:
            self.wannabe = touch.pos

    def move(self):
        self.vector = Vector((self.wannabe[0] - 25 - self.pos[0]) * 0.03,
                             (self.wannabe[1] - 25 - self.pos[1]) * 0.03)
        if self.vector.length() > 10:
            self.vector = self.vector.normalize() * 10
        self.pos = Vector(self.vector) + self.pos


class UPDOWNRocket(Widget):
    vector = Vector(0, 6)
    direction = 0

    def move(self):
        if self.pos[1] > 1080 or self.pos[1] < -451:
            if self.vector[1] < 15:
                self.vector[1] = self.vector[1] * 1.2
            self.direction = randint(0, 1) * 180
            if self.direction == 0:
                self.pos = (randint(0, 1450), -450)
            else:
                self.pos = (randint(0, 1450), 999)
        self.pos = Vector(*self.vector).rotate(self.direction) + self.pos


class LEFTRIGHTRocket(Widget):
    vector = Vector(6, 0)
    direction = 0

    def move(self):
        if self.pos[0] > 1500 or self.pos[0] < -451:
            if self.vector[0] < 15:
                self.vector[0] = self.vector[0] * 1.1
            self.direction = randint(0, 1) * 180
            if self.direction == 0:
                self.pos = (-450, randint(0, 950))
            else:
                self.pos = (1500, randint(0, 950))
        self.pos = Vector(*self.vector).rotate(self.direction) + self.pos


class SideBoard(Widget):
    hits = NumericProperty(0)


class DodgeThisApp(App):
    def build(self):
        self.load_kv('main.kv')
        game = GameScreen()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    DodgeThisApp().run()
