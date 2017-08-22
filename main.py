from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
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
Config.set('graphics', 'resizable', 0)
from kivy.core.window import Window


class GameScreen(FloatLayout):
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
    wannabe = [Window.width / 2, Window.height / 2]
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
    vector = Vector(0, Window.height * 0.0055)
    direction = 0

    def move(self):
        if self.pos[1] > Window.height or self.pos[1] < - Window.height * 0.417:
            if self.vector[1] < Window.height * 0.025:
                self.vector[1] = self.vector[1] * 1.1
            self.direction = randint(0, 1) * 180
            if self.direction == 0:
                self.pos = (randint(0, int(Window.width * 0.7552)), -Window.height * 0.417)
            else:
                self.pos = (randint(0, int(Window.width * 0.7552)), Window.height * 0.925)
        self.pos = Vector(*self.vector).rotate(self.direction) + self.pos


class LEFTRIGHTRocket(Widget):
    vector = Vector(Window.width * 0.003125, 0)
    direction = 0

    def move(self):
        if self.pos[0] > Window.width * 0.78125 or self.pos[0] < -Window.width * 0.2348:
            if self.vector[0] < Window.width * 0.01875:
                self.vector[0] = self.vector[0] * 1.1
            self.direction = randint(0, 1) * 180
            if self.direction == 0:
                self.pos = (-Window.width * 0.2348, randint(0, int(Window.height * 0.9537)))
            else:
                self.pos = (Window.width * 0.78125, randint(0, int(Window.height * 0.9537)))
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
