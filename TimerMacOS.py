from MineSweeperMacOS import MineSweeper
from tkinter import Label
from tkinter import Tk
import time


class Timer(Tk):
    padx = 60
    pady = 20
    msec = 1000

    def __init__(self):
        super().__init__()
        self.label = Label(self, text="timer", padx=self.padx, pady=self.pady)
        self.label.pack()
        self.update_clock()

    def update_clock(self):  # обновление счетчика каждую секунду
        now = int(time.strftime("%s")) - MineSweeper.time_started
        self.label.configure(text=now)
        self.after(self.msec, self.update_clock)
