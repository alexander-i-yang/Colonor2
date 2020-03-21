import tkinter as tk
import Image as Im


class Layer(tk.Canvas):
    def __init__(self, master, w, h, keyword, bg="white"):
        super().__init__(master, width=w, height=h, bg=bg)
        self.objs = []
        self.pack()
        self.w = w
        self.h = h
        self.init_objs(keyword)

    def init_objs(self, keyword):
        if keyword == "player":
            player = Im.AnimatedImage(
                x=self.w / 2, y=self.h / 2,
                canvas=self,
                path="static/images/Avatar/Walking %s.png",
                distance=1,
                max_img=11,
                anchor=tk.CENTER,
                skip=[0]
            )
            self.objs.append(player)
        if keyword == "background":
            self.objs.append(Im.AnimatedImage(
                x=0, y=0,
                canvas=self,
                path="static/images/Avatar/Walking %s.png",
                distance=1,
                max_img=11,
                anchor=tk.CENTER,
                skip=[0]
            ))

    def draw(self):
        for o in self.objs:
            o.draw()

    def play(self):
        for o in self.objs:
            o.play()
