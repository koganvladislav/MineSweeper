from random import shuffle
from tkinter.messagebox import showinfo, showerror
import NewButton
import time
import tkinter as tk


class MineSweeper:
    lines = 10
    columns = 10
    mines = 15
    window = tk.Tk()
    GameOver = False
    count = 0
    button_width = 5
    button_height = 3
    font = ("Aria 13", 13, "bold")
    pad = 20
    apply_row = 3
    color = ''
    time_started = int(time.strftime("%S"))

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.lines + 2):
            line_now = []
            for j in range(MineSweeper.columns + 2):
                button = NewButton.NewButton(MineSweeper.window, x=i, y=j, number=0, width=self.button_width,
                                             height=self.button_height)
                button.config(command=lambda func=button: self.push(func))
                button.bind('<Button-2>', self.flag)
                button.bind('<Button-3>', self.flag)
                line_now.append(button)
            self.buttons.append(line_now)
        MineSweeper.count = 0

    def flag(self, event):  # расставляем флажки
        now = event.widget
        if now['state'] == 'normal':
            now['state'] = 'disabled'
            now['text'] = ' 🚩'
            MineSweeper.count += 1
        elif now['text'] == ' 🚩':
            now['state'] = 'normal'
            now['text'] = ''
            MineSweeper.count -= 1
        MineSweeper.congratulations(self)

    def set_color(self, button_now: NewButton):  # присваиваем цвет цифре в зависимости от количества мин по соседству
        if button_now.neighbor == 0:
            self.color = '#F5F5F5'
        if button_now.neighbor == 1:
            self.color = 'blue'
        if button_now.neighbor == 2:
            self.color = 'green'
        if button_now.neighbor == 3:
            self.color = 'red'
        if button_now.neighbor == 4:
            self.color = 'darkblue'
        if button_now.neighbor == 5:
            self.color = 'brown'
        if button_now.neighbor == 6:
            self.color = 'aqua'
        if button_now.neighbor == 7:
            self.color = 'black'
        if button_now.neighbor == 8:
            self.color = '#778899'

    def congratulations(self):  # проверка на конец игры + поздравление
        flag = True
        for i in range(1, MineSweeper.lines + 1):
            for j in range(1, MineSweeper.columns + 1):
                if self.buttons[i][j]['state'] != 'disabled':
                    flag = False
        if MineSweeper.count == MineSweeper.mines and flag:
            showinfo('win', f'Congrats!\n Your score: {int(time.strftime("%S")) - self.time_started} seconds')
            self.time_started = int(time.strftime("%S"))

    def show_mines(self):  # показываем, где находились мины, в случае если игра проиграна
        for i in range(1, MineSweeper.lines + 1):
            for j in range(1, MineSweeper.columns + 1):
                if self.buttons[i][j].mine:
                    self.buttons[i][j].config(text='💣', state='disabled')
                else:
                    self.buttons[i][j].config(state='disabled')

    def push(self, button_now: NewButton):  # обработка нажатий на кнопки
        MineSweeper.set_color(self, button_now)
        if button_now.mine:
            button_now.config(text='💣', state='disabled')
            button_now.opened = True
            MineSweeper.GameOver = True
            showinfo('Game Over', 'GAME OVER')
            self.time_started = int(time.strftime("%S"))
            MineSweeper.show_mines(self)
        else:
            button_now.config(text=button_now.neighbor, width=self.button_width, height=self.button_height,
                              font=self.font, disabledforeground=self.color, state='disabled')
            button_now.opened = True
            if not button_now.neighbor:
                self.search(button_now)
        MineSweeper.congratulations(self)

    def search(self, button: NewButton):  # Функция, раскрывающая поля без цифр и мин
        queue = [button]
        while queue:
            now = queue.pop()
            if now.neighbor:
                MineSweeper.set_color(self, now)
                now.config(text=now.neighbor, width=self.button_width, height=self.button_height, font=self.font,
                           disabledforeground=self.color, state='disabled')
            now.config(state='disabled')
            now.opened = True
            if now.neighbor == 0:
                x, y = now.x, now.y
                ceils = [self.buttons[x][y + 1], self.buttons[x][y - 1], self.buttons[x - 1][y], self.buttons[x + 1][y],
                         self.buttons[x + 1][y + 1], self.buttons[x + 1][y - 1], self.buttons[x - 1][y + 1],
                         self.buttons[x - 1][y - 1]]
                for ceil in ceils:
                    if ceil.opened or (1 > ceil.x or ceil.x > MineSweeper.lines) or \
                            (1 > ceil.y or ceil.y > MineSweeper.columns) or ceil in queue:
                        continue
                    queue.append(ceil)

    def restart(self):  # перезапуск игры
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
        line_entry.grid(row=0, column=1, padx=self.pad, pady=self.pad)
        tk.Label(window_settings, text='COLUMNS QUANTITY').grid(row=1, column=0)
        column_entry = tk.Entry(window_settings)
        column_entry.insert(0, str(MineSweeper.columns))
        column_entry.grid(row=1, column=1, padx=self.pad, pady=self.pad)
        tk.Label(window_settings, text='MINES QUANTITY').grid(row=2, column=0)
        mines_entry = tk.Entry(window_settings)
        mines_entry.insert(0, str(MineSweeper.mines))
        mines_entry.grid(row=2, column=1, padx=self.pad, pady=self.pad)
        btn = tk.Button(window_settings, text='Apply',
                        command=lambda: self.change(line_entry, column_entry, mines_entry))
        btn.grid(row=self.apply_row, column=0, columnspan=2, padx=self.pad, pady=self.pad)

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
    def exit():  # остановить программу, если нажали на file - exit
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
                    neighbor += (bool(self.buttons[i - 1][j - 1].mine))
                    neighbor += (bool(self.buttons[i - 1][j].mine))
                    neighbor += (bool(self.buttons[i - 1][j + 1].mine))
                    neighbor += (bool(self.buttons[i][j - 1].mine))
                    neighbor += (bool(self.buttons[i][j + 1].mine))
                    neighbor += (bool(self.buttons[i + 1][j - 1].mine))
                    neighbor += (bool(self.buttons[i + 1][j].mine))
                    neighbor += (bool(self.buttons[i + 1][j + 1].mine))
                button.neighbor = neighbor

    def start_game(self):
        MineSweeper.time_started = int(time.strftime("%S"))
        MineSweeper.make_table(self)
        MineSweeper.insert(self)
        MineSweeper.count_neighbors(self)
        MineSweeper.window.mainloop()
        MineSweeper.count = 0
