import tkinter as tk
import Image as Im


class Layers:
    def __init__(self, canvas, w, h):
        self.canvas = canvas
        self.layers = []

        self.init_objs(w, h)

        self.pos_objs = self.draw_pos_objs()
        self.reorganize()

    def draw_pos_objs(self):
        ret = []
        for i in self.layers:
            pos_obj = self.canvas.create_rectangle(0, 0, 0, 0, fill="red")
            ret.append(pos_obj)
        return ret

    # Sorts the layers by distance and reorganizes them using pos_objs as a reference.
    def reorganize(self):
        self.layers = sorted(self.layers, key=lambda x: x.get_distance())
        print([x.get_distance() for x in self.layers])
        self.layers.reverse()
        for i in range(0, len(self.layers)):
            cur_layer = self.layers[i]
            cur_obj = self.pos_objs[i]
            cur_layer.lower(cur_obj)

    def init_objs(self, w, h):
        player_img = Im.AnimatedImage(
            x=w / 2, y=h / 2,
            canvas=self.canvas,
            dynamic_path="static/images/Avatar/Walking %s.png",
            max_img=11,
            anchor=tk.CENTER,
            skip=[0]
        )
        self.player = Layer(
            canvas=self.canvas,
            distance=0,
            objs=[player_img]
        )
        bg = Im.Tessellate(
            canvas=self.canvas,
            x=0, y=0,
            w=w, h=h,
            classname="MovImage",
            base_img_args={
                "x": 0, "y": 0,
                "canvas": self.canvas,
                "image_path": "static/images/space-notime.png",
            }
        )
        self.bg = Layer(
            canvas=self.canvas,
            distance=10,
            objs=[bg]
        )
        ground = Im.Tessellate(
            canvas=self.canvas,
            x=0, y=h/2+player_img.get_height()/2-3,
            w=w, h=h/2-player_img.get_height()/2,
            classname="MovImage",
            base_img_args={
                "x":0, "y":0,
                "canvas":self.canvas,
                "image_path":"static/images/mars.png",
            }
        )
        self.ground_and_objs = Layer(
            canvas=self.canvas,
            distance=5,
            objs=[ground]
        )
        self.layers.append(self.player)
        self.layers.append(self.bg)
        self.layers.append(self.ground_and_objs)

    def draw(self):
        for l in self.layers:
            l.draw()

    def move_left(self):
        self.player.play()
        self.player.set_flip_x(True)
        for l in self.layers:
            l.move_left()

    def move_right(self):
        self.player.play()
        self.player.set_flip_x(False)
        for l in self.layers:
            l.move_right()

    def stop_moving(self):
        self.player.stop()
        for l in self.layers:
            l.stop_moving()


class Layer:
    def __init__(self, canvas, distance, objs):
        self.objs = objs
        self.canvas = canvas
        self.distance = distance

    def apply_to_all(self, method, *args, **kwargs):
        for obj in self.objs:
            getattr(obj, method)(*args, **kwargs)

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, d):
        self._distance = d
        self.apply_to_all("set_distance", d)

    def draw(self):
        self.apply_to_all("draw")

    def play(self):
        self.apply_to_all("play")

    def get_distance(self):
        return self.distance

    def lower(self, cur_obj):
        self.apply_to_all("lower_to_obj", cur_obj)

    def move_left(self):
        self.apply_to_all("move_left")

    def move_right(self):
        self.apply_to_all("move_right")

    def stop_moving(self):
        self.apply_to_all("set_vx", 0)

    def stop(self):
        self.apply_to_all("stop")

    def set_flip_x(self, flip_x):
        self.apply_to_all("set_img_flip_x", flip_x)
