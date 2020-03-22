import Image as Im


class Sprite(Im.AnimatedImage):
    def __init__(self, x, y, canvas, dynamic_path, max_img):
        super().__init__(x, y, canvas, dynamic_path, max_img)