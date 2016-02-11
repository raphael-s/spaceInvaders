class Alien():
    def __init__(self, sizex, sizey, movex, movey, id):
        self.sizex = sizex
        self.sizey = sizey
        self.movex = movex
        self.movey = movey
        self.id = id

    def move_down(self):
        if self.movex > 0:
            self.movex = 2
        else:
            self.movex = -2
        self.movey = 2

    def move_down_rev(self):
        if self.movex > 0:
            self.movex = -2
        else:
            self.movex = 2

    def move_rev(self):
        if self.movex > 0:
            self.movex = 4
        else:
            self.movex = -4
        self.movey = 0
