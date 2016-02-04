import os

from Tkinter import Canvas, Frame, Tk

from random import randint

from PIL import ImageTk

from alien import Alien

from shot import Shot

import tkFont

# Size of the pitch
WIDTH = 500
HEIGHT = 750
# Size of the top (menu) bar
MENUBARSIZE = 30
# Gap between top bar and spawning aliens
MENUGAP = 80
# Border to outer edge of pitch. Used for alien movement AND game over screen
BORDER = 50
# Size of the spaceship
SHIPSIZE = 54
# Delay between call of onTick method
DELAY = 50
# Main directory of the game
ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))


# Class that contains most of the game's logic.
# Creates new canvas and then starts the game in it
class Board(Canvas):
    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="white", highlightthickness=0)
        self.initGame()
        self.pack()

    def initGame(self):
        self.score = 0
        self.level = 1
        self.health = 3
        self.alienSpawnCount = 6
        self.spawnDelay = 30
        self.shootCooldown = 0
        self.bind_all("<a>", self.moveLeft)
        self.bind_all("<d>", self.moveRight)
        self.bind_all("<space>", self.shoot)
        self.initObj()
        self.after(DELAY, self.onTimer)

    def initObj(self):
        self.menu = []
        menuFont = tkFont.Font(size="20", family="Helvetica")
        healthimg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/heart.png")
        self.healthimg = healthimg
        alienGreen = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/green.png")
        self.alienGreen = alienGreen
        shipimg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/space_ship.png")
        self.shipimg = shipimg
        bg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/bg.png")
        self.bg = bg
        self.create_image(0, -50, image=self.bg, anchor="nw", tag="bg1")
        self.create_image(0, -850, image=self.bg, anchor="nw", tag="bg2")
        self.menu.append(self.create_rectangle(0, 0, WIDTH, MENUBARSIZE, width=0, fill="grey", tag="menuBar"))
        self.menu.append(self.create_text(5, 5, text="Score: ", anchor="nw", font=menuFont, tag="scoreLabel"))
        self.menu.append(self.create_text(self.coords(self.find_withtag("scoreLabel"))[0] + 65, 5, text=str(self.score), anchor="nw", font=menuFont, tag="score"))
        self.menu.append(self.create_text(205, 5, text="Level: ", anchor="nw", font=menuFont, tag="levelLabel"))
        self.menu.append(self.create_text(self.coords(self.find_withtag("levelLabel"))[0] + 63, 5, text=str(self.level), anchor="nw", font=menuFont, tag="level"))
        for i in range(self.health):
            count = i + 1
            self.menu.append(self.create_image(WIDTH - (25 * count), 6, image=healthimg, tag="health" + str(count), anchor="nw"))
        self.spaceship = self.create_image(WIDTH / 2 - SHIPSIZE / 2, HEIGHT - SHIPSIZE - 20, image=self.shipimg, anchor="nw")
        self.alienList = []
        self.shotList = []

    def checkCollision(self):
        if len(self.alienList) > 0:
            if self.coords(self.alienList[0].id)[1] + self.alienList[0].sizey >= self.coords(self.spaceship)[1]:
                self.health = 0

        remShotList = []
        remAlienList = []
        remHealthList = []
        for alien in self.alienList:
            if self.coords(alien.id)[0] == WIDTH - BORDER - alien.sizex or (self.coords(alien.id)[0] == BORDER and self.coords(alien.id)[1] > MENUBARSIZE + MENUGAP + 1):
                if alien.movex == 2 or alien.movex == -2:
                    alien.move_down()
                else:
                    alien.move_rev()

            if self.coords(alien.id)[0] == WIDTH - BORDER - 20 or (self.coords(alien.id)[0] == BORDER - 20 and self.coords(alien.id)[1] > MENUBARSIZE + MENUGAP + 1):
                alien.move_down_rev()

        for shot in self.shotList:
            shotx = range(int(self.coords(shot.id)[0]), int(self.coords(shot.id)[0]) + shot.sizex)
            shoty = range(int(self.coords(shot.id)[1]), int(self.coords(shot.id)[1]) + shot.sizey)
            if self.coords(shot.id)[1] <= MENUBARSIZE or self.coords(shot.id)[1] >= HEIGHT:
                remShotList.append(shot)

            if shot.id not in self.find_withtag("alienShot"):
                for alien in self.alienList:
                    alienx = range(int(self.coords(alien.id)[0]), int(self.coords(alien.id)[0] + alien.sizex + 1))
                    alieny = range(int(self.coords(alien.id)[1]), int(self.coords(alien.id)[1] + alien.sizey + 1))
                    for x in shotx:
                        if x in alienx:
                            for y in shoty:
                                if y in alieny and x in alienx:
                                    remShotList.append(shot)
                                    remAlienList.append(alien)

            elif shot.id in self.find_withtag("alienShot"):
                shipx = range(int(self.coords(self.spaceship)[0]), int(self.coords(self.spaceship)[0]) + 50)
                shipy = range(int(self.coords(self.spaceship)[1]), int(self.coords(self.spaceship)[1]) + 50)
                for x in shotx:
                    if x in shipx:
                        for y in shoty:
                            if y in shipy:
                                remShotList.append(shot)
                                remHealthList.append(self.find_withtag("health" + str(self.health)))

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
            self.delete(item.id)

    def remAlien(self, elements):
        for item in elements:
            del self.alienList[self.alienList.index(item)]
            self.delete(item.id)
            self.score += 1
            self.itemconfigure(self.find_withtag("score"), text=self.score)

    def remHealth(self, elements):
        for item in elements:
            self.delete(item)
            self.health -= 1

    def doMove(self):
        for alien in self.alienList:
            self.move(alien.id, alien.movex, alien.movey)

        for shot in self.shotList:
            self.move(shot.id, shot.movex, shot.movey)

        bg1y = self.coords(self.find_withtag("bg1"))[1]
        bg2y = self.coords(self.find_withtag("bg2"))[1]

        if bg1y >= HEIGHT:
            self.move(self.find_withtag("bg1"), 0, -1550)
        else:
            self.move(self.find_withtag("bg1"), 0, 2)

        if bg2y >= HEIGHT:
            self.move(self.find_withtag("bg2"), 0, -1550)
        else:
            self.move(self.find_withtag("bg2"), 0, 2)

    def doShoot(self):
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

        rand = randint(1, 100 / self.level * 1.5)
        if rand == 1:
            if len(self.alienList) > 0:
                randAlien = self.alienList[randint(0, len(self.alienList) - 1)]
                shotPosx = self.coords(randAlien.id)[0] + (randAlien.sizex / 2) - 1
                shotPosy = self.coords(randAlien.id)[1] + randAlien.sizey
                self.shotList.append(Shot(shotPosx, 2, 4, 0, 4, self.create_rectangle(shotPosx, shotPosy, shotPosx + 2, shotPosy + 4, width=1, tag="alienShot", fill="red")))

    def moveRight(self, e):
        if self.coords(self.spaceship)[0] + 55 <= WIDTH:
            self.move(self.spaceship, 5, 0)

    def moveLeft(self, e):
        if self.coords(self.spaceship)[0] - 5 >= 0:
            self.move(self.spaceship, -5, 0)

    def shoot(self, e):
        if self.shootCooldown == 0:
            shotPos = self.coords(self.spaceship)[0] + SHIPSIZE / 2
            self.shotList.append(Shot(shotPos, 4, 10, 0, -20, self.create_rectangle(shotPos - 2, HEIGHT - SHIPSIZE, shotPos + 2, HEIGHT - SHIPSIZE - 10, width=0, fill="blue", tag="SpaceShipShot")))
            self.shootCooldown = 50

    def checkHealth(self):
        if not self.health > 0:
            self.create_rectangle(BORDER, HEIGHT / 2 - (BORDER * 3), WIDTH - BORDER, HEIGHT / 2 + BORDER, fill="white", tag="gameOverBg", width=0)
            self.create_text(WIDTH / 2, HEIGHT / 2 - (BORDER * 2), text="Game Over", font=tkFont.Font(size="30"), tag="gameOverText")
            self.create_text(WIDTH / 2, HEIGHT / 2, text="Score: " + str(self.score), font=tkFont.Font(size="70"), tag="finalScore")
            self.unbind_all("<a>")
            self.unbind_all("<d>")
            self.unbind_all("<space>")
        else:
            self.timer = self.after(DELAY, self.onTimer)

    def spawnAliens(self):
        if self.spawnDelay == 0:
            self.spawnDelay = 35
            if self.alienSpawnCount > 0:
                self.alienList.append(Alien(44, 32, 2, 0, self.create_image(-40, MENUBARSIZE + MENUGAP, image=self.alienGreen, tag="alien", anchor="nw")))
                self.alienSpawnCount -= 1

            if self.alienSpawnCount == 0 and len(self.find_withtag("alien")) == 0:
                self.level += 1
                if self.health < 5:
                    self.health += 1
                    self.menu.append(self.create_image(WIDTH - (25 * self.health), 6, image=self.healthimg, tag="health" + str(self.health), anchor="nw"))
                self.itemconfigure(self.find_withtag("level"), text=self.level)
                self.alienSpawnCount = (self.level * 6)
        else:
            self.spawnDelay -= 1

    # Timer method, always gets called again after DELAY from checkHealth method
    # until the game has finished
    def onTimer(self):
        self.checkHealth()
        self.checkCollision()
        self.doMove()
        self.doShoot()
        self.spawnAliens()


# Main class of game. Creates new canvas from class Board
class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        Board()
        self.pack()


# Function that gets called first on run. Creates a new Game instance
def main():
    root = Tk()
    root.title("Space Invaders")
    Game()
    root.mainloop()

# Executes the main method
if __name__ == '__main__':
    main()
