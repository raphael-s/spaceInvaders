import os

from Tkinter import Canvas, Frame, Tk

from random import randint

from PIL import ImageTk

from alien import Alien

from bomber import Bomber

from shot import Shot

from drop import Drop

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
        green_big_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/green_big.png")
        self.green_big_img = green_big_img
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
        self.infoList.append(self.create_text(120, 360, text="And you will get one of the following:", font=self.listSmallHeaderFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 400, text="- 1 extra Life", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 430, text="- Some free score points", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(WIDTH / 2, HEIGHT - BORDER * 2, text="Press <space> to start the game", font=self.startGameFont))
        self.infoList.append(self.create_image(WIDTH / 2, 540, image=self.green_big_img))
        self.bind_all("<space>", self.startGame)

    # Gets called by user pressing space on info screen. Initializes the game
    def startGame(self, arg1):
        self.unbind_all("<space>")
        self.delete("all")
        self.initGame()

    # Init vars for the game and bind the keys.
    # Calls the initObj function to init all objects to the board
    def initGame(self):
        self.score = 0
        self.level = 1
        self.health = 3
        self.xhealth = 0
        self.alienSpawnCount = 12
        self.spawnDelay = 30
        self.bomberRespawnDelay = 200
        self.shootCooldown = 0
        self.bomberCooldown = 0
        self.accHits = 0
        self.accShots = 0
        self.bind_all("<a>", self.moveLeft)
        self.bind_all("<d>", self.moveRight)
        self.bind_all("<space>", self.shoot)
        self.initObj()
        self.after(DELAY, self.onTimer)

    # Adds all the objects to the board, including menu bar and spaceship.
    def initObj(self):
        # Import all the images and save them to a reference var
        health_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/heart.png")
        xhealth_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/xheart.png")
        empty_heart_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/heart_empty.png")
        alien_green_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/green.png")
        alien_green_des_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/green_destroy.png")
        ship_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/space_ship.png")
        ship_hit_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/space_ship_hit.png")
        ship_des_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/space_ship_des.png")
        bg_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/bg.png")
        drop_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/crate.png")
        bomber_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/bomber.png")
        bomber_shot_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/bombershot.png")
        bomber_des_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/bomber_destroy.png")
        explosion_img = ImageTk.PhotoImage(file=ROOT_DIR + "/gfx/explosion.png")
        self.health_img = health_img
        self.xhealth_img = xhealth_img
        self.empty_heart_img = empty_heart_img
        self.alien_green_img = alien_green_img
        self.alien_green_des_img = alien_green_des_img
        self.ship_img = ship_img
        self.ship_hit_img = ship_hit_img
        self.ship_des_img = ship_des_img
        self.bg_img = bg_img
        self.drop_img = drop_img
        self.bomber_img = bomber_img
        self.bomber_shot_img = bomber_shot_img
        self.bomber_des_img = bomber_des_img
        self.explosion_img = explosion_img

        # Create background images
        self.bg = []
        self.bg.append(self.create_image(0, -50, image=self.bg_img, anchor="nw", tag="bg1"))
        self.bg.append(self.create_image(0, -850, image=self.bg_img, anchor="nw", tag="bg2"))

        # Add menu bar and all of its elements to the board
        self.menu = []
        self.menuFont = tkFont.Font(size="20", family="Helvetica")

        # Display the menu bar and add all the items to the menu list
        self.menu.append(self.create_rectangle(0, 0, WIDTH, MENUBARSIZE, width=0, fill="grey", tag="menuBar"))
        self.menu.append(self.create_text(5, 5, text="Score: ", anchor="nw", font=self.menuFont, tag="scoreLabel"))
        self.menu.append(self.create_text(self.getx(self.find_withtag("scoreLabel")) + 65, 5, text=str(self.score), anchor="nw", font=self.menuFont, tag="score"))
        self.menu.append(self.create_text(205, 5, text="Level: ", anchor="nw", font=self.menuFont, tag="levelLabel"))
        self.menu.append(self.create_text(self.getx(self.find_withtag("levelLabel")) + 63, 5, text=str(self.level), anchor="nw", font=self.menuFont, tag="level"))
        for j in range(5):
            self.menu.append(self.create_image(WIDTH - (25 * (j + 1)), 6, image=self.empty_heart_img, tag="empty_heart", anchor="nw"))
        for i in range(self.health):
            count = i + 1
            self.menu.append(self.create_image(WIDTH - (25 * count), 6, image=self.health_img, tag="health" + str(count), anchor="nw"))

        # Add spaceship to board and init lists for aliens & shots
        self.spaceship = self.create_image(WIDTH / 2 - SHIPSIZE / 2, HEIGHT - SHIPSIZE - 20, image=self.ship_img, anchor="nw")
        self.alienList = []
        self.shotList = []
        self.dropList = []
        self.bomber = ""

    # Check collision between all relevant objects on the field
    def checkCollision(self):
        # Lists for elements that collided. Lists get forwarded to remove methods
        # at the end of checkCollision. This avoids index errors in the object lists.
        # Lists are used because one obj can get hit multiple times in a tick,
        # by using the set method of lists duplicates can be removed.
        remShotList = []
        remAlienList = []
        remHealthList = []
        remxHealthList = []
        remDropList = []
        remBomberList = []

        # Check if drop has reached the bottom of the pitch.
        # Also check if the drop has collided with the ship
        for drop in self.dropList:
            if self.gety(drop.id) >= HEIGHT - drop.sizey - 20:
                drop.movey = 0
            spacex = range(int(self.getx(self.spaceship)), int(self.getx(self.spaceship) + SHIPSIZE))
            for dropx in range(int(self.getx(drop.id)), int(self.getx(drop.id) + drop.sizex)):
                if dropx in spacex and drop.movey == 0:
                    remDropList.append(drop)
                elif dropx in spacex:
                    for dropy in range(int(self.gety(drop.id)), int(self.gety(drop.id) + drop.sizey)):
                        if dropy >= self.gety(self.spaceship):
                            remDropList.append(drop)

        # Check if aliens reached the bottom of the pitch/the spaceship
        if len(self.alienList) > 0:
            if self.gety(self.alienList[0].id) + self.alienList[0].sizey >= self.gety(self.spaceship):
                if self.xhealth > 0:
                    remxHealthList.append(self.find_withtag("xhealth" + str(self.xhealth)))
                else:
                    remHealthList.append(self.find_withtag("health" + str(self.health)))
                remAlienList.append(self.alienList[0])

        # Check collisions for all the shots currently on the pitch
        for shot in self.shotList:
            if shot.id in self.find_withtag("bomberShot"):
                if self.gety(shot.id) >= HEIGHT - 20 - shot.sizey:
                    remShotList.append(shot)
                    self.create_image(self.getx(shot.id) + (shot.sizex / 2), self.gety(shot.id) - 10, image=self.explosion_img, tag="explosion")
                    self.after(300, self.remExplosion)
                    for shipy in range(int(self.getx(self.spaceship)), int(self.getx(self.spaceship) + SHIPSIZE)):
                        if shipy in range(int(self.getx(shot.id) - 50), int(self.getx(shot.id) + 50)):
                            if self.xhealth > 0:
                                remxHealthList.append(self.find_withtag("xhealth" + str(self.xhealth)))
                            else:
                                remHealthList.append(self.find_withtag("health" + str(self.health)))

            # Check if any shots reached the end of the pitch.
            # If so, append them to the remList to remove them
            shotx = range(int(self.getx(shot.id)), int(self.getx(shot.id)) + shot.sizex)
            shoty = range(int(self.gety(shot.id)), int(self.gety(shot.id)) + shot.sizey)
            if self.gety(shot.id) <= MENUBARSIZE or self.gety(shot.id) >= HEIGHT:
                remShotList.append(shot)

            # Check for all player shots if they hit an alien.
            # If so, add the alien & the shot to the remList to remove them
            if shot.id not in self.find_withtag("alienShot") and shot.id not in self.find_withtag("bomberShot"):
                # Check if shots collided with the bomber alien
                if len(self.find_withtag("bomber")) > 0:
                    bomberx = range(int(self.getx(self.bomber.id)), int(self.getx(self.bomber.id) + self.bomber.sizex))
                    bombery = range(int(self.gety(self.bomber.id)), int(self.gety(self.bomber.id) + self.bomber.sizey))
                    for y in shoty:
                        if y in bombery:
                            for x in shotx:
                                if x in bomberx:
                                    remShotList.append(shot)
                                    remBomberList.append(self.bomber)

                # Check if the shots collided with the green aliens
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
                                if self.xhealth > 0:
                                    remxHealthList.append(self.find_withtag("xhealth" + str(self.xhealth)))
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

        # If any health objs were added to the remList, remHealth method is
        # called to remove them
        if len(remHealthList) > 0:
            remHealthList = set(remHealthList)
            self.remHealth(remHealthList)

        # If any extra health objs were added to the remList, remxHealth method
        # is called to remove them
        if len(remxHealthList) > 0:
            remxHealthList = set(remxHealthList)
            self.remxHealth(remxHealthList)

        # If any Drops collided with the player, they get removed from the pitch
        # by calling the remDrop method
        if len(remDropList) > 0:
            remDropList = set(remDropList)
            self.remDrop(remDropList)

        # If the bomber was hitted, the obj is added to the remList and then
        # removed by calling remBomber
        if len(remBomberList) > 0:
            remBomberList = set(remBomberList)
            self.remBomber(remBomberList)

    # Method to remove all the shots in remList
    def remShots(self, remList):
        for item in remList:
            del self.shotList[self.shotList.index(item)]
            self.delete(item.id)

    # If the bomber shot hits the ground the explosion image is displayed
    def bomberShotExplode(self, shot):
        self.create_image(self.getx(shot.id) + (shot.sizex / 2), self.gety(shot.id) - 10, image=self.explosion_img, tag="explosion")
        self.after(300, self.remExplosion)
        for shipy in range(int(self.getx(self.spaceship)), int(self.getx(self.spaceship) + SHIPSIZE)):
            if shipy in range(int(self.getx(shot.id) - 50), int(self.getx(shot.id) + 50)):
                print "HIT"

    # Method to remove the explosion image from the pitch
    def remExplosion(self):
        for item in self.find_withtag("explosion"):
            self.delete(item)

    # Method to remove all the aliens in remList
    # For each removed alien the score gets added up and updated on the board
    # Adds a destroy image to the canvas removes it by a delayed call to remDesImg
    def remAlien(self, remList):
        for item in remList:
            self.alienScorePopup("+20", item)
            self.create_image(self.getx(item.id), self.gety(item.id), image=self.alien_green_des_img, anchor="nw", tag="desImg")
            self.after(100, self.remDesImg)
            del self.alienList[self.alienList.index(item)]
            self.delete(item.id)
            self.score += 20
            self.accHits += 1
            self.itemconfigure(self.find_withtag("score"), text=self.score)

    # Method to remove all the images of destroyed aliens on the pitch
    def remDesImg(self):
        for item in self.find_withtag("desImg"):
            self.delete(item)

    # Method to remove all the health in remList
    # Calls method to let the ship "blink" red
    def remHealth(self, remList):
        for item in remList:
            self.delete(item)
            self.health -= 1
            if self.health > 0:
                self.repeatHit = True
                self.shipHit()
            else:
                self.itemconfigure(self.spaceship, image=self.ship_des_img)

    # Method gets called if ship is hit. Sets a red ship img that is
    # then removed again by remShipHit
    def shipHit(self):
        self.itemconfigure(self.spaceship, image=self.ship_hit_img)
        self.after(300, self.remShipHit)

    # Removes the red ship image and sets it to the blue one again.
    # Gets called 2 times, the first time it calls shipHit again to make the ship "blink"
    def remShipHit(self):
        self.itemconfigure(self.spaceship, image=self.ship_img)
        if self.repeatHit:
            self.repeatHit = False
            self.after(300, self.shipHit)

    # Method to remove the extra health. Does not affect health var
    def remxHealth(self, remList):
        for item in remList:
            self.delete(item)
            self.xhealth -= 1

    # Method to remove the drops that collided from the pitch
    def remDrop(self, remList):
        for item in remList:
            del self.dropList[self.dropList.index(item)]
            self.delete(item.id)
            self.randUpgrade()

    # Method to remove the bomber from the pitch if he has been hitted
    def remBomber(self, remList):
        for item in remList:
            self.alienScorePopup("+50", item)
            self.create_image(self.getx(item.id), self.gety(item.id), image=self.bomber_des_img, anchor="nw", tag="desBombImg")
            self.after(100, self.remDesBombImg)
            self.bomber = ""
            self.delete(item.id)
            self.score += 50
            self.accHits += 1
            self.itemconfigure(self.find_withtag("score"), text=self.score)
            self.bomberRespawnDelay = 1000

    # Method to remove the destroy image of the bomber, gets called after
    # a set delay form remBomber
    def remDesBombImg(self):
        for item in self.find_withtag("desBombImg"):
            self.delete(item)

    # Method called by the timer. Moves all the moving objs on the pitch around
    def doMove(self):
        # Check if aliens reached the border of the pitch and if so make them go down and turn
        for alien in self.alienList:
            if self.getx(alien.id) == WIDTH - BORDER - alien.sizex + 2 or (self.getx(alien.id) == BORDER + 2 and self.gety(alien.id) > MENUBARSIZE + MENUGAP + 1):
                if alien.movex == 4 or alien.movex == -4:
                    alien.move_down()
                else:
                    alien.move_rev()

            if self.getx(alien.id) == WIDTH - BORDER - 20 or (self.getx(alien.id) == BORDER - 20 and self.gety(alien.id) > MENUBARSIZE + MENUGAP + 1):
                alien.move_down_rev()

        # Check if the bomber has reached the end of the pitch, if so
        # make him move the other way
        if len(self.find_withtag("bomber")) > 0:
            if self.getx(self.bomber.id) == WIDTH - BORDER - self.bomber.sizex or (self.getx(self.bomber.id) == BORDER and self.bomber.movex < 0):
                self.bomber.move_rev()

            self.move(self.bomber.id, self.bomber.movex, self.bomber.movey)

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

        # Moves the drop crate downwards
        for drop in self.dropList:
            self.move(drop.id, drop.movex, drop.movey)

        # Reduce shoot cooldown for spaceship by every tick
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

    # Do all the shooting for the aliens
    def doShoot(self):
        # Get ranom number to decide if aliens shoot in this tick.
        # The higher the level the smaller the range for the random number
        rand = randint(1, int(100 / (self.level * 2)))
        # if randint is one, a random alien shoots
        if rand == 1:
            if len(self.alienList) > 0:
                randAlien = self.alienList[randint(0, len(self.alienList) - 1)]
                shotPosx = self.getx(randAlien.id) + (randAlien.sizex / 2) - 3
                shotPosy = self.gety(randAlien.id) + randAlien.sizey
                self.shotList.append(Shot(7, 6, 0, 4, self.create_rectangle(shotPosx, shotPosy, shotPosx + 6, shotPosy + 7, width=1, tag="alienShot", fill="red")))
        # if randint is two, the bomber shoots, but only if there is no shot
        # on the pitch yet
        elif rand == 2 and len(self.find_withtag("bomber")) > 0 and len(self.find_withtag("bomberShot")) <= 1 and self.getx(self.bomber.id) > BORDER and self.bomberCooldown == 0:
            self.shotList.append(Shot(12, 12, 0, 3, self.create_image(self.getx(self.bomber.id) + (self.bomber.sizex / 2), self.gety(self.bomber.id) + self.bomber.sizey, image=self.bomber_shot_img, tag="bomberShot", anchor="nw")))
            self.bomberCooldown = 100
        elif self.bomberCooldown > 0:
            self.bomberCooldown -= 1

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
            self.shotList.append(Shot(4, 10, 0, -20, self.create_rectangle(shotPos - 2, HEIGHT - SHIPSIZE, shotPos + 2, HEIGHT - SHIPSIZE - 10, width=0, fill="blue", tag="SpaceShipShot")))
            self.shootCooldown = 25
            self.accShots += 1

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
            self.gameoversmallfont = tkFont.Font(size="40")
            self.restartfont = tkFont.Font(size="35")
            self.create_rectangle(BORDER, HEIGHT / 2 - (BORDER * 3), WIDTH - BORDER, HEIGHT / 2 + (BORDER * 2), fill="white", tag="gameOverBg", width=0)
            self.create_text(WIDTH / 2, HEIGHT / 2 - (BORDER * 2), text="Game Over", font=self.gameoverfont, tag="gameOverText")
            self.create_text(WIDTH / 2, HEIGHT / 2, text="Score: " + str(self.score), font=self.gameoversmallfont, tag="finalScore")
            self.create_text(WIDTH / 2, HEIGHT / 2 + BORDER, text="Accuracy: " + str(self.getAccuracy()) + "%", font=self.gameoversmallfont, tag="accuracy")
            self.create_rectangle(BORDER, HEIGHT - (BORDER * 2), WIDTH - BORDER, HEIGHT - BORDER, fill="white", tag="startNewGame", width=0)
            self.create_text(WIDTH / 2, HEIGHT - 75, text="Press <space> to restart", font=self.restartfont, tag="restartGameText")
            self.unbind_all("<a>")
            self.unbind_all("<d>")
            self.unbind_all("<space>")
            self.bind_all("<space>", self.startGame)
        else:
            self.doShoot()
            self.timer = self.after(DELAY, self.onTimer)

    def getAccuracy(self):
        if self.accShots > 0:
            return int(100 * float(self.accHits)/float(self.accShots))
        else:
            return "0"

    # Method that creates a popup display that is then removed again by
    # calling remPopUp.
    # Method is used to display level ups
    def popUpText(self, text):
        self.popUpList = []
        self.popUpFont = tkFont.Font(size="50")
        self.popUpList.append(self.create_rectangle(BORDER, HEIGHT / 2 - BORDER, WIDTH - BORDER, HEIGHT / 2 + BORDER, fill="white", width=0, tag="popUp"))
        self.popUpList.append(self.create_text(WIDTH / 2, HEIGHT / 2, text=text, font=self.popUpFont, tag="popUp"))
        self.after(1500, self.remPopUp)

    # Method that removes the popup text
    def remPopUp(self):
        for item in self.find_withtag("popUp"):
            self.delete(item)

    # Creates a popup dialog box at the position of an alien.
    # Used to show +score points
    def alienScorePopup(self, text, alien):
        self.create_rectangle(self.getx(alien.id) + alien.sizex + 5, self.gety(alien.id) - 5, self.getx(alien.id) + alien.sizex + 40, self.gety(alien.id) + 20, fill="white", width=0, tag="scorePopup")
        self.create_text(self.getx(alien.id) + alien.sizex + 10, self.gety(alien.id), text=text, anchor="nw", tag="scorePopup")
        self.after(400, self.remScorePopup)

    # Removes all score popup boxes currently on the pitch
    def remScorePopup(self):
        for item in self.find_withtag("scorePopup"):
            self.delete(item)

    # Method to create a small popup message at the location of the spaceship.
    # Message gets automatically removed by calling remShipPopUp method
    def shipPopUp(self, text):
        self.remShipPopUp()
        self.shipPopUpList = []
        self.shipPopUpFont = tkFont.Font(size="20")
        popx = self.getx(self.spaceship) + SHIPSIZE + 10
        popy = HEIGHT - SHIPSIZE - 40
        self.shipPopUpList.append(self.create_rectangle(popx, popy, popx + 90, popy + 30, fill="white", width=0, tag="shipPopUp"))
        self.shipPopUpList.append(self.create_text(popx + 5, popy + 5, text=text, font=self.shipPopUpFont, tag="shipPopUp", anchor="nw"))
        self.after(1000, self.remShipPopUp)

    # Method to remove the message created by shipPopUp
    def remShipPopUp(self):
        for item in self.find_withtag("shipPopUp"):
            self.delete(item)

    # Method called if the spaceship collides with a crate.
    # Randomly gets the player some score points or an extra life
    def randUpgrade(self):
        randNum = randint(1, 2)
        popText = ""
        if randNum == 1:
            if self.xhealth < 3:
                self.xhealth += 1
                self.menu.append(self.create_image(WIDTH - (25 * 5 + (25 * self.xhealth)), 6, image=self.xhealth_img, tag="xhealth" + str(self.xhealth), anchor="nw"))
                popText = "+1 Life"
            else:
                self.randUpgrade()
        elif randNum == 2:
            self.score += 10 * self.level
            self.itemconfigure(self.find_withtag("score"), text=self.score)
            popText = "++ Score"
        if not popText == "":
            self.shipPopUp(popText)

    # Method to add new aliens to the board.
    def spawnAliens(self):
        # Each tick the spawnDelay gets set a bit lower, if it reaches 0, a new alien spawns
        if self.spawnDelay == 0:
            self.spawnDelay = 20
            if self.alienSpawnCount > 0:
                self.alienList.append(Alien(44, 32, 4, 0, self.create_image(-40, MENUBARSIZE + MENUGAP, image=self.alien_green_img, tag="alien", anchor="nw")))
                self.alienSpawnCount -= 1

            # If there are no aliens left to spawn and all the spawned aliens have already
            # been removed/destroyed then the next level gets initialized.
            if self.alienSpawnCount == 0 and len(self.find_withtag("alien")) == 0:
                self.level += 1
                if self.health < 5:
                    self.health += 1
                    self.menu.append(self.create_image(WIDTH - (25 * self.health), 6, image=self.health_img, tag="health" + str(self.health), anchor="nw"))
                self.itemconfigure(self.find_withtag("level"), text=self.level)
                self.alienSpawnCount = (12 + (self.level * 6))
                self.popUpText("Level " + str(self.level))
        elif self.spawnDelay > 0:
            self.spawnDelay -= 1

        # Spawn bomber after a set delay after destruction of the previuos bomber
        if not len(self.find_withtag("bomber")) > 0 and self.bomberRespawnDelay == 0:
            self.spawnBomber()
        elif self.bomberRespawnDelay > 0:
            self.bomberRespawnDelay -= 1

    # Method to add the bomber to the pitch
    def spawnBomber(self):
        self.bomber = Bomber(64, 28, 1, 0, self.create_image(-64, MENUBARSIZE + 20, image=self.bomber_img, tag="bomber", anchor="nw"))
        self.bomberCooldown = 100

    # Randomly spawns drops
    def spawnDrop(self):
        if randint(1, 2500) == 1:
            randx = randint(10, WIDTH - 30)
            self.dropList.append(Drop(20, 20, 0, 5, self.create_image(randx, MENUBARSIZE, image=self.drop_img, anchor="nw", tag="drop")))

    # Timer method, always gets called again after DELAY from checkHealth method
    # until the game has finished
    def onTimer(self):
        self.checkHealth()
        self.checkCollision()
        self.doMove()
        self.spawnAliens()
        self.spawnDrop()


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
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print ""
        print "Program stopped by KeyboardInterrupt"

# Executes the main method
if __name__ == '__main__':
    main()
