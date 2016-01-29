class Alien():
    sizex = 20
    sizey = 20
    def __init__(self):
        self.x = 2
        self.y = 0

    def move_down(self):
        if self.x > 0:
            self.x = 1
        else:
            self.x = -1
        self.y = 1

    def move_down_rev(self):
        if self.x > 0:
            self.x = -1
        else:
            self.x = 1

    def move_rev(self):
        if self.x > 0:
            self.x = 2
        else:
            self.x = -2
        self.y = 0