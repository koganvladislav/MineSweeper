import tkinter as tk


class NewButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(NewButton, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.mine = False
        self.neighbor = 0
        self.opened = False
