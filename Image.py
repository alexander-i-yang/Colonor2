import tkinter as tk
from PIL import Image, ImageTk
import Movable as Mov


class SimpleImage:
    def __init__(self, canvas, image_path, width=0, height=0, debug=False, anchor=tk.NW):
        self.canvas = canvas
        loaded_image = Image.open(image_path)
        if width != 0 and height != 0:
            loaded_image = loaded_image.resize((int(width), int(height)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(master=canvas, image=loaded_image)
        self.canvas = canvas
        self.img_width = img.width()
        self.img_height = img.height()
        self.img = img
        self.tk_img = -1
        self.debug = debug
        self.anchor = anchor

    def get_canvas(self):
        return self.canvas

    def get_width(self):
        return int(self.img_width)

    def get_height(self):
        return int(self.img_height)

    def get_tk_img(self):
        return self.tk_img

    def draw(self, x, y):
        ret = self.get_canvas().create_image((x, y), anchor=self.anchor, image=self.img)
        self.tk_img = ret
        if self.debug:
            canvas = self.get_canvas()
            r = canvas.create_rectangle(canvas.bbox(ret, fill="white"))
            canvas.tag_lower(r, ret)
        return ret

    def update_img(self, path, flip_x=1):
        loaded_image = Image.open(path)
        loaded_image = loaded_image.resize((self.img_width, self.img_height), Image.ANTIALIAS)
        if flip_x > 0:
            loaded_image = loaded_image.transpose(Image.FLIP_LEFT_RIGHT)
        img = ImageTk.PhotoImage(loaded_image)
        self.img = img
        self.canvas.itemconfig(self.tk_img, image=self.img)

    def blank(self):
        self.get_canvas().delete(self.tk_img)


class AnimatedImage(Mov.Movable, SimpleImage):

    def __init__(self, x, y, canvas, path, max_img, distance, oscillate=False, static_path="", skip=None, mspf=100, anchor=tk.NW, static=False):
        if skip is None:
            skip = []
        self.path = path
        self.oscillate = oscillate
        self.max_img = max_img
        self.moving = False
        self.rotate_state = 0
        self.rotate_direction = 1
        self.img_flip = False
        self.static = static
        self.static_path = static_path if static_path else self.get_path(0)
        self.skip = skip
        self.mspf = mspf
        SimpleImage.__init__(
            self=self,
            canvas=canvas,
            image_path=self.static_path,
            anchor=anchor
        )
        Mov.Movable.__init__(
            self=self,
            x=x, y=y,
            canvas=canvas,
            distance=distance
        )

    def set_direction(self, direction):
        self.rotate_direction = direction

    def play(self):
        if not self.moving:
            self.set_direction(1)
            self.rotate_img()
            self.moving = True

    def stop(self):
        self.moving = False
        self.set_direction(0)
        self.rotate_state = 0
        self.update_img(static=True)

    def set_img_direction(self, x_flip):
        self.img_flip = x_flip
        self.update_img()

    def rotate_img(self):
        if self.rotate_direction != 0:
            if self.oscillate:
                if self.rotate_state == self.max_img * self.rotate_direction:
                    self.set_direction(-1 * self.rotate_direction)
                self.rotate_state += self.rotate_direction
            else:
                if self.rotate_state < self.max_img:
                    self.rotate_state += 1
                else:
                    self.rotate_state = 0
                if self.rotate_state in self.skip:
                    self.rotate_state += 1
            self.update_img()
            self.canvas.after(self.mspf, self.rotate_img)

    def update_img(self, static=False, path=None):
        new_path = self.static_path if static else self.get_path(self.rotate_state)
        if path:
            new_path = path
        super().update_img(new_path, flip_x=self.img_flip)

    def set_path(self, path):
        self.path = path
        self.update_img()
        print(self.get_width())

    def get_path(self, num):
        if self.get_max_img() > 9 and num < 10:
            num = "0" + str(num)
        return self.path % num

    def get_max_img(self):
        return self.max_img

    def undraw(self):
        super(SimpleImage).blank()

    def set_max_img(self, max_num):
        self.max_img = max_num

    def draw(self):
        self.update_img(static=True)
        SimpleImage.draw(self=self, x=self.get_x(), y=self.get_y())
