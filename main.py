import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror
from tkinter import *
import time


class Timer(Tk):
    time_started = int(time.strftime("%s"))

    def __init__(self):
        super().__init__()
        self.label = Label(self, text="timer", padx=60, pady=20)
        self.label.pack()
        self.update_clock()

    def update_clock(self):
        now = int(time.strftime("%s")) - self.time_started
        self.label.configure(text=now)
        self.after(1000, self.update_clock)


class NewButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(NewButton, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.mine = False
        self.neighbor = 0
        self.opened = False


class MineSweeper:
    lines = 10
    columns = 10
    mines = 15
    window = tk.Tk()
    GameOver = False
    count = 0

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.lines + 2):
            line_now = []
            for j in range(MineSweeper.columns + 2):
                button = NewButton(MineSweeper.window, x=i, y=j, number=0, width=5, height=3)
                button.config(command=lambda func=button: self.push(func))
                button.bind('<Button-2>', self.flag)
                button.bind('<Button-3>', self.flag)
                line_now.append(button)
            self.buttons.append(line_now)
        MineSweeper.count = 0

    def flag(self, event):
        now = event.widget
        if now['state'] == 'normal':
            now['state'] = 'disabled'
            now['text'] = ' 🚩'
            MineSweeper.count += 1
        elif now['text'] == ' 🚩':
            now['state'] = 'normal'
            now['text'] = ''
            MineSweeper.count -= 1
        flag = True
        for i in range(1, MineSweeper.lines + 1):
            for j in range(1, MineSweeper.columns + 1):
                if self.buttons[i][j]['state'] != 'disabled':
                    flag = False
        if MineSweeper.count == MineSweeper.mines and flag:
            showinfo('win', 'Congrats!')

    def push(self, button_now: NewButton):  # обработка нажатий на кнопки
        if button_now.neighbor == 0:
            color = '#F5F5F5'
        if button_now.neighbor == 1:
            color = 'blue'
        if button_now.neighbor == 2:
            color = 'green'
        if button_now.neighbor == 3:
            color = 'red'
        if button_now.neighbor == 4:
            color = 'darkblue'
        if button_now.neighbor == 5:
            color = 'brown'
        if button_now.neighbor == 6:
            color = 'aqua'
        if button_now.neighbor == 7:
            color = 'black'
        if button_now.neighbor == 8:
            color = '#778899'
        if button_now.mine:
            button_now.config(text='💣', state='disabled')
            button_now.opened = True
            MineSweeper.GameOver = True
            showinfo('Game Over', 'GAME OVER')
            Timer.time_started = int(time.strftime("%s"))
            for i in range(1, MineSweeper.lines + 1):
                for j in range(1, MineSweeper.columns + 1):
                    if self.buttons[i][j].mine:
                        self.buttons[i][j].config(text='💣', state='disabled')
                    else:
                        self.buttons[i][j].config(state='disabled')
        else:
            button_now.config(text=button_now.neighbor, width=5, height=3, font=("Arial 13", 13, "bold"),
                              disabledforeground=color, state='disabled')
            button_now.opened = True
            if not button_now.neighbor:
                self.search(button_now)
        flag = True
        for i in range(1, MineSweeper.lines + 1):
            for j in range(1, MineSweeper.columns + 1):
                if self.buttons[i][j]['state'] != 'disabled':
                    flag = False
        if MineSweeper.count == MineSweeper.mines and flag:
            showinfo('win', 'Congrats!')
            Timer.time_started = int(time.strftime("%s"))

    def search(self, button: NewButton):  # Функция, раскрывающая поля без цифр и мин
        queue = [button]
        while queue:
            now = queue.pop()
            if now.neighbor:
                if now.neighbor == 1:
                    color = 'blue'
                if now.neighbor == 2:
                    color = 'green'
                if now.neighbor == 3:
                    color = 'red'
                if now.neighbor == 4:
                    color = 'darkblue'
                if now.neighbor == 5:
                    color = 'brown'
                if now.neighbor == 6:
                    color = 'aqua'
                if now.neighbor == 7:
                    color = 'black'
                if now.neighbor == 8:
                    color = '#778899'
                now.config(text=now.neighbor, width=5, height=3, font=("Aria 13", 13, "bold"),
                           disabledforeground=color, state='disabled')
            else:
                now.config(state='disabled')
            now.config(state='disabled')
            now.opened = True
            if now.neighbor == 0:
                x = now.x
                y = now.y
                up = self.buttons[x][y + 1]
                down = self.buttons[x][y - 1]
                left = self.buttons[x - 1][y]
                right = self.buttons[x + 1][y]
                diagonal1 = self.buttons[x + 1][y + 1]
                diagonal2 = self.buttons[x - 1][y + 1]
                diagonal3 = self.buttons[x + 1][y - 1]
                diagonal4 = self.buttons[x - 1][y - 1]
                ceils = [up, down, left, right, diagonal1, diagonal2, diagonal3, diagonal4]
                for ceil in ceils:
                    if ceil.opened or (1 > ceil.x or ceil.x > MineSweeper.lines) or (
                            1 > ceil.y or ceil.y > MineSweeper.columns) or ceil in queue:
                        continue
                    queue.append(ceil)

    def restart(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.start_game()
        MineSweeper.count = 0

    def settings(self):  # Меню
        window_settings = tk.Toplevel(self.window)
        window_settings.wm_title('Settings')
        tk.Label(window_settings, text='LINES QUANTITY').grid(row=0, column=0)
        line_entry = tk.Entry(window_settings)
        line_entry.insert(0, str(MineSweeper.lines))
        line_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(window_settings, text='COLUMNS QUANTITY').grid(row=1, column=0)
        column_entry = tk.Entry(window_settings)
        column_entry.insert(0, str(MineSweeper.columns))
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(window_settings, text='MINES QUANTITY').grid(row=2, column=0)
        mines_entry = tk.Entry(window_settings)
        mines_entry.insert(0, str(MineSweeper.mines))
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        btn = tk.Button(window_settings, text='Apply',
                        command=lambda: self.change(line_entry, column_entry, mines_entry))
        btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change(self, line: tk.Entry, column: tk.Entry, mine: tk.Entry):  # хотим изменить параметры игры
        try:
            int(line.get()), int(column.get()), int(mine.get())
        except (Exception,):
            showerror('error', 'bruh...''\n'
                               'int, not str')
        MineSweeper.lines = int(line.get())
        MineSweeper.columns = int(column.get())
        MineSweeper.mines = int(mine.get())
        self.restart()

    @staticmethod
    def exit():
        exit(0)

    def make_table(self):  # Заполняем таблицу, добавляем меню
        self.window.title('MineSweeper')
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        settings = tk.Menu(menu)
        settings.add_command(label='Play', command=self.restart)
        settings.add_command(label='Settings', command=self.settings)
        settings.add_command(label='Exit', command=exit)
        menu.add_cascade(label='file', menu=settings)
        for i in range(1, MineSweeper.lines + 1):
            for j in range(1, MineSweeper.columns + 1):
                button = self.buttons[i][j]
                button.grid(row=i, column=j)

    @property
    def mines_place(self):  # Создаем массив из случайных чисел, количеством равным количеству мин
        mas = list(range(1, MineSweeper.lines * MineSweeper.columns + 1))
        shuffle(mas)
        return mas[:MineSweeper.mines]

    def insert(self):  # биективно ставим в соответствие числу из массива координату поля, в котором находится мина
        indexes = list(self.mines_place)
        for index in indexes:
            if index % self.columns == 0:
                coord_y = self.columns
            else:
                coord_y = index % self.columns
            self.buttons[((index - 1) // self.columns) + 1][coord_y].mine = True

    def count_neighbors(self):  # считаем количество мин по соседству
        for i in range(1, MineSweeper.lines + 1):
            for j in range(1, MineSweeper.columns + 1):
                button = self.buttons[i][j]
                neighbor = 0
                if not button.mine:
                    if self.buttons[i - 1][j - 1].mine:
                        neighbor += 1
                    if self.buttons[i - 1][j].mine:
                        neighbor += 1
                    if self.buttons[i - 1][j + 1].mine:
                        neighbor += 1
                    if self.buttons[i][j - 1].mine:
                        neighbor += 1
                    if self.buttons[i][j + 1].mine:
                        neighbor += 1
                    if self.buttons[i + 1][j - 1].mine:
                        neighbor += 1
                    if self.buttons[i + 1][j].mine:
                        neighbor += 1
                    if self.buttons[i + 1][j + 1].mine:
                        neighbor += 1
                button.neighbor = neighbor

    def start_game(self):
        Timer.time_started = int(time.strftime("%s"))
        MineSweeper.make_table(self)
        MineSweeper.insert(self)
        MineSweeper.count_neighbors(self)
        MineSweeper.window.mainloop()
        MineSweeper.count = 0


app = Timer()
app.title('Timer')
game = MineSweeper()
MineSweeper.start_game(game)
