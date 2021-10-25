from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import time

root = Tk()
root.title("YouTube Downloader")
root.geometry("500x400")


class YoutubeDL:
    def __init__(self, master):
        self.master = master
        self.path = ""
        self.url = ""
        self.choices = ["720p", "144p", "Audio only"]
        self.percent = StringVar()

        self.percentLabel = Label(self.master, textvariable=self.percent)
        self.textLabel = Label(self.master, text="Enter the URL of the video", font=("jost", 15), pady=10)
        self.textError = Label(root, text="Please choose a valid url ", fg="red", font=("jost", 10))
        self.pathLabel = Label(self.master, text="Save your file", font=("jost", 15), pady=10)
        self.pathError = Label(root, text="Please choose a valid path", fg="red", font=("jost", 10), pady=10)
        self.textEntry = Entry(self.master, bd=5, width=50)
        self.textEntry.bind("<KeyRelease>", self.verifyUrl)
        self.choiceLabel = Label(self.master, text="Select quality", font=("jost", 15), pady=10)
        self.comboBox = ttk.Combobox(self.master, values=self.choices, state="readonly")
        self.comboBox.current(0)
        self.progressBar = ttk.Progressbar(self.master, orient="horizontal", length=200)

        self.pathBtn = Button(self.master, text="Select path", padx=20, command=self.choosePath,bd =2)
        self.dlBtn = Button(self.master, text="Download", padx=20,bd=2, command=lambda: [self.progress(), self.download()])

        self.textLabel.pack()
        self.textEntry.pack()
        self.textError.pack()
        self.choiceLabel.pack()
        self.comboBox.pack()
        self.pathLabel.pack()
        self.pathBtn.pack()
        self.pathError.pack()
        self.dlBtn.pack()

    def progress(self):
        self.url = self.textEntry.get()
        if self.verifyUrl("") and len(self.url) > 1:
            self.progressBar.pack()
            self.percentLabel.pack()
            tasks = 100
            x = 0
            speed = 1
            while x < tasks:
                time.sleep(0.01)
                self.progressBar["value"] += (speed / tasks) * 100
                x += speed
                self.percent.set(str(int((x / tasks) * 100)) + "%")
                self.master.update_idletasks()

    def verifyUrl(self, e):
        self.url = self.textEntry.get()
        if self.url.startswith("https://www"):
            self.textError.config(text="")
            return True
        else:
            self.textError.config(text="Please choose a valid url")

    def choosePath(self):
        self.path = filedialog.askdirectory()
        if len(self.path) > 1:
            self.pathError.config(text=f"Path choosed : {self.path}", fg="black")

    def download(self):
        self.url = self.textEntry.get()
        choice = self.comboBox.get()
        if self.verifyUrl("") and len(self.url) > 1:
            self.progressBar.pack()
            self.percentLabel.pack()
            yt = YouTube(self.url)
            if choice == "720p":
                select = yt.streams.filter(progressive=True)[1]
            elif choice == "140p":
                select = yt.streams.filter(progressive=True, file_extension="mp4")[-1]
            else:
                select = yt.streams.filter(only_audio=True)[0]
            select.download(self.path)
            self.progressBar["value"] = 0
            self.percent.set(str(int(0)) + "%")
        self.progressBar.pack_forget()
        self.percentLabel.pack_forget()


b = YoutubeDL(root)
root.resizable(False, False)
root.mainloop()
