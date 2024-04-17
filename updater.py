from threading import Thread
from time import sleep
from tkinter import TclError
from typing import Callable
from abc import ABC, abstractmethod


class UpdaterError(Exception):
    ...


class UpdateWidget(ABC):
    @abstractmethod
    def update_eval(self) -> bool:
        """Function that evals if it has to be updated

        Returns:
            bool: Indicate that have to be updated
        """
        ...

    @abstractmethod
    def update_widget(self) -> None:
        """Function that update with the new value the widget
        """
        ...

    pending_to_update: bool = False


class Updater:
    """The Updater ask for the widgets that can be updated. Look if they have to update and append to a list
    """
    def __init__(
        self,
        widget_list: Callable[[], list[UpdateWidget]],
        get_time: Callable[[], int],
    ) -> None:
        """Constructor

        Args:
            widget_list (Callable[[], list[Updatewidget]]): Callback to know the list of widgets to update
            get_time (Callable[[], int]): Callback to know the time to update
        """
        self._get_time = get_time
        self.update_widgets_list: list[UpdateWidget] = []
        self.widget_list = widget_list
        self.mutex: bool = True
        self.close_updater = False
        self.updater = Thread(
            target=self._thread_gestor, name="Updater", daemon=True)
        self.updater.start()

    def time_to_update(self) -> int:
        return self._get_time()

    def _update_widgets(self) -> None:
        for widget in self.widget_list():
            if not widget.pending_to_update:
                try:
                    if widget.update_eval():
                        widget.pending_to_update = True
                        self.update_widgets_list.append(widget)
                except ValueError:
                    ...
                except TclError:
                    ...

    def _thread_gestor(self) -> None:
        """Loop that look if the some widget has to update
        """
        while not self.close_updater:
            if self.mutex:
                self.mutex = False
                if len(self.update_widgets_list) == 0:
                    self._update_widgets()
                self.mutex = True
                time_to_sleep = self.time_to_update()
            else:
                time_to_sleep = self.time_to_update() + 1
            for _ in range(time_to_sleep):
                sleep(1)
                if self.close_updater:
                    break

    def obtain_list(self) -> list[UpdateWidget]:
        """Public class to obtain the list of widgets that need to be updated

        Returns:
            list[UpdateWidget]: List of widgets to update
        """
        if self.mutex:
            update_widgets_list = self.update_widgets_list
            return update_widgets_list
        else:
            return []

    def erase_list(self) -> bool:
        """Public class that erase the list of widgets that neeeded to be updated

        Returns:
            bool: False in case that list hasn't be erased or True in case that list has been erased
        """
        if self.mutex:
            self.update_widgets_list = []
            return True
        else:
            return False

    def closing_updater(self) -> None:
        """Function to indicate that updater has to being closed
        """
        self.close_updater = True
