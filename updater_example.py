from updater import Updater, UpdateWidget
import tkinter as tk
from tkinter import ttk, Misc
import time
import datetime


class App(tk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.frame1 = Frame(self)
        self.frame1.pack()
        self.updater = Updater(self.get_widget, self.get_time)
        self.after(ms=1000, func=self.update)

    def update(self) -> None:
        if len(self.updater.obtain_list()) != 0:
            for widget in self.updater.obtain_list():
                widget.update_widget()
                widget.pending_to_update = False
            self.updater.erase_list()
        self.after(500, self.update)

    def get_time(self) -> int:
        return 1

    def get_widget(self) -> list[UpdateWidget]:
        return [self.frame1]


class Frame(UpdateWidget, tk.Frame):
    def __init__(self, master: Misc) -> None:
        super().__init__(master)
        self.time_label = ttk.Label(master=self, text="Time right now")
        self.actual_time = time.time()
        self.actual_time_label = ttk.Label(
            master=self,
            text=datetime.datetime.fromtimestamp(self.actual_time).strftime('%c'))

        self.time_label.pack()
        self.actual_time_label.pack()

    def update_eval(self) -> bool:
        return True

    def update_widget(self) -> None:
        self.actual_time = time.time()
        self.actual_time_label.configure(
            text=datetime.datetime.fromtimestamp(self.actual_time).strftime('%c'))
        self.actual_time_label.update()
        self.focus_force()


main = tk.Tk()
App(main).pack()
main.mainloop()
