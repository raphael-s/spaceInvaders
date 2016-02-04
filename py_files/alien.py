class Alien():
    def __init__(self, sizex, sizey, movex, movey, id):
        self.sizex = sizex
        self.sizey = sizey
        self.movex = movex
        self.movey = movey
        self.id = id

    def move_down(self):
        if self.movex > 0:
            self.movex = 1
        else:
            self.movex = -1
        self.movey = 1

    def move_down_rev(self):
        if self.movex > 0:
            self.movex = -1
        else:
            self.movex = 1

    def move_rev(self):
        if self.movex > 0:
            self.movex = 2
        else:
            self.movex = -2
        self.movey = 0