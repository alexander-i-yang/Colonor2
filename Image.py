import tkinter as tk
from PIL import Image, ImageTk
import Movable as Mov


def get_class(kls, args):
    parts = kls.split('.')
    m = getattr(__import__("Image"), parts[0])
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m(args_dict=args)


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
        self.img_path = image_path
        self.tk_img = -1
        self.debug = debug
        self.anchor = anchor
        self.img_flip = False

    @property
    def width(self):
        return int(self.img_width)

    def get_height(self):
        return int(self.img_height)

    def get_tk_img(self):
        return self.tk_img

    def set_img_flip_x(self, i):
        self.img_flip = i

    def draw(self, x, y):
        ret = self.canvas.create_image((x, y), anchor=self.anchor, image=self.img)
        self.tk_img = ret
        if self.debug:
            canvas = self.canvas
            r = canvas.create_rectangle(canvas.bbox(ret, fill="white"))
            canvas.tag_lower(r, ret)
        return ret

    def update_img(self, path=""):
        path = path if path else self.img_path
        self.img_path = path
        loaded_image = Image.open(path)
        loaded_image = loaded_image.resize((self.img_width, self.img_height), Image.ANTIALIAS)
        if self.img_flip:
            loaded_image = loaded_image.transpose(Image.FLIP_LEFT_RIGHT)
        img = ImageTk.PhotoImage(loaded_image)
        self.img = img
        self.canvas.itemconfig(self.tk_img, image=img)

    def blank(self):
        self.canvas.delete(self.tk_img)

    def lower_to_obj(self, o):
        if o != -1:
            self.canvas.tag_lower(self.get_tk_img(), o)


class MovImage(Mov.Movable, SimpleImage):
    def __init__(self, x=None, y=None, canvas=None, image_path=None, anchor=tk.NW, debug=False, args_dict=None):
        if args_dict:
            x = args_dict["x"]
            y = args_dict["y"]
            canvas = args_dict["canvas"]
            image_path = args_dict["image_path"]
            anchor = args_dict["anchor"] if "anchor" in args_dict.keys() else tk.NW
            debug = args_dict["debug"] if "debug" in args_dict.keys() else False
        super(MovImage, self).__init__(
            x=x, y=y,
            canvas=canvas,
            debug=debug
        )
        SimpleImage.__init__(
            self=self,
            canvas=canvas,
            image_path=image_path,
            anchor=anchor,
            debug=debug
        )

    def draw(self):
        SimpleImage.draw(self, super().x, super().y)

    def incr_pos(self, dx, dy):
        super().incr_pos(dx, dy)
        super().canvas.coords(SimpleImage.get_tk_img(self), super().x+dx, super().y+dy)


class AnimatedImage(MovImage):
    def __init__(self, x, y, canvas, dynamic_path, max_img, w=0, h=0, oscillate=False, static_path="",
                 skip=None,
                 mspf=100, anchor=tk.NW, debug=False):
        if skip is None:
            skip = []
        self.dynamic_path = dynamic_path
        self.oscillate = oscillate
        self.max_img = max_img
        self.moving = False
        self.rotate_state = 0
        self.rotate_direction = 1
        self.static_path = static_path if static_path else self.get_path(0)
        self.skip = skip
        self.mspf = mspf
        super().__init__(
            x=x, y=y,
            canvas=canvas,
            image_path=self.static_path,
            anchor=anchor,
            debug=debug
        )

    def incr_pos(self, dx, dy):
        self.canvas.move(SimpleImage.get_tk_img(self), dx, dy)

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
        self.update_img_path(static=True)

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
            self.update_img_path()
            self.canvas.after(self.mspf, self.rotate_img)

    def update_img_path(self, static=False, path=None):
        new_path = self.static_path if static else self.get_path(self.rotate_state)
        if path:
            new_path = path
        super().update_img(new_path)

    def get_path(self, num):
        if self.get_max_img() > 9 and num < 10:
            num = "0" + str(num)
        return self.dynamic_path % num

    def get_max_img(self):
        return self.max_img

    def undraw(self):
        super(SimpleImage).blank()

    def set_max_img(self, max_num):
        self.max_img = max_num

    def draw(self):
        self.update_img_path(static=True)
        super().draw()


class Tessellate(Mov.Movable):

    def __init__(self, canvas, x, y, w, h, classname, base_img_args):
        super().__init__(x=x, y=y, canvas=canvas)
        self.imgs = []
        self._w = w
        self._h = h
        self.padding = 50
        self._classname = classname
        self._base_img_args = base_img_args
        self.set_img_x()
        self.left_bound = super().x-self.padding
        self.right_bound = super().x+self.w+self.padding
        canvas.create_rectangle(x, y, x+w, y+h, fill="blue")

    @property
    def base_img_args(self):
        return self._base_img_args

    @base_img_args.setter
    def base_img_args(self, b):
        self._base_img_args = b

    @property
    def classname(self):
        return self._classname

    @classname.setter
    def classname(self, c):
        self._classname = c

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, wid):
        self._w = wid

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, hei):
        self._h = hei

    def set_img_x(self):
        last_x = super().x-self.w
        while last_x < super().x + 2*self.w:
            cur = get_class(self.classname, self.base_img_args)
            cur.x = last_x
            cur.y = super().y
            self.imgs.append(cur)
            last_x += cur.width

    def draw(self):
        self.apply_to_all("draw")

    def move_left(self):
        self.apply_to_all("move_left")
        self.check_bounds()

    def move_right(self):
        self.apply_to_all("move_right")
        self.check_bounds()

    def check_bounds(self):
        first = self.imgs[0]
        last = self.imgs[-1]
        if first.x > self.left_bound:
            self.new(
                x=first.x - first.width + Mov.BASE_SPEED * 20, y=super().y,
                distance=first.distance,
                insert=0
            )
        if first.x+first.width < self.left_bound:
            self.delete(first)
        if last.x+last.width < self.right_bound:
            self.new(
                x=last.x + last.width - Mov.BASE_SPEED * 15, y=super().y,
                distance=last.distance,
                insert=-1
            )
        if last.x > self.right_bound:
            self.delete(last)

    def new(self, x, y, distance, insert=-1):
        cur = get_class(self.classname, self.base_img_args)
        cur.x = x
        cur.y = y
        if insert == -1: self.imgs.append(cur)
        else: self.imgs.insert(insert, cur)
        cur.distance = distance
        cur.draw()

    def delete(self, item):
        item.blank()
        self.imgs.remove(item)
        del item

    def apply_to_all(self, method: str, *args: object, **kwargs: object) -> None:
        for obj in self.imgs:
            getattr(obj, method)(*args, **kwargs)

    def set_distance(self, d):
        self.apply_to_all("set_distance", d)

    def lower_to_obj(self, o):
        self.apply_to_all("lower_to_obj", o)

    def set_vx(self, v):
        self.apply_to_all("set_vx", v)