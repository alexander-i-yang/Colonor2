import tkinter as tk
import Layer as Layer
import Keys as K

DEBUG = True


class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        if DEBUG:
            self.screen_width = 500
            self.screen_height = 500
        else:
            self.screen_width = self.winfo_screenwidth() + 20
            self.screen_height = self.winfo_screenheight() + 20
        self.resize()
        if not DEBUG:
            self.overrideredirect(1)

        self.title("Colonor")

        self.scene_layers = {}

        self.player = Layer.Layer(self, self.screen_width, self.screen_height, "player")
        self.scene_layers["player"] = self.player

        bg = Layer.Layer(self, self.screen_width, self.screen_height, "background", bg="black")
        self.scene_layers["background"] = bg

        self.keys = K.Keys(self)

        self.draw()

        self.mainloop()

    def draw(self):
        for l in self.scene_layers:
            layer = self.scene_layers[l]
            layer.draw()

    def resize(self):
        self.geometry("{0}x{1}+-3+-5".format(
            self.screen_width,
            self.screen_height
        ))


if __name__ == '__main__':
    root = Game()
