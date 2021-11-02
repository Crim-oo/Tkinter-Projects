import tkinter
from tkinter import *
from PIL import Image, ImageTk
from pandas import DataFrame
import time
import random

SIDE_W = 200
WIDTH = 400 + SIDE_W
HEIGHT = 400

root = Tk()
root.title("2048")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
canvas = Canvas(root, width=WIDTH - SIDE_W, height=HEIGHT, highlightthickness=0)
canvas.pack(side=LEFT)
side = Canvas(root, width=SIDE_W, height=HEIGHT, bg="#bcd4de", highlightthickness=0)
resetButton = Button(side, text="Reset", font=("courier", 15, "bold"), bd=4)
side.pack(side=RIGHT)
root.update()
resetButtonWindow = side.create_window(side.winfo_width() / 2, (2 * side.winfo_height() / 3),
                                       window=resetButton, width=100)
scoreTxt = side.create_text(side.winfo_width() / 2, side.winfo_height() / 3, font=("courier", 15, "bold"))
winTxt = side.create_text(side.winfo_width() / 2, side.winfo_height() / 6, font=("courier", 15, "bold"))


class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.update()
        self.loadAssets()

        self.blockSize = 100
        self.imgDict = {0: self.bg, 2: self.img2, 4: self.img4, 8: self.img8, 16: self.img16, 32: self.img32,
                        64: self.img64, 128: self.img128, 256: self.img256, 512: self.img512, 1024: self.img1024,
                        2048: self.img2048}
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.isRunning = True
        self.generateCoords()
        self.drawBoard()

        self.master.bind_all("<Up>", self.onPressUp)
        self.master.bind_all("<Down>", self.onPressDown)
        self.master.bind_all("<Right>", self.onPressRight)
        self.master.bind_all("<Left>", self.onPressLeft)

    def loadAssets(self):
        try:
            self.bgImg = Image.open("./assets/empty.jpeg")
            self.bg = ImageTk.PhotoImage(self.bgImg)

            self.i2 = Image.open("assets/2.jpeg")
            self.img2 = ImageTk.PhotoImage(self.i2)

            self.i4 = Image.open("assets/4.jpeg")
            self.img4 = ImageTk.PhotoImage(self.i4)

            self.i8 = Image.open("assets/8.jpeg")
            self.img8 = ImageTk.PhotoImage(self.i8)

            self.i16 = Image.open("assets/16.png")
            self.img16 = ImageTk.PhotoImage(self.i16)

            self.i32 = Image.open("assets/32.png")
            self.img32 = ImageTk.PhotoImage(self.i32)

            self.i64 = Image.open("assets/64.png")
            self.img64 = ImageTk.PhotoImage(self.i64)

            self.i128 = Image.open("assets/128.png")
            self.img128 = ImageTk.PhotoImage(self.i128)

            self.i256 = Image.open("assets/256.png")
            self.img256 = ImageTk.PhotoImage(self.i256)

            self.i512 = Image.open("assets/512.png")
            self.img512 = ImageTk.PhotoImage(self.i512)

            self.i1024 = Image.open("assets/1024.png")
            self.img1024 = ImageTk.PhotoImage(self.i1024)

            self.i2048 = Image.open("assets/2048.png")
            self.img2048 = ImageTk.PhotoImage(self.i2048)

        except IOError as error:
            print('Caught this error: ' + repr(error))
            raise

    def drawBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.master.create_image(col * self.blockSize, row * self.blockSize,
                                         image=self.imgDict[self.board[row][col]], anchor=NW)

    def generateCoords(self):
        if self.isEmptySpace():
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while self.board[row][col] != 0:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            self.board[row][col] = random.choice([2, 4])

    def stack(self):
        newBoard = [[0] * 4 for _ in range(4)]
        for row in range(len(self.board)):
            pos = 0
            for col in range(len(self.board[row])):
                if self.board[row][col] != 0:
                    newBoard[row][pos] = self.board[row][col]
                    pos += 1
        self.board = newBoard

    def combine(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row]) - 1):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row][col + 1]:
                    self.board[row][col] *= 2
                    self.board[row][col + 1] = 0
                    self.score += self.board[row][col]

    def reverse(self):
        newBoard = []
        for row in range(len(self.board)):
            newBoard.append([])
            for col in range(len(self.board[row])):
                newBoard[row].append(self.board[row][3 - col])
        self.board = newBoard

    def transpose(self):
        newBoard = [[0] * 4 for _ in range(4)]
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                newBoard[row][col] = self.board[col][row]
        self.board = newBoard

    def onPressLeft(self, e):
        self.stack()
        self.combine()
        self.stack()
        self.generateCoords()
        self.drawBoard()

    def onPressRight(self, e):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.generateCoords()
        self.drawBoard()

    def onPressUp(self, e):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.generateCoords()
        self.drawBoard()

    def onPressDown(self, e):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.generateCoords()
        self.drawBoard()

    def isEmptySpace(self):
        for row in self.board:
            if 0 in row: return True
        return False

    def isMoveExist(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row]) - 1):
                if self.board[row][col] == self.board[row][col + 1]:
                    return True

        for row in range(len(self.board) - 1):
            for col in range(len(self.board[row])):
                if self.board[row][col] == self.board[row + 1][col]:
                    return True

        return False

    def gameOverCheck(self):
        for row in self.board:
            if 2048 in row:
                side.itemconfigure(winTxt, text="You Win !")
                self.isRunning = False
        if not self.isMoveExist() and not self.isEmptySpace():
            self.isRunning = False
            side.itemconfigure(winTxt, text="You Lost !")

    def reset(self):
        self.master.delete(ALL)
        side.itemconfigure(winTxt, text="")
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.generateCoords()
        self.drawBoard()


game = Game2048(canvas)
resetButton.config(command=game.reset)

while True:
    side.itemconfigure(scoreTxt, text=f"Score: {game.score}")
    game.gameOverCheck()
    time.sleep(0.01)
    root.update()

root.mainloop()
