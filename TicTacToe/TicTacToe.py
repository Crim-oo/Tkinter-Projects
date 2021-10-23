from tkinter import *
import random

root = Tk()
root.title("Tic-Tac-Toe")


class TicTacToe:
    def __init__(self, master):
        self.player = random.choice(["x", "o"])
        self.label = Label(master, text=self.player + " turn", font=('consolas', 40))
        self.label.pack(side="top")
        self.resetButton = Button(master, text="restart", font=('consolas', 20), command=self.reset)
        self.resetButton.pack(side="bottom")
        self.frame = Frame(master)
        self.frame.pack()
        self.board = [[Button(self.frame)] * 3 for _ in range(3)]
        self.moveLeft = 9
        self.drawBoard()

    def drawBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.board[row][col] = Button(self.frame, text="", font=('consolas', 40), width=5, height=2,
                                              command=lambda row=row, column=col: self.checkTurn(row, column))
                self.board[row][col].grid(row=row, column=col)

    def changeTurn(self):
        if self.player == "x":
            self.player = "o"
        else:
            self.player = "x"

        self.label.config(text=self.player + " turn")

    def checkTurn(self, row, col):
        if self.board[row][col]["text"] == "":
            self.moveLeft -= 1
            self.board[row][col]["text"] = self.player
            self.changeTurn()
            if self.isWinner():
                self.changeTurn()
                self.label.config(text=self.player + " wins")
                self.disableButtons()
            elif self.isTie():
                self.changeTurn()
                self.label.config(text="It's a tie")
                self.disableButtons()

    def checkHorizontal(self):
        for row in range(len(self.board)):
            if self.board[row][0]['text'] == self.board[row][1]['text'] == self.board[row][2]['text'] != "":
                self.board[row][0].config(bg="green")
                self.board[row][1].config(bg="green")
                self.board[row][2].config(bg="green")
                return True

    def checkVertical(self):
        for col in range(len(self.board)):
            if self.board[0][col]['text'] == self.board[1][col]['text'] == self.board[2][col]['text'] != "":
                self.board[0][col].config(bg="green")
                self.board[1][col].config(bg="green")
                self.board[2][col].config(bg="green")
                return True

    def checkDiagonals(self):
        if self.board[0][0]['text'] == self.board[1][1]['text'] == self.board[2][2]['text'] != "":
            self.board[0][0].config(bg="green")
            self.board[1][1].config(bg="green")
            self.board[2][2].config(bg="green")
            return True

        elif self.board[0][2]['text'] == self.board[1][1]['text'] == self.board[2][0]['text'] != "":
            self.board[0][2].config(bg="green")
            self.board[1][1].config(bg="green")
            self.board[2][0].config(bg="green")
            return True

    def isTie(self):
        if self.moveLeft <= 0:
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    self.board[row][col].config(bg="yellow")
            return True

    def isWinner(self):
        if self.checkHorizontal():
            return True
        elif self.checkVertical():
            return True
        elif self.checkDiagonals():
            return True

    def reset(self):
        self.board = [[Button(self.frame)] * 3 for _ in range(3)]
        self.player = random.choice(["x", "o"])
        self.label.config(text=self.player + " turn")
        self.moveLeft = 9
        self.drawBoard()

    def disableButtons(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.board[row][col]["state"] = DISABLED


game = TicTacToe(root)
root.resizable(False, False)
root.mainloop()

