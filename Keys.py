import main as m


class Keys:
    def __init__(self, master):
        self.keys = {
            'Escape': [27, master.quit]
        }
        master.bind('<Key>', self.key_pressed)
        master.bind('<KeyRelease>', self.key_released)

    def key_pressed(self, event):
        for key in self.keys:
            key_code = self.keys[key][0]
            if event.keycode == key_code:
                print(self.keys[key])
                self.keys[key][1]()

    def key_released(self, event):
        print("released:", event)
