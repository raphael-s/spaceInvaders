from Tkinter import *

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
		self.spaceMove = 0
		self.bind_all("<a>", self.moveLeft)
		self.bind_all("<d>", self.moveRight)
		self.initObj()
		self.after(DELAY, self.onTimer)

	def initObj(self):
		self.spaceship = self.create_rectangle(0, HEIGHT-50, 50, HEIGHT, width=0, fill="green", tag="spaceship")
		self.alienList = []
		self.alienList.append(Alien())

	def checkCollision(self):
		pass

	def doMove(self):
		for alien in alienList:
			alien.x += 5

	def moveRight(self, e):
		self.move(self.spaceship, 5, 0)

	def moveLeft(self, e):
		self.move(self.spaceship, -5, 0)


	def onTimer(self):
		self.alienSpawn += 1
		if (alienSpawn > 100):
			self.alienList.append(Alien())
		self.checkCollision()
		self.doMove()
		self.after(DELAY, self.onTimer)

class Game(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.board = Board()
		self.pack()

class Alien():
	x = 0
	y = 0
	def __init__(self):


def main():

    root = Tk()
    game = Game()
    root.mainloop()  


if __name__ == '__main__':
    main()