import tkinter
from tkinter import *
from PIL import Image, ImageTk
import time
import random

from sqlalchemy import true

WIDTH = 716
HEIGHT = 616
SIDE = 200

root = Tk()
root.title("Connect 4")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False,False)

canvas = Canvas(root, bg="black", width=WIDTH - SIDE, height=HEIGHT)
canvas.pack(side=LEFT)
side = Canvas(root, width=SIDE, height=HEIGHT, bg="#bcd4de")
resetButton = Button(side, text="Reset", font=("courier", 15, "bold"), bd=4)
side.pack(side=RIGHT)
root.update()
resetButtonWindow = side.create_window(side.winfo_width() / 2, (2*side.winfo_height() /3),
                                       window=resetButton, width=100)
turnTxt = side.create_text(side.winfo_width() / 2, side.winfo_height() / 3, font=("courier", 15, "bold"))


class Connect4:
    def __init__(self, master):
        self.master = master
        self.master.update()
        self.isRunning = True

        self.turn = random.choice(["B", "R"])
        self.colors = {"R": "red", "B": "blue"}
        self.blockSize = 86
        self.circleRad = 60
        self.board = [[""] * 6 for _ in range(6)]
        self.mousePos = [(0, 0)]
        self.circle = self.master.create_oval(0, 0, 0, 0)

        self.loadAssets()
        self.drawBoard()
        self.master.bind_all("<Button-1>", self.onClick)
        self.master.bind('<Motion>', lambda e: [self.motion(e), self.drawCircle(e)])

    def loadAssets(self):
        try:
            self.bgImg = Image.open("./assets/bg.png")
            self.bg = ImageTk.PhotoImage(self.bgImg)

            self.squareEmptyImg = Image.open("assets/empty.png")
            self.squareEmpty = ImageTk.PhotoImage(self.squareEmptyImg)

            self.squareBlueImg = Image.open("assets/blue.png")
            self.squareBlue = ImageTk.PhotoImage(self.squareBlueImg)

            self.squareRedImg = Image.open("assets/red.png")
            self.squareRed = ImageTk.PhotoImage(self.squareRedImg)

        except IOError as error:
            print('Caught this error: ' + repr(error))
            root.destroy()
            raise

    def drawBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == "":
                    self.master.create_image(0 + col * self.blockSize, 100 + row * self.blockSize,
                                             image=self.squareEmpty, anchor=NW)
                elif self.board[row][col] == "R":
                    self.master.create_image(col * self.blockSize - 2, 98 + row * self.blockSize, image=self.squareRed,
                                             anchor=NW)
                elif self.board[row][col] == "B":
                    self.master.create_image(0 + col * self.blockSize, 100 + row * self.blockSize,
                                             image=self.squareBlue, anchor=NW)

    def drawCircle(self, event):
        self.master.delete(self.circle)
        if 0 < self.mousePos[0][0] < self.master.winfo_width() - self.circleRad and 0 < self.mousePos[0][1] < 100:
            for pos in self.mousePos:
                self.circle = self.master.create_oval(pos[0], 50 - self.circleRad // 2, pos[0] + self.circleRad,
                                                      50 + self.circleRad // 2,
                                                      fill=self.colors[self.turn])

    def changeTurn(self):
        if self.turn == "R":
            self.turn = "B"
        elif self.turn == "B":
            self.turn = "R"

    def motion(self, event):
        self.mousePos = [(event.x, event.y)]

    def onClick(self, event):
        if self.isRunning:
            endPos = []
            if 0 < self.mousePos[0][0] < self.master.winfo_width() - self.circleRad and 0 < self.mousePos[0][1] < 100:
                currCol = self.mousePos[0][0] // self.blockSize
                for row in range(len(self.board)):
                    if self.board[row][currCol] == "":
                        endPos = [row, currCol]
                if len(endPos) > 1:
                    self.board[endPos[0]][endPos[1]] = self.turn
                    self.drawBoard()
                    if not self.checkWinner():
                        self.changeTurn()
                    else:
                        self.isRunning = False

    def checkHorizontal(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row]) - 3):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][
                    col + 3] != "":

                    return True
        return False

    def checkVertical(self):
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[row])):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][
                    col] != "":
                    return True
        return False

    def checkDiagonals(self):
        for row in range(3, len(self.board)):
            for col in range(len(self.board[row]) - 3):
                if self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == \
                        self.board[row - 3][
                            col + 3] != "":
                    return True
        for row in range(3, len(self.board)):
            for col in range(3, len(self.board[row])):
                if self.board[row][col] == self.board[row - 1][col - 1] == self.board[row - 2][col - 2] == \
                        self.board[row - 3][
                            col - 3] != "":
                    return True
        return False

    def checkWinner(self):
        return self.checkVertical() or self.checkHorizontal() or self.checkDiagonals()

    def reset(self):
        self.master.delete(tkinter.ALL)
        self.circle = self.master.create_oval(0, 0, 0, 0)
        self.board = [[""] * 6 for _ in range(6)]
        self.turn = random.choice(["B", "R"])
        self.mousePos = [(0, 0)]
        self.drawBoard()
        self.isRunning = True


game = Connect4(canvas)
resetButton.config(command=game.reset)
while True:
    if game.isRunning:
        side.itemconfigure(turnTxt, text=f"It's {game.colors[game.turn].upper()} turn")
    else:
        side.itemconfigure(turnTxt, text=f"{game.colors[game.turn].upper()} Wins !")
    time.sleep(0.01)
    root.update()

root.mainloop()
