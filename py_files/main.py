from Tkinter import *
from random import randint

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

        for shot in self.shotList:
            if self.coords(shot[0])[1] == 0 or self.coords(shot[0])[1] == HEIGHT - 100:
                print "remove"
                del self.shotList[self.shotList.index(shot)]
                self.delete(shot[0])
                print len(self.shotList)

            for i in range(int(self.coords(shot[0])[1]), int(self.coords(shot[0])[1]) + shot[1].sizey):
                for alien in self.alienList:
                    prev
                    if self.coords(alien[0])[1] <= i <= self.coords(alien[0])[1] + alien[1].sizey:
                        if prev != i:
                            print "ALIEN Y####"
                            print self.coords(alien[0])[1]
                            print i
                            print self.coords(alien[0])[1] + alien[1].sizey
                            print prev
                            prev = i
                            print prev
                            print "ALIEN Y----"
                #         for j in range(int(self.coords(shot[0])[0]), int(self.coords(shot[0])[0]) + shot[1].sizex):
                #             if self.coords(alien[0])[0] <= j <= self.coords(alien[0])[0] + alien[1].sizex:
                #                 print "remove"
                #                 del self.shotList[self.shotList.index(shot)]
                #                 self.delete(shot[0])
                #                 del self.alienList[self.alienList.index(alien)]
                #                 self.delete(alien[0])
                #                 print len(self.shotList)
                #                 continue

    def doMove(self):
        for alien in self.alienList:
            self.move(alien[0], alien[1].x, alien[1].y)

        for shot in self.shotList:
            self.move(shot[0], shot[1].movex, shot[1].movey)

    def doShoot(self):
        if len(self.alienList) >= 10:
            rand = randint(1,100)
            if rand == 1:
                randAlien = self.alienList[randint(0, len(self.alienList)-1)]
                shotPosx = self.coords(randAlien[0])[0] + (randAlien[1].sizex/2) -1
                shotPosy = self.coords(randAlien[0])[1] + randAlien[1].sizey
                self.shotList.append((self.create_rectangle(shotPosx, shotPosy, shotPosx+2, shotPosy+4, width=1, tag="alienShot"), Shot(shotPosx, 2, 4, 0, 3)))
                print "add"
                print len(self.shotList)

    def moveRight(self, e):
        if self.coords(self.spaceship)[0] + 55 <= WIDTH:
            self.move(self.spaceship, 5, 0)

    def moveLeft(self, e):
        if self.coords(self.spaceship)[0] - 5 >= 0:
            self.move(self.spaceship, -5, 0)

    def shoot(self, e):
        shotPos = self.coords(self.spaceship)[0] + 25
        self.shotList.append((self.create_rectangle(shotPos-2, HEIGHT-50, shotPos+2, HEIGHT-60, width=0, fill="blue", tag="SpaceShipShot"), Shot(shotPos, 4, 10, 0, -3)))

    def onTimer(self):
        self.alienSpawn += 1
        if (self.alienSpawn > 30):
            self.alienList.append((self.create_rectangle(-20, 20, 0, 40, width=0, fill="red", tag="alien"), Alien()))
            self.alienSpawn = 0
        self.checkCollision()
        self.doMove()
        self.doShoot()
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

class Shot():
    def __init__(self, pos, sizex, sizey, movex, movey):
        self.x = pos
        self.sizex = sizex
        self.sizey = sizey
        self.movex = movex
        self.movey = movey

def main():

    root = Tk()
    game = Game()
    root.mainloop()  


if __name__ == '__main__':
    main()