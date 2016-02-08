class Bomber():
    def __init__(self, sizex, sizey, movex, movey, id):
        self.sizex = sizex
        self.sizey = sizey
        self.movex = movex
        self.movey = movey
        self.id = id

    def move_rev(self):
        self.movex = - self.movex
