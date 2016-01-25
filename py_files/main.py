from Tkinter import *
import threading

WIDTH = 500
HEIGHT = 750
DELAY = 50

class Board(Canvas):
    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, 
            background="white", highlightthickness=0)
        self.initGame()
        self.pack()

    def initGame(self):
        self.alienSpawn = 0
        self.spaceMove = 0
        self.bind_all("<a>", self.moveLeft)
        self.bind_all("<d>", self.moveRight)
        self.bind_all("<space>", self.shoot)
        self.initObj()
        self.after(DELAY, self.onTimer)

    def initObj(self):
        self.spaceship = self.create_rectangle(0, HEIGHT-50, 50, HEIGHT, width=0, fill="green", tag="spaceship")
        self.alienList = []
        self.alienList.append((self.create_rectangle(20, 20, 40, 40, width=0, fill="red", tag="alien"), Alien()))
        self.shotList = []

    def checkCollision(self):
        for alien in self.alienList:
            if self.coords(alien[0])[0] == 440 or (self.coords(alien[0])[0] == 40 and self.coords(alien[0])[1] > 20):
                if alien[1].x == 2 or alien[1].x == -2:
                    alien[1].move_down()
                else:
                    alien[1].move_rev()

            if self.coords(alien[0])[0] == 460 or (self.coords(alien[0])[0] == 20 and self.coords(alien[0])[1] > 20):
                alien[1].move_down_rev()

    def doMove(self):
        for alien in self.alienList:
            self.move(alien[0], alien[1].x, alien[1].y)

        for shot in self.shotList:
            self.move(shot[0], 0, -3)

    def moveRight(self, e):
        self.move(self.spaceship, 5, 0)

    def moveLeft(self, e):
        self.move(self.spaceship, -5, 0)

    def shoot(self, e):
        shotPos = self.coords(self.spaceship)[0] + 25
        self.shotList.append((self.create_rectangle(shotPos-2, HEIGHT-50, shotPos+2, HEIGHT-60, width=0, fill="blue", tag="shot"), Shot(shotPos)))

    def onTimer(self):
        self.alienSpawn += 1
        if (self.alienSpawn > 30):
            self.alienList.append((self.create_rectangle(20, 20, 40, 40, width=0, fill="red", tag="alien"), Alien()))
            self.alienSpawn = 0
        self.checkCollision()
        self.doMove()
        self.after(DELAY, self.onTimer)

class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.board = Board()
        self.pack()

class Alien():
    sizex = 20
    sizey = 20
    def __init__(self):
        self.alive = True
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

    def die(self):
        self.alive = False

class Shot():
    sizex = 10
    sizey = 4
    def __init__(self, pos):
        self.x = pos

def main():

    root = Tk()
    game = Game()
    root.mainloop()  


if __name__ == '__main__':
    main()