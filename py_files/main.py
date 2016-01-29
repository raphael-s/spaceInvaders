from Tkinter import *
from random import randint
import tkFont
from alien import Alien

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
        self.score = IntVar(self, 0)
        self.level = IntVar(self, 1)
        self.health = 3
        self.alienSpawn = 0
        self.shootCooldown = 0
        self.bind_all("<a>", self.moveLeft)
        self.bind_all("<d>", self.moveRight)
        self.bind_all("<space>", self.shoot)
        self.initObj()
        self.after(DELAY, self.onTimer)

    def initObj(self):
        self.menu = []
        menuFont = tkFont.Font(size="20")
        #self.spaceShipImage = imageTK.PhotoImage(file="../gfx/green.png")
        self.menu.append(self.create_rectangle(0, 0, WIDTH, 30, width=0, fill="grey", tag="menuBar"))
        self.menu.append(self.create_text(5, 5, text="Score: ", anchor="nw", font=menuFont, tag="scoreLabel"))
        self.menu.append(self.create_text(self.coords(self.find_withtag("scoreLabel"))[0]+65, 5, text=str(self.score.get()), anchor="nw", font=menuFont, tag="score"))
        self.menu.append(self.create_text(205, 5, text="Level: ", anchor="nw", font=menuFont, tag="levelLabel"))
        self.menu.append(self.create_text(self.coords(self.find_withtag("levelLabel"))[0]+63, 5, text=str(self.level.get()), anchor="nw", font=menuFont, tag="level"))
        for i in range(self.health):
            count = i + 1
            self.menu.append(self.create_rectangle(WIDTH - (25 * count), 5, WIDTH - (25 * count) + 20, 25, fill="red", tag="health"+str(count)))
        self.spaceship = self.create_rectangle(0, HEIGHT-50, 50, HEIGHT, tag="spaceship", fill="green")
        self.alienList = []
        self.shotList = []

    def checkCollision(self):
        remShotList = []
        remAlienList = []
        remHealthList = []
        for alien in self.alienList:
            if self.coords(alien[0])[0] == 440 or (self.coords(alien[0])[0] == 40 and self.coords(alien[0])[1] > 50):
                if alien[1].x == 2 or alien[1].x == -2:
                    alien[1].move_down()
                else:
                    alien[1].move_rev()

            if self.coords(alien[0])[0] == 460 or (self.coords(alien[0])[0] == 20 and self.coords(alien[0])[1] > 50):
                alien[1].move_down_rev()

        for shot in self.shotList:
            shotx = range(int(self.coords(shot[0])[0]), int(self.coords(shot[0])[0]) + shot[1].sizex)
            shoty = range(int(self.coords(shot[0])[1]), int(self.coords(shot[0])[1]) + shot[1].sizey)
            if self.coords(shot[0])[1] <= 0 or self.coords(shot[0])[1] >= HEIGHT:
                remShotList.append(shot)

            if not shot[0] in self.find_withtag("alienShot"):
                for alien in self.alienList:
                    alienx = range(int(self.coords(alien[0])[0]), int(self.coords(alien[0])[0] + alien[1].sizex + 1))
                    alieny = range(int(self.coords(alien[0])[1]), int(self.coords(alien[0])[1] + alien[1].sizey + 1))
                    for x in shotx:
                        if x in alienx:
                            for y in shoty:
                                if y in alieny and x in alienx:
                                    remShotList.append(shot)
                                    remAlienList.append(alien)

            elif shot[0] in self.find_withtag("alienShot"):
                shipx = range(int(self.coords(self.spaceship)[0]), int(self.coords(self.spaceship)[0]) + 50)
                shipy = range(int(self.coords(self.spaceship)[1]), int(self.coords(self.spaceship)[1]) + 50)
                for x in shotx:
                    if x in shipx:
                        for y in shoty:
                            if y in shipy:
                                remShotList.append(shot)
                                remHealthList.append(self.find_withtag("health"+str(self.health)))

        if len(remAlienList) > 0:
            remAlienList = set(remAlienList)
            self.remAlien(remAlienList)

        if len(remShotList) > 0:
            remShotList = set(remShotList)
            self.remShots(remShotList)

        if len(remHealthList) > 0:
            remHealthList = set(remHealthList)
            self.remHealth(remHealthList)

    def remShots(self, elements):
        for item in elements:
            del self.shotList[self.shotList.index(item)]
            self.delete(item[0])

    def remAlien(self, elements):
        for item in elements:
            del self.alienList[self.alienList.index(item)]
            self.delete(item[0])
            self.score.set(self.score.get()+1)
            self.itemconfigure(self.find_withtag("score"), text=self.score.get())

    def remHealth(self, elements):
        for item in elements:
            self.delete(item)
            self.health -= 1

    def doMove(self):
        for alien in self.alienList:
            self.move(alien[0], alien[1].x, alien[1].y)

        for shot in self.shotList:
            self.move(shot[0], shot[1].movex, shot[1].movey)

    def doShoot(self):
        if self.shootCooldown > 0:
            self.shootCooldown -= 1
        if len(self.alienList) >= 10:
            rand = randint(1,100)
            if rand == 1:
                randAlien = self.alienList[randint(0, len(self.alienList)-1)]
                shotPosx = self.coords(randAlien[0])[0] + (randAlien[1].sizex/2) -1
                shotPosy = self.coords(randAlien[0])[1] + randAlien[1].sizey
                self.shotList.append((self.create_rectangle(shotPosx, shotPosy, shotPosx+2, shotPosy+4, width=1, tag="alienShot"), Shot(shotPosx, 2, 4, 0, 3)))

    def moveRight(self, e):
        if self.coords(self.spaceship)[0] + 55 <= WIDTH:
            self.move(self.spaceship, 5, 0)

    def moveLeft(self, e):
        if self.coords(self.spaceship)[0] - 5 >= 0:
            self.move(self.spaceship, -5, 0)

    def onChangeScore(self, arg1, arg2, arg3):
        self.itemconfigure(self.find_withtag("score"), text=self.score.get())

    def onChangeLevel(self, arg1, arg2, arg3):
        self.itemconfigure(self.find_withtag("level"), text=self.level.get())

    def shoot(self, e):
        if self.shootCooldown == 0:
            shotPos = self.coords(self.spaceship)[0] + 25
            self.shotList.append((self.create_rectangle(shotPos-2, HEIGHT-50, shotPos+2, HEIGHT-60, width=0, fill="blue", tag="SpaceShipShot"), Shot(shotPos, 4, 10, 0, -3)))
            self.shootCooldown = 50

    def checkHealth(self):
        if not self.health > 0:
            self.create_text(WIDTH/2, HEIGHT/2 - 100, text="Game Over", font=tkFont.Font(size="70"), tag="GameOver")
            #self.create_text(WIDTH/2, HEIGHT/2, text="Score: " + str(self.score.get()), font=tkFont.Font(size="70"), tag="finalScore")
            self.unbind_all("<a>")
            self.unbind_all("<d>")
            self.unbind_all("<space>")
        else:
            self.timer = self.after(DELAY, self.onTimer)

    def onTimer(self):
        self.checkHealth()
        self.alienSpawn += 1
        if (self.alienSpawn > 30):
            self.alienList.append((self.create_rectangle(-20, 50, 0, 70, width=0, fill="red", tag="alien"), Alien()))
            self.alienSpawn = 0
        self.checkCollision()
        self.doMove()
        self.doShoot()

class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.board = Board()
        self.pack()

class Shot():
    def __init__(self, pos, sizex, sizey, movex, movey):
        self.x = pos
        self.sizex = sizex
        self.sizey = sizey
        self.movex = movex
        self.movey = movey

def main():
    root = Tk()
    root.title("Space Invaders")
    game = Game()
    root.mainloop()


if __name__ == '__main__':
    main()