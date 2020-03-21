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
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.layers = Layer.Layers(self.canvas, self.screen_width, self.screen_height)

        self.keys = K.Keys(self)

        self.draw()

        self.mainloop()

    def draw(self):
        self.layers.draw()

    def resize(self):
        self.geometry("{0}x{1}+-3+-5".format(
            self.screen_width,
            self.screen_height
        ))


if __name__ == '__main__':
    root = Game()
