import time
import abc

BASE_SPEED = 1


class Movable(abc.ABC):
    def __init__(self, x, y, canvas, debug=False):
        self._canvas = canvas
        self.x_coord = Coord(x, canvas, self.move_x)
        self.y_coord = Coord(y, canvas, self.move_y)
        self._distance = 0
        self.debug = debug

    @property
    def canvas(self): return self._canvas

    @canvas.setter
    def canvas(self, c): self._canvas = c

    def move_left(self):
        self.x_coord.move_speed(BASE_SPEED, self.distance)

    def move_right(self):
        self.x_coord.move_speed(-1*BASE_SPEED, self.distance)

    def set_vx(self, v):
        self.x_coord.v = v

    def set_vy(self, v):
        self.y_coord._v = v

    def get_debug(self):
        return self.debug

    def move_x(self, dx):
        self.incr_pos(dx, 0)

    def move_y(self, dy):
        self.incr_y(dy)

    @abc.abstractmethod
    def draw(self):
        pass

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, d):
        self._distance = d

    def set_distance(self, d):
        self._distance = d

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

    @property
    def x(self):
        return self.x_coord.get_coord()

    @x.setter
    def x(self, x):
        self.x_coord.set_coord(x)

    @property
    def y(self):
        return self.y_coord.get_coord()

    @y.setter
    def y(self, y): self.y_coord.set_coord(y)

    def incr_pos(self, dx, dy):
        self.incr_x(dx)
        self.incr_y(dy)

    def get_pos(self): return self.x, self.y


class Coord:
    def __init__(self, pos, canvas, move_func):
        self._pos = pos
        self._v = 0
        self._last_update = 0
        self.canvas = canvas
        self.move_func = move_func

    @property
    def v(self): return self._v

    @v.setter
    def v(self, v):
        self._v = v
        if v != 0:
            self.move()

    def set_coord(self, pos):
        self._pos = pos

    def incr_coord(self, d):
        self._pos += d

    def set_v(self, v):
        self._v = v

    def get_coord(self):
        return self._pos

    def move_speed(self, speed, distance):
        if distance == 0:
            return
        new_v = speed/distance
        self.v = new_v

    def move(self):
        if self._last_update == 0:
            self._last_update = time.time()
        dt = time.time() - self._last_update
        self._last_update = time.time()
        dx = self._v * dt * 1000
        self.move_func(dx)
        self._pos += dx
        if self._v != 0:
            self.canvas.after(10, self.move)
        else:
            self._last_update = 0
