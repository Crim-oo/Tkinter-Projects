import tkinter
from tkinter import *
from PIL import Image, ImageTk
import time
import random

HEIGHT = 500
WIDTH = 700
MESSAGE = "To play, use the arrow keys to move the snake and eat the apple"

root = Tk()
root.title("Snake")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
canvas = Canvas(root, bg="#bcd4de", width=500, height=500)
canvas.pack(side=LEFT)
side = Canvas(root, width=200, height=500)
resetButton = Button(side, text="Reset", font=("courier", 15, "bold"), bd=4)
side.pack(side=RIGHT)
root.update()
resetButtonWindow = side.create_window(side.winfo_width() / 2, (side.winfo_height() - side.winfo_height() / 5),
                                       window=resetButton, width=100)
scoreTxt = side.create_text(side.winfo_width() / 2, side.winfo_height() / 5, font=("courier", 15, "bold"))
instructionsTxt = side.create_text(side.winfo_width() / 2, side.winfo_height() / 2, text=MESSAGE,
                                   font=("courier", 15, "bold"), width=200)


class Snake:
    def __init__(self, master):
        self.master = master
        self.master.update()
        self.blockSize = 20
        self.snakePos = [(100, 100)]
        self.head = self.snakePos[0]
        self.score = 0
        self.direction = "Down"
        self.load_assets()
        self.drawSnake()

        self.isRunning = True
        self.foodAlive = False

        self.master.bind_all("<KeyPress>", self.onKeyPress)
        self.gameOverTxt = self.master.create_text(self.master.winfo_width() / 2, self.master.winfo_height() / 2,
                                                   font=("courier", 15, "bold"))

    def runGame(self):
        self.move()
        self.spawnFood()
        self.checkCollision()
        self.checkFoodCollisions()

    def load_assets(self):
        try:
            self.snakeBodyImg = Image.open("./assets/snake.png")
            self.snakeBody = ImageTk.PhotoImage(self.snakeBodyImg)
            self.foodImg = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.foodImg)
        except IOError as error:
            print('Caught this error: ' + repr(error))
            root.destroy()
            raise

    def onKeyPress(self, e):
        direction = e.keysym

        allDirections = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if direction in allDirections and {direction, self.direction} not in opposites:
            self.direction = direction

    def drawSnake(self):
        for pos in self.snakePos:
            self.master.create_image(pos[0], pos[1], image=self.snakeBody, tag="snake")

    def move(self):
        if self.direction == "Right":
            self.head = (self.head[0] + 5, self.head[1])
        elif self.direction == "Left":
            self.head = (self.head[0] - 5, self.head[1])
        elif self.direction == "Up":
            self.head = (self.head[0], self.head[1] - 5)
        elif self.direction == "Down":
            self.head = (self.head[0], self.head[1] + 5)

        self.snakePos = [self.head] + self.snakePos[:-1]
        for idx, pos in zip(self.master.find_withtag("snake"), self.snakePos):
            self.master.coords(idx, pos)

    def checkFoodCollisions(self):
        if self.foodPos[0] - 20 <= self.head[0] <= self.foodPos[0] + 20 and self.foodPos[1] - 20 <= self.head[1] <= \
                self.foodPos[1] + 20:
            self.score += 1
            self.master.delete(self.master.find_withtag("food"))
            self.snakePos.append(self.snakePos[-1])
            self.master.create_image(self.snakePos[-1], image=self.snakeBody, tag="snake")
            self.foodAlive = False

    def checkCollision(self):
        if self.head in self.snakePos[1:] \
                or self.head[0] in (0, self.master.winfo_width() - 4) \
                or self.head[1] in (0, self.master.winfo_height()):
            self.isRunning = False

    def spawnFood(self):
        if not self.foodAlive:
            posx = random.randint(20, self.master.winfo_width()-20)
            posy = random.randint(20, self.master.winfo_height()-20)
            self.foodPos = (posx, posy)
            self.foodAlive = True
            self.master.create_image(posx, posy, image=self.food, tag="food")

    def reset(self):
        self.master.delete(tkinter.ALL)
        self.gameOverTxt = self.master.create_text(self.master.winfo_width() / 2, self.master.winfo_height() / 2,
                                                   font=("courier", 15, "bold"))
        self.snakePos = [(100, 100)]
        self.head = self.snakePos[0]
        self.score = 0
        self.direction = "Down"
        self.isRunning = True
        self.foodAlive = False
        self.drawSnake()
        self.spawnFood()


snake = Snake(canvas)
resetButton.config(command=snake.reset)

while True:
    while snake.isRunning:
        snake.runGame()
        side.itemconfigure(scoreTxt, text=f"Score: {snake.score}")
        root.update()
        time.sleep(0.01)
    snake.master.itemconfigure(snake.gameOverTxt, text="Game Over !")
    root.update()

root.mainloop()
