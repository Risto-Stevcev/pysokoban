#!/usr/bin/env python

try:
    import Tkinter as tk
    from tkFileDialog import askopenfilenames
except ImportError:
    import tkinter as tk
    from tkinter.filedialog import askopenfilenames
import pydoc
import os


__author__ = "Risto Stevcev"
__version__ = "1.1"
if not __package__:
    __package__ = "pysokoban"

_ROOT = os.path.abspath(os.path.dirname(__file__))


def enum(**enums):
    return type('Enum', (), enums)
Hole = enum(filled=True, empty=False)


class Menu(object):
    def __init__(self, app):
        self.app = app

    def OpenFile(self):
        self.app.grid_forget()
        level_files = self.app.tk.splitlist(askopenfilenames(initialdir=os.path.join(_ROOT, 'levels')))
        self.app.level_files = list(level_files)
        self.app.start_next_level()

    def About(self):
        AboutDialog()


class Direction(object):
    left = 'Left'
    right = 'Right'
    up = 'Up'
    down = 'Down'


class AboutDialog(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("About")

        info = tk.Label(self, text=("%s v%s - by %s" % (__package__, __version__, __author__)))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)


class CompleteDialog(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("Level(s) complete!")

        info = tk.Label(self, text=("You completed every level!"))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)


class Level(object):
    wall = '*'
    hole = 'o'
    crate_in_hole = '@'
    crate = '#'
    player = 'P'
    floor = ' '


class Image(object):
    wall = os.path.join(_ROOT, 'images/wall.gif')
    hole = os.path.join(_ROOT, 'images/hole.gif')
    crate_in_hole = os.path.join(_ROOT, 'images/crate-in-hole.gif')
    crate = os.path.join(_ROOT, 'images/crate.gif')
    player = os.path.join(_ROOT, 'images/player.gif')
    player_in_hole = os.path.join(_ROOT, 'images/player-in-hole.gif')


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.configure(background="black")
        self.master.title("%s v%s" % (__package__, __version__))
        self.master.resizable(0,0)
        icon = tk.PhotoImage(file=Image.crate)
        self.master.tk.call('wm', 'iconphoto', self.master._w, icon)
        self.create_menu()

        self.DEFAULT_SIZE = 200
        self.frame = tk.Frame(self, height=self.DEFAULT_SIZE, width=self.DEFAULT_SIZE)
        self.frame.grid()
        self.default_frame()

        self.player_position = ()
        self.player = None

        self.current_level = None
        self.level_files = []
        self.level = []
        self.crates = {}
        self.holes = {}
        
    def key(self, event):
        directions = {Direction.left, Direction.right, Direction.up, Direction.down}
        if event.keysym in directions:
            self.move_player(event.keysym)

    def create_menu(self):
        root = self.master
        menu = tk.Menu(root)
        user_menu = Menu(self)
        root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Restart", command=self.restart_level)
        file_menu.add_command(label="Open...", command=user_menu.OpenFile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=menu.quit)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=user_menu.About)

    def default_frame(self):
        start_width = 30
        start_label = tk.Label(self.frame, text="Welcome to PySokoban!\n", width=start_width)
        start_label.grid(row=0, column=0)

        start_label2 = tk.Label(self.frame, text="To play: File -> New/Open\n", width=start_width)
        start_label2.grid(row=1, column=0)

    def clear_level(self):
        self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid()
        self.level = []

    def start_next_level(self):
        self.clear_level()
        if len(self.level_files) > 0:
            self.current_level = self.level_files.pop()
            level = open(self.current_level, "r")
            self.grid()
            self.load_level(level)
            self.master.title("%s v%s - %s" % (__package__, __version__, self.current_level.split("/")[-1]))
        else:
            self.current_level = None
            self.master.title("%s v%s" % (__package__, __version__))
            self.default_frame()
            CompleteDialog()

    def restart_level(self):
        if self.current_level:
            self.level_files.append(self.current_level)
            self.start_next_level()

    def load_level(self, level):
        self.clear_level()

        for row, line in enumerate(level):
            level_row = list(line)
            for column,x in enumerate(level_row):
                if x == Level.player:
                    level_row[column] = Level.floor

                elif x == Level.hole:
                    self.holes[(row, column)] = Hole.empty

                elif x == Level.crate_in_hole:
                    self.holes[(row, column)] = Hole.filled

            self.level.append(level_row)

            for column, char in enumerate(line):
                if char == Level.wall:
                    wall = tk.PhotoImage(file=Image.wall)
                    w = tk.Label(self.frame, image=wall)
                    w.wall = wall
                    w.grid(row=row, column=column)

                elif char == Level.hole:
                    hole = tk.PhotoImage(file=Image.hole)
                    w = tk.Label(self.frame, image=hole)
                    w.hole = hole
                    w.grid(row=row, column=column)

                elif char == Level.crate_in_hole:
                    crate_in_hole = tk.PhotoImage(file=Image.crate_in_hole)
                    w = tk.Label(self.frame, image=crate_in_hole)
                    w.crate_in_hole = crate_in_hole
                    w.grid(row=row, column=column)
                    self.crates[(row, column)] = w

                elif char == Level.crate:
                    crate = tk.PhotoImage(file=Image.crate)
                    w = tk.Label(self.frame, image=crate)
                    w.crate = crate
                    w.grid(row=row, column=column)
                    self.crates[(row, column)] = w

                elif char == Level.player:
                    player_image = tk.PhotoImage(file=Image.player)
                    self.player = tk.Label(self.frame, image=player_image)
                    self.player.player_image = player_image
                    self.player.grid(row=row, column=column)
                    self.player_position = (row, column)

    def move_player(self, direction):
        row, column = self.player_position
        prev_row, prev_column = row, column

        blocked = True
        if direction == Direction.left and self.level[row][column - 1] is not Level.wall and column > 0:
            blocked = self.move_crate((row, column - 1), (row, column - 2))
            if not blocked:
                self.player_position = (row, column - 1)

        elif direction == Direction.right and self.level[row][column + 1] is not Level.wall:
            blocked = self.move_crate((row, column + 1), (row, column + 2))
            if not blocked:
                self.player_position = (row, column + 1)

        elif direction == Direction.down and self.level[row + 1][column] is not Level.wall:
            blocked = self.move_crate((row + 1, column), (row + 2, column))
            if not blocked:
                self.player_position = (row + 1, column)

        elif direction == Direction.up and self.level[row - 1][column] is not Level.wall and row > 0:
            blocked = self.move_crate((row - 1, column), (row - 2, column))
            if not blocked:
                self.player_position = (row - 1, column)

        all_holes_filled = True
        for hole in self.holes.values():
            if hole is not Hole.filled:
                all_holes_filled = False

        if all_holes_filled:
            self.start_next_level()
            return

        row, column = self.player_position
        if self.level[prev_row][prev_column] is Level.hole and not blocked:
            hole = tk.PhotoImage(file=Image.hole)
            w = tk.Label(self.frame, image=hole)
            w.hole = hole
            w.grid(row=prev_row, column=prev_column)

        if not blocked:
            self.player.grid_forget()

            if self.level[row][column] is Level.hole:
                player_image = tk.PhotoImage(file=Image.player_in_hole)
            else:
                player_image = tk.PhotoImage(file=Image.player)

            self.player = tk.Label(self.frame, image=player_image)
            self.player.player_image = player_image
            self.player.grid(row=row, column=column)

    def move_crate(self, location, next_location):
        row, column = location
        next_row, next_column = next_location

        if self.level[row][column] is Level.crate and self.level[next_row][next_column] is Level.floor:
            self.crates[(row, column)].grid_forget()
            crate = tk.PhotoImage(file=Image.crate)
            w = tk.Label(self.frame, image=crate)
            w.crate = crate
            w.grid(row=next_row, column=next_column)

            self.crates[(next_row, next_column)] = w
            self.level[row][column] = Level.floor
            self.level[next_row][next_column] = Level.crate

        elif self.level[row][column] is Level.crate and self.level[next_row][next_column] is Level.hole:
            self.crates[(row, column)].grid_forget()
            crate_in_hole = tk.PhotoImage(file=Image.crate_in_hole)
            w = tk.Label(self.frame, image=crate_in_hole)
            w.crate = crate_in_hole
            w.grid(row=next_row, column=next_column)

            self.crates[(next_row, next_column)] = w
            self.level[row][column] = Level.floor
            self.level[next_row][next_column] = Level.crate_in_hole
            self.holes[(next_row, next_column)] = Hole.filled

        elif self.level[row][column] is Level.crate_in_hole and self.level[next_row][next_column] is Level.floor:
            self.crates[(row, column)].grid_forget()
            crate = tk.PhotoImage(file=Image.crate)
            w = tk.Label(self.frame, image=crate)
            w.crate = crate
            w.grid(row=next_row, column=next_column)

            self.crates[(next_row, next_column)] = w
            self.level[row][column] = Level.hole
            self.level[next_row][next_column] = Level.crate
            self.holes[(row, column)] = Hole.empty

        elif self.level[row][column] is Level.crate_in_hole and self.level[next_row][next_column] is Level.hole:
            self.crates[(row, column)].grid_forget()
            crate_in_hole = tk.PhotoImage(file=Image.crate_in_hole)
            w = tk.Label(self.frame, image=crate_in_hole)
            w.crate_in_hole = crate_in_hole
            w.grid(row=next_row, column=next_column)

            self.crates[(next_row, next_column)] = w
            self.level[row][column] = Level.hole
            self.level[next_row][next_column] = Level.crate_in_hole
            self.holes[(row, column)] = Hole.empty
            self.holes[(next_row, next_column)] = Hole.filled

        if self.is_blocked(location, next_location):
            return True
        return False

    def is_blocked(self, location, next_location):
        row, column = location
        next_row, next_column = next_location

        if self.level[row][column] is Level.crate and self.level[next_row][next_column] is Level.wall:
            return True
        elif self.level[row][column] is Level.crate_in_hole and self.level[next_row][next_column] is Level.wall:
            return True
        elif (self.level[row][column] is Level.crate_in_hole and
                  (self.level[next_row][next_column] is Level.crate or
                           self.level[next_row][next_column] is Level.crate_in_hole)):
            return True
        elif (self.level[row][column] is Level.crate and
                  (self.level[next_row][next_column] is Level.crate or
                           self.level[next_row][next_column] is Level.crate_in_hole)):
            return True


def main():
    app = Application()
    app.bind_all("<Key>", app.key)
    app.mainloop()


if __name__ == "__main__":
    main()
