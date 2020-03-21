import tkinter as tk
import Image as Im


class Layers:
    def __init__(self, canvas, w, h):
        self.layers = []
        self.canvas = canvas
        self.bg = Layer(canvas, w, h, "background")
        self.player = Layer(canvas, w, h, "player")
        self.test = Layer(canvas, w, h, "background")

        self.layers.append(self.player)
        self.layers.append(self.bg)
        self.layers.append(self.test)

        self.pos_objs = self.draw_pos_objs(w, h)
        self.reorganize()

    def draw_pos_objs(self, w, h):
        ret = []
        for o in self.layers:
            pos_obj = self.canvas.create_rectangle(w, h, w, h, fill="red")
            ret.append(pos_obj)
        return ret

    # Sorts the layers by distance and reorganizes them using pos_objs as a reference.
    def reorganize(self):
        sorted(self.layers, key=lambda x: x.get_distance(), reverse=True)
        self.layers.reverse()
        for i in range(0, len(self.layers)):
            cur_layer = self.layers[i]
            cur_obj = self.pos_objs[i]
            cur_layer.lower(cur_obj)

    def draw(self):
        for l in self.layers:
            print(l.get_distance())
            l.draw()


class Layer:
    def __init__(self, canvas, w, h, keyword, bg="white"):
        self.distance = -1
        self.objs = []
        self.canvas = canvas
        self.w = w
        self.h = h
        self.init_objs(keyword)

    def init_objs(self, keyword):
        if keyword == "player":
            self.distance = 1
            player = Im.AnimatedImage(
                x=self.w / 2, y=self.h / 2,
                canvas=self.canvas,
                path="static/images/Avatar/Walking %s.png",
                distance=1,
                max_img=11,
                anchor=tk.CENTER,
                skip=[0]
            )
            self.objs.append(player)
        elif keyword == "background":
            self.distance = 10
            self.objs.append(Im.AnimatedImage(
                x=0, y=0,
                canvas=self.canvas,
                path="",
                static_path="static/images/space-notime.png",
                distance=self.distance,
                max_img=0,
            ))
        else:
            print("ERROR: INVALID LAYER KEYOWRD: %s" % keyword)
            raise ValueError

    def draw(self):
        for o in self.objs:
            o.draw()

    def play(self):
        for o in self.objs:
            o.play()

    def get_distance(self): return self.distance

    def lower(self, cur_obj):
        for o in self.objs:
            tk = o.get_tk_img()
            if tk != -1:
                self.canvas.tag_lower(cur_obj.get_tk_img(), o)
