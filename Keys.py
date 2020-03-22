import main as m


class Keys:
    def __init__(self, master):
        self.keys = {
            'Left': {"a": 37, "p": master.move_left, "r": master.stop_moving_x},
            'Right': {"a": 39, "p": master.move_right, "r": master.stop_moving_x},
            'Escape': {"a": 27, "p": master.quit}
        }
        master.bind('<Key>', self.key_pressed)
        master.bind('<KeyRelease>', self.key_released)

    def key_pressed(self, event):
        for key in self.keys:
            key_code = self.keys[key]["a"]
            key_code = key_code if key_code else ord(key)
            if event.keycode == key_code:
                self.keys[key]["p"]()

    def key_released(self, event):
        for key in self.keys:
            key_code = self.keys[key]["a"]
            key_code = key_code if key_code else ord(key)
            if event.keycode == key_code:
                if self.keys[key]["r"]:
                    self.keys[key]["r"]()
