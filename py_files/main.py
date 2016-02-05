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
    # Initialize the info screen
    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="white", highlightthickness=0)
        self.initInfoScreen()
        self.pack()

    # Shows an info text about the level system before game starts
    def initInfoScreen(self):
        self.infoList = []
        self.titleFont = tkFont.Font(size="60")
        self.smallTitleFont = tkFont.Font(size="40")
        self.listHeaderFont = tkFont.Font(size="25")
        self.listSmallHeaderFont = tkFont.Font(size="21")
        self.listFont = tkFont.Font(size="18")
        self.startGameFont = tkFont.Font(size="30")
        self.infoList.append(self.create_rectangle(0, 0, WIDTH, HEIGHT, width=0, fill="grey", tag="infoBg"))
        self.infoList.append(self.create_text(WIDTH / 2, BORDER, text="Space Invaders", font=self.titleFont))
        self.infoList.append(self.create_text(WIDTH / 2, BORDER * 3, text="Info about Levels:", font=self.smallTitleFont))
        self.infoList.append(self.create_text(120, BORDER * 4, text="For each finished Level:", font=self.listHeaderFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 250, text="- The amount of aliens will double", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 280, text="- The aliens will shoot more", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 310, text="- You will get 1 extra life", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(120, 360, text="And one of the following:", font=self.listSmallHeaderFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 400, text="- You will be able to shoot faster", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 430, text="- Your shot cooldown will get shorter", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 460, text="- You will get 1 extra life", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 490, text="- You get some free score points", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(WIDTH / 2, HEIGHT - BORDER * 2, text="Press <space> to start the game", font=self.startGameFont))
        self.bind_all("<space>", self.startGame)

    # Gets called by user pressing space on info screen. Initializes the game
    def startGame(self, arg1):
        self.unbind_all("<space>")
        for item in self.infoList:
            self.delete(item)
        self.initGame()

    # Init vars for the game and bind the keys.
    # Calls the initObj function to init all objects to the board
    def initGame(self):
        self.score = 0
        self.level = 1
        self.health = 3
        self.xhealth = 0
        self.alienSpawnCount = 1
        self.spawnDelay = 30
        self.shootCooldown = 0
        self.extraCooldown = 0
        self.extraShotSpeed = 0
        self.bind_all("<a>", self.moveLeft)
        self.bind_all("<d>", self.moveRight)
        self.bind_all("<space>", self.shoot)
        self.initObj()
        self.after(DELAY, self.onTimer)

    # Adds all the objects to the board, including menu bar and spaceship.
    def initObj(self):
        # Import all the images and save them to a reference var
        healthimg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/heart.png")
        xhealthimg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/xheart.png")
        empty_heartimg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/heart_empty.png")
        alienGreen = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/green.png")
        shipimg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/space_ship.png")
        bgimg = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/bg.png")
        self.healthimg = healthimg
        self.xhealthimg = xhealthimg
        self.empty_heartimg = empty_heartimg
        self.alienGreen = alienGreen
        self.shipimg = shipimg
        self.bgimg = bgimg

        # Create background images
        self.bg = []
        self.bg.append(self.create_image(0, -50, image=self.bgimg, anchor="nw", tag="bg1"))
        self.bg.append(self.create_image(0, -850, image=self.bgimg, anchor="nw", tag="bg2"))

        # Add menu bar and all of its elements to the board
        self.menu = []
        menuFont = tkFont.Font(size="20", family="Helvetica")

        self.menu.append(self.create_rectangle(0, 0, WIDTH, MENUBARSIZE, width=0, fill="grey", tag="menuBar"))
        self.menu.append(self.create_text(5, 5, text="Score: ", anchor="nw", font=menuFont, tag="scoreLabel"))
        self.menu.append(self.create_text(self.getx(self.find_withtag("scoreLabel")) + 65, 5, text=str(self.score), anchor="nw", font=menuFont, tag="score"))
        self.menu.append(self.create_text(205, 5, text="Level: ", anchor="nw", font=menuFont, tag="levelLabel"))
        self.menu.append(self.create_text(self.getx(self.find_withtag("levelLabel")) + 63, 5, text=str(self.level), anchor="nw", font=menuFont, tag="level"))
        for j in range(5):
            self.menu.append(self.create_image(WIDTH - (25 * (j + 1)), 6, image=self.empty_heartimg, tag="empty_heart", anchor="nw"))
        for i in range(self.health):
            count = i + 1
            self.menu.append(self.create_image(WIDTH - (25 * count), 6, image=self.healthimg, tag="health" + str(count), anchor="nw"))

        # Add spaceship to board and init lists for aliens & shots
        self.spaceship = self.create_image(WIDTH / 2 - SHIPSIZE / 2, HEIGHT - SHIPSIZE - 20, image=self.shipimg, anchor="nw")
        self.alienList = []
        self.shotList = []

    # Check collision between all relevant objects on the field
    def checkCollision(self):
        # Lists for elements that collided. Lists get forwarded to remove methods
        # at the end of checkCollision. This avoids index errors in the object lists
        remShotList = []
        remAlienList = []
        remHealthList = []

        # Check if aliens reached the bottom of the pitch/the spaceship
        if len(self.alienList) > 0:
            if self.gety(self.alienList[0].id) + self.alienList[0].sizey >= self.gety(self.spaceship):
                if len(self.find_withtag("xhealth")) > 0:
                    remHealthList.append(self.find_withtag("xhealth" + str(self.xhealth)))
                else:
                    remHealthList.append(self.find_withtag("health" + str(self.health)))
                remAlienList.append(self.alienList[0])

        # Check if aliens reached the border of the pitch and if so make them go down and turn
        for alien in self.alienList:
            if self.getx(alien.id) == WIDTH - BORDER - alien.sizex or (self.getx(alien.id) == BORDER and self.gety(alien.id) > MENUBARSIZE + MENUGAP + 1):
                if alien.movex >= 2 or alien.movex <= -2:
                    alien.move_down()
                else:
                    alien.move_rev()

            if self.getx(alien.id) == WIDTH - BORDER - 20 or (self.getx(alien.id) == BORDER - 20 and self.gety(alien.id) > MENUBARSIZE + MENUGAP + 1):
                alien.move_down_rev()

        # Check collisions for all the shots currently on the pitch
        for shot in self.shotList:

            # Check if shots any shots reached the end of the pitch.
            # If so, append them to the remList to remove them
            shotx = range(int(self.getx(shot.id)), int(self.getx(shot.id)) + shot.sizex)
            shoty = range(int(self.gety(shot.id)), int(self.gety(shot.id)) + shot.sizey)
            if self.gety(shot.id) <= MENUBARSIZE or self.gety(shot.id) >= HEIGHT:
                remShotList.append(shot)

            # Check for all player shots if they hit an alien.
            # If so, add the alien & the shot to the remList to remove them
            if shot.id not in self.find_withtag("alienShot"):
                for alien in self.alienList:
                    alienx = range(int(self.getx(alien.id)), int(self.getx(alien.id) + alien.sizex + 1))
                    alieny = range(int(self.gety(alien.id)), int(self.gety(alien.id) + alien.sizey + 1))
                    for x in shotx:
                        if x in alienx:
                            for y in shoty:
                                if y in alieny and x in alienx:
                                    remShotList.append(shot)
                                    remAlienList.append(alien)

            # Check for all alien shots if they collide with the spaceship.
            # If so, add the shot and the last heart obj to the remList to remove them
            elif shot.id in self.find_withtag("alienShot"):
                shipx = range(int(self.getx(self.spaceship)), int(self.getx(self.spaceship)) + 50)
                shipy = range(int(self.gety(self.spaceship)), int(self.gety(self.spaceship)) + 50)
                for x in shotx:
                    if x in shipx:
                        for y in shoty:
                            if y in shipy:
                                remShotList.append(shot)
                                if len(self.find_withtag("xhealth1")) > 0:
                                    remHealthList.append(self.find_withtag("xhealth" + str(self.xhealth)))
                                else:
                                    remHealthList.append(self.find_withtag("health" + str(self.health)))

        # If any aliens have collided the remAlien method is called to
        # remove all objs in the remList
        if len(remAlienList) > 0:
            remAlienList = set(remAlienList)
            self.remAlien(remAlienList)

        # If any shots were added to the remList, remShots method is called
        # to remove all the objs in the remList
        if len(remShotList) > 0:
            remShotList = set(remShotList)
            self.remShots(remShotList)

        # If any health objs werde added to the remList, remHealth method is
        # called to remove them
        if len(remHealthList) > 0:
            remHealthList = set(remHealthList)
            self.remHealth(remHealthList)

    # Method to remove all the shots in remList
    def remShots(self, remList):
        for item in remList:
            del self.shotList[self.shotList.index(item)]
            self.delete(item.id)

    # Method to remove all the aliens in remList
    # For each removed alien the score gets added up and updated on the board
    def remAlien(self, remList):
        for item in remList:
            del self.alienList[self.alienList.index(item)]
            self.delete(item.id)
            self.score += 1
            self.itemconfigure(self.find_withtag("score"), text=self.score)

    # Method to remove all the health in remList
    def remHealth(self, remList):
        for item in remList:
            self.delete(item)
            self.health -= 1

    # Method called by the timer. Moves all the moving objs on the pitch around
    def doMove(self):
        # Move all the aliens on the pitch according to their movement directions
        for alien in self.alienList:
            self.move(alien.id, alien.movex, alien.movey)

        # Move all the shots on the pitch according to their movement directions
        for shot in self.shotList:
            self.move(shot.id, shot.movex, shot.movey)

        # Move both bg images downwards and check if they reached the bottom.
        # If they reached the bottom, set them up again.
        for bg in self.bg:
            if self.gety(bg) >= HEIGHT:
                self.move(bg, 0, -1550)
            else:
                self.move(bg, 0, 1)

        # Reduce shoot cooldown for spaceship by every tick
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

    # Do all the shooting for the aliens
    def doShoot(self):
        # Get ranom number to decide if aliens shoot in this tick.
        # The higher the level the smaller the range for the random number
        rand = randint(1, int(100 / self.level * 1.5))
        if rand == 1:
            if len(self.alienList) > 0:
                randAlien = self.alienList[randint(0, len(self.alienList) - 1)]
                shotPosx = self.getx(randAlien.id) + (randAlien.sizex / 2) - 2
                shotPosy = self.gety(randAlien.id) + randAlien.sizey
                self.shotList.append(Shot(shotPosx, 4, 4, 0, 4, self.create_rectangle(shotPosx, shotPosy, shotPosx + 4, shotPosy + 4, width=1, tag="alienShot", fill="red")))

    # Event method for player movement with the spaceship
    def moveRight(self, e):
        if self.getx(self.spaceship) + 55 <= WIDTH:
            self.move(self.spaceship, 5, 0)

    # Event method for player movement with the spaceship
    def moveLeft(self, e):
        if self.getx(self.spaceship) - 5 >= 0:
            self.move(self.spaceship, -5, 0)

    # Event method for player shooting with the spaceship
    def shoot(self, e):
        if self.shootCooldown == 0:
            shotPos = self.getx(self.spaceship) + SHIPSIZE / 2
            self.shotList.append(Shot(shotPos, 4, 10, 0, -20 + self.extraShotSpeed, self.create_rectangle(shotPos - 2, HEIGHT - SHIPSIZE, shotPos + 2, HEIGHT - SHIPSIZE - 10, width=0, fill="blue", tag="SpaceShipShot")))
            self.shootCooldown = 50 + self.extraCooldown

    # Method to easily get the x cords of an obj
    def getx(self, id):
        return self.coords(id)[0]

    # Method to easily get the y cords of an obj
    def gety(self, id):
        return self.coords(id)[1]

    # Method called by the timer. Checks if the player has health left, and if
    # so calls the onTimer method again after DELAY.
    # If the player has no health left, the game ends and the game over screen appears.
    def checkHealth(self):
        if not self.health > 0:
            self.gameoverfont = tkFont.Font(size="70")
            self.create_rectangle(BORDER, HEIGHT / 2 - (BORDER * 3), WIDTH - BORDER, HEIGHT / 2 + BORDER, fill="white", tag="gameOverBg", width=0)
            self.create_text(WIDTH / 2, HEIGHT / 2 - (BORDER * 2), text="Game Over", font=self.gameoverfont, tag="gameOverText")
            self.create_text(WIDTH / 2, HEIGHT / 2, text="Score: " + str(self.score), font=self.gameoverfont, tag="finalScore")
            self.unbind_all("<a>")
            self.unbind_all("<d>")
            self.unbind_all("<space>")
        else:
            self.doShoot()
            self.timer = self.after(DELAY, self.onTimer)

    def popUpText(self, text):
        self.popUpList = []
        self.popUpFont = tkFont.Font(size="50")
        self.popUpList.append(self.create_rectangle(BORDER, HEIGHT / 2 - BORDER, WIDTH - BORDER, HEIGHT / 2 + BORDER, fill="white", width=0, tag="popUp"))
        self.popUpList.append(self.create_text(WIDTH / 2, HEIGHT / 2, text=text, font=self.popUpFont, tag="popUp"))
        self.after(1500, self.remPopUp)

    def remPopUp(self):
        for item in self.find_withtag("popUp"):
            self.delete(item)

    def randLevelUpEffect(self):
        randNum = randint(1, 4)
        popText = ""
        if randNum == 1:
            if self.extraCooldown > -40:
                self.extraCooldown -= 15
                popText = "Shorter Cooldown"
            else:
                self.randLevelUpEffect()
        elif randNum == 2:
            if self.extraShotSpeed < -10:
                self.extraShotSpeed -= 5
                popText = "Faster Shots"
            else:
                self.randLevelUpEffect()
        elif randNum == 3:
            if self.xhealth < 4:
                self.xhealth += 1
                self.menu.append(self.create_image(WIDTH - (25 * 5 + (25 * self.xhealth)), 6, image=self.xhealthimg, tag="xhealth" + str(self.xhealth), anchor="nw"))
                popText = "Extra Life"
            else:
                self.randLevelUpEffect()
        elif randNum == 4:
            self.score += 10 * self.level
            self.itemconfigure(self.find_withtag("score"), text=self.score)
            popText = "Free Points"
        if not popText == "":
            self.popUpText(popText)

    # Method to add new aliens to the board.
    def spawnAliens(self):
        # Each tick the spawnDelay gets set a bit lower, if it reaches 0, a new alien spawns
        if self.spawnDelay == 0:
            self.spawnDelay = 35
            if self.alienSpawnCount > 0:
                self.alienList.append(Alien(44, 32, 2, 0, self.create_image(-40, MENUBARSIZE + MENUGAP, image=self.alienGreen, tag="alien", anchor="nw")))
                self.alienSpawnCount -= 1

            # If there are no aliens left and all the spawned aliens have already
            # been removed/destroyed then the next level gets initialized.
            if self.alienSpawnCount == 0 and len(self.find_withtag("alien")) == 0:
                self.level += 1
                if self.health < 5:
                    self.health += 1
                    self.menu.append(self.create_image(WIDTH - (25 * self.health), 6, image=self.healthimg, tag="health" + str(self.health), anchor="nw"))
                self.itemconfigure(self.find_withtag("level"), text=self.level)
                self.alienSpawnCount = (self.level * 1)
                self.randLevelUpEffect()
        else:
            self.spawnDelay -= 1

    # Timer method, always gets called again after DELAY from checkHealth method
    # until the game has finished
    def onTimer(self):
        self.checkHealth()
        self.checkCollision()
        self.doMove()
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
