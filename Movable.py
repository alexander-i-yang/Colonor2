import time
import abc


class Movable(abc.ABC):
    def __init__(self, x, y, canvas, distance, fill="#8c2d18", debug=False):
        self.canvas = canvas
        self.x_coord = Coord(x, canvas, self.move_x)
        self.y_coord = Coord(y, canvas, self.move_y)
        self.fill = fill
        self.debug = debug
        self.distance = distance

    def left_vx(self):
        v = 1.0 / self.distance
        v = v * 10 if self.debug else v
        self.set_vx(v)

    def right_vx(self):
        v = -1.0 / self.distance
        v = v * 10 if self.debug else v
        self.set_vx(v)

    def set_vx(self, v): self.x_coord.set_v(v)

    def set_vy(self, v): self.y_coord.set_v(v)

    def get_debug(self): return self.debug

    def move_x(self, dx):
        self.incr_x(dx)
        self.draw()

    def move_y(self, dy):
        self.incr_y(dy)
        self.draw()

    def get_distance(self): return self.distance

    @abc.abstractmethod
    def draw(self):
        pass

    def get_canvas(self):
        return self.canvas

    def set_pos(self, *args):
        if len(args) == 1:
            args = args[0]
        x = args[0]
        y = args[1]
        self.move_x(x - self.x_coord.get_coord())
        self.move_y(y - self.y_coord.get_coord())

    def incr_x(self, dx):
        self.x_coord.incr_coord(dx)

    def incr_y(self, dy):
        self.y_coord.incr_coord(dy)

    def get_x(self): return self.x_coord.get_coord()

    def get_y(self): return self.y_coord.get_coord()


class Coord:
    def __init__(self, pos, canvas, move_func):
        self.pos = pos
        self.v = 0
        self.last_update = 0
        self.canvas = canvas
        self.move_func = move_func

    def set_coord(self, pos):
        self.pos = pos

    def incr_coord(self, d):
        self.pos += d

    def set_v(self, v):
        self.v = v
        if v != 0: self.move()

    def get_coord(self):
        return self.pos

    def move(self):
        if self.last_update == 0:
            self.last_update = time.time()
        dt = time.time() - self.last_update
        self.last_update = time.time()
        dx = self.v * dt * 1000
        self.move_func(dx)
        self.pos += dx
        if self.v != 0:
            self.canvas.after(10, self.move)
        else:
            self.last_update = 0
